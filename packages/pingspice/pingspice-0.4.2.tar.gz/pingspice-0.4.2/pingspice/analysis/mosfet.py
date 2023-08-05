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
A power MOSFET model with evolved parameters.

Includes constraints to avoid torturing Ngspice with bogus parameter
combinations, L{Constraints.vto} and L{Constraints.rs}.

@see: L{pingspice.lib.mosfets} and L{pingspice.analysis.diode}.
"""

import numpy as np
from twisted.internet import defer

from pingspice.util import *
from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Subcircuit
from pingspice.lib.semiconductor import PowerSemiconductorInclude
from pingspice.lib.current import CurrentLimiter, TempShort
from pingspice.lib.active import Capacitance_Meter

from pingspice.analysis import mosfet_analyzers as ma
from pingspice.analysis import diode, mosfet_model
from pingspice.analysis.timing import \
    Q, TimingEvaluator, ReverseRecoveryEvaluator
from pingspice.analysis.fixture import \
    PowerSupply, DrainResistor, HelperBase, DiodeRecoveryFixture
from pingspice.analysis import param


class Constraints(diode.Constraints):
    """
    I provide two constraint checkers in addition to the
    I{diode.Constraints.fwd} and I{diode.Constraints.ts_fwd} checkers
    of my base class: L{rds}, and L{vt}.
    
    @ivar mp: An instance of L{mosfet_model.MOSFET_Physics}.

    @ivar Rds_on: Minimum on-state resistance.

    @ivar Vgs_Rds_on: Vgs at Rds_on.
    
    @ivar VT_max: The maximum allowable value of VT.
    
    """
    registry = {
        'rds': [
            {'rd', 'rs'},                               # Linear
            None,                                       # Log
        ],
        'vt': [
            None,                                       # Linear
            {'m_tox', 'm_NA'},                          # Log
        ],
    }
    registry.update(diode.Constraints.registry)

    def __init__(self, *args, **kw):
        self.mp = mosfet_model.MOSFET_Physics()
        diode.Constraints.__init__(self, *args, **kw)

    def rds(self, p):
        """
        Ensures that I{rd} + I{rs} is less than I{Rds_on}, since the Ohmic
        extrinsic resistances don't even account for the accumulation
        region and fully inverted channel.

        Also keeps I{rs} from being larger than I{rd}. In reality, it
        should be considerably smaller. Not only do electrons have to
        travel much farther in the drift region for I{rd}, but the
        light doping there (<10% of NA in p+ region) makes its
        resistivity much higher than that of the p+ source region for
        I{rs}. The fact that it has more cross-sectional area than the
        source region does not compensate much for those two factors.

        Zheng Yang ("Power MOSFET," ECE442 handout) has VDMOS source
        plus source contact resistivity at 0.06 mOhm/cm^2, with most
        of that being from the contact, and drift plus substrate plus
        drain contact (all part of I{rd}) being 0.41 mOhm/cm^2. (That
        doesn't include accumulation resistance he puts at 0.66
        mOhm/cm^2 and JFET resistance at 0.19 mOhm/cm^2.) This
        corresponds to an I{rs}/I{rd} ratio of about 15%.

        For UMOS, Zheng Yang has source plus contact at 0.0505
        mOhm/cm^2, with the source part vanishingly small. Drift plus
        substrate drain contact is 0.27 mOhm/cm^2 (not including
        accumulation resistance he puts at 0.055 mOhm/cm^2). This
        corresponds to an I{rs}/I{rd} ratio of about 19%.
        """
        if p['rs'] > p['rd']: return False
        Rds = p['rd'] + p['rs'] + 2*self.R_lead
        return Rds < self.Rds_on

    def vt(self, p):
        """
        Ensures that the threshold voltage isn't too high to not allow
        inversion at the lowest Vgs value of setup 211.

        Assumes 1e+18 for polysilicon gate doping.

        B{TODO}: Account for eta. Maybe do Vt calculation the same way
        MOS3 does.
        """
        NG = 1e18
        # Keeps things conservative, so that erroneous VT calculation
        # doesn't preclude legit parameter combos
        extra = 1.2
        return self.mp.VT(p['m_tox'], p['m_NA'], NG) < extra*self.VT_max

    
class MOSFET_Helper(HelperBase):
    """
    Helper for L{MOSFET_Finder}.

    Construct me with an instance of L{analysis.param.Specs} that's
    been populated with attributes defining device-specific variables,
    the device's parameter-finding goals, and any known parameters.

    @cvar w: Dict with default emphases for each setup ID, each
        entry's value scaling its target's weight by the square of
        that value. If no entry, default emphasis is 0.5, which works
        out to unity.

    @cvar s211_scale: Extra weight (scaling) for highest Vgs curve,
        left end increasing to right end.
    """
    s211_scale = (2.0, 3.0)
    
    def __init__(self, specs):
        """
        C{MOSFET_Helper(specs)}
        """
        super(MOSFET_Helper, self).__init__(specs)
        self.weight_rg = self.emphasis(121)
        self.weight_212 = self.emphasis(212, 1)
        self.weight_220 = self.emphasis(220, 5)
        self.weight_Isd = self.emphasis(231, 3e5)
        self.weight_261 = self.emphasis(261, 1e3)
        self.weight_timing = self.emphasis(331, 1.0)
        self.weight_rr = self.emphasis(341, 1.5)
    
    def timeSetup(self, s):
        """
        Sets up TRAN simulation args for step, stop, and possibly stop
        time.
        """
        N = 500
        tsu = self.timeSetupCommon(s)
        # Gate charge stop time (there's no useable default)
        tStop = s.get('params', 321, 'tStop')
        if tStop:
            tsu[321] = [tStop/N, tStop, 0, tStop/(20*N)] # Was 4*N
        # Switching time
        if s.get('timing'):
            tStop = 2*sum([
                s.get('timing', x) for x in ('on', 'rise', 'off', 'fall')])
            tStep = tStop/N
            tList =  [tStep, tStop]
            tMax = max([5E-9, tStep/4])
            if tMax < tStep: tList.extend([0, tMax])
            tsu[331] = tList
        # Turn-on
        for ID, tStop in ((351, 5E-6), (361, 1E-4), (371, 60E-3)):
            t0 = s.get('params', ID, 'ttrig')
            tMax = max([1E-8, tStop/(2*N)])
            tsu[ID] = [tStop/N, t0+tStop, t0, tMax]

    def transform_v2rds(self, ID, Ids, drain):
        """
        Transform Ids (or Isd for P-channel) and V(drain) into Rds.
        """
        return np.abs(drain / Ids)
            
    def transform_v2nrds(self, ID, Tj, Vds):
        """
        Transform Vds (or Vsd for P-channel) with constant known Ids into
        Rds, normalized to Rds at nominal Tj. Make sure that one of
        the swept Tj values is at or very close to nominal.
        """
        rds = np.abs(Vds / self.s.get('params', 271, 'Ids'))
        k = np.argmin(np.abs(Tj-self.s.Tj_nom))
        return rds / rds[k]

    def transform_vgs2nvgs(self, ID, Tj, Vgs):
        """
        Transform Vgs (or Vsg for P-channel) with constant known Ids into
        normalized with Vgs=1.0 at nominal Tj. Make sure that one of
        the swept Tj values is at or very close to nominal.
        """
        k = np.argmin(np.abs(Tj-self.s.Tj_nom))
        return Vgs / Vgs[k]
    
    def transform_i2q(self, ID, t, Vin, Vout):
        """
        Transform current and time into charge with trapezoidal integration.
        """
        if getattr(self, '_Rg_gc', None) is None:
            self._Rg_gc = self.s.get('params', 321, 'Rg')
        I = (Vin - Vout) / self._Rg_gc
        return Q(t, I)

    def transform_ttrig(self, ID, t):
        return t - self.s.get('params', ID, 'ttrig')
    
    def weight_Ids_si(self, ID, x):
        """
        Weighting of setups 211, 221, 222. For setup 223, unity weight
        because Ids isn't the vector of interest.

        For setup 211, the highest Ids at the highest Vgs curve is
        weighted more to help encourage the Ids vs Vds curve to bend
        downward.
        """
        def warp(frac):
            X = self.s.Xrange(ID, 'vds#branch')
            Ids_focus = (1-frac)*X.min() + frac*X.max()
            return self.warp(x, Ids_focus)

        if ID == 223: return 1.0
        scale = 1.4 if ID == 211 else 0.5 if ID == 221 else 5.0
        weight = self.emphasis(
            ID, scale, 25.0, warp(0.5 if ID == 211 else 0.3))
        if ID == 211:
            # Higher weight for highest Vgs curve, especially for
            # higher Vds
            xd = np.diff(x)
            k = np.flatnonzero(xd < -xd.max())[-1] + 1
            S = np.concatenate([
                np.ones(k), np.linspace(
                    self.s211_scale[0], self.s211_scale[1], len(x)-k)])
            weight *= S
        return weight

    def weight_Ids_wi(self, ID, x):
        """
        Weighting of setup 242.
        """
        return self.emphasis(ID, 200)
    
    def weight_Rds(self, ID, x):
        """
        Weighting of setup 223 for Rds with controlled drain current.
        """
        return self.emphasis(ID, 3E6/self.s.Rds_on)

    def weight_vdd(self, ID, x):
        """
        Weighting of setups 241, 351, 361, and 371, for drain voltage
        after a resistor.

        For setups 351, 361, and 371, L{weight_drain} and
        L{weight_gate} also (and primarily) factor into the weighting.
        """
        if ID == 241:
            return self.emphasis(241, 40)
        # Vdd is of secondary importance to drain and gate
        return 0.2
    
    def weight_tempsens(self, ID, x):
        """
        Weighting of setups 261, 271, 272, for temperature sensitivity.

        High for setups 271, 272. Each one is just a single curve for
        a separate important aspect of the MOSFET operation, with
        fairly low SSE produced by significant departures from
        desired.

        (Array) weight values are scaled by each expected value of
        I{x}, and scaled down in aggregate by the cube of the mean
        expected value.
        """
        w = self.emphasis(ID)
        if ID == 261: return w*10
        c = 3E4 if ID == 271 else 1.5E5
        return c*w*x  / np.mean(x)**3

    def weight_gate(self, ID, x):
        """
        Weighting of setup 321, for gate charge, and of setups 351, 361,
        and 371 for gate voltage.

        High for setup 321 because the error figures are relatively
        small compared to IDs, and it's just one curve for an
        important aspect of the MOSFET operation.

        For setups 351, 361, and 371, L{weight_vdd} and (primarily)
        L{weight_drain} also factor into the weighting.
        """
        if ID < 300: return 1.0
        if ID == 321: return self.emphasis(321, 400)
        # Scaled by 10x because drain voltages are usually about that
        # much bigger than gate voltages
        return 10.0
    
    def weight_drain(self, ID, x):
        """
        Weighting of setups 351, 361, 371, for drain voltage with
        controlled current.

        Nominal, but higher around 7A for setup 351.

        L{weight_vdd} and L{weight_gate} also factor into the
        weighting, secondarily.
        """
        if ID < 300: return 1.0
        return self.emphasis(ID, self.warp(x, 7), 10)

    
class MOSFET_Setups(param.Setups):
    """
    Setups for L{MOSFET_Finder}.
    
    Rather than doing a copy-paste of the L{param.ParameterFinder}
    setup config for each and every MOSFET you wish to model, you're
    better off just setting I{Specs} in your subclass to a class whose
    attributes define the particulars, goals, and knowns of that
    device.

    There's really no substitute for looking at the
    U{source<edsuom.com/pingspice/pingspice.analysis.mosfet.py>}.

    See L{param.Setups}, my base class, for information about the
    various dicts that must be defined as class attributes or
    dict-producing methods. I define L{plotSpecs}, L{analyzers},
    L{Xs}, L{weights}, L{transforms} via those dict-producing methods.
    
    @cvar Specs: You must define this in your subclass to a class
        whose attributes define the device-specific variables refenced
        in my setup methods, the device's parameter-finding goals, and
        any known parameters.

    @cvar EvalHelper: My L{param.Setups} base class lets subclasses
        define an evaluation helper that gets instantiated into their
        Specs instances with the I{eh} attribute. Mine is
        L{MOSFET_Helper}.
    
    @cvar defaultSpecs: Default values for my attributes that are
        common to most all MOSFETs. You can override any of these in
        your component's .specs file.
    @type defaultSpecs: dict

    @cvar package: The name of the package L{Subcircuit} in
        L{lib.thermal} for the device used in actual device testing,
        for setups that rely on an actual DUT (e.g., 351).
    @type package: str
    """
    package = None
    EvalHelper = MOSFET_Helper

    defaultSpecs = {
        # Package lead resistance (must be non-zero, as these are used as
        # shunts for power dissipation calculation)
        'R_lead': 0.25E-3,
        # Nominal operating temperature
        'Tj_nom': 25,
        # Minimum operating temperature
        'Tj_min': -50,
        # Maximum operating temperature
        'Tj_max': +175,
    }

    nameLists = {
        #--- Python-only, very fast -------------------------------------------
        # High Rg penalizer
        121:[],
        #--- DC, pretty fast --------------------------------------------------
        # Ids vs Vds, Vgs
        211:['+drain', '+gate', '+vds#branch'],
        212:['+drain', '+gate', '+vds#branch'],
        213:['+drain', '+gate', '+vds#branch'],
        # Weak Inversion to Moderate Inversion: Ids vs Vgs
        220:['+gate', '+vds#branch'],
        # Ids vs Vgs
        221:['+gate', 'tj', '+vds#branch'],
        222:['+gate', 'tj', '+vds#branch'],
        # Rds vs Ids
        223:['+vds#branch', 'rds'],
        # Isd vs -Vdd (body diode)
        231:['vsd#branch', 'tj', 'vfbd'],
        # -Vds vs -Vdd (body diode)
        241:['+drain', '+vdd'],
        # Vds vs Vgs
        242:['+gate', '+vdd#branch'],
        # Ids vs Tj (body diode, leakage)
        261:['+drain', 'tj', '+vdd#branch'],
        262:['tj', '+drain', '+vdd#branch'],
        # Normalized Rds vs Tj
        271:['tj', 'nrds'],
        # Normalized Vgs vs Tj
        272:['tj', 'nvgs'],
        #--- TRAN, medium to slow ---------------------------------------------
        # Gate charge
        321:['charge', '+gate'],
        # Switching times
        331:['time', '+gate', '+drain'],
        # Reverse recovery time (body diode)
        341:['time', 'current'],
        # Turn-on, fast
        351:['ttrig', '+gate', '+vdd', '+drain'],
        # Turn-on, slow
        361:['ttrig', '+gate', '+vdd', '+drain'],
        # Vgs TRAN sweep
        371:['time', '+gate', '+vdd', '+drain'],
        #--- Dynamic capacitance measurements (also TRAN, very slow) ----------
        411:['bias', 'cap'],
        421:['bias', 'cap'],
        431:['bias', 'cap'],
        #----------------------------------------------------------------------
    }
    
    def plotSpecs(self, s):
        ps = {
        111:("Crss vs Vds", 'drain', 'crss', 'coss', 'ciss'),
        121:("Rg penalty",),
        
        211:("Ids vs. Vds, with stepped Vgs", 'drain', 'vds#branch'),
        212:("Ids vs. Vds, with stepped Vgs", 'drain', 'vds#branch'),
        231:("Body diode: Isd vs. Vsd", 'vsd#branch', 'vfbd'),
        241:("Body diode: |Vdd| vs Vsd", 'drain', 'vdd'),
        261:("Body diode: log(Ids) vs Tj", 'tj', 'vdd#branch'),
        262:("Body diode: log(Ids) vs Tj", 'tj', 'vdd#branch'),
        271:("Normalized Rds vs Tj", 'tj', 'nrds'),
        272:("Normalized Vgs vs Tj", 'tj', 'nvgs'),
        
        321:("Vgs vs. gate charge", 'charge', 'gate'),
        331:("Switching Times", 'time', 'gate', 'drain'),
        341:("Reverse Recovery Times", 'time', 'current'),
        351:(sub(
            "Turn-on (Rg={:.0f}, Rd={:.2f})", *s.gp(351, 'Rg', 'Rd')),
            'ttrig', 'gate', 'vdd', 'drain'),
        361:(sub(
            "Turn-on (Rg={:.0f}, Rd={:.2f})", *s.gp(361, 'Rg', 'Rd')),
            'ttrig', 'gate', 'vdd', 'drain'),
        371:("Vdd, Vds vs. Vgs", 'time', 'vdd', 'drain', 'gate'),
        411:("Ciss vs Vds bias", 'bias', 'cap'),
        421:("Coss vs Vds bias", 'bias', 'cap'),
        431:("Crss vs Vds bias", 'bias', 'cap'),
        }
        for Tj in s.gperator(213, 'Tj'):
            ps[213] = (
                sub("Ids vs. Vds, stepped Vgs, Tj={:+.1f}", Tj),
                'drain', 'vds#branch')
        for Vds in s.gperator(220, 'Vds'):
            ps[220] = (
                sub("Weak to Moderate Inversion (Vds={:.1f})", Vds),
                'gate', 'vds#branch')
        for Vds in s.gperator(221, 'Vds'):
            ps[221] = (
                sub("Ids vs. Vgs (Vds={:.1f})", Vds), 'gate', 'vds#branch')
        for Vds in s.gperator(222, 'Vds'):
            ps[222] = (
                sub("Ids vs. Vgs (Vds={:.1f})", Vds), 'gate', 'vds#branch')
        for Vgs in s.gperator(223, 'Vgs'):
            ps[223] = (
                sub("Rds vs. Ids (Vgs={:.1f})", Vgs), 'vds#branch', 'rds')
        Vdd, Rd, Tj = s.gp(242, 'Vdd', 'Rd', 'Tj')
        if Vdd and Rd:
            if not Tj: Tj = 25.0
            ps[242] = (
                sub("Ids vs Vgs (Vdd={:.2f}, Rd={:.5g}, Tj={:+.1f}",
                    Vdd, Rd, Tj),
                'gate', 'vdd#branch')
        return ps
    
    def analyzers(self, s):
        return ma.Analyzers(s)()
    
    def independents(self, s):
        ad = {
        111:['drain'],
        121:[],
        211:['drain', 'gate'],
        212:['drain', 'gate'],
        213:['drain', 'gate'],
        220:['gate'],
        221:['gate'],
        222:['gate', 'tj'],
        223:['vds#branch'],
        231:['vsd#branch'],
        241:['drain'],
        242:['gate'],
        261:['drain', 'tj'],
        262:['tj'],
        271:['tj'],
        272:['tj'],
        321:['charge'],
        331:['time'],
        341:['time'],
        351:['ttrig'],
        361:['ttrig'],
        371:['time', 'gate'],
        411:['bias'],
        421:['bias'],
        431:['bias'],
        }
        if s.ge('tempsens'):
            for ID in (221, 231):
                ad[ID].append('tj')
        return ad

    def Xs(self, s):
        X = {}
        Vgs, Vds_max = s.gp(331, 'Vgs', 'Vds_max')
        X[331] = TimingEvaluator(
            Vgs, Vds_max,
            s.get('timing', 'on'),
            s.get('timing', 'rise'),
            s.get('timing', 'off'),
            s.get('timing', 'fall'),
            weight=s.eh.weight_timing)
        N_channel = s.get('architecture', 'N_channel', default=True)
        X[341] = ReverseRecoveryEvaluator(
            s.g.trr, s.g.Qrr, s.g.Irr_max, N_channel, weight=s.eh.weight_rr)
        if s.get('params', 212, 'Vds_max'):
            X[212] = ma.StrongInversionAnalyzer(s.eh.weight_212)
        Vgs_min, Ids_min = s.gp(220, 'Vgs_min', 'Ids_min')
        if Vgs_min:
            X[220] = ma.WeakToModerateInversionAnalyzer(
                s.g.Vgs_min, s.g.Ids_min, s.eh.weight_220)
        return X

    def weights(self, s): return {
        'vds#branch':           s.eh.weight_Ids_si,
        'vdd#branch':           s.eh.weight_Ids_wi,
        'vfbd':                 s.eh.weight_Isd,
        'vdd':                  s.eh.weight_vdd,
        'drain':                s.eh.weight_drain,
        'gate':                 s.eh.weight_gate,
        'nrds':                 s.eh.weight_tempsens,
        'nvgs':                 s.eh.weight_tempsens,
        'rds':                  s.eh.weight_Rds,
        'cap':                  s.eh.weight_capacitance,
    }

    def transforms(self, s): return {
        'rds':          [s.eh.transform_v2rds, 'vds#branch', 'drain'],
        'nrds':         [s.eh.transform_v2nrds, 'tj', 'drain'],
        'nvgs':         [s.eh.transform_vgs2nvgs, 'tj', 'gate'],
        'charge':       [s.eh.transform_i2q, 'time', '+gc_2', '+gate'],
        'ttrig':        [s.eh.transform_ttrig, 'time'],
        # These next two operate in tandem
        'bias':         [s.eh.transform_bias, 'bias1', 'cap1'],
        'cap':          [s.eh.transform_capacitance, 'bias1', 'cap1'],
    }
    
    def constraints(self, s):
        IV_231 = s.XYmax(231, 'vsd#branch', 'vfbd', tj=self.Tj_nom)
        IV = [0, 0] if IV_231 is None else IV_231
        VV_241 = s.XYmax(241, 'drain', 'vdd')
        if VV_241 is not None:
            Vd, Vdd = VV_241
            R = s.get('params', 241, 'Rd')
            I = (Vdd-Vd)/R
            if I > IV[0]: IV = [I, Vd]
        return Constraints(
            VT_max=s.Xrange(211, 'gate')[0],
            Rds_on=self.Rds_on, R_lead=self.R_lead,
            IV_fwd_max=IV, Tj_min=self.Tj_min, Vds_BV=self.Vds_BV)
    
    logValues = {'vdd#branch', 'cap'}

        
class MOSFET_Finder(param.ParameterFinder):
    """
    I am a parameter finder for all MOSFETs, hopefully flexible enough
    that the only subclassing you need to do is to change my I{Setups}
    attribute to your own subclass of L{MOSFET_Setups}.
    
    Here is the general progression of node numbering from the package
    leads to the MOSFET primitives::
    
         drain -> 11 -> 15 -> 17 -> 19
          gate -> 21 -> 25 -> 27 -> 29
        source -> 31 -> 35 -------> 39

    @ivar s: An instance that I construct of the L{MOSFET_Setups}
        subclass referenced in your subclass of me with the I{Setups}
        class attribute.

    @cvar Setups: The subclass of L{MOSFET_Setups} that your subclass
        uses.

    @cvar L_tfr: Conservatively estimated series inductance (H) of a
        test fixture resistor plus connecting conductors. See
        U{https://www.edn.com/design/components-and-packaging/4423492/Resistors-aren-t-resistors}.
        Also, per Marc Thompson (Intuitive Analog Circuit Design,
        p. 419), 10 nH per cm of lead length, over a ground plane.
    """
    Setups = MOSFET_Setups
    showNetlists = []
    L_tfr = 7E-9 # H

    @property
    def ao(self):
        if not hasattr(self, '_ao'):
            self._ao = mosfet_model.ArchOpts(self.s.get('architecture'))
        return self._ao
    
    def sc_leads(self, f):
        """
        Setup circuit: Package lead impedances, plus power dissipation
        measurement using resistive portions of those impedances::
    
             drain -> 11 -> 15 |
              gate -> 21 -> 25 |
            source -> 31 -> 35 |
                               +-- pdiss
        
        Lead inductances can cause simulation trouble even though
        they're small, because they create high transient voltages at
        very high frequencies, probably a lot higher than you're
        interested in. If I{ts} (time step) is set, either in my
        spec/subclass/instance or globally, the inductors will be
        simulation-friendly with parallel capacitance and resistance
        added to mitigate that.

        ON Semiconductor's Application Note AN-6099 says, "Industry
        standard through-hole type TO-220 package has 7nH of typical
        lead inductance, but typical lead inductance of PQFN56 SMD
        package is only 1nH." Parameter finding of a few MOSFETs with
        TO220 and TO247 packages has come up with drain inductance
        I{ld} values in that range, perhaps a bit lower, and
        I{lgs_vs_ld} (a multiple of drain inductance for gate and
        source inductance, modeling the different connection those
        terminals make to the semiconductor die) of up to 3x or more,
        which seems a bit unrealistic.
        
        Inductance will be omitted if there is a 'transient' item set
        in the spec's 'disabled' dict.
        """
        if not self.s.ge('transient'):
            k = 4
            ts = None
        else:
            k = 0
            # The range of ld is quite a bit bigger than realistic,
            # but sometimes you can sacrifice a little bit of realism
            # to make the model fit. Sometimes, and carefully.
            Ld = f.av('ld', 5.0E-10, 1.2E-8)
            # One would expect the drain connection to have the lowest
            # inductance as it connects directly to the bottom surface
            # of the die, whereas gate and source connections are wire
            # bonded. But 3.5x inductance for those latter two is a
            # bit higher than realistic. Again, go ahead and make the
            # model fit, but with caution.
            Lgs = Ld * f.av('lgs_vs_ld', 1.0, 3.5)
            ts = f.get(self, 'ts')
            if ts is None:
                f.L(11, 15, Ld)
                f.sca6(11, 15)
                f.L(21, 25, Lgs)
                f.sca6(21, 25)
                f.L(31, 35, Lgs)
                f.sca6(31, 35)
            else:
                f.L(11, 15, Ld, ts=ts)
                f.L(21, 25, Lgs, ts=ts)
                f.L(31, 35, Lgs, ts=ts)
        parts = []
        scale = 1.0 / self.R_lead
        for kk, n1 in enumerate(('drain', 'gate', 'source')):
            n2 = kk*10+k+11
            parts.append(sub("{:.5g}*V({})*V({},{})", scale, n1, n1, n2))
            f.R(n1, n2, self.R_lead)
            if ts is None: continue
            # TODO: Is this cap really necessary for SCA? Can throw
            # off pdiss calc!
            f.C(n1, n2, 2*ts*scale)
        # Power dissipation is in kiloWatts, not Watts. That is an
        # attempt to limit the overall numerical range of values being
        # processed, since leakage currents are in the picoAmps.
        f.B('pdiss', 0, V=sub("0.001*abs({})", " + ".join(parts)))
        f.R('pdiss', 0, 1.0) # SCA

    def setup(self, f):
        """
        My circuit setup method, which constructs the overall MOSFET model
        circuit by constructing an instance of L{MOSFET_Model} and
        calling its L{MOSFET_Model.setup} method.
        """
        self.N_channel = self.s.get('architecture', 'N_channel', default=True)
        self.sc_leads(f)
        kw = {
            # Breakdown voltage and current at breakdown (implemented
            # with body diode)
            'Vbv': self.Vds_BV,
            'Ibv': self.Ids_BV,
            # For resistance
            'Rds_on': self.Rds_on,
            'Rg_leakage': self.Vgs_max/self.Ig_leakage,
            # For temp sensitivity
            'Tj_nom': self.Tj_nom,
            'Tj_min': self.Tj_min,
            # For capacitance
            'Cj_min': self.Coss_min,
            'Cj_max': self.Coss_max,
            'Crss_min': self.Crss_min,
            'Crss_max': self.Crss_max,
            'Ciss_min': self.Ciss_min,
        }
        if hasattr(self, 'ts'): kw['ts'] = self.ts
        Irev = self.s.g.Irev
        kw['Irev_min'] = min(Irev.values()) if Irev else 1E-7
        mm = mosfet_model.MOSFET_Model(self.s, **kw)
        mm.setup(f)
    
    def R(self, f, n1, n2, resistance):
        """
        A slightly more realistic test fixture resistor, with a small
        amount of parasitic inductance from the connecting conductors
        and the resistance material itself.
        """
        n12 = f.iNode(n1)
        f.R(n1, n12, resistance)
        f.L(n12, n2, self.L_tfr, ts=f.get(self, 'ts'))
        
    def stc_211(self, f, Tj=None):
        """
        Setup B{211}: Ids (-Ids) vs Vds (Vsd), Vgs (Vsg)
        """
        f.Vds(*self.ao.npr('drain', 'source', 'DC', 0)) # swept
        f.Vgs(*self.ao.npr('gate', 'source', 'DC', 0)) # swept
        f.Vtj('tj', 0, 'DC', self.Tj_nom if Tj is None else Tj)

    def stc_212(self, f):
        """
        Setup B{212}: Ids (-Ids) vs Vds (Vsd), Vgs (Vsg)
        """
        self.stc_211(f)

    def stc_213(self, f):
        """
        Setup B{213}: Ids (-Ids) vs Vds (Vsd), Vgs (Vsg), non-nominal Tj.
        """
        Tj = self.s.get('params', 213, 'Tj')
        self.stc_211(f, Tj)
        
    def stc_220(self, f, V=None):
        """
        Setup B{220}: Ids (-Ids) vs Vgs (Vsg) with fixed Vds (Vsd)
        """
        if V is None: V = self.s.get('params', 220, 'Vds')
        f.Vds(*self.ao.npr('drain', 'source', 'DC', V))
        f.Vgs(*self.ao.npr('gate', 'source', 'DC', 0)) # swept
        f.Vtj('tj', 0, 'DC', self.Tj_nom)

    def stc_221(self, f, V=None):
        """
        Setup B{221}: Ids (-Ids) vs Vgs (Vsg) with fixed Vds (Vsd)
        """
        self.stc_220(f, self.s.get('params', 221, 'Vds'))
        
    def stc_222(self, f):
        """
        Setup B{222}: Just like L{stc_221}.
        """
        self.stc_220(f, self.s.gp(222, 'Vds'))

    def stc_223(self, f):
        """
        Setup B{223}: Rds vs Ids.
        """
        # Current meter because couldn't get i-sweep to show up
        f.Vds(*self.ao.npr('drain_1', 0, 0))
        f.Ids(*self.ao.npr('drain_1', 'drain', 'DC', 0)) # swept
        f.Vgs('gate', 'source', self.s.gp(223, 'Vgs'))
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # Room temperature
        
    def stc_231(self, f):
        """
        Setup B{231}: Body diode, forward-bias current -Ids vs -Vds. For
        PMOS, Ids vs -Vsd.
        """
        # Current meter because couldn't get i-sweep to show up
        f.Vsd(*self.ao.npr('bd_1', 0, 0))
        f.Isd(*self.ao.npr('drain', 'bd_1', 'DC', 0)) # swept
        f.Vgs('gate', 'source', 1) # shorted
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # swept, with just a few steps
        # Voltage meter across BD anode-cathode, positive for both
        # NMOS and PMOS
        f.E('vfbd', 0, 'source', 'drain', self.ao.npi(+1))
        
    def stc_241(self, f):
        """
        Setup B{241}: Body diode, forward-bias voltage -Vds vs -Vdd after a
        known resistance I{R}. For PMOS, Vds vs Vdd.
        """
        f.Vdd(*self.ao.npr('source', 'vdd', 'DC', 0)) # swept
        self.R(f, 'vdd', 'drain', self.s.get('params', 241, 'Rd'))
        f.R('gate', 'source', 0) # shorted
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # Room temperature

    def stc_242(self, f):
        """
        Setup B{242}: Vds after drain resistor vs Vgs in weak and moderate
        inversion.
        """
        Vdd, Rd, Tj = self.s.gp(242, 'Vdd', 'Rd', 'Tj')
        f.Vdd(*self.ao.npr('vdd', 'source', 'DC', Vdd))
        f.Vgs(*self.ao.npr('gate', 'source', 'DC', 0)) # swept
        self.R(f, 'vdd', 'drain', Rd)
        if not Tj: Tj = 25.0
        f.Vtj('tj', 0, 'DC', Tj)
        
    def stc_261(self, f):
        """
        Setup B{261}: Body diode, reverse-bias current Ids vs Vds with one
        or more junction temperatures tj. For PMOS, Isd & Vsd.
        """
        f.Vdd(*self.ao.npr('drain', 'source', 'DC', self.s.gp(261, 'Vds_max')))
        f.Vgs('gate', 'source', 0) # shorted
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # fixed at nominal or stepped

    def stc_262(self, f):
        """
        Setup B{262}: Body diode, reverse-bias current Ids vs
        junction temperature tj with one or more Vds. For PMOS, Isd &
        Vsd.
        """
        f.Vdd(*self.ao.npr('drain', 'source', 'DC', 0)) # swept
        f.Vgs('gate', 'source', 0) # shorted
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # swept
        
    def stc_271(self, f):
        """
        Setup B{271}: Normalized on-state Rds vs junction temperature tj
        with fixed Vgs and Ids. For PMOS, fixed -Vgs & -Ids.
        """
        Vgs, Ids = self.s.gp(271, 'Vgs', 'Ids')
        f.Vgs('gate', 'source', self.ao.npi(Vgs))
        f.Ids('source', 'drain', self.ao.npi(Ids))
        f.R('source', 'drain', 1E6) # For when bogus params make Rds infinite
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # swept

    def stc_272(self, f):
        """
        Setup B{272}: Normalized Vgs with gate shorted to drain to achieve
        a fixed Ids vs junction temperature tj. For PMOS, fixed -Ids.
        """
        f.Rgd('gate', 'drain', 1)
        f.Ids('source', 'drain', self.ao.npi(
            self.s.gp(272, 'Ids', default=250e-6)))
        f.R('source', 'drain', 1E7) # SCA, 1E9 was too high
        f.Vtj('tj', 0, 'DC', self.Tj_nom) # swept

    def _checkTestConditions(self, ID):
        """
        Called by L{stc_321}, L{stc_331}, and L{stc_341} to ensure that this
        device's test conditions have been specified for this setup I{ID}.
        """
        if ID not in self.eh.tsu:
            raise AttributeError(sub(
                "Test conditions not defined for setup {:d}", ID))
        
    def stc_321(self, f):
        """
        Setup B{321}: Gate charge.
        
        Adapted from test circuit in ST Datasheet, STB75NF20, STP75NF20 -
        STW75NF20, Figure 16 ("Gate charge test circuit")
        """
        self._checkTestConditions(321)
        Vds_max, Vgs, Ig, Rg, Id = self.s.gp(
            321, 'Vds_max', 'Vgs', 'Ig', 'Rg', 'Id')
        # Rails: Source is always at ground, even with PMOS device
        # -------------------------------------------------------------------
        f.Vds('vdd', 0, self.ao.npi(Vds_max))
        # Gate
        # -------------------------------------------------------------------
        f.V('gc_1', 0, 'DC', 0, Paren('PULSE', 0, self.ao.npi(Vgs), 0, 20E-6))
        # Gate current limiter
        CurrentLimiter(
            f, Imax=abs(Ig), Vmin=0.01*Vgs, uni=True,
            reverse=self.ao.P_channel)('gc_1', 'gc_2')
        # Gate resistor
        self.R(f, 'gc_2', 'gate', Rg)
        f.sca('gate')
        # Drain
        # -------------------------------------------------------------------
        # Drain current limiter
        CurrentLimiter(
            f, Imax=abs(Id), Vmin=0.01*Vds_max, uni=True,
            reverse=self.ao.P_channel)('vdd', 'drain')
        f.R('drain', 'source', 1e6) # SCA
    
    def stc_331(self, f):
        """
        Setup B{331}: Switching times.
        """
        self._checkTestConditions(331)
        Vds_max, Vgs, Rg, Rd = self.s.gp(331, 'Vds_max', 'Vgs', 'Rg', 'Rd')
        Vg = self.ao.npi(Vgs)
        f.V('st_1', 0, 'DC', 0, Paren(
            'PULSE', 0, Vg, 2E-8, 5E-9, 5E-9, 0.5*self.eh.tsu[331][1]))
        self.R(f, 'st_1', 'gate', Rg)
        f.V('vdd', 0, self.ao.npi(Vds_max))
        self.R(f, 'vdd', 'drain', Rd)
    
    def stc_341(self, f):
        """
        Setup B{341}: Reverse recovery time (body diode).
        """
        self._checkTestConditions(341)
        Vdd, Is, dI, dt = self.eh.get_rrParams()
        drf = DiodeRecoveryFixture(f, V_rev=Vdd, I_fwd=Is, dIdt=dI/dt)
        drf(*self.ao.npr('source', 'drain', 'current'))
        f.R('gate', 'source', self.s.get('params', 341, 'Rgs', default=RMIN))
        f.Vtj('tj', 0, 'DC', self.s.get(
            'params', 341, 'Tj', default=self.Tj_nom))

    def _drainCircuit(self, f, params):
        P_channel = not self.s.get('architecture', 'N_channel', default=True)
        PowerSupply(
            f, t0=params['ttrig'],
            Vbatt=params['Vbatt'], isNegative=P_channel)('vdd', 0)
        DrainResistor(f, R=params['Rd'])('vdd', 'drain')
    
    def stc_351(self, f, ID=351):
        """
        Setup B{351}: Turn-on, fast, with measurements from an actual
        device.

        Control voltage ramps up to short analog switches and hasten
        charging, then ramps down to restore analog switches to
        desired resistance.
        """
        params = self.s.get('params', ID)
        if not params:
            return
        t0 = params['ttrig']
        self._drainCircuit(f, params)
        f.Vgs('vgs', 0, 'DC', 0, Paren(
            'PULSE', 0, self.ao.npi(9.0), t0, 30E-9))
        TempShort(f, t0=t0, R_off=params['Rg'], R_on=10)('vgs', 'to_1')
        # ~1 mm wire/component lead about 1 cm over ground plane for
        # about 4 cm
        ts = f.get(self, 'ts')
        f.L('to_1', 'gate', 25E-6, ts=ts)
        f.sca('to_1', 'gate')
    
    def stc_361(self, f):
        """
        Setup B{361}: Turn-on, slow, with measurements from an actual
        device. See L{stc_351}.
        """
        self.stc_351(f, 361)

    def stc_371(self, f):
        """
        Setup B{371}: Vgs, TRAN, with measurements from an actual device.
        """
        params = self.s.get('params', 371)
        if not params:
            return
        self._drainCircuit(f, params)

    def stc_411(self, f):
        """
        Setup B{411}: Ciss, dynamically measured with sinusioid and bias
        on drain using an L{AC_Current_Meter} subcircuit::

                                                            +--------+
                                                            |        |
            +---------------+              +---<-- C --+---<|D <\    |
            |               |              |           |    |   ^    |
            |          npos |>-- 'gate' ---|--->-------|--->|G >X    |
            |           :   |              |           |    |   V    |
            |   CM.sB   :   |              V           |    |   V    |
            |           :   |              |           |    |   V    |
            |    +---< nneg |<-- 'source'--+---<-------|---<|S </    |
            |    |          |                          |    |        |
            |    0          |                          |    +--------+
            |               |                          |
            |          bias |>---- R -- 'drain' -------+    
            |               |                          |
            |           cap |>-------------------------|-------: 'cap1' 
            |               |                          |
            |       filt_in |<-------------------------+
            |               |
            |      filt_out |>---------------------------------: 'bias1'
            |               |
            +---------------+   

        B-source I{B:current} calculates the current flowing through R
        and adds it to I{current0} to generate the final output
        voltage at node I{current}.

        There is some tension with the values of R and C. The value of
        C has to be significantly higher than the MOSFET's Cgd. The
        value of R has to be low enough, in combination with C, that
        the RC time constant (to charge C as bias increases) is
        significantly less than the ramp-up time of the bias
        voltage. But the lower R is, the more AC current will leak
        through it back to the bias source instead of being measured.

        In order to keep R high, a relatively high time constant is
        tolerated and the bias output of CM is overdriven.
        """
        # Higher Vds_max to make up for RC time constant of
        # bias/blocking circuit and matching LPF in CM
        Vds_max = 1.2*self.s.Xmax('bias', 411)
        Capacitance_Meter.mc_separateBias(
            f, 'gate', 'source', 'bias', 'cap1', 'drain', 'bias1',
            Vac=0.2, Vdc=[Vds_max, -0.2], invert_bias=self.ao.P_channel,
            fa=self.s.g.fa_cap, Na=self.s.g.Na_cap, Nd=self.s.g.Nd_cap,
            Ls=f.av('ld')*f.av('lgs_vs_ld'))
        # Select R, C for DC bias and blocking
        # -----------------------------------------------------------------
        C = 0.2e-6 # >> Max Ciss (200 nF vs <5 nF)
        tsu = self.eh.tsu[411]
        tc = tsu[1] - tsu[2]
        R = 0.1*tc/C # Time constant << Vds ramp time 
        f.R('bias', 'drain', R)
        f.C('drain', 'source', C)
        # -----------------------------------------------------------------
        f.Vtj('tj', 0, 'DC', self.Tj_nom)
        
    def stc_421(self, f):
        """
        Setup B{421}: Coss, dynamically measured with biased sinusioid::
                                              
            +-----------------+                   +--------+
            |                 |                   |        |
            |  +--(+)--> npos |>-------->-------->|D >\    |
            |  |          :   |                   |   V    |
            |  |          :   |           +------<|G <X    |
            |  |          :   |           |       |   V    |
            |  |    +--< nneg |<-----<----+       |   V    |
            |  |    |         |           |       |   V    |
            |  |    0         |           +------<|S </    |
            |  |              |                   |        |
            |  |   CM.aB      |                   +--------+
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

        Leakage current from the DC bias at the drain could affect
        capacitance measurement, but should be very small.
        """
        Vds_max = 1.2*self.s.Xmax('bias', 421)
        Capacitance_Meter.mc_addedBias(
            f, 'drain', 'gate', 'bias1', 'cap1',
            Vac=0.2, Vdc=[Vds_max, 0], invert_bias=self.ao.P_channel,
            fa=self.s.g.fa_cap, Na=self.s.g.Na_cap, Nd=self.s.g.Nd_cap,
            Ls=f.av('ld'))
        f.R('gate', 'source', 0)
        f.Vtj('tj', 0, 'DC', self.Tj_nom)

    def stc_431(self, f):
        """
        Setup B{431}: Crss, dynamically measured with biased sinusioid::
                                              
            +-----------------+                   +--------+
            |                 |                   |        |
            |  +--(+)--> npos |>-------->-------->|D >\    |
            |  |          :   |                   |   V    |
            |  |          :   |           +------<|G <X    |
            |  |          :   |           |       |   V    |
            |  |    +--< nneg |<-----<----+       |   V    |
            |  |    |         |                   |   V    |
            |  |    0         |             +----<|S </    |
            |  |              |             |     |        |
            |  |   CM.aB      |             0     +--------+
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

        Leakage current from the DC bias at the drain could affect
        capacitance measurement, but should be very small.

        """
        Vds_max = 1.2*self.s.Xmax('bias', 431)
        Capacitance_Meter.mc_addedBias(
            f, 'drain', 'gate', 'bias1', 'cap1',
            Vac=0.2, Vdc=[Vds_max, 0], invert_bias=self.ao.P_channel,
            fa=self.s.g.fa_cap, Na=self.s.g.Na_cap, Nd=self.s.g.Nd_cap,
            Ls=f.av('ld')+f.av('ld')*f.av('lgs_vs_ld'))
        f.R('source', 0, RMIN)
        f.Vtj('tj', 0, 'DC', self.Tj_nom)
        
    def setupTestCircuit(self, f, ID):
        """
        Sets up the test circuit for the specified setup I{ID} during
        parameter finding.

        Increases my I{ts} sim option to the computational timestep of
        this setup's transient analysis if needed to make
        simulation-friendly components work.

        For all setups but the capacitance measurements, source is
        tied to ground.
        """
        f.NODESET(pdiss=0)
        if ID in self.eh.tsu:
            tArgs = self.eh.tsu[ID]
            f.set('ts', tArgs[3] if len(tArgs) > 3 else tArgs[0])
        if ID < 400: f.R('source', 0, RMIN)
        getattr(self, sub("stc_{:02d}", ID))(f)
        if ID in (321, 331, 351, 361, 371):
            # Actual device measurements with potential effects from
            # self-heating; attach a package if one was defined in specs
            package = getattr(self, 'package', None)
            if not package:
                raise ValueError(sub(
                    "Setup {:d} requires the modeled MOSFET in the test "+\
                    "circuit to have a package defined", ID))
            # Device characterization tests are done in open air
            # in a cool room, with the DUT mounted on a large heatsink
            ambient = 22.0
            tc0 = self.s.get('params', ID, 'Tc', default=None)
            # If Tc was stupidly not measured at start of test, use
            # stupid guess of ambient+10 degrees C
            tca0 = 10 if tc0 is None else tc0-ambient
            f.vav('tca0', tca0)
            # Second element of heatsink (cth_c) is a guess based on a
            # guess of 3x mass of Ohmite WV-T247-101E
            PowerSemiconductorInclude(
                f, 'tj', 'pdiss',
                # Second element of heatsink (cth_c) is a guess
                # based on a guess of 3x mass of Ohmite
                # WV-T247-101E
                heatsink=(2.6, 36.0),
                package=package, ambient=ambient)


class MOSFET(Subcircuit):
    """
    A MOSFET semiconductor die (including the leads but not the
    package thermal behavior), using the setup defined in and params
    discovered by L{MOSFET_Finder}.

    @cvar nodes: 'drain', 'gate', 'source', 'pdiss' (power
        dissipation), and 'tj' (junction temperature). L{PowerMOSFET}
        will also have 'tc' and 'tca0' at the end.
    """
    Finder = MOSFET_Finder
    nodes = ['drain', 'gate', 'source', 'pdiss', 'tj']
