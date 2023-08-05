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
Current flow regulating stuff.
"""

import numpy as np
from scipy.optimize import minimize

from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Subcircuit
from pingspice.analysis.capacitance import Capacitance
from pingspice.lib import thermal
from pingspice.util import *


# SCA = SPICE Convergence Aid


class SwitchMixin:
    """
    @ivar R_off: Resistance in OFF state. Typically very high.

    @ivar R_on: Resistance in ON state. Typically very low, but can't
        be any lower than 1 mOhm (1E-3 Ohms).
    
    @ivar log: Set C{True} to use log transition between resistance
        states instead of linear.
    
    @ivar initially_on: Set C{True} if the switch goes from I{R_off}
        resistance to I{R_on}. Otherwise, it starts out with I{R_on}
        resistance.
    """
    log = False
    initially_on = False
    
    @classmethod
    def _nodes(cls, N):
        if not hasattr(cls, '_count'):
            cls._count = -N
        cls._count += N
        return [sub("nsw_{:d}", cls._count+k) for k in range(N)]
    
    def asModel(self, f, prefix):
        """
        Returns an XSPICE B{a}nalog B{s}witch model with the supplied
        I{prefix}.

        If you try to set my I{R_on} on-resistance below 1 mOhm, an
        exception is raised because the XSPICE model quietly refuses
        to use anything lower than that.
        """
        if self.R_on < 1E-3:
            raise ValueError("Minimum aswitch ON resistance is 1 mOhm")
        return f.MODEL(
            prefix, 'aswitch',
            r_off=self.R_off, r_on=self.R_on, log=self.log)
    
    def st_vctl(self, f, tr, tstart=0, tw=None):
        tStart = max([0, tstart-tr/3])
        n1, n2 = self._nodes(2)
        args = [
            1.00 if self.initially_on else 0.0,
            0.0 if self.initially_on else 1.00,
            tstart, tr]
        if tw: args.extend([tr, tw-2*tr-tr/3])
        f.V(n1, 0, 'DC', 0, Paren('PULSE', *args))
        # SCA
        f.R(n1, n2, 1.0)
        f.C(n2, 0, 0.05*tr)
        return n2


class Switch(Subcircuit, SwitchMixin):
    """
    A switch using the XSPICE analog switch model.
    
    B{TODO}: Somehow model contact bounce.
    
    @ivar N: The number of ganged switches. There will be twice as
        many nodes as switches, with each successive node pair
        corresponding to one switch in the gang.

    @ivar t0: The time at which the switch transition is completed.

    @ivar t1: The time at which the switch reverts to its original state
        (C{None} if it never does)

    @ivar tr: The transition (control rise) time of the switch transition.

    @ivar td: Delay between transition of first switch and transitions
        of all others in the gang. (Obviously ignored if N=1.)

    """
    N = 1

    t0 = 0
    t1 = None
    tr = 1E-6
    td = 150E-6

    R_off = 1E6
    R_on = 1E-3 # WARNING: Analog switch will not go any lower than 1 mOhm!
    
    @property
    def nodes(self):
        """
        Property: a0, a1, b0, b1, ...
        """
        result = []
        for k in range(self.N):
            for kk in (0, 1):
                result.append(sub("{}{:d}", chr(97+k), kk))
        return result
    
    def setup(self, f):
        ncs = []
        nodes = self.nodes
        model = self.asModel(f, 'sw_s')
        for k in range(self.N):
            n1, n2 = nodes[2*k:2*k+2]
            if len(ncs) < 2:
                td = 0 if k==0 else self.td
                if not ncs or td:
                    tw = None if self.t1 is None else self.t1-self.t0
                    ncs.append(self.st_vctl(
                        f, self.tr, tstart=self.t0+td, tw=tw))
            f.A(ncs[-1], sub("%gd({} {})", n1, n2), model)


class TempShort(Subcircuit, SwitchMixin):
    """
    Logarithmic analog switch set to temporarily short out two nodes
    with a smooth transition between normal and shorted modes.
    """
    # Re difference between log=True and log=Flse, XSPICE Analog
    # switch source code:
    # -------------------------------------------------------------
    # log=True
    #   intermediate = log(r_off / r_on) / (cntl_on - cntl_off);
    #   r = r_on * exp(intermediate * (cntl_on - INPUT(cntl_in)));
    #   if(r<=1.0e-9) r=1.0e-9;/* minimum resistance limiter */
    #   pi_pvout = 1.0 / r;
    #   pi_pcntl = intermediate * INPUT(out) / r;
    #
    # log = False
    #   intermediate = (r_on - r_off) / (cntl_on - cntl_off);
    #   r = INPUT(cntl_in) * intermediate + ((r_off*cntl_on - 
    #           r_on*cntl_off) / (cntl_on - cntl_off));
    #   if(r<=1.0e-9) r=1.0e-9;/* minimum resistance limiter */
    #   pi_pvout = 1.0 / r;
    #   pi_pcntl = -intermediate * INPUT(out) / (r*r);
    
    t0 = 1E-6
    trf = 0.1
    
    R_off = 1E6
    R_on = 1E-3 # WARNING: Analog switch will not go any lower than 1 mOhm!

    nodes = ['a', 'b']

    def setup(self, f):
        tr = self.trf * self.t0
        nc = self.st_vctl(f, tr, tw=self.t0)
        model = self.asModel(f, 'sw_ts')
        f.A(nc, Paren(None, 'a', 'b'), model)


class GangedBreakers(Subcircuit):
    """
    Two 80A DC circuit breakers ganged together with each other and a
    0.5 A DC breaker, originally intended for PV ground-fault
    protection.

    If I{t0} is C{None}, the breakers never get set or trip. Rather,
    they are just modeled as the on or off resistance.

    B{TODO:} Model overcurrent protection, with both thermal
    (long-term, relatively low current) and magnetic (short-term, high
    current) tripping mechanisms.
    """
    # Estimated resistances of circuit breakers, Ohms
    R = [5.0, 2E-3]     # 0.5A, 80A

    t0 = None
    tr = 20E-6
    td = 150E-6
    initially_on = False

    nodes = ['a0', 'a1', 'b0', 'b1', 'c0', 'c1']

    def setup(self, f):
        if self.t0 is None:
            for a, b, k in (
                    ('a0', 'a1', 0), ('b0', 'b1', 1), ('c0', 'c1', 1)):
                resistance = self.R[k] if self.initially_on else 1E9
                f.R(a, b, resistance)
            return
        Switch(
            f, N=3, t0=self.t0, tr=self.tr, td=self.td,
            log=True, initially_on=self.initially_on, R_on=self.R[1])(
                11, 'a1', 'b0', 'b1', 'c0', 'c1')
        f.R(11, 'a0', self.R[0]-self.R[1])


class CurrentLimiter(Subcircuit):
    """
    Limits the absolute value of current flow between I{b} and I{b} to
    I{Imax} with a small series resistance and reverse current from a
    behavioral current source::

                       +-------+       
            a >---+--->| shunt |>----------- 1 -- Rs ---+--------> b
                  |    +-------+                        | 
                  |        |                            | 
                  |        x                            | 
                  |    +-------+                        | 
                  |    | H:Lpf |>-- 2 -- R --+-- C --+  | 
                  |    +-------+             |       |  | 
                  ^                          3       0  V
                  |                          |          |
                  |                          x          | 
                  |                      +--------+     | 
                  +---------------------<| B:Irev |<----+
                                         +--------+

    This is a bidirectional limiter; it develops voltage drop to
    counteract current flow approaching the limit regardless of what
    direction the current is flowing. Viewing the subcircuit from the
    outside, it appears that the series resistance I{Rs} increases
    drastically as the current approaches the limit.

    The series resistance I{Rs} is calculated based on I{Imax} and
    I{Vmin}. Lower values of I{Vmin} result in a lower I{Rs} and a
    sharper cutoff at the current limit. The "knee" voltage
    transitioning from linear to current-limited behavior is
    approximately equal to I{Vmin}.

    When I{ts} is set, the CCVS with RC LPF on its output is included
    for SCA. Without it (at least as observed in unidirectional mode),
    the behavioral source sometimes oscillates in an effort to limit
    current that is very close to zero.

    @ivar Imax: The current limit in Amperes.

    @ivar Vmin: The minimum voltage that the limiter is expected to
        drop at the current limit. Default: 0.5 V.
    
    @ivar n: The exponent used in the saturation equation. A higher
        exponent means sharper, more drastic limiting. Default: 2.0

    @ivar uni: Set C{True} to use a unidirectional current limiter,
        which is more reliable given Ngspice's habit of messing up
        operating point with B-sources. When set, current is only
        limited if it flows from 'a' to 'b'.
    @type uni: bool

    @ivar reverse: Set C{True} to use unidirectional current limiting
        with current flowing from 'b' to 'a'. Sets I{uni}.
    @type reverse: bool
    """
    n = 2.0
    Vmin = 0.5
    uni = False
    reverse = False
    nodes = ['a', 'b']
    
    def setup(self, f):
        if self.reverse:
            n_in, n_out = 'b', 'a'
            self.uni = True
        else: n_in, n_out = 'a', 'b'
        f.Vsh(n_in, 1, 0)
        Rs = self.Vmin / self.Imax
        f.R(1, n_out, Rs)
        ts = f.get(self, 'ts')
        if ts:
            expr_current = "v(3)"
            f.H(2, 0, 'vsh', 1)
            f.R(2, 3, 0.1)
            f.C(3, 0, ts)
        else: expr_current = "i(vsh)"
        if self.uni:
            proto = "{}*(1 - ((1 + ({}/{:g})^{:g})^{:g}))"
        else: proto = "{}*(1 - ((1 + (abs({})/{:g})^{:g})^{:g}))"
        expr = sub(
            proto, expr_current, expr_current, self.Imax, self.n, -1.0/self.n)
        if self.uni: expr = sub("i(vsh) < 0 ? 0 : {}", expr)
        f.B(n_out, n_in, I=expr)


class InrushLimiter(Subcircuit):
    """
    NTC thermistor inrush limiter.
        
    @ivar tc: Time constant (seconds). Use I{timeWarp} to speed up the
        thermal response for your fraction of a second of transient
        simulation. But watch out for artificial interaction with
        capacitors with a time warp of more than 1000x.

    @ivar df: Dissipation factor (also called dissipation constant),
        if known (mW/K). (The device's thermal resistance is
        1000/I{df}.)
    
    @ivar Iss: Maximum steady-state current (Amps).
    @ivar R0: Resistance with no current (full inrush limiting).
    @ivar R25: Resistance with 25% Iss.
    @ivar R50: Resistance with 50% Iss.
    @ivar R75: Resistance with 75% Iss.
    @ivar R100: Resistance with 100% Iss.
    """
    # Time constant (seconds). Set smaller for simulation purposes or
    # use timeWarp.
    tc = 100
    timeWarp = 1.0
    # Default is to solve for thermal resistance
    df = None
    # Ambient temperature (degrees C)
    Ta = 25.0

    nodes = ['a', 'b', 'pdiss', 'tj']

    @property
    def Rth(self):
        if self.df is None: return
        return 1000.0 / self.df
    
    def TvI(self, I, R, Rth):
        P = I**2 * R
        return 298.15 + Rth*P
    
    def RvI(self, I, beta, Rw, Rth=None):
        R0 = self.R0 - Rw
        R_prev = self.R50
        if Rth is None: Rth = self.Rth
        for k in range(20):
            T = self.TvI(I, R_prev, Rth)
            R = R0 * np.exp(beta*(1.0/T - 0.00335401643468)) + Rw
            if I == 0 or abs(R/R_prev - 1.0) < 0.001: break
            R_prev += 0.5*(R-R_prev)
        return R
    
    def findCoeffs(self):
        """
        Returns coefficients
        """
        def SSE_ratios(coeffs):
            SSE = 0
            beta, Rw = coeffs[:2]
            Rth = coeffs[2] if self.Rth is None else self.Rth
            for k, Ik in enumerate(I):
                R = self.RvI(Ik, beta, Rw, Rth)
                SSE += (R/R_expected[k] - 1.0)**2
            #print SSE
            return SSE

        I = np.linspace(0, self.Iss, 5)
        R_expected = [self.R0, self.R25, self.R50, self.R75, self.R100]
        X0 = [1500, 0.05]
        bounds = [(1000, 5000), (0, 1.0)]
        if self.Rth is None:
            X0.append(30)
            bounds.append((30, 250))
        result = minimize(SSE_ratios, X0, method='SLSQP', bounds=bounds)
        return result.x
    
    def setup(self, f):
        """
        Sets up my subcircuit::
        
                                                 +-------+
                               +----------------x| B:V   |--+-----> pdiss
                               |            +---x| pdiss |  |
                               |            |    +-------+  |
              +-------+        |   +-----+  |               |
        a --->|+ Vsh -|--- 10 -+-->| B:R |--+---------------|---------> b
              +-------+            +-----+                  |
                                     x                      |
                                     |     +----------------|--------> tj
                                     |     |                |
                                     |     |   +--------+   |
                                     +-----+--<| R_expr |x--+
                                               +--------+
        """
        stuff = self.findCoeffs()
        if len(stuff) > 2:
            beta, Rw, Rth = stuff
        else:
            beta, Rw = stuff
            Rth = self.Rth
        # Current measurement
        f.Vsh('a', 10, 0)
        f.H(100, 0, 'vsh', 1.0)
        # The resistance, starting at R0
        R_expr = sub(
            "{{TIME > 0 ? "+\
            "{{{:g}*exp({:g}*((1.0/(V(tj)+298.15))-0.00335401643468))+{:g}}}"+\
            " : {:g}}}", self.R0-Rw, beta, Rw, self.R0)
        f.R(10, 'b', R=R_expr)
        f.R(10, 'b', 1E3)
        # Power dissipation measurement, across the resistance, starting at 0 W
        f.B('pdiss', 0, V="{TIME > 0 ? {V(10,b)*V(100)} : 0}")
        # Averaged with time constant from thermistor mass
        f.R('pdiss', 220, 1.0)
        Capacitance(
            f, 220, 0, C=self.tc, tcon=self.tc, timeWarp=self.timeWarp)
        # Self-heating temperature (deg C), ambient if no power dissipation
        T_expr = sub(
            "{{TIME > 0 ? {{V(220)*{:g}+{:g}}} : {:g}}}", Rth, self.Ta, self.Ta)
        f.B('tj', 0, V=T_expr)

        
class Ammeter(Subcircuit):
    """
    Provides a voltage on output node 'amps' that equals the current
    flowing from 'inp' to 'out'.
    """
    invert = False
    nodes = ['inp', 'out', 'amps']
    
    def setup(self, f):
        f.Vsh('inp', 'out', 0)
        f.H('amps', 0, 'vsh', -1.0 if self.invert else 1.0)
