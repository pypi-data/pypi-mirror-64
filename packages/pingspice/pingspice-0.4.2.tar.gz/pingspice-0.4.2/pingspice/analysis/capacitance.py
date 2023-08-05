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
Stuff supporting special capacitors that can charge faster and get
forced rapidly but in a simulation-friendly manner to an initial
voltage.

Using the XSPICE capacitance having an initial voltage results in
convergence problems, unfortunately.
"""

import re

import numpy as np

from pingspice.util import *
from pingspice.circuit.av import AV
from pingspice.circuit.netlist import Include, Subcircuit
from pingspice.analysis.expressions import Expressionist


class FastChargeCap(Include):
    """
    A special capacitor that initially has its capacitance effectively
    cut into a fraction 1/I{faster} so it can be fast-charged for an
    initial interval of I{tSwitch} seconds:

                 +--------+
        n1 --+---| C_fast |-----+--------------+------------+--------------- n2
             |   +--------+     |              |            |
             |                  |              |            |
          ...|..................|..............|............|...............
             |                  |              |            |  
             |               +--------+        |            |   
             |               | C_norm |        |            |   Lower part
             |               +--------+        |   +----+   |   only included   
             |                  |              +-->|   -|x--+   if faster > 1
             |  +----+          |   +----+         | E  |
             +--| S0 |--- n3 ---+---| S1 |-- n4 --<|   +|x--+
             |  +----+              +----+         +----+   |
             |    x                   x                     |
             |    |                   |                     |
             +----|-------------------|---------------------+
                  |                   |
                  n5 (1-0-1)          n6 (0-1-0)
    
    Construct with two nodes, which are assigned local variables I{n1}
    and I{n2}. in my L{setup}.

    Switch S0 momentarily opens up, for I{tSwitch} seconds, to keep
    I{C_norm} from bogging down the charging of I{C_fast}. During this
    initial interval, C_norm is supplied with as much current as
    needed (through switch S1, which momentarily closes during the
    interval) for its voltage to keep up with that across
    I{C_fast}. There is an Ngspice limitation to how fast I{C_norm}
    can be forced to tag along with I{C_fast}, though: The minimum
    resistance of S1.
        
    @ivar C: The capacitance value. Can be an AV object.

    @ivar faster: The ratio of how much faster the voltage increases
        if I{fivi} is set. There is no default; if you don't need
        faster initial charging, you don't want to use me. If
        I{faster} is equal to 1, only a capacitor (perhaps with V0)
        will be used.

    @ivar tSwitch: The number of seconds in fast-charge mode before
        switching to regular mode.

    @ivar t0: The number of seconds to delay before beginning
        fast-charge mode (default is zero).
    
    @ivar V0: Set to an initial voltage to use the XSPICE capacitance
        model with an initial voltage. Fast-charging will start from
        there.
    """
    t0 = 0
    V0 = None
    
    def setup(self, f, n1, n2):
        # AV compatible
        f.C(n1, n2, self.C/self.faster, V0=self.V0) # C0, fast
        if self.faster == 1:
            # No point in anything else if not actually faster
            return
        # NOTE: Never fix the reference designator for stuff inside an
        # Include, because you might include it more than once
        ts = f.get(self, 'ts', 1E-9)
        n3, n4, n5, n6 = self.iNode(N=4)
        switch = f.MODEL('sw', VT=0.5, RON=1E-6, ROFF=1E6)
        f.S(n1, n3, n5, 0, switch) # S0
        f.S(n3, n4, n6, 0, switch) # S1
        f.V(n5, 0, DC=1, PULSE=[1, 0, self.t0, ts, ts, self.tSwitch])
        f.V(n6, 0, DC=0, PULSE=[0, 1, self.t0, ts, ts, self.tSwitch])
        # AV compatible
        f.C(n3, n2, self.C*(1-1.0/self.faster), V0=self.V0) # C1, norm
        f.E(n4, n2, n1, n2, 1.0)


class Initializer(Include):
    """
    I charge a capacitance in parallel with two nodes very quickly,
    but in a simulation-friendly manner, to an initial voltage.

    Construct with three nodes, which are assigned local variables
    I{n1}, I{n2}, and I{nv0} in my L{setup}. The last one is an input
    voltage that tells my circuitry what the initial voltage is.::

              +----------------------------------------------------------+
              | +------------------------------------------------------+ |
              | |                                                      | |
              | |   +------+                                 +-----+   | |
        n1 ---|-+--x|-     |         +----+                  |     |>--+ |
              |     |  B:V |-- n3 ---| R1 |-------+--- n4 --x|  G  |     |
        n2 ---+----x|+     |         +----+       |          |     |<----+
                    |      |                    +----+       +-----+
        nv0 -------x|+     |                    | C1 |
                    +------+                    +----+
                                                  |
                                               n5 |  +----+   
                                                  +--| R2 |--0
                                                     +----+   

    The LPF of R1+C1 keeps the error voltage at the input n4 to G from
    transitioning too fast. The minimum transition time is 1/5 Nts*ts
    or 2*ts, whichever is larger. This imparts a bit of "I" into the
    PID loop, along with the "P". (There never will be any
    implementation of a "D" term.)
    
    @ivar C: The capacitance value. Can be an AV object, but only one
        with a known value.

    @ivar ti: The time alloted for initial charging at the beginning
        of the TRAN simulation for the capacitor to approach
        completion of its transition to the initial
        value. (Read-only.)

    @cvar Nts: Minimum number of simulation timesteps for initial
        charging interval.
    
    @cvar I_max: Maximum initial charging current. (Going very far
        beyond this risks numerical problems, non-convergence.)

    @cvar P: Proportional (and only) term of PID driving the charging
        current.
    """
    Nts = 50
    I_max = 1e6
    P = 1000
    I = 1500

    def _calc_C1R2(self, tt):
        """
        Calculates values of R1, C1, and R2 in the RC LPF that implements
        the "P" and "I" terms of the PID loop with transition time I{tt}.
        (No "D" term is implemented.)::

            The P term is G*R2/(R1+R2).
            The I term is G.
            
            Thus, I*R2/(R1+R2) = P
            So R1+R2 = I*R2/P
            and thus R1 = R2*(I/P - 1).
            
            R1 is set to 1.0. So, finally, R2 = 1.0 / (I/P - 1).

        Note that I > P. You can't implement a PI loop with P > I
        using this simple RC circuit.
        """
        if self.I <= self.P:
            raise CapacitanceConfigError(
                "Can't make an initializer PI loop with P={:g} and I={:g}",
                self.P, self.I)
        R2 = 1.0 / (float(self.I)/self.P - 1.0)
        C1 = tt / (1.0+R2)
        return C1, R2
    
    def setup(self, f, n1, n2, nv0):
        ts = f.get(self, 'ts')
        # AV compatible for C, only with known value.
        C = float(self.C)
        # Initialization time
        I_max = self.I_max
        self.ti = 5*C / I_max
        if self.ti < self.Nts*ts:
            self.ti = self.Nts*ts
            I_max = 5*C / self.ti
        f.raw("* Initial charging interval {:g} seconds", self.ti)
        ex = Expressionist()
        ex.ap("{:g}", I_max*self.I)
        ex.ap("tanh(TIME*{:g}*(V({})+V({})-V({})))", 10.0/self.ti, nv0, n2, n1)
        expr = ex.ep("*")
        expr = ex.ifelse("0", expr, "TIME > {:g}", self.ti)
        n3, n4, n5 = f.iNode(N=3)
        f.B(n3, 0, V=expr)
        f.R(n3, n4, 1.0)
        tt = max([0.2*self.Nts*ts, 2*ts])
        C1, R2 = self._calc_C1R2(tt)
        f.C(n4, n5, C1); f.R(n5, 0, R2)
        f.G(n2, n1, n4, 0, 1.0)
        return {'ti': self.ti}


class Capacitance(Include):
    """
    I provide circuitry for a capacitance that can get charged to a
    steady-state or desired voltage quickly.

    I overcome some huge Ngpsice limitations with initial capacitor
    voltages, including convergence problems while using the 'v0'
    option for the 'capacitance' model provided by XSPICE. (I can
    still use that option if you wish, however. Sometimes it works.)

    Instead, to have me fast-charge myself to an initial capacitor
    voltage, supply a third node to my constructor, referred to
    locally as I{nv0}, with the desired voltage. My capacitor will
    then get fast-charged within a few multiples of the simulation
    timestep specified in pingspice-only simulation variable
    I{ts}. Happily, due to the way Ngspice computes a DC solution
    prior to a TRAN analysis, just having the L{Initializer} circuitry
    present will bring the initial voltage to what you desire at the
    very first simulation step.

    You should keep the pingspice-only simulation option I{timeWarp}
    consistent for all thermal subcircuits in a given
    simulation. Define it as a constructor keyword for your
    L{Netlist}.

    You can use either inital-voltage setting technique with or
    without a fast initialing voltage interval set by I{fivi}.
    
    @ivar C: The capacitance value. Can be an AV object.
    
    @ivar tcon: Set to an RC time constant that this capacitance is
        part of to avoid having it scaled down so far that the time
        constant is less than the I{ts} pingspice-only simulation
        option value. Can be an AV object, though with some
        substantial limitiations.

    @ivar timeWarp: Set this to a time speed-up factor to make things
        charge up (and down) x times faster. The speed-up will be
        limited to I{tcon} if it is set. Default is 1.0, for no time
        warp.
    
    @ivar fivi: Set to the initial time allocated for B{f}ast
        B{i}nitialing B{v}oltage B{i}nterval, for irregular but
        simulation-friendly initial charge-up. Set to C{None} for no
        such irregular warm-up (the default). If set C{True} or to a
        value less than 10x the pingspice-only simulation variable
        I{ts}, will be forced to 10x I{ts}. NOTE: I{timeWarp}, if any,
        still applies.

    @ivar faster: The ratio of how much faster the voltage increases
        if I{fivi} is set. Default is 100.
    
    @ivar V0s: Set C{True} to cause the capacitance to be subject to
        an initial voltage-zeroing short circuit. Not compatible with
        using I{fivi} or supplying a third node with a fast-charge
        initial voltage.

    @ivar V0: Set to an initial voltage to use the XSPICE capacitance
        model with an initial voltage. Not compatible with supplying a
        third node with a fast-charge initial voltage.

    @ivar ti: The time you should set aside for my initial and/or fast
        charging at the beginning of your TRAN simulation for the
        capacitor. (Read-only.) Also appears as the 'ti' entry of my
        I{setupResults}.
    """
    tcon = None
    timeWarp = 1.0
    fivi = None
    faster = 100
    V0s = False
    V0 = None
    ti = 0
    reDivision = re.compile(r'/([0-9]\.?[0-9]*)')
    
    def tryMakeFaster(self, ts, ratio, prevRatio=1):
        """
        Tries to return a ratio that makes my time constant I{tcon}
        faster.

        If the pingspice simulation option I{ts} is specified and you
        set I{tcon} to an RC time constant that my capacitance forms
        in conjunction with some resistance, I will ensure that the
        I{timeWarp} version of C is not scaled down so far that
        I{tcon} is less than I{ts}.

        This is done by keeping the returned ratio as big as possible
        to reduce I{tcon} to just over I{ts}. The value of I{tcon}
        divided by I{ratio} (further divided by I{prevRatio} if
        specified) will be kept at least as large as I{ts}.

        If I{tcon} is an C{AV} object, I use its known float value
        (after doing mods). If it doesn't have a known value, it is
        disregarded; there's no lower capacitance limit during
        parameter finding. (You shouldn't be using I{timeWarp} for
        that.)
        """
        if ts is None or self.tcon is None: return ratio
        tcon = float(self.tcon)
        effectiveRatio = ratio*prevRatio
        if tcon/effectiveRatio < ts:
            effectiveRatio = max([1, int(tcon/ts)])
            ratio = max([1, effectiveRatio/prevRatio])
        return ratio
    
    def setup(self, f, *nodes):
        """
        Using the circuit generation tool I{f}, implements a thermal
        capacitance element between nodes referred to locally as I{n1}
        and I{n2}.

        If I was constructed with a third node, that is referred to
        locally as I{nv0} and causes me to fast-charge my capacitance
        to the voltage at that node.
        """
        ti = 0
        n1, n2 = nodes[:2]
        ts = f.get(self, 'ts')
        # Obtaining a printable value of 'C' is only for the netlist comment
        C = str(self.C) if isinstance(self.C, AV) else float(self.C)
        f.raw("* Special Capacitor, {} F", C)
        timeWarp = 1.0 if self.timeWarp is None else self.timeWarp
        if timeWarp > 1:
            timeWarp = self.tryMakeFaster(ts, self.timeWarp)
            if timeWarp > 1:
                f.raw("* Time warped {:d}x", int(timeWarp))
        capacitance = self.C/timeWarp
        # With or without fivi, we will have a capacitance across n1, n2
        if len(nodes) > 2:
            nv0 = nodes[2]
            proto = "Third node '{}' supplied, incompatible with "
            if self.V0 is not None:
                raise CapacitanceConfigError(
                    proto+"XSPICE-based voltage initialization to V0={}",
                    nv0, self.V0)
            if self.V0s:
                raise CapacitanceConfigError(
                    proto+"initial capacitance shorting", nv0)
            f.raw("* Initialized to voltage at node '{}'", nv0)
            ti = Initializer(f, n1, n2, nv0, C=self.C).ti
        elif self.V0s:
            f.raw("* Shorted at startup")
            f.R(n1, n2, R="{TIME > 0 ? 1E12 : 1E-6}")
        # Implement capacitance, with FastChargeCap or f.C
        if self.fivi:
            if self.V0s:
                raise CapacitanceConfigError(
                    "No doing an initial short when using fivi option")
            fivi = self.fivi
            if ts and (fivi is True or fivi < 10*ts):
                fivi = 10*ts
            faster = self.tryMakeFaster(ts, self.faster, timeWarp)
            f.raw("* {:d}x faster for {:.5g} sec", faster, fivi)
            FastChargeCap(
                f, n1, n2,
                C=capacitance,
                t0=ti, V0=self.V0, faster=faster, tSwitch=fivi)
            ti += fivi
        else:
            if self.V0 is not None:
                f.raw("* Using XSPICE to initialize voltage to {}", self.V0)
            f.C(n1, n2, capacitance, V0=self.V0)
        self.ti = ti
        return {'ti': self.ti}
