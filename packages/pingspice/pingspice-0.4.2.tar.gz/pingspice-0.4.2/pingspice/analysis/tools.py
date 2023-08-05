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
Tools for dealing with interesting simulation vectors.
"""

import numpy as np
from scipy import stats, signal, interpolate, optimize

from pingspice.util import *


class SwitchmodeTools(object):
    """
    Toolbox for simulation vectors from a switchmode power converter.
    """
    # Number of points in smoothed temperature boundary
    N_bound = 100
    # Interpolation and Decimation ratio for smoothing with
    # anti-aliasing filtering
    M_smoothing = 16
    
    def __init__(self, fs, **kw):
        self.fs = fs
        for name in kw:
            setattr(self, name, kw[name])

    def N(self, t, ts=None):
        """
        Given a simulation time vector I{t} and my switching frequency
        I{fs}, returns the number of switching periods in the
        simulation, including any partial ones at the ends.

        You can specify a sample interval I{ts} and then the returned
        number will be the number of samples required to represent the
        time vector at that equispaced sample interval.
        """
        scale = self.fs if ts is None else 1.0/ts
        return int(np.ceil((t[-1] - t[0]) * scale))

    def pick(self, t0, t, *args):
        """
        Returns a copy of I{t} where t >= t0, and copies of the args
        supplied after I{t} with matching elements.
        """
        K = np.flatnonzero(t >= t0)
        return [t[K]] + [arg[K] for arg in args]
    
    def linregress(self, t, X, t0=0):
        """
        Returns the slope and y-intercept of a line fitted to the supplied
        time and value vectors I{t} and I{X}. If you set I{t0} to a
        time in the range of I{t}, the linear regression will only
        operate on points after that time.
        """
        t, X = self.pick(t0, t, X)
        return stats.linregress(t, X)[:2]
    
    def extrapolatePdiss(self, t, P):
        """
        Returns copies of I{t} and I{P} with additional items
        appended to each with predicted power dissipation.

        The last predicted point has twice the absolute time as the
        last element of I{t} as supplied.
        """
        def func(x, a, b, c, d):
            return a*np.exp(-b*x) + c*x + d
        
        tMid = 0.5*(t[-1] + t[0])
        t2, P2 = self.pick(tMid, t, P)
        coeffs = optimize.curve_fit(func, t2, P2)[0]
        te = np.linspace(t[-1], 2*t[-1], len(t2))
        Pe = func(te, *coeffs)
        return np.append(t, te), np.append(P, Pe)
    
    def monotime(self, t, M=1, N=None):
        """
        Returns an equispaced monotonic time vector from minimum time to
        maximum with I{M} points per switching period.

        You may specify the number of points with I{N} instead of
        using a calculation based on switching frequency and I{M}.
        """
        if N is None: N = M*self.N(t)
        return np.linspace(t[0], t[-1], N)
            
    def interpolate(self, t, X, N, s=0.02, linear=False):
        """
        Returns equispaced monotonic time vector from minimum time to
        maximum, with I{N} points, and spline-interpolated values of
        I{X} at each of those points.

        For a faster fit, you can set I{linear} C{True} and then
        simple linear interpolation will be used.
        """
        try:
            if linear:
                func = interpolate.interp1d(t, X)
            else: func = interpolate.UnivariateSpline(t, X, s=s)
        except:
            import sys, traceback, pdb
            tb = sys.exc_info()[2]
            traceback.print_exc()
            pdb.post_mortem(tb)
        tm = self.monotime(t, N=N)
        return tm, func(tm)
    
    def smoothed(self, V):
        """
        Returns a version of the C{Vectors} object where the 'time' vector
        has exactly one sample per switching cycle and the others are
        smoothed and decimated to have the same reduced sample rate.
        """
        t = V.time
        M = self.M_smoothing
        tm = self.monotime(t, M)
        V2 = V.copy()
        V2['time'] = tm[::M]
        for name in V:
            func = interpolate.interp1d(t, V[name])
            V2[name] = signal.decimate(func(tm), M)
        return V2
    
    def periodAveraged(self, t, X):
        """
        Returns the average value of I{X} for each switching cycle.
        """
        # There will be one sample per switching interval, except we
        # will discard the one at either end
        N2 = self.N(t)
        # The mean sample interval
        ts = np.mean(np.diff(t))
        # The number of equispaced samples at that mean interval
        # (starting point for M calculation)
        N1 = self.N(t, ts)
        # The integer decimation ratio closest to satisfying N1/N2
        M = int(np.round(float(N1) / N2))
        # Revised N1 to make M work exactly
        N1 = N2*M
        # Monotonic versions of t and X
        tm, Xm = self.interpolate(t, X, N1, linear=True)
        # There will be one time sample per switching cycle
        t2 = self.monotime(t, N=N2)
        # Decimate monotonic X to one sample per switching cycle
        X2 = signal.decimate(Xm, M, ftype='fir')
        # Discard suspect values at either end
        return t2[1:-1], X2[1:-1]
    
    def lowerBound(self, t, X):
        """
        Returns a 2-tuple with equispaced time and value vectors from
        lower smoothed bound of I{X}.
        """
        N = self.N(t)
        K = signal.find_peaks(-X, distance=N)[0]
        if not len(K):
            K = np.arange(0, len(t), N)
        return self.interpolate(t[K], X[K], N)
