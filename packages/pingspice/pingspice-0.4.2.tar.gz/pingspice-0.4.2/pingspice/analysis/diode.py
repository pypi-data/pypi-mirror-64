#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.
#
# Copyright (C) 2017-20 by Edwin A. Suominen,
# http://edsuom.com/pingspice
#
# See edsuom.com for API documentation as well as information about
# Ed's background and other projects, software and otherwise.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#
# I'm serious about this: There are NO GUARANTEES to this
# software. None. If you simulate a circuit and everything looks
# great, and then you build it and it blows up, I CANNOT AND WILL NOT
# BE RESPONSIBLE. Nor do I make any promises as to how closely the
# included models compare to the actual devices whose behavior they
# attempt to simulate. Nor have the manufacturers of ANY of those
# devices provided (or been asked to provide) any endorsement about
# the models. This is free software, OK? You don't even get a
# money-back guarantee, because you paid nothing to begin with.

"""
A power diode model with evolved parameters.

Includes L{Constraints} to avoid torturing Ngspice with bogus
parameter combinations.

@see: L{pingspice.lib.diodes}.
"""

import numpy as np
from twisted.internet import defer

from pingspice.util import *
from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Subcircuit
from pingspice.lib.active import Capacitance_Meter

from pingspice.analysis import constraints, psim
from pingspice.analysis.sim import DC
from pingspice.analysis.timing import ReverseRecoveryEvaluator
from pingspice.analysis.fixture import HelperBase, DiodeRecoveryFixture
from pingspice.analysis import param


class Constraints(constraints.Constraints):
    """
    I provide L{fwd} and L{ts_fwd} constraint checkers.

    @ivar IV_fwd_max: Maximum forward-bias current and voltage to be
        considered.

    @ivar R_lead: Lead resistance (each).

    @ivar Tj_min: Minimum operating temperature (deg C).
    """
    # Boltzmann's constant
    k = 1.38062e-23 # J/K
    # The charge of an electron
    q = 1.60219e-19 # C
    # Nominal SPICE temperature
    T = 300.15 # K
    # Thermal voltage
    Vt = k*T/q
    
    registry = {
        'fwd': [
            None,                               # Linear
            {'d_is', 'd_n', 'd_rs'}],           # Log
        'ts_fwd': [
            None,                               # Linear
            {'if_hcb', 'd_rs'}],                # Log
    }
    
    def fwd(self, params):
        """
        Forward-bias voltage as determined by the diode equation must be
        no less than 1/2 and no more than 2x what is expected at
        maximum specified current.
        """
        maxRatio = 2
        Imax, Vmax = self.IV_fwd_max
        V = params['d_n'] * self.Vt * np.log(Imax/params['d_is'] + 1)
        V += Imax*(params['d_rs'] + 2*self.R_lead)
        if maxRatio*V < Vmax: return False
        return V < maxRatio*Vmax
    
    def ts_fwd(self, params):
        """
        Denominator of current source expression simulating temp-sensitive
        Rs must be > 0 even at coldest rated temp of Tj_min:
    
        M{V(if_hca)*(V(tj)-Tj_min)^2 + V(if_hcb)*V(tj) + V(d_rs)}
        
        """
        denom =  params['if_hcb']*self.Tj_min + params['d_rs']
        return denom > 0


class CapacitanceAnalyzer(psim.Analyzer):
    """
    I analyze diode junction capacitance by calculating what it should
    be given the parameters I{d_vj}, I{cp}, I{d_cjo}, and I{d_m}.
    """
    def avDefine(self, f):
        f.av('d_vj')
        f.av('d_cjo')
        f.av('d_m')
        f.av('cp')

    def func(self, Vca, **kw):
        """
        Returns calculated diode capacitance in Farads.
        """
        Vcar = 1.0/kw['d_vj'] * Vca
        return [kw['cp'] + kw['d_cjo']*np.power(1.0 + Vcar, -kw['d_m'])]


class Diode_Helper(HelperBase):
    """
    Helper for L{Diode_Finder}.

    @ivar w: Emphases for each evaluation. Each entry's value scales
        its target's weight by the square of that value. Default
        values defined in my class attribute I{w} may be overridden by
        an 'emphases' dict spec.
    """
    def __init__(self, specs):
        """
        C{Diode_Helper(specs)}
        """
        super(Diode_Helper, self).__init__(specs)
        self.weight_rr = self.emphasis(341)

    def timeSetup(self, s):
        """
        Everything in diode time setup is common to diodes and MOSFETs.
        """
        self.timeSetupCommon(s)
    
    def weight_IV(self, ID, x):
        if ID > 230 and ID < 233:
            # Setup 231 or 232
            return self.emphasis(ID, 3e5)
        if ID > 260 and ID < 263:
            # Setup 261 or (TODO) 262
            return self.emphasis(ID, 500)
        raise ValueError(sub("Unhandled setup {:d}", ID))

    def weight_Tj(self, ID, x):
        return self.emphasis('temp', 1.0 - 1.2E-4*(x-100.0)**2)


class Diode_Setups(param.Setups):
    """
    Setups for L{Diode_Finder}.
    """
    EvalHelper = Diode_Helper

    defaultSpecs = {
        # Package lead resistance (must be non-zero, as these are used as
        # shunts for power dissipation calculation)
        'R_lead': 0.25E-3,
        # Nominal operating temperature
        'Tj_nom': 25,
        # Minimum operating temperature
        'Tj_min': -50,
        # Maximum operating temperature
        'Tj_max': +200,
    }
    
    def nameLists(self, s):
        x = {}
        #--- DC, pretty fast --------------------------------------------------
        x[231] = ['vac#branch', 'tj', 'vfbd']
        # Setup 232 is only for when no Tj dependency is specified for
        # Vac vs Iac. You won't have both 231 and 232
        if s.gp(232, 'Vmax'):
            x[232] = ['vac#branch', 'vfbd']
        if s.gp(261, 'Vmax'):
            x[261] = ['cathode', '+vca#branch']
            if s.ge('tempsens'):
                x[261].insert(1, 'tj')
        #--- TRAN, medium to slow ---------------------------------------------
        if s.trr:
            x[341] = ['time', 'current']
        #--- Dynamic capacitance measurements (also TRAN, very slow) ----------
        x[441] = ['bias', 'cap']
        #----------------------------------------------------------------------
        return x
    
    def plotSpecs(self, s):
        x = {
        111:("Capacitance vs V", 'cathode', 'cj'),
        231:("Iac vs. Vac", 'vac#branch', 'vfbd'),
        232:("Iac vs. Vac", 'vac#branch', 'vfbd'),
        441:("Cj vs cathode bias", 'bias', 'cap'),
        }
        if s.gp(261, 'Vmax'):
            x[261] = ("Ica vs. Vca", 'cathode', 'vca#branch')
        if s.trr:
            x[341] = ("Reverse Recovery Times", 'time', 'current')
        return x

    def analyzers(self, s):
        ad = {}
        #--- 231 --------------------------------------------------------------
        Vmin, Vmax = s.gp(231, 'Vmin', 'Vmax')
        sweepArgs = s.eh.mms(231, 'vac#branch', N=300)
        if sweepArgs:
            ad[231] = [DC, 'Iac'] + sweepArgs
            if s.ge('tempsens'):
                ad[231].extend(s.eh.Tj_sa(231))
        #--- 232 --------------------------------------------------------------
        if s.gp(232, 'Vmax'):
            ad[232] = [DC, 'Iac'] + s.eh.mms(232, 'vac#branch', N=300)
        #--- 261 --------------------------------------------------------------
        Vmin, Vmax = s.gp(261, 'Vmin', 'Vmax')
        if Vmax:
            ad[261] = [DC, 'Vca'] + s.eh.mms(Vmin, Vmax, 50)
            if s.ge('tempsens'):
                ad[261].extend(s.eh.Tj_sa(261))
        # TODO: 262
        transient = s.ge('transient')
        #--- 341 --------------------------------------------------------------
        if transient and s.g.trr:
            s.eh.TRAN(ad, 341)
        #--- 441 --------------------------------------------------------------
        if transient and s.g.fa_cap:
            s.eh.TRAN(ad, 441)
        #----------------------------------------------------------------------
        return ad

    def independents(self, s):
        x = {
        111:['cathode'],
        231:['vac#branch', 'tj'],
        232:['vac#branch',],
        261:['cathode'],
        341:['time'],
        441:['bias'],
        }
        if s.ge('tempsens'): x[261].append('tj')
        return x

    def Xs(self, s):
        if not s.g.trr:
            return {}
        rre = ReverseRecoveryEvaluator(
            s.trr, s.Qrr, s.Irr_max, True, weight=s.eh.weight_rr)
        rre.errorPerAmp = 10
        return {341: rre}

    def weights(self, s): return {
        'cap':          s.eh.weight_capacitance,
        'vac#branch':   s.eh.weight_IV,
        'vca#branch':   s.eh.weight_IV,
        'vfbd':         s.eh.weight_IV,
        'tj':           s.eh.weight_Tj,
    }

    def transforms(self, s): return {
        # These two operate in tandem
        'bias':         [s.eh.transform_bias, 'bias1', 'cap1'],
        'cap':          [s.eh.transform_capacitance, 'bias1', 'cap1'],
    }
    
    def constraints(self, s):
        IV = s.XYmax(231, 'vac#branch', 'vfbd', tj=self.Tj_nom)
        return Constraints(
            R_lead=self.R_lead, IV_fwd_max=IV, Tj_min=self.Tj_min)
    
    logValues = {'vca#branch', 'cap'}


class DiodeMixin:
    """
    Base class for stuff used by L{Diode_Finder} and also by body
    diode of C{analysis.mosfet.MOSFET_Finder}.
    """
    def sc_diode_fwd(self, f, na, nc, capacitance=False):
        """
        The forward-biased diode primitive. Call with L{Elements} instance
        I{f}, anode node I{na}, and cathode node I{nc}.

        This part of the model has, in series, a (1)
        temperature-sensitive series resistance modeled by a
        behavioral current source and (2) temperature-sensitive
        voltage offset::

            Tj ------------------------------------------------------+
                                                                     |
                    +-- R_sca --+               +------------------+ |
                    |           |               |                  | |
                    |           |               |                  x x
                    |  +-----+  |         +---------+           +-------+
            na -----+->|+ D -|>-+- 110 -->|+ shunt -|>-- 114 -->|+ B:V -|>---+
                       +-----+            +---------+           +-------+    |
                                                                             |
                       +---+                                                 |
            nc <-------| R |<------- 116 -------------<----------------------+
                       +---+
        
        The increase (1) in series resistance with higher temp brings
        forward-biased current curves slightly closer together for a
        given voltage at higher current. Only effective when forward
        biased. Its parameters (all log space) are I{if_hca} and
        I{if_hcb}, plus I{d_rs}, the diode series resistance at the
        coldest temperature I{Tj_min}, defining the total series
        resistance of the diode:

        M{R = if_hca*(Tj-Tj_min)^2 + if_hcb*(Tj-Tj_min) + if_hcc + d_rs}

        The I{if_hcc} term is set to make R = d_rs at nominal
        temperature I{Tj_nom}. It doesn't add a parameter because its
        AV object is entirely computed from I{if_hca} and I{if_hcb}.
        
        Note that the linearized values of I{if_hca} and I{if_hcb} are
        typically many orders of magnitude smaller than I{d_rs}. The
        modeled series resistance doesn't change that much with
        temperature.

        The temperature-sensitive voltage offset (2), a (linear)
        reduction in forward voltage with junction temperature, has a
        single parameter, I{vf_lca} in log space. The offset is zero
        at nominal temperature.

        M{Voff = tanh(6*Vac^2)*vf_lca*(Tj-Tj_nom)} if M{Vac > 0} else
        M{Voff = 0}.
        """
        def expr_rs():
            """
            Increase in series resistance with higher temperature.
            """
            p = "V(if_hca)*(V(tj)-{:g})^2 + V(if_hcb)*(V(tj)-{:g}) + V(if_hcc)"
            expr = sub(p, self.Tj_min, self.Tj_min)
            # Made into a series voltage, and only when diode
            # primitive is forward biased
            return sub("V({},110) > 0 ? i(vsh_df)*({}) : 0", na, expr)

        def expr_vf():
            """
            Decrease in "public" Vf with higher temp, and thus an increase in
            the part of Vf that's across the diode primitive. But
            never to the point of switching between fwd and rev biasing.

            The constant 6 inside the M{tanh()} scales the voltage
            offset to 91% at Vf=0.5 and 36% at Vf=0.25. With Vf >
            0.75, there's substantially no scaling.
            """
            # The linear dVdT term
            expr = sub("V(vf_lca)*(V(tj)-{:g})", self.Tj_nom)
            # Scaled down dramatically when total Vf is low, and zero
            # when total Vf is negative
            return sub(
                "V({},{}) > 0 ? tanh(6*V({},{})^2)*{} : 0",
                na, nc, na, nc, expr)
        
        # -- The diode primitive ----------------------------------------------
        kw = {
            'CJP':      0,
            'FC':       0.5,
            'IS':       f.av('d_is', -16, -2, 'log'),
            # Have not found a single MOSFET body diode that benefited
            # from including the IK term in its model
            'IKR':      f.av('d_ikr', -50, -2, 'log'),
            # I'm not entirely sure that N < 1.0 (linear space) is
            # even a thing. Only a PMOS body diode so far is N > 2.8,
            # and that by a lot.
            'N':        f.av('d_n', -0.3, +0.6, 'log'),
        }
        if capacitance:
            # Ngspice limits VJ to < 1/FC, FC is left at default (0.5)
            kw['VJ'] = f.av('d_vj', 0.03, 1.0) * 1.9999999
            kw['CJO'] = f.av('d_cjo', 0.1*self.Cj_min, 3*self.Cj_max)
            # Ngspice upper limit is M <= 0.9
            kw['M'] = f.av('d_m', 0.1, 0.9)
            kw['TT'] = f.av('d_tt', -11, -5, 'log')
        if self.Vbv and self.Ibv:
            kw['BV'] = self.Vbv
            kw['IBV'] = self.Ibv
        diode = f.MODEL('diode', 'D', **kw)
        f.D(na, 110, diode)
        f.R(na, 110, 1E20) # SCA
        if self.s.ge('tempsens'):
            # Variable part of R_series
            a = f.vav('if_hca', -20, -5, 'log')
            b = f.vav('if_hcb', -20, -3, 'log')
            T_nm = self.Tj_nom - self.Tj_min
            c = -a*(T_nm**2) - b*T_nm
            f.vav('if_hcc', c)
            f.vav('vf_lca', -6, -2, 'log')
            f.Vsh_df(110, 114, 0)
            f.B(114, 116, V=sub("({}) - ({})", expr_rs(), expr_vf()))
            f.R(114, 116, 1.0) # SCA
        else: f.R(110, 116, 0)
        # Fixed part of R_series
        f.R(116, nc, f.av('d_rs', -4, -0, 'log'))
    
    def sc_diode_rev(self, f, na, nc):
        """
        The reverse-biased diode primitive. Call with L{Elements} instance
        I{f}, anode node I{na}, and cathode node I{nc}.::

            Tj -----------+
                          |
                          x
                     +----------+   
            nc --+-->|+ B:temp -|>--+-- na
                 |   +----------+   |
                 |                  |
                 |      +----+      |
                 +------| Rp |------+
                        +----+

        Resistance Rp sets a floor for cathode-anode leakage
        current. This linear response will typically be a minor part
        of overall contributions to leakage current.
        
        If temperature-sensitive reverse leakage modeling is
        considered feasible, this will increase the reverse current at
        higher temperatures. But the leakage from the diode primitive
        (L{sc_diode_fwd}) and will remain regardless.
        
        This method is B{not} used by my subclass L{MOSFET_Model}. It
        models temperature-dependent MOSFET leakage current with its
        L{MOSFET_Model.channel} method.
        """
        if self.s.ge('tempsens'):
            # Current increase over baseline leakage to model increase
            # with higher tj (this simply adds to baseline leakage
            # without caring what it is)
            f.vav('T_chl', -8, -1.5, 'log')
            # If your diode is running hotter than +200 degrees C, you
            # have a problem
            expr = sub(
                "V({},{})*V(T_chl)*(V(tj) > 200 ? 1 : exp(0.08*(V(tj)-200)))",
                nc, na)
            f.B(nc, na, I=expr)
        f.R(nc, na, f.av('Rp', +7, +19.9, 'log'))


class Diode_Finder(param.ParameterFinder, DiodeMixin):
    """
    I am a parameter finder for all stand-alone diodes.
    """
    Setups = Diode_Setups
    showNetlists = []

    def setup(self, f):
        # Parasitics
        self.sc_parasitics(f)
        # Forward-biased diode behavior
        self.sc_diode_fwd(f, 11, 19, capacitance=True)
        # Reverse-biased diode behavior
        self.sc_diode_rev(f, 11, 19)

    def sc_parasitics(self, f):
        # Lead resistance (all lumped onto one lead)
        R = 2*self.R_lead
        f.R('anode', 11, R)
        # Power dissipation measurement using lead resistance as a
        # shunt
        f.B('pdiss', 0, V=sub("{:.5g}*V(anode,{})^2", 1.0/R, 11))
        # Lead inductance (all lumped onto one lead)
        L = f.av('l', 1E-10, 30E-9)
        ts = f.get(self, 'ts')
        f.L(19, 'cathode', L*2, ts=ts)
        if ts is None: f.sca6(19, 'cathode')
        # Fixed parasitic capacitance
        f.C(11, 19, f.av('cp', -14, -9, 'log'))
    
    def stc_231(self, f):
        """
        Setup B{231}: Forward-bias current Iac vs Vac, vs Tj.
        """
        # Current meter because couldn't get i-sweep to show up
        f.Vac('bd_1', 0, 0)
        f.Iac('cathode', 'bd_1', 'DC', 0) # swept
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # swept, with just a few steps
        # Voltage meter across anode-cathode
        f.E('vfbd', 0, 'anode', 'cathode', +1)

    def stc_232(self, f):
        """
        Setup B{232}: Forward-bias current Iac vs Vac, with no temperature
        dependency.
        """
        f.Iac('anode', 'cathode', 'DC', 0) # swept
        f.Vtj('tj', 0, 'DC', self.get('params', 232, 'Tj', default=25.0))
        
    def stc_261(self, f):
        f.Vca('cathode', 'anode', 'DC', 0) # swept
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # Fixed or stepped

    def _checkTestConditions(self, ID):
        """
        Called by L{stc_341} to ensure that this device's test conditions
        have been specified for this setup I{ID}.
        """
        if ID not in self.eh.tsu:
            raise AttributeError(sub(
                "Test conditions not defined for setup {:d}", ID))
        
    def stc_341(self, f):
        """
        Reverse recovery time. The diode is forward-biased with I{I_rr}
        and then the current decreases, crossing into negative
        territory, at a rate of I{dIdt_rr} V/sec.
        """
        self._checkTestConditions(341)
        V, I, dI, dt = self.eh.get_rrParams()
        drf = DiodeRecoveryFixture(f, V_rev=V, I_fwd=I, dIdt=dI/dt)
        drf('anode', 'cathode', 'current')
        f.Vtj('tj', 0, 'DC', self.s.get(
            'params', 341, 'Tj', default=self.Tj_nom))

    def stc_441(self, f):
        """
        Setup B{441}: Capacitance, dynamically measured with biased sinusioid::
                                              
            +-----------------+                   +--------+
            |                 |                   |        |
            |  +--(+)--> npos |>-------->-------->|C >\    |
            |  |          :   |                   |   V    |
            |  |          :   |                   |   V    |
            |  |          :   |                   |   V    |
            |  |    +--< nneg |<-----<-----------<|A </    |
            |  |    |         |                   |        |
            |  |    0         |                   +--------+
            |  |              |                   
            |  |   CM.aB      |                   
            |  |              |
            |  +-------< bias |>---+
            |                 |    |
            |             cap |>---|-----------------------------: 'cap1' 
            |                 |    |
            |         filt_in |<---+
            |                 |
            |        filt_out |>---------------------------------: 'bias1'
            |                 | 
            +-----------------+ 

        Leakage current from the DC bias at the cathode could affect
        capacitance measurement, but should be very small.

        @see: L{MOSFET_Finder.stc_421} for an analogous test setup of
            what is mostly the body diode capacitance of a MOSFET.
        """
        Vmax = 1.2*self.s.Xmax('bias', 441)
        Capacitance_Meter.mc_addedBias(
            f, 'cathode', 'anode', 'bias1', 'cap1',
            Vac=0.2, Vdc=[Vmax, 0], invert_bias=False,
            fa=self.s.g.fa_cap, Na=self.s.g.Na_cap, Nd=self.s.g.Nd_cap,
            Ls=f.av('l'))
        f.Vtj('tj', 0, 'DC', self.Tj_nom)
        
    def setupTestCircuit(self, f, ID):
        """
        Sets up the test circuit for the specified setup I{ID} during
        parameter finding, with the anode tied to ground.
        """
        f.R('anode', 0, RMIN)
        getattr(self, sub("stc_{:02d}", ID))(f)


class Diode(Subcircuit):
    """
    A diode using the setup defined in and params discovered by
    L{Diode_Finder}.

    @cvar nodes: 'anode', 'cathode', 'pdiss' (power
        dissipation), and 'tj' (junction temperature)

    """
    Finder = Diode_Finder
    nodes = ['anode', 'cathode', 'pdiss', 'tj']

    
