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
Analyzers and analyzer setup for a power MOSFET model with evolved
parameters.

Imported into L{pingspice.analysis.mosfet}.
"""

import re

import numpy as np

from pingspice.util import *

from pingspice.analysis import psim
from pingspice.analysis.sim import DC, TRAN
from pingspice.analysis.fixture import LumpinessCalculator


class GateResistancePenalizer(psim.Analyzer):
    """
    Pushes back against the model's tendency of unrealistically
    increasing gate resistance to conform to datasheets' conservative
    transition times.

    @ivar weight: The weight to multiply SSE by.
    
    @ivar us_rg: The multiple between I{rg} and my target I{rg0} that
        results in an unweighted SSE contribution of one. The penalty
        is B{cubed}, so double this multiple will cause SSE+8.

    @ivar rg0: The estimated gate resistance, from datasheet or
        educated guess. There's no default, because this analyzer
        isn't included unless an at least guesstimated gate resistance
        is known.
    """
    weight = 1.0
    us_rg = 1.20

    def __init__(self, rg0, us_rg=None, weight=None):
        """C{GateResistancePenalizer(rg0, us_rg=None)}"""
        self.rg0 = rg0
        if not us_rg: us_rg = self.us_rg 
        self.coeff = 1.0/us_rg
        if weight: self.weight = weight

    def __getstate__(self):
        """
        Needed for WireEvaluator because L{__init__} sets attributes.
        """
        return {'rg0':self.rg0, 'coeff':self.coeff, 'weight':self.weight}
    def __setstate__(self, state):
        for name in state:
            setattr(self, name, state[name])
        
    def avDefine(self, f):
        f.av('rg')
        
    def func(self, **kw):
        """
        Returns an SSE that is non-zero and thus a penalty for 'rg' above
        my I{rg0} value.
        """
        Rg = kw['rg']
        if Rg < self.rg0: return 0.0
        return self.weight * np.power(self.coeff*Rg/self.rg0, 3)


class WeakToModerateInversionAnalyzer(object):
    """
    I evaluate the transition from weak inversion to moderate
    inversion, including switch-off to <= I{Ids_0} at I{Vgs_0} and
    smoothness, for setup 220.

    @cvar us_smooth: The amount of lumpiness that adds 1 to the
        SSE. Squared, so 10x that lumpiness will add SSE +100.

    @cvar us_off: The amount of Ids in excess of the target I{Ids_0}
        at I{Vgs_0} that adds 1 to the SSE. Squared, so 10x that much
        excess current will add SSE +100.
    """
    us_smooth = 0.1
    us_off = 0.05
    
    def __init__(self, Vgs_0, Ids_0, weight, invert=False):
        self.Vgs_0 = Vgs_0
        self.Ids_0 = Ids_0
        self.weight = weight
        self.lc = LumpinessCalculator(clipping=True)
        self.sign = -1 if invert else +1

    def offness(self, X, Y):
        # This should result in k = 0
        k = np.argmin(np.abs(X-self.Vgs_0))
        Ids_0 = Y[k]
        if Ids_0 < self.Ids_0: return 0, k
        return ((Ids_0 - self.Ids_0)/self.us_off)**2, k

    def smoothness(self, X, Y):
        m, XY = self.lc(X, self.sign*Y)
        return m/(self.us_smooth**2), XY
    
    def __call__(self, Vgs, Ids):
        offness, k0 = self.offness(Vgs, Ids)
        smoothness, XY = self.smoothness(Vgs, Ids)
        XY_left = np.array([[Vgs[k0], self.Ids_0]])
        XY_right = np.array([[Vgs[-1], Ids[-1]]])
        XY = [XY_left, XY, XY_right] if len(XY) else [XY_left, XY_right]
        return self.weight*(offness+smoothness), np.row_stack(XY)


class StrongInversionAnalyzer(object):
    """
    I evaluate the Ids vs Vds curves in strong inversion to ensure
    that the curves are sensible as Vds increases to near breakdown
    voltage, for setup 212.

    The curve for each Vgs should never have a negative first
    derivative. It also shouldn't have a positive second derivative,
    though that incurs less drastic of an SSE penalty.

    @cvar us_first: The amount of negative d(Ids)/d(Vds) between
        any pair of points on any Vgs curve that adds 1 to the
        SSE. Square, so 10x this negative slope will add SSE +100.

    @cvar us_second: The amount of positive d2(Ids)/d(Vds)2 between
        any pair of points on any Vgs curve that adds 1 to the
        SSE. Not squared, so 10x this negative slope will add SSE +10.
    """
    us_first = 0.2
    us_second = 4e-3

    def __init__(self, weight):
        self.weight = weight

    def derivative(self, X, Y):
        dX = np.diff(X)
        K = np.flatnonzero(dX)
        if len(K):
            dY = np.diff(Y)[K]
            dX = dX[K]
            return dY / dX
        
    def __call__(self, Vds, Vgs, Ids):
        def addXY():
            for k, SSEk in zip(Kf, SSE):
                if SSEk > 1:
                    XY.append([Vds_K[k], Vgs_k, Ids_K[k]])
        
        SSE_total = 0
        XY = [[Vds.min(), Vgs.min(), Ids.min()]]
        for Vgs_k in np.unique(Vgs):
            K = np.flatnonzero(Vgs == Vgs_k)
            Vds_K = Vds[K]
            Ids_K = Ids[K]
            # -- First derivative ------------------------------
            dIdV = self.derivative(Vds_K, Ids_K)
            if dIdV is None: continue
            Kf = np.flatnonzero(dIdV < 0)
            SSE = np.square(dIdV[Kf]/self.us_first)
            addXY()
            SSE_total += np.sum(SSE)
            # -- Second derivative -----------------------------
            d2IdV2 = self.derivative(Vds_K[1:], dIdV)
            if d2IdV2 is None: continue
            Kf = np.flatnonzero(d2IdV2 > 0)
            SSE = d2IdV2[Kf]/self.us_second
            addXY()
            SSE_total += np.sum(SSE)
            # --------------------------------------------------
        XY.append([Vds.max(), Vgs.max(), Ids.max()])
        return self.weight*SSE_total, np.array(XY)


class RevCurrentEvaluator(object):
    """
    I evaluate temperature-sensitive reverse leakage current for setup
    261.

    B{TODO}: Delete this. Do this like it's done for diode setup 261.
    """
    def __init__(self, TI, weight):
        self.TI = TI
        self.TI_log = {}
        for ID in TI:
            self.TI_log[ID] = np.log10(TI[ID])
        self.weight = weight
        
    def __call__(self, Tj, Ids):
        """
        Evaluates junction temps I{Tj} and I{Ids} (the latter supplied in
        log space) at those temps, given expectations in my dict
        I{TI_log}.
        """
        SSE = 0
        points = []
        for k, I_log in enumerate(Ids):
            Tjk = Tj[k]
            key = int(Tjk)
            if key not in self.TI: continue
            Ie_log = self.TI_log[key]
            SSE += np.square(I_log - Ie_log)
            points.append([Tjk, Ie_log])
        # SSE independent of number of points evaluated
        SSE /= k+1
        SSE *= self.weight
        return SSE, np.array(points)


class Analyzers(object):
    """
    Construct an instance of me with a L{Specs} object and then you
    can call the instance to obtain a dict of appropriate analyzers.

    Used by L{MOSFET_Setups.analyzers}.
    """
    reSetupMethod = re.compile(r's[1-9][0-9]{2}$')
    
    def __init__(self, s):
        self.s = s
        self.mms = s.eh.mms
        self.tsu = s.eh.tsu
        self.tempsens = s.ge('tempsens')
        self.body_diode = s.ge('body_diode')
        self.transient = s.ge('transient')

    def TRAN(self, ID, **kw):
        """
        Adds an L{analysis.sim.TRAN} analyzer to my analyzer dict I{ad}
        for the specified setup I{ID}, with I{(name, value)} tuples
        for any keywords supplied.
        """
        if ID in self.tsu:
            ads = [TRAN]
            ads.extend(self.tsu[ID])
            for name in kw:
                ads.append((name, kw[name]))
            self.ad[ID] = ads
        
    def add(self, ID, *args):
        """
        Adds an analyzer for setup I{ID}, using the supplied args.

        The args are all concatenated into a list that becomes the
        entry for that ID. If an arg is a list, its elements are what
        get concatenated.
        """
        items = []
        for arg in args:
            if isinstance(arg, list):
                items.extend(arg)
            else: items.append(arg)
        self.ad[ID] = items

    def __call__(self):
        """
        Call my instance to obtain a dict of appropriate analyzers.
        """
        self.ad = {}
        for name in dir(self):
            if self.reSetupMethod.match(name):
                f = getattr(self, name)
                f(self.s)
        return self.ad
    
    def s121(self, s):
        """
        Penalty for unrealistic gate resistance.
        """
        if self.transient and s.g.Rg:
            self.add(
                121, GateResistancePenalizer(s.g.Rg, weight=s.eh.weight_rg))
            
    def s211(self, s):
        """
        DC curve trace: Ids vs Vds for several Vgs.

        Most basic setup, always run.
        """
        self.add(
            211, DC,
            'Vds', self.mms(211, 'drain'), 'Vgs', self.mms(211, 'gate'))

    def s212(self, s):
        """
        DC curve trace: Ids vs Vds for several Vgs, with extended Vds.

        Curve shapes evaluated by L{StrongInversionAnalyzer}.
        """
        Vds_max, Vgs_min, Vgs_max = s.gp(212, 'Vds_max', 'Vgs_min', 'Vgs_max')
        if not Vds_max: return
        if not Vgs_max: Vgs_max = s.g.Vgs_max
        self.add(
            212, DC,
            'Vds', self.mms(0, Vds_max, 100),
            'Vgs', np.floor(Vgs_min), np.ceil(Vgs_max), 1.0)

    def s213(self, s):
        """
        DC curve trace: Ids vs Vds for several Vgs, at non-nominal Tj.
        """
        self.add(
            213, DC,
            'Vds', self.mms(213, 'drain'), 'Vgs', self.mms(213, 'gate'))
        
    def s220(self, s):
        """
        DC curve trace: Ids vs Vgs with fixed Vds.

        Curve shape evaluated by L{WeakToModerateInversionAnalyzer}.
        """
        Vds, Vgs_min, Vgs_max = s.gp(220, 'Vds', 'Vgs_min', 'Vgs_max')
        if not Vds: return
        if not Vgs_min:
            raise ValueError("You must specify 220:Vgs_min")
        if not Vgs_max: Vgs_max = min([2*Vgs_min, 0.5*s.Vgs_max])
        self.add(220, DC, 'Vgs', self.mms(Vgs_min, Vgs_max, 100))

    def s221(self, s):
        """
        DC curve trace: Ids vs Vgs with fixed Vds, possibly at multiple
        temperatures.
        """
        args = [DC, 'Vgs'] + self.mms(221, 'gate', N=100)
        if self.tempsens: args.extend(s.eh.Tj_sa(221))
        self.add(221, *args)

    def s222(self, s):
        """
        DC curve trace: Ids vs Vgs with fixed Vds, at multiple
        temperatures.

        Add this analysis setup to setup 221 when the MOSFET datasheet
        specified an additional set of Ids vs Vgs curves for a
        different Vds range, and at multiple temperatures.
        """
        if s.gp(222, 'Vds') and self.tempsens:
            self.add(222, DC, 'Vgs', self.mms(222, 'gate'), s.eh.Tj_sa(222))

    def s223(self, s):
        """
        On-resistance Rds calculated from Ids & Vds, vs Ids, at fixed Vgs.
        """
        if s.gp(223, 'Vgs'):
            self.add(223, DC, 'Ids', self.mms(223, 'vds#branch', notZero=True))

    def s231(self, s):
        if not self.body_diode or not s.gp(231, 'Isd_max'): return
        args = [DC, 'Isd'] + self.mms(231, 'vsd#branch', N=100)
        if self.tempsens:
            args.extend(s.eh.Tj_sa(231, maxStep=10))
        self.add(231, *args)

    def s241(self, s):
        """
        DC curve trace: Vdd (voltage across MOSFET and drain resistor in
        series) vs reverse MOSFET voltage, i.e. forward-biased body
        diode voltage.

        From measurements done with an actual device under test.
        """
        if not self.body_diode or not s.gp(241, 'Rd'): return
        Vdd_max = s.Xmax('vdd', 241)
        if Vdd_max:
            self.add(241, DC, 'Vdd', 0, Vdd_max, 0.1)

    def s242(self, s):
        """
        DC curve trace: Vdd (voltage across MOSFET and drain resistor in
        series), Vds, vs Vgs in weak and moderate inversion.

        From measurements done with an actual device under test.
        """
        Vgs_min, Vgs_max = s.gp(242, 'Vgs_min', 'Vgs_max')
        if Vgs_max:
            self.add(242, DC, 'Vgs', self.mms(Vgs_min, Vgs_max, 50))
            
    def s261(self, s):
        """
        DC curve trace: Ids vs Vdd, with Tj fixed at nominal or stepped.
        """
        Vds_min, Vds_max = s.gp(242, 'Vds_min', 'Vds_max')
        if Vds_max:
            args = [262, DC] + self.mms(Vds_min, Vds_max, 50)
            if self.tempsens:
                args.extend(s.eh.Tj_sa(231, maxStep=10))
            self.add(261, *args)

    def s262(self, s):
        if not self.tempsens: return
        self.add(
            262, DC,
            'Vtj', self.mms(262, 'tj', N=100),
            'Vdd', self.mms(262, 'drain'))

    def s271(self, s):
        if not self.tempsens: return
        self.add(271, DC, 'Vtj', s.Tj_min, s.Tj_max, 1)

    def s272(self, s):
        if not self.tempsens: return
        self.add(272, DC, 'Vtj', s.Tj_min, s.Tj_max, 1)
        
    def s321(self, s):
        """
        Gate charge.
        """
        if self.transient: self.TRAN(321)

    def s331(self, s):
        """
        Switching time.
        """
        if self.transient: self.TRAN(331)

    def s341(self, s):
        """
        Body diode reverse recovery.
        """
        if self.body_diode and self.transient: self.TRAN(341)

    def s351(self, s):
        """
        Fast turn-on.
        """
        if self.transient: self.TRAN(351)

    def s361(self, s):
        """
        Slow turn-on.
        """
        if self.transient: self.TRAN(361)

    def s371(self, s):
        """
        Vgs TRAN.
        """
        if self.transient: self.TRAN(371)

    def s411(self, s):
        """
        Capacitance measurement: Ciss.
        """
        if self.transient and s.g.fa_cap: self.TRAN(411)

    def s421(self, s):
        """
        Capacitance measurement: Coss.
        """
        if self.transient and s.g.fa_cap: self.TRAN(421)

    def s431(self, s):
        """
        Capacitance measurement: Crss.
        """
        if self.transient and s.g.fa_cap: self.TRAN(431)
