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
Evaluators for time-based semiconductor device behavior.
"""

import numpy as np

from pingspice.analysis.fixture import LumpinessCalculator
from pingspice.util import *


def Q(t, I):
    """
    Transforms time I{t} and current I{I} into charge using
    trapezoidal integration.
    """
    tPrev, Iprev = t[0], 0
    charge = np.empty_like(t)
    charge[0] = 0
    for k, tNow in enumerate(t[1:]):
        Qk = 0.5 * (tNow - tPrev) * (Iprev + I[k])
        charge[k+1] = charge[k] + Qk
        tPrev, Iprev = tNow, I[k]
    return charge


class GenericEvaluator(object):
    """
    Subclasses of me evaluate timing-based behavior of semiconductor
    devices. See L{TimingEvaluator} and L{ReverseRecoveryEvaluator}.

    @keyword weight: A value for my I{weight} coefficient other than
    the subclass default.

    @keyword us_dt: A value for my I{us_dt} coefficient other than my
        subclass's default.
    """
    Ndiff_LR = 2
    debug = False

    def __init__(self, weight=None, us_dt=None):
        if weight is not None:
            self.weight = weight
        if us_dt is not None:
            self.us_dt = us_dt

    @property
    def worst_SSE(self):
        return self.weight * 1E5

    def setup(self, time):
        self.time = time
        self.k0 = 0
        self.SSE = 0
        self.points = []
    
    def V(self, *args):
        name = "V" + "_".join(args)
        Vf = getattr(self, name)
        return Vf * getattr(self, sub("V{}_max", args[0]))

    def findFirstReally(self, X, op, Xk, noneLater=False):
        Z = list(op(X[self.k0:], Xk))
        if True not in Z:
            return
        N = len(Z)
        for k in range(Z.index(True), N):
            if Z[k]:
                kLeft = max([k-self.Ndiff_LR, 0]) + self.k0
                kRight = min([k+self.Ndiff_LR, N-1]) + self.k0
                if np.all(op(np.diff(X[kLeft:kRight]), 0)):
                    if noneLater:
                        if np.all(op(X[self.k0+k+1:], Xk)):
                            return k
                    else:
                        return k

    def _resultFrom(self, k):
        """
        Adds I{k} to my index I{k0} and, if the updated value is still a
        valid index for my I{time} vector, returns it along with the
        time value at that index.

        Otherwise, returns a 2-tuple with two C{None} values.

        Called by L{timeWhenGreater} and L{timeWhenLess}.
        """
        if k:
            self.k0 += k
            if self.k0 < len(self.time):
                return self.k0, self.time[self.k0]
        return None, None
    
    def timeWhenGreater(self, X, Xk):
        """
        Returns a 2-tuple with (1) the index of the first element of
        supplied 1-D array I{X} that is greater than scalar value
        I{Xk} and (2) the time value at that index.

        If no such index is found, returns a 2-tuple with C{None}
        values.
        """
        # Find first element that is greater and isn't just a local
        # maximum
        k = self.findFirstReally(X, np.greater, Xk)
        return self._resultFrom(k)

    def timeWhenLess(self, X, Xk, noneLater=False):
        """
        Returns a 2-tuple with (1) the index of the first element of
        supplied 1-D array I{X} that is less than scalar value I{Xk}
        and (2) the time value at that index.

        If no such index is found, returns a 2-tuple with C{None}
        values.
        """
        k = self.findFirstReally(X, np.less, Xk, noneLater)
        return self._resultFrom(k)
    
    def add_SSE(self, value, expected, unityError, notSquared=False):
        """
        Adds to my running SSE total the scaled square (unless
        I{notSquared} set) of the difference between the two supplied
        scalars I{value} and I{expected}, multiplied by my I{weight}.

        The scaling is done by dividing the difference by
        I{unityError} before squaring.

        @keyword notSquared: Set C{True} to use the absolute linear
            difference rathern than the squared difference.
        """
        op = np.abs if notSquared else np.square
        SSE = self.weight * op((value-expected)/unityError)
        if self.debug:
            if not self.SSE:
                print("")
            print(sub("SSE {:.1f} -> {:.1f}", self.SSE, self.SSE+SSE))
        self.SSE += SSE

    def evalTimeDiff(self, t1, t2, dtExpected, us_dt=None):
        """
        Adds to my running SSE total the squared difference between (1)
        the interval I{t2}-I{t1} and (2) the expected interval
        I{dtExpected}.

        @keyword us_dt: The difference between an observed and
            expected interval that results in an SSE contribution of
            one. Defaults to my I{us_dt} attribute value.
        """
        if us_dt is None: us_dt = self.us_dt
        self.add_SSE(t2-t1, dtExpected, us_dt)

    def result(self):
        """
        Returns my running SSE total and a 2-D Numpy array of goal points
        that will be plotted with the "x" symbol.
        """
        return self.SSE, np.array(self.points)


class TimingEvaluator(GenericEvaluator):
    """
    I evaluate rise and fall times.
    
    Construct me with your device's specified turn-on delay time
    I{tdOn}, rise time I{tR}, turn-off delay time I{tdOff}, and fall
    time I{tF}, and then call the instance with three vectors (time,
    trigger (gate) voltages, and result (drain) voltages) from your
    simulated test circuit to get an SSE-equivalent fitness metric.

    @cvar us_dt: The difference between an observed and expected time
        that results in an SSE contribution of one. (Because the SSE
        contribution is the square of the time error, 10x this time
        error will result in an SSE contribution of 100.) My default
        is 1E-9, which works out to an SSE delta of one per
        nanosecond.

    @cvar us_lumpiness: The lumpiness metric for the result (drain)
        voltage's negative-going transition that results in an an SSE
        contribution of one. (Not squared in this case; twice this
        metric will result in an SSE contribution of two.) A really
        lumpy transition will have a metric around of around one, so
        I{us_lumpiness} should be set to a small fraction of 1.0 if a
        lumpy transition bothers you.
    
    @ivar tSpecs: (on, rise, off, fall)
    """
    Vt_start_up = 0.1
    Vt_start_down = 0.9
    Vr_start_down = 0.9
    Vr_full_down = 0.1
    Vr_start_up = 0.1
    Vr_full_up = 0.9

    weight = 1.0
    us_dt = 3E-9
    us_lumpiness = 0.03
    
    def __init__(self, Vt_max, Vr_max, *tSpecs, **kw):
        """
        TimingEvaluator(Vt_max, Vr_max, *tSpecs, **kw)
        """
        self.Vt_max = Vt_max
        self.Vr_max = Vr_max
        self.tSpecs = tSpecs
        self.lc = LumpinessCalculator()
        GenericEvaluator.__init__(self, **kw)

    def interval(self, time, t0, t1):
        return np.flatnonzero(np.logical_and(time >= t0, time < t1))
        
    def eval_lumpiness(self, time, Z, t0, t1):
        """
        Adds an SSE penalty for the slope of the supplied vector I{Z}
        being lumpy between times I{t0} and I{t1} of the supplied
        I{time} vector.
        """
        K = self.interval(time, t0, t1)
        metric = self.lc(time[K], -Z[K])[0]
        self.add_SSE(metric, 0, self.us_lumpiness, notSquared=True)
        
    def __call__(self, time, Vtrigger, Vresult):
        def Vt(t, V=None):
            if V is None:
                V = Vtrigger[k]
            self.points.append([t, V, np.nan])

        def Vr(t, V=None):
            if V is None:
                V = Vresult[k]
            self.points.append([t, np.nan, V])

        self.setup(time)
        #--- Start of Vtrigger rise -------------------------------------------
        Vk = self.V('t', 'start', 'up')
        k, t0 = self.timeWhenGreater(Vtrigger, Vk)
        if not t0:
            self.SSE = self.worst_SSE
            return self.result()
        Vt(t0)
        #--- Start of Vresult fall --------------------------------------------
        Vk = self.V('r', 'start', 'down')
        k, t1 = self.timeWhenLess(Vresult, Vk)
        if not t1:
            self.SSE = self.worst_SSE
            return self.result()
        Vr(t0+self.tSpecs[0], Vk)
        self.evalTimeDiff(t0, t1, self.tSpecs[0])
        #--- End of Vresult fall ----------------------------------------------
        Vk = self.V('r', 'full', 'down')
        k, t2 = self.timeWhenLess(Vresult, Vk)
        if not t2:
            self.SSE = self.worst_SSE
            return self.result()
        Vr(t0+self.tSpecs[0]+self.tSpecs[1], Vk)
        self.evalTimeDiff(t1, t2, self.tSpecs[1])
        #--- Start of Vtrigger fall -------------------------------------------
        self.k0 = np.argmax(Vtrigger)
        Vk = self.V('t', 'start', 'down')
        k, t3 = self.timeWhenLess(Vtrigger, Vk, True)
        if not t3:
            self.SSE = self.worst_SSE
            return self.result()
        Vt(t3)
        #--- Start of Vresult rise --------------------------------------------
        Vk = self.V('r', 'start', 'up')
        k, t4 = self.timeWhenGreater(Vresult, Vk)
        if not t4:
            self.SSE = self.worst_SSE
            return self.result()
        Vr(t3+self.tSpecs[2], Vk)
        self.evalTimeDiff(t3, t4, self.tSpecs[2])
        #--- Vresult rise time ------------------------------------------------
        Vk = self.V('r', 'full', 'up')
        k, t5 = self.timeWhenGreater(Vresult, Vk)
        if not t5:
            self.SSE = self.worst_SSE
            return self.result()
        Vr(t3+self.tSpecs[2]+self.tSpecs[3], Vk)
        self.evalTimeDiff(t4, t5, self.tSpecs[3])
        # Include the lumpiness penalty, for the result (drain)
        # voltage transition from t1 to t2
        self.eval_lumpiness(time, Vresult, t1, t2)
        #--- Done with all four transition times ------------------------------
        return self.result()


class ReverseRecoveryEvaluator(GenericEvaluator):
    """
    I evaluate a diode's reverse recovery behavior.
    
    Construct me with your device's specified reverse recovery time
    I{trr}, reverse recovery charge I{Qrr}, and maximum reverse
    current I{Irr_max}, and then call the instance with two vectors
    (time, and drain-source current) from your simulated test circuit
    to get an SSE-equivalent fitness metric.

    Not all datasheets specify total reverse recovery charge. If it's
    not known for your part, set I{Qrr} to C{None}.

    @cvar us_dt: The difference (seconds) between actual and expected
        reverse recovery time that results in an SSE contribution of
        one. (Squared, so twice this time deviation will result in an
        SSE contribution of four.)
    
    @cvar us_Imax: The % error deviation between peak reverse current
        and expected I{Irr_max} that results in an SSE contribution of
        one. (Squared, so twice this % deviation will result in an SSE
        contribution of four.)

    @cvar us_lumpiness: The lumpiness metric for the transition from
        max Ids to reverse recovery that results in an an SSE
        contribution of one. (Not squared in this case; twice this
        metric will result in an SSE contribution of two.) A really
        lumpy transition will have a metric around of around one, so
        I{us_lumpiness} should be set to a small fraction of 1.0 if a
        lumpy transition bothers you.
    
    @cvar us_undershoot: The fraction of negative spike current vs
        expected I{Irr_max} that results in an SSE contribution of
        one. This addition to SSE is to strongly penalize for
        undershoot after reverse recovery. With the default setting
        and weight, a mere 10% undershoot adds 25 to the
        SSE. (Squared, so 20% of undershoot would then add 100 to the
        SSE.)
    
    @cvar us_charge: The Coloumbs of error between total reverse
        charge deviating and expected I{Qrr} that results in an SSE
        contribution of one.

    @cvar us_skew: The difference (seconds) between the time of peak
        reverse current and half the expected reverse recovery time
        that results in an SSE contribution of one. This was intended
        to add a penalty as the reverse recovery curve starts to look
        increasingly unrealistic. But in many case you don't actually
        know what "realistic" looks like, so this is set to have very
        low impact.
    """
    Ids_full_down = 0.1

    weight = 1.0

    us_dt = 3E-9
    us_Imax = 2.0
    us_undershoot = 0.02
    us_lumpiness = 0.02
    us_charge = 3E-7
    us_skew = 1E-6
    
    def __init__(self, trr, Qrr, Irr_max, N_channel, **kw):
        self.trr = trr
        self.Qrr = Qrr
        self.Irr_max = Irr_max
        self.N_channel = N_channel
        self.lc = LumpinessCalculator()
        GenericEvaluator.__init__(self, **kw)

    def find_zero_crossing(self, X):
        """
        If there is a point in the supplied vector I{X} where one value is
        positive and the next value is zero or negative, returns the
        index for that point.

        If not, adds 3x my I{worst_SSE} to my running I{SSE} total.
        """
        for k in range(1, len(X)):
            if X[k] > 0 and X[k-1] <= 0:
                return k
        self.SSE = 3*self.worst_SSE

    def eval_Imax(self, I, k0=0):
        """
        Locates the maximum current, returning the index where it occurs
        and the amperage.
        
        If I{Irr_max} is defined (not zero or C{None}), adds SSE for
        the maximum value in the supplied vector I{I} deviating from
        my I{Irr_max} expectation. The error is relative, not
        absolute. Adds a plot point with an x-value of time when the
        maximum value occurred and a y-value of I{Irr_max}.
        """
        k = np.argmax(I[k0:]) + k0
        if k == 0 or k == len(I)-1:
            self.SSE = 2*self.worst_SSE
            return None, None
        Imax = I[k]
        if self.Irr_max:
            self.add_SSE(Imax/self.Irr_max, 1.0, 0.01*self.us_Imax)
            self.points.append([self.time[k], self.Irr_max])
        return k, Imax

    def eval_Q(self, I, k0, k1):
        """
        Adds SSE for the total reverse charge (computed from current
        values from index I{k0} to I{k1} in the supplied vector I{I})
        deviating from my I{Qrr} expectation.

        The total reverse charge is computed by calling L{timing.Q}
        with a slice C{k0:k1} from my I{time} vector and from I{I}. My
        L{__call__} method finds the current's zero crossing (via a
        call to L{find_zero_crossing} and sets the first index I{k0}
        to the sample that occurs then. It sets the last index I{k1}
        to the first sample that decays to below my I{Ids_full_down}
        threshold after maximum I{I} is reached.

        Adds no plot points.
        """
        if self.Qrr is None:
            return
        charge = Q(self.time[k0:k1], I[k0:k1])
        self.add_SSE(charge[-1], self.Qrr, self.us_charge)

    def eval_lumpyTransition(self, time, I, k0, k1):
        """
        Adds SSE for lumpiness (due to excessive inductive ringing) in the
        transition from max current to reverse recovery.
        """
        lumpiness, points = self.lc(time[k0:k1], -I[k0:k1])
        self.add_SSE(lumpiness, 0, self.us_lumpiness, notSquared=True)
        
    def eval_undershoot(self, I):
        """
        Adds an SSE penalty for the current in the supplied vector I{I}
        going negative again after reverse recovery.
        """
        def localMin(k):
            K = np.flatnonzero(np.abs(dIdt[k:]))
            if len(K):
                X = dIdt[K]
                K2 = np.flatnonzero(np.sign(X[:-1]) != np.sign(X[1:]))
                if not len(K2): return
                return I[K[K2[0]]+1]

        dIdt = np.diff(I)
        # Find steepest downward slope following recovery
        k = np.argmin(dIdt)
        # Find point, if any, where post-recovery current reaches
        # negative spike
        I_spike = localMin(k)
        if I_spike is None: return
        if I_spike < 0 and self.Irr_max:
            SSE = self.SSE
            try:
                self.add_SSE(I_spike/self.Irr_max, 0, self.us_undershoot)
            except:
                # DEBUG
                print "\nUS\t", I_spike, self.SSE-SSE, "\n"
                import pdb; pdb.set_trace() 
    
    def __call__(self, time, Ids):
        """
        Call this with two Numpy vectors representing I{time} and
        drain-source current I{Ids}.

        Returns (1) an SSE reflecting how closely that conforms with
        expected reverse-recovery behavior, and (2) a 2-D Numpy array
        of points to put "x" symbols at.

        Timing calculations are referenced from a point t0 where Ids
        is no longer negative, i.e., when the body diode stops being
        forward biased. (That is the first plot point.)
        """
        # DEBUG
        #import pdb; pdb.set_trace() 
        self.setup(time)
        k0 = self.find_zero_crossing(Ids)
        if k0 is None:
            return self.result()
        t0 = self.time[k0]
        self.points.append([t0, 0.0])
        # Find and possibly evaluate max reverse-diode current
        k1, Imax = self.eval_Imax(Ids, k0)
        if k1 is None:
            return self.result()
        # Impose penalty for max deviating from half expected recovery
        # time
        if self.us_skew:
            self.evalTimeDiff(t0, self.time[k1], 0.5*self.trr, self.us_skew)
        # Impose significant penalty for any negative post-recovery spike
        self.eval_undershoot(Ids)
        # Find and evaluate time until reverse-diode current
        # sufficiently decays
        self.k0 = k1
        Ik = self.Ids_full_down * Imax
        k2, null = self.timeWhenLess(Ids, Ik)
        if k2 is None:
            self.SSE += self.worst_SSE
            return self.result()
        t2 = self.time[k2]
        self.evalTimeDiff(t0, t2, self.trr)
        self.points.append([t2, Ik])
        t3 = t0+self.trr
        self.points.append([t3, 0.0])
        self.eval_Q(Ids, k0, k2)
        # Impose penalty for lumpiness in recovery transition
        self.eval_lumpyTransition(time, Ids, k1, k2)
        # All done
        return self.result()
