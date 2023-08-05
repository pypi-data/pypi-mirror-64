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
Evaluation helpers, for L{pingspice.analysis.mosfet} but perhaps
useful elsewhere.
"""

from decimal import Decimal, ROUND_DOWN, ROUND_UP

import numpy as np
from scipy import stats

from twisted.internet import defer

from pingspice.util import *
from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Subcircuit
from pingspice.analysis.sim import TRAN
from pingspice.lib.passive import Capacitor, Wire, WirePair


class PowerSupply(Subcircuit):
    """
    For Vdd -> drain, the test fixture for real-component
    characterization used a stack of 9V batteries in series, a 75 Ohm
    wirewound power resistor, a 22000 uF capacitor, with some smaller
    capacitors in parallel, and a nominally 10 Ohm thin-film power resistor.

    @ivar t0: Set this to the charge-up time.
    """
    Vbatt = 63.3
    R_charge = 75.0
    # From measurements, and within +/- 20% tolerance of 22000 uF
    C = 19000E-6
    isNegative = False

    nodes = ['pos', 'neg']
    
    def setup(self, f):
        # A nominally 22000 uF capacitor was used, fed through a 75
        # Ohm resistor by seven 9V batteries in series. Short the
        # resistor and possibly scale down its capacitance for fast
        # charging.
        Vbatt = -self.Vbatt if self.isNegative else self.Vbatt
        tr = 0.1*self.t0
        f.V(11, 'neg', 'DC', 0, Paren(
            'PULSE', 0, Vbatt, 0, tr))
        f.R(11, 12, self.R_charge)
        f.C(12, 'neg', 0.2*tr/self.R_charge) # Essential SCA!
        # Nominally 22000 uF cap with its rated ESR and default
        # guesstimated ESL
        Capacitor(
            f, C=self.C, ESR=10.8E-3, fivi=self.t0)(12, 'neg')
        # Very loosely twisted pair, 18 AWG, from big cap to test
        # fixture (was more like 9 inches and 10-20 mm gap, but trying
        # to match how it behaved)
        WirePair(
            f, a_has_all_RL=True,
            awgs=[18, 18], length=4, gap=5)(12, 'pos')
        # Two 220 uF electrolytics in series right near the drain resistor
        # 2x ESR, rated at 10% dissipation factor. But ripple seemed better
        # than 2 x 0.6 Ohms.
        Capacitor(
            f, C=110E-6, ESR=0.8, ESL=5E-9,
            V_max=100, fivi=self.t0)('pos', 'neg')
        # A 1 uF film cap right near the drain resistor
        f.C('pos', 102, 1E-6)
        Wire(f, awg=18, length=0.8)(102, 'neg')


class DrainResistor(Subcircuit):
    """
    A drain power resistor used for characterization of behavior not
    specified in a datasheet. Used for the RFP12N10L MOSFET.

    @ivar R: The resistance measured during the characterization test.
    """
    nodes = ['vdd', 'drain']
    
    def setup(self, f):
        f.R('vdd', 1, self.R)
        # The thick film Vishay RCH50S10R00JS06, is rated at "<0.1 uH"
        f.L(1, 'drain', 0.1E-6, ts=f.get(self, 'ts'))


class DiodeRecoveryFixture(Subcircuit):
    """
    A test fixture for testing diode reverse recovery in a
    simulation-friendly way::

                            +---+         +----+ 
             +-- 10 ----+-->| R |-------->| A+ |
             |          |   +---+         |    | 
             |          |                 |    |
         +---------+    |        +-------<| C- |
         |   +     |   R (SCA)   |        +----+ 
         | V:Pulse |    |        |         DUT   
         |   -     |    |        |
         +---------+    |        |
             |          |        |
             +----------+--------+

    The V source starts at +I{V_rev}, with R selected to push I{I_fwd}
    amps through the forward-biased diode, assuming it has a typical
    voltage drop of 0.7V (much smaller than the voltage source, so
    doesn't have to be exact or even really accounted for).

    There is a high-value resistance in parallel with the V source for
    SCA (SPICE convergence aid), as with many V and B sources
    throughout. (Usually, SCA resistors are not shown on the diagram.)

    To drop the current at the specified rate of I{dIdt}, the V source
    goes from full positive to zero in time M{I_fwd / dIdt}::

        +---//--------------------------//-------------+
        |:       :         :               :           |
        |:--//---,         :               :         ,-|
        |:       :\        :               :        /  |
        |:       : \       :               :       /   |
        |:       :  \      :               :      /    |
        |:       :   \     :               :     /     |
        |.............\........................./......|
        |:       :     \   :               :   /       |
        |:       :      \  :               :  /        |
        |:       :       \ :               : /         |
        |:       :        \:   V:Pulse     :/          |
        |:       :         '---------------' <----------- V_rev
        |:       :         :               :           |
        +:--//---:---------:------------//-:-----------+
         :       :         :               :           
         :       :         :               :           
        +:--//---:---------:------------//-:-----------+
        |:       :         :               :           |
        |:--//---,     <--- I_fwd          :           |
        |:       :\        :               :           |
        |:       : \       :               :           |
        |:       :  \      :               :           |
        |:       :   \     :        Iac    :           |
        |:..//........\........ ,,------//-:-----------|
        |:       :     \   :   /           :           |
        |:       :      ''---''            :           |
        |0       ts        ts+tr           ts+tr+tp    |
        +:--//---:---------:------------//-:-----------+
         :       :        
         :       +------- Beginning of "rise" time
         +------------Beginning of TRAN simulation
    
    @ivar V_rev: The cathode-anode voltage at full reverse bias.
    
    @ivar I_fwd: The forward current supplied at full forward
        bias.

    @ivar dIdt: The derivative of diode current as it transitions from
        forward to reverse bias.

    """
    reverse = False
    
    nodes = ['anode', 'cathode', 'current']

    @staticmethod
    def timing(I_fwd, dIdt):
        """
        Returns pulse start time I{ts}, rise (and fall) time I{tr}, and
        pulse width time I{tp}.
        """
        tr = 2 * I_fwd / dIdt
        ts = 10*tr
        tp = 10*tr
        return ts, tr, tp
    
    def setup(self, f):
        ts, tr, tp = self.timing(self.I_fwd, self.dIdt)
        f.Vpulse(10, 'cathode', DC=0, PULSE=[
            +self.V_rev, -self.V_rev, ts, tr, tr, tp])
        f.R(10, 'cathode', 1e9) # SCA
        R = self.V_rev / self.I_fwd
        f.R(10, 'anode', R)
        f.H('current', 0, 'Vpulse', +1)
        f.R('current', 0, 1) # SCA


class HelperBase(object):
    """
    Base class for L{Diode_Helper} and L{MOSFET_Helper}.

    Construct me with an instance of L{analysis.param.Specs} that's
    been populated with attributes defining device-specific variables,
    the device's parameter-finding goals, and any known parameters.
    
    @cvar w: Dict with emphases for each evaluation setup, each entry
        keyed by setup ID and scaling its target's weight by the
        square of its value.

    @cvar weightN: Weight of number of steps column vs excess range
        column in L{prettyStep}.
    """
    weightN = 0.2

    def __init__(self, specs):
        """
        C{MOSFET_Helper(specs)}
        """
        self.s = specs
        self.w = {}
        w = specs.get('emphasis')
        for ID in w:
            self.w[ID] = w[ID]
        self.timeSetup(specs)
        self.bc_cache = {}; self.bmaxs = {}

    def timeSetup(self, s):
        """
        Override this in your subclass.
        """
        raise NotImplementedError()
        
    def timeSetupCommon(self, s):
        """
        Call this from your subclass's override of L{timeSetup} to get
        common stuff done.
 
        Returns a reference to my timing setup dict I{tsu}, with
        entries for partial (common) setup. There may be entries that
        won't ever be used for your particular type of device, and
        that's OK.
        """
        tsu = self.tsu = {}
        # Reverse recovery setup 341
        V, I, dI, dt = self.get_rrParams()
        ts, tr, tp = DiodeRecoveryFixture.timing(I, dI/dt)
        tsu[341] = [tr/100, ts+tr+tp, ts]
        # Capacitance setups 4xx
        fa = s.g.fa_cap
        if fa:
            # Number of timesteps per AC test cycle, minimum 10
            Ns = s.g.Ns_cap; Ns = max([Ns, 10])
            # Number of AC test cycles in the ramp-up, minimum 100
            Na = s.g.Na_cap; Na = max([Na, 100])
            # Number of AC test cycles in warm-up before ramp-up starts
            Nd = s.g.Nd_cap
            # Ngspice TRAN time values
            tStep = 1.0/(Ns*fa)
            tRamp = float(Na)/fa
            tStart = float(Nd)/fa
            for ID in range(411, 451, 10):
                # MOSFET setup 411 with its RC in the bias circuit
                # needs more time to let actual bias (at drain) settle
                # down to near zero
                tDwell = 10*tStart if ID == 411 else tStart
                tsu[ID] = [tStep, tRamp+tStart+tDwell, tStart]
        # Done with common stuff
        return tsu

    def get_rrParams(self):
        """
        Call this to get a 4-tuple with parameters V, I, dI, and dt for
        reverse recovery.
        """
        V, I, R, dI, dt = self.s.gp(341, 'V', 'I', 'R', 'dI', 'dt')
        if R and I:
            # Current and series resistance are specified, so voltage
            # can be derived
            V = R*I
        elif V and I:
            # Voltage and current are specified, so series resistance
            # can be derived
            R = V/I
        elif V and R:
            # Voltage and series resistance are specified, so current
            # can be derived
            I = V/R
        else: raise ValueError("You must specify two of V, I, and R")
        return V, I, dI, dt
        
    def TRAN(self, analyzerDict, ID, **kw):
        """
        Adds an L{analysis.sim.TRAN} analyzer to the supplied
        I{analyzerDict} for the specified setup I{ID}, with I{(name,
        value)} tuples for any keywords supplied.
        """
        if ID in self.tsu:
            ads = [TRAN]
            ads.extend(self.tsu[ID])
            for name in kw:
                ads.append((name, kw[name]))
            analyzerDict[ID] = ads

    def gcd_seq(self, X):
        """
        Returns the greatest common denominator of values in sequence
        I{X}, or C{None} if there is no GCD.

        The result will be C{None} if the values are not all equal to
        integers.
        """
        def gcd(a, b):
            while b:
                a, b = b, a%b
            return a

        if len(X) == 1: return X[0]
        worst = None
        for kx, x in enumerate(X):
            for ky, y in enumerate(X):
                if kx == ky: continue
                this_gcd = gcd(x, y)
                if this_gcd < 1: return
                if worst is None or this_gcd < worst:
                    worst = this_gcd
        return worst

    def sss(self, X, N_max, M=1, maxStep=None, minStep=None):
        """
        Returns a 3-list with the start, stop, and step values for doing a
        DC sweep of values in sequence I{X} that lands exactly on all
        its values, or C{None} if no such sweep is possible.

        @keyword M: Multiplier of the number of steps. Sometimes M > 1
             helps Ngspice convergence.
        """
        if M != int(M):
            raise ValueError("M must be an integer.")
        if len(X) == 1: return [X[0], X[0], 1]
        try:
            Xd = np.diff(X)
        except:
            print "Error trying to differentiate X, fix!"
            print X
            import pdb; pdb.set_trace() 
        coeffs = np.array([1, 2, 4, 5, 10])
        coeffs = np.unique(np.concatenate(
            [coeffs, 2*coeffs, 5*coeffs, 10*coeffs]))
        for coeff in coeffs:
            gcd = self.gcd_seq(coeff*Xd)
            if gcd is not None:
                step = 1.0/coeff * gcd
                break
        else: return
        start = X.min()
        stop = X.max()
        while M > 0:
            step_k = step / M
            if maxStep and step_k > maxStep:
                M += 1
                continue
            if minStep and step_k <= minStep:
                break
            if (stop - start)/step_k < N_max:
                break
            M -= 1
        else: return
        return [start, stop, step_k]
    
    def Tj_sa(self, ID, N=50, maxStep=None, minStep=None):
        """
        Returns the additional arguments for a secondary DC sweep of the
        junction temperature that best fits the 'tj' values for goals
        of the specified setup I{ID}.
        """
        Tjs = self.s.Xrange(ID, 'tj')
        if Tjs is None:
            Tjs = np.array([-50, +175])
        sss = self.sss(Tjs, N, maxStep=maxStep, minStep=minStep)
        if sss is None:
            raise ValueError(sub(
                "No valid sweep possible for Tj! in setup {:d}!", ID))
        return ['Vtj'] + sss

    @staticmethod
    def decimal(value, mult, ceil=False):
        if ceil:
            value = mult*np.ceil(value/mult)
        else:
            value = mult*np.floor(value/mult)
        value = Decimal(value).quantize(Decimal(str(mult)))
        return float(value)
    
    def prettyStep(self, Zmin, Zmax, Nmax, mult=0.01, notStep=None):
        """
        Finds a "pretty" step size to go from I{Zmin} (or slightly below)
        to I{Zmax} (or slightly above) in as close as possible (but
        not more than) I{Nmax} steps with limited precision.

        Returns the step size and number of steps.

        @keyword mult: Set to the precision of the step size (e.g.,
            0.1 for one digit, 0.01 for two digits).
        """
        Zmm = Zmax - Zmin
        ZRE = 1.0 / np.arange(max([1, Nmax/10]), Nmax+1)
        ZRE = np.column_stack([ZRE, ZRE])
        SN = []
        for k, NN in enumerate(ZRE[:,0]):
            Zstep = mult*np.ceil(NN*Zmm/mult)
            if Zstep == notStep:
                err = float('+inf')
            else:
                Zrange = Zstep/NN
                err = (Zrange - Zmm) / Zmm
            ZRE[k,1] = err
            SN.append([Zstep, int(np.round(1.0/NN))])
        ZRE[:,0] *= self.weightN
        k = np.argmin(np.sum(np.square(ZRE), axis=1))
        return self.decimal(SN[k][0], mult), SN[k][1]

    @staticmethod
    def includesZero(Zmin, Zmax, step):
        Z = Zmin
        while Z <= Zmax:
            if Z == 0: return True
            Z += step
    
    def prettyRange(self, Zmin, Zmax, Nmax, mult, notZero=False, notStep=None):
        """
        """
        def lower(N):
            return self.decimal(Zmid - 0.5*step*N, mult)

        def upper(N):
            return self.decimal(Zmid + 0.5*step*N, mult, ceil=True)

        step, N = self.prettyStep(Zmin, Zmax, Nmax, mult=mult, notStep=notStep)
        Zmid = 0.5*(Zmin + Zmax)
        Zmid = mult*np.round(Zmid/mult)
        ZZmin = lower(N)
        ZZmax = upper(N)
        if notZero:
            while self.includesZero(ZZmin, ZZmax, step):
                ZZmin, ZZmax, step = self.prettyRange(
                    Zmin, Zmax, Nmax, mult=mult, notStep=step)
        return [ZZmin, ZZmax, step]
    
    def mms(self, *args, **kw):
        """
        Returns a suitable B{m}in, B{m}ax, and B{s}tep for a DC sweep of a
        vector.

        Call patterns with 1, 2, or 3 arguments:

            - Sequence I{Z}: 1-D Numpy array with unique values.

            - Setup I{ID} and vector I{name}: Uses the unique
              values of the goal points of that vector.

            - I{Zmin}, I{Zmax}, and I{N}: Lower and upper bounds to be
              covered and a maximum number of steps acceptable for the
              sweep.
        
        For some stupid reason, it sometimes does seem to help Ngspice
        convergence to keep the step size "pretty", e.g., 0.1 to go
        from 3.0 to 10.1 in 72 steps instead of 0.071 in 100
        steps. But it's not consistent.

        @keyword N: The maximum number of steps acceptable for the
            sweep. (Disregarded with 3 args.)

        @keyword M: Multiplier of the number of steps. Sometimes M > 1
            helps Ngspice convergence. (Disregarded with 3 args.)

        @keyword N_digits: The number of digits after the decimal
            point allowable in the step size.

        @keyword maxStep: The maximum step to use if an exact match is
            found. (Disregarded with 3 args.)
        
        @keyword notZero: Set C{True} to prevent the sweep from
            including exactly zero.
        """
        N = kw.get('N', 500)
        M = kw.get('M', 1)
        mult = 10**-kw.get('N_digits', 2)
        maxStep = kw.get('maxStep', None)
        notZero = kw.get('notZero', False)
        N_args = len(args)
        if N_args == 1:
            Z = args[0]
        elif N_args == 2:
            Z = self.s.Xrange(*args)
        else:
            return self.prettyRange(args[0], args[1], args[2], mult, notZero)
        if Z is None: return
        sss = self.sss(Z, N, M, maxStep)
        if sss is None:
            Zmin = Z.min()
            Zmax = Z.max()
            sss = self.prettyRange(Zmin, Zmax, N, mult, notZero)
        return sss
    
    def warp(self, x, x0, power=0.3):
        """
        Warps the values of I{x} that are close to I{x0}.

        Called by L{weight_Ids} and I{weight_drain} to put increased
        emphasis at goal points near certain drain currents and
        voltage.
        """
        y = np.power(np.abs(x)/x0 + 1.0, -power)
        return np.power(2, power) * y

    def emphasis(self, ID, *args):
        """
        Returns the square of the emphasis for the specified setup I{ID},
        multiplied by the product of any arguments.
        
        Nominal emphasis is 0.5, so compensates for that by multiplying
        its square by 4.0.
        """
        result = 4*self.w.get(ID, 0.5)**2
        for x in args:
            result *= x
        return result

    def _bc_fix(self, ID, bias1, cap1):
        """
        Called by L{transform_bias} and L{transform_capacitance} to obtain
        a cleaned-up version of I{bias1} and I{cap1}.

        The clean up consists of (1) flipping each vector so that bias
        is in ascending order of voltage, and (2) in the flipped
        version, clipping bias just past the maximum goal value and
        setting capacitance to the value at the clipped bias value.

        All transformed vectors must have the exact same number of
        elements as the input vectors, and this method honors that
        requirement.
        
        The first time called with a given pair of I{bias} and I{cap}
        vectors, stores the cleaned-up pair in my I{bc_cache}
        dict. The second time, pops the stored pair and returns that
        instead of re-computing. A given pair is never retrieved from
        the cache more than once.
        """
        # The sum of Numpy array Python id (memory location) values is
        # a perfectly reasonable way to sort-of hash the pair of those
        # objects
        key = id(bias1) + id(cap1)
        if key in self.bc_cache:
            # Cached, return and lose cached version
            return self.bc_cache.pop(key)
        # Flip so bias voltage is in ascending order
        bias = np.flipud(bias1)
        cap = np.flipud(cap1)
        # Clip at just past maximum goal value
        if ID not in self.bmaxs:
            # Only need to calculate maxBias once per setup
            self.bmaxs[ID] = self.s.Xmax('bias', ID) * 1.05
        # Clip bias
        k = np.argmin(np.abs(bias-self.bmaxs[ID]))
        bias[k:] = bias[k]
        cap[k:] = cap[k]
        # Save and return
        bc = (bias, cap)
        self.bc_cache[key] = bc
        return bc
    
    def transform_bias(self, ID, bias1, cap1):
        return self._bc_fix(ID, bias1, cap1)[0]
    
    def transform_capacitance(self, ID, bias1, cap1):
        return self._bc_fix(ID, bias1, cap1)[1]

    def weight_capacitance(self, ID, x):
        """
        Weighting of 'cap' tranformed value for setups 4xx.
        """
        K = np.argsort(x)
        w = np.empty_like(x)
        w[K] = 1 + 5*np.linspace(1, 0, len(x))**4
        return self.emphasis(ID, 3e3, 1.0/(x.max()-x.min())**2) * w


class LumpinessCalculator(object):
    """
    Call an instance of me to obtain a scalar metric that indicates
    the "lumpiness" of a vector I{Y} that transitions from a lower
    value to a higher value.

    The metric is computed using the second derivative of I{Y}, given
    the accompanying I{X} vector. The values of I{Y} can be all
    positive, all negative, or transition from negative to
    positive. Only the derivatives matter.

    The value of the metric is zero for a smooth, non-reversing
    transition. That is achieved when the second
    derivative never goes from negative to positive.

    The metric is proportional (nonlinearly) to the sum of slopes of
    all positive-going zero crossings of the second derivative
    I{ss}.

    If the I{clipping} constructor keyword is set C{True}, the metric
    also includes a term I{c} times I{pr}, the latter being the ratio
    of negative 2nd-derivative peak to standard deviation of the
    2nd-derivative, taken to power I{Nc}.

    With unity I{weight}, the metric should be around one for a very
    lumpy vector, assuming there isn't clipping causing I{pr} to be
    significant. The equation for the metric is::

        metric = weight*((a*ss/(Y[-1]-Y[0]))^b + c*pr

    where I{ss} is the sum of slopes and M{Y[-1]-Y[0]} is the total
    transition that I{Y} makes over the interval, and M{pr =
    abs((min(ddY)-mp)/mp))^Nc} and I{mp} is the maximum positive peak
    of I{ddY}, if any.

    The metric is scaled down by the square of the number of lumps as
    that number starts to exceed fifteen or so. The idea is that a
    vector with tons of very tiny lumps isn't really lumpy at all,
    just slightly quantized.
    
    @keyword clipping: Set C{True} to check clipping with by including
        the I{pr} term.

    @cvar Ns: The number of samples +/- I{k} for the linear regression
        that calculates the slopes in L{slope}.

    @cvar Nc: The exponent for calculation of I{pr}.
    """
    Ns = 6
    a = 150
    b = 0.4
    c = 0.01
    Nc = 4
    weight = 1.0

    def __init__(self, clipping=False):
        self.check_clipping = clipping
    
    def find_zero_crossings_NP(self, Y):
        """
        Returns a list of indices of the supplied vector I{Y} where the
        value is negative and the next value is positive.

        Negative values within 10^-15 of zero are not considered negative.
        """
        K = np.flatnonzero(Y < -1e-15)
        KK = np.flatnonzero(np.diff(K) > 1)
        result = K[KK]
        if len(K) and K[-1] < len(Y)-1:
            result = np.append(result, K[-1])
        return result

    def zero_crossingerator(self, Y):
        """
        Yields 2-tuples, each with (1) an index of the supplied vector
        I{Y} at a zero crossing and (2) a bool that is C{True} if the
        zero crossing was negative-going.
        """
        K_np = self.find_zero_crossings_NP(Y)
        K_pn = self.find_zero_crossings_NP(-Y)
        K = np.unique(np.concatenate([K_np, K_pn]))
        for k in K:
            yield k, k in K_pn
    
    def find_next_peak(self, Y, k, negative=False):
        """
        Returns a 2-tuple with (1) the sample distance to the right of
        index I{k} and (2) the height of the next peak after I{k}.
        """
        N = len(Y)
        if N <= k:
            return None, None
        if negative: Y = -Y
        Yd = np.diff(Y[k:])
        K = np.flatnonzero(Yd < 0)
        if not len(K):
            return N-k-1, Y[-1]
        kn = K[0]
        return kn, Y[k+kn]
        
    def find_prev_peak(self, Y, k, positive=False):
        """
        Returns a 2-tuple with (1) the sample distance to the left of
        index I{k} and (2) the height of the previous peak before I{k}.
        """
        Y = np.flip(Y[:k])
        if not positive: Y = -Y
        return self.find_next_peak(Y, 0)
    
    def slope(self, X, Y, k, invert=False):
        """
        Returns the slope of I{Y} vs I{X} for the zero crossing at index
        I{k}. Calculated from the difference between the adjacent
        negative and positive peaks divided by the distance between
        them.
        """
        k1, p1 = self.find_prev_peak(Y, k, positive=invert)
        k2, p2 = self.find_next_peak(Y, k, negative=invert)
        if k1 is None:
            num = p2
            denom = X[k+k2]
        elif k2 is None:
            num = p1
            denom = X[k-k1]
        else:
            num = p1 + p2
            denom = X[k+k2] - X[k-k1]
        m = num / denom if denom else num
        return 0 if m < 0 else m

    def clipping(self, ddY):
        """
        Given the second derivative of the values I{ddY}, returns the
        ratio, taken to exponent I{Nc}, of the absolute value of the
        negative peak minus the standard deviation, divided by the
        standard deviation. If the absolute value of the negative peak
        is less than or equal to the standard deviation, the result is
        zero.

        This is an indicator of an abrupt downward curvature, i.e.,
        clipping.
        """
        negPeakValue = np.abs(np.min(ddY))
        sd = np.std(ddY)
        if sd < 1e-10 or negPeakValue <= sd:
            # There is no penalty for small negative curvature or,
            # implausibly, nearly uniform curvature.
            return 0
        return ((negPeakValue - sd) / sd)**self.Nc
    
    @staticmethod
    def dydx(X, Y):
        k1 = len(X) - len(Y)
        dX = np.diff(X[k1:])
        K = np.flatnonzero(dX)
        return np.diff(Y)[K] / dX[K]

    def __call__(self, X, Y):
        """
        Call my instance with an I{X} vector and a corresponding vector
        I{Y} of ascending values.

        Returns a 2-tuple with (1) the lumpiness metric and (2) a 2-D
        Numpy array of X, Y coordinates where the second derivative of
        I{Y} had a zero crossing.
        """
        XY = []
        if len(Y) < 3:
            metric = 0
        else:
            sumOfSlopes = 0
            # Normalize X vector into the rough equivalent of an
            # arange(0, len(X)) to account for differing spacings
            # (e.g., Ngspice's simulation step sizes when I{X} is the
            # time vector) but avoid blowing up the slopes.
            Xn = X - X[0]
            Xn *= len(X) / Xn[-1]
            dY = self.dydx(Xn, Y)
            ddY = self.dydx(Xn, dY)
            for k, posToNeg in self.zero_crossingerator(ddY):
                sumOfSlopes += self.slope(Xn, ddY, k, posToNeg)
                XY.append([X[k], Y[k]])
            Yrange = Y[-1]-Y[0]
            if sumOfSlopes and Yrange > 0:
                metric = self.weight*np.power(
                    self.a*sumOfSlopes / Yrange, self.b)
            else: metric = 0
            if self.check_clipping:
                metric += self.c * self.clipping(ddY)
        N = len(XY)
        if N: metric /= 1 + 0.001*(N**2)
        return metric, np.array(XY)
