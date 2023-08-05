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
Possibly more realistic passive stuff.
"""

import math

from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Subcircuit, Include
from pingspice.analysis import expressions, capacitance
from pingspice.lib.current import TempShort
from pingspice.util import *


class Capacitor(Subcircuit):
    """
    I am a realistic capacitor that you can get rapidly charged up to
    an initial value in a couple of different ways.

    My I{V0} attribute sets an initial voltage of the capacitor
    rapidly but not instantly using a fast and simulation-friendly
    error-feedback approach. The value of I{V0} can be any of several
    different types that determine my behavior differently:

        - C{None}: No initial voltage (the default). This is mandatory
          if you set I{bypass}, because it makes no sense to have me
          quickly charge up to an unknown voltage when you have set
          what it actually is.

        - C{float} or C{int}: Set my initial voltage to this fixed
          value. If my I{V0x} attribute is set C{True}, Ngspice's
          XSPICE-based capacitor model will be used with its initial
          condition set to this value (voltage). That's simple, but
          can result in convergence problems. Otherwise (the default),
          pingspice's L{capacitance.Initializer} will be used. Not AV
          compatible, and typically will just be used to force a
          capacitor to start discharged with V0=0.

        - C{True}: This will make me expect a third node 'v0', an
          input that determines my initial voltage. This is the only
          way to initialize the capacitor voltage to an alterable
          value; define your C{f.vav} AV-controlled voltage source
          outside the subcircuit.

    I set the I{ti} entry of I{setupResults} to my initial charging
    time, when my I{V0} attribute is set C{True}. Otherwise, I set it
    to C{None}.

    FIVI
    ====
    
        If you set I{fivi} to a B{f}ast B{i}nitial B{v}oltage
        B{i}nterval (seconds, usually in the microsecond range), my
        underlying L{Capacitance} will do what it can to quickly
        charge up my voltage at the very beginning of your transient
        simulation. It uses a L{FastChargeCap} to do this.

        You can set I{fivi} to C{None} for no such irregular warm-up
        (that is the default). You can also set it to C{True} or to a
        value less than 10x the pingspice-only simulation variable
        I{ts}, in which case its value will be forced to 10x
        I{ts}. NOTE: I{timeWarp}, if any, still applies.
        
        If you set my L{bypass} constructor keyword (and thus instance
        attribute) C{True}, I will also bypass my ESR and ESL during
        that initial interval. B{Note}: Setting this with I{V0} also
        set C{True} will raise an exception, because there's no point
        setting an initial voltage and also doing an initial
        fast-charge to some unknown terminal voltage. The resistance
        of the bypass path will be made as low as needed for the
        capacitor voltage to reach 99.9% of the terminal voltage, but
        not lower than 1 mOhm.

    @ivar C: The capacitance value. This is technically AV compatible,
        but, as with all subcircuit attributes, its value can't
        actually altered at runtime.

    @ivar V0: The initial voltage that the capacitance is fast-charged
        to reach within I{Initializer.Nts} multiples of the simulation
        timestep specified in pingspice-only simulation variable
        I{ts}. See discussion above for the several different types
        that this value can be.
    
    @ivar tcon: Set to an RC time constant that this capacitance is
        part of to avoid having it scaled down so far that the time
        constant is less than the I{ts} pingspice-only simulation
        option value. Technically can be an AV object, though, again,
        subcircuit attributes can't be altered at runtime.
    
    @ivar timeWarp: Set this to a time speed-up factor to make things
        charge up (and down) x times faster. The speed-up will be
        limited to I{tcon} if it is set. Default is 1.0, for no time warp.
    
    @ivar fivi: Set to the initial time allocated for B{f}ast
        B{i}nitial B{v}oltage B{i}nterval, for an initially fast and
        still simulation-friendly initial charge-up.

    @ivar faster: The ratio of how much faster the voltage increases
        if I{fivi} is set. Default is 100.
    
    @ivar V0s: Set C{True} to cause the capacitance to be subject to
        an initial voltage-zeroing short circuit. Only applies if
        I{fivi} is not set and I{V0} is C{None}.

    @ivar V0x: Set C{True} to use the XSPICE version of voltage
        initialization. This can cause convergence problems, but is a
        bit simpler. If it works for your circuit, use it! Setting
        this with C{fivi} set raises an exception.
    
    @ivar ESR: Equivalent series resistance, Ohms. If you set this,
        you can set I{pdiss} C{True} to get an output node with my
        power dissipation.

    @ivar ESL: Equivalent series inductance, Henries. Seldom known,
        calculated from I{leadSpacing} if not and that is specified.

    @ivar leadSpacing: Radial lead or screw-terminal spacing (mm,
        provides an I{ESL} estimate)

    @ivar df: Dissipation factor (fraction) and frequency (Hz), as a
        2-tuple or 2-element list. (These may be specified instead of
        I{ESR}.)

    @ivar I_leakage: Leakage current (if specified).

    @ivar R_leakage: May be used with I{V_max} to compute I{I_leakage}.

    @ivar V_max: Rated voltage, presently only used for computing
        leakage current with UCC's formula.

    @ivar pdiss: Set C{True} if a 'pdiss' (power dissipation) node is
        desired. Setting this without I{ESR} defined raises an
        exception. The 'pdiss' node will come after the second
        capacitor node, or after the third one if I{V0} is set
        C{True}.

    @ivar bypass: Set C{True} to also bypass my ESR and ESL for my
        I{fivi} time in addition to reducing my capacitance during
        that interval. I{fivi} must be set, but I{V0} must not be.
    """
    V0 = None

    tcon = None
    timeWarp = 1.0
    fivi = None
    faster = 100
    V0s = False
    V0x = False
    bypass = False

    ESR = None
    ESL = None
    leadSpacing = None
    df = None
    I_leakage = None
    R_leakage = None
    V_max = None
    pdiss = False

    @property
    def nodes(self):
        """
        Property: There are two basic nodes 'a' and 'b' and two optional
        ones.

        If my I{V0} attribute is set C{True}, then those are followed
        by a third node 'v0', a high-impedance input that you can set
        to an initial capacitance voltage, fast-charged within a few
        simulation time steps by L{capacitance.Initializer}. If there
        is no input, 'v0' floats to zero, and then that is the initial
        capacitance voltage.
        
        If my I{pdiss} attribute is set C{True}, then 'a' and 'b' and
        possibly also 'v0' are followed by an output node 'pdiss'
        whose voltage equals the total power dissipation of the
        capacitor.
        """
        nList = ['a', 'b']
        if self.V0 is True:
            nList.append('v0')
        if self.pdiss:
            nList.append('pdiss')
        return nList
    
    @property
    def R(self):
        """
        Property: Effective series resistance.

        If my I{ESR} attribute is set, then that is the value of
        I{R}. Otherwise, if my I{df} (dissipation factor) is set to a
        2-element sequence (df, freq), then I{R} is set based on how
        much power dissipation there is at that frequency, given my
        capacitance value I{C}.
        """
        R = getattr(self, 'ESR', None)
        if R is None and self.df:
            if not hasattr(self.df, '__iter__') or len(self.df) != 2:
                raise ValueError(
                    "(Diss. factor, freq) df must be a 2-element sequence")
            df, freq = self.df
            R = df / (2*np.pi*freq*self.C)
        return R
    
    @property
    def L(self):
        """
        Property: Series inductance.

        If my I{ESL} attribute is set, then that is the value of
        I{L}. Otherwise, if my I{leadSpacing} is set (mm), the series
        inductance is calculated from that.

        The formula is simply 1.5 nH per mm of spacing between the
        leads. This is from Sam G. Parler, Jr., "Improved Spice Models
        of Aluminum Electrolytic Capacitors for Inverter
        Applications," p. 3: "Typical series inductance values of
        radial and screw-terminal capacitors are about 1-2 nH/mm
        terminal spacing. This value does not vary significantly with
        temperature or frequency..."
        """
        L = getattr(self, 'ESL', None)
        if L is None and self.leadSpacing:
            L = 1.5E-9 * self.leadSpacing
        return L

    def check_config(self):
        """
        Checks my configuration with all its possible variations of
        attributes for incompatible combinations. Returns C{True} if
        my I{V0} attribute is a number, C{False} otherwise.
        """
        def error(*args):
            raise CapacitanceConfigError(*args)
        
        if self.pdiss and not self.R:
            error("There's no power dissipation with no ESR")
        if self.bypass and not self.fivi:
            error("You must define a fivi to use bypass")
        if self.fivi and self.V0x:
            error("You can't define a fivi when using XSPICE-base V0")
        V0_isnum = self.V0 is not True and isinstance(self.V0, (float, int))
        if self.V0x and not V0_isnum:
            # Using the XSPICE capacitor model, you can only set an
            # initial capacitance voltage to a numeric value
            error("Can't do XSPICE-based V0={}", self.V0)
        return V0_isnum
    
    def setup_leakage(self, f):
        """
        Adds a parallel resistance for rated or computed leakage current.

        If I{V_max} is specified but I{I_leakage} is not, uses UCC's
        formula for their big capacitors.
        """
        I = self.I_leakage
        if I is None:
            R = self.R_leakage
            if R is None and self.V_max:
                I = min([5E-3, 0.02*self.C*self.V_max])
        if I is None: return
        R = self.V_max / I
        n1, n2 = self.nodes[:2]
        f.R(n1, n2, R)

    def setup_seriesImpedance(self, f):
        """
        Inserts a series resistance and possibly also a series
        inductance.

        If there's a series resistance and I{pdiss} is set C{True},
        also inserts a power dissipation measuring device with output
        node 'pdiss'.

        Returns a reference to the node that will connect to the
        actual capacitor from the first subcircuit node.
        """
        n0 = self.nodes[0]
        R = self.R
        if R:
            n1 = self.iNode()
            f.R(n0, n1, R)
            if self.pdiss:
                f.B('pdiss', 0, V=sub("V({},{})^2/{:.5g}", n0, n1, R))
            n0 = n1
        L = self.L
        if L:
            n1 = self.iNode()
            f.L(n0, n1, L, ts=f.get(self, 'ts'))
            n0 = n1
        return n0

    def setup_bypass(self, f, n1, n2):
        """
        Adds a L{TempShort} that connects I{n1} to I{n2} via a very low
        resistance, bypasses my ESR and ESL for fast initial charging
        to some unknown terminal voltage.
        """
        if self.V0:
            raise CapacitanceConfigError(
                "You can't bypass ESR, ESL with an initial voltage!")
        if not self.fivi:
            raise CapacitanceConfigError(
                "You must specify fivi to (temporarily) bypass ESR, ESL!")
        R_bypass = -0.8*self.fivi/(self.C*np.log(0.001))
        if R_bypass < 1E-3:
            print "WARNING: R_bypass hit 1 mOhm minimum"
            R_bypass = 1E-3
        TempShort(f, t0=self.fivi, R_on=R_bypass)(n1, n2)
    
    def setup(self, f):
        # Check configuration
        V0_isnum = self.check_config()
        # Leakage current
        self.setup_leakage(f)
        # Series resistance and inductance, with optional power
        # dissipation measurement
        nodes = self.nodes
        nodes[0] = self.setup_seriesImpedance(f)
        # Fast-charging bypass
        if self.bypass:
            self.setup_bypass(f, self.nodes[0], nodes[0])
        # If power dissipation output node present, remove it
        if self.pdiss: nodes.pop(-1)
        kw = {}
        for name in ('C', 'tcon', 'timeWarp', 'fivi', 'faster', 'V0s'):
            kw[name] = getattr(self, name)
        if self.V0x:
            kw['V0'] = self.V0
        elif V0_isnum:
            # Initial fast-charge to V0
            nv0 = f.iNode('v0')
            f.V(nv0, 0, self.V0)
            nodes.append(nv0)
        ti = capacitance.Capacitance(f, *nodes, **kw).ti
        return {'ti': ti}


class Coil(Subcircuit):
    """
    A more realistic inductor, with effective series resistance, core
    saturation, and self-resonance from interwinding capacitance::

                                                 +---+
            +-------------------------------+----| C |--------------------+
            |                               |    +---+                    |
            |                               |          +----+             |
            |                               +----------| Rp |-------------+
            |                                          +----+             |
            |                                                             |
            |  +----+        +----+       +-------+          +-----+      |
        a --+--| Rs |-- 11 --| L0 |--+--->|+ Vs1 -|>-- 13 -->|+ F -|>--+--+-- b
               +----+        +----+  |    +-------+          +-----+   |     
                                     |       |                  x      |   
              +-------- 12 ----------+       |                  |      |
              |                              |                  |      |
            +----+            +-----<--------+                  |      |   
            | R0 |            |         f(I)            1:1     |      |
            +----+            x                 +----->---------+      |
              |           +------+              |                      |
              +--- 14 ---x|+     |          +-------+                  |
              |           |  B:V |>-- 21 -->|+ Vs2 -|--+               |
            +----+    +--x|-     |          +-------+  | 22            |
            | C0 |    |   +------+                     |               |   
            +----+    |                                |               |
              |       |                                |               |
              +-------+--------------------------------|---------------+
                                                       |
                          .............................|.....
                          :                            |    :
                     +---------+-------+-------+-------+    :
                     |    :    |       |       |       |    :
                  +----+  : +----+  +----+  +----+  +----+  :
                  | L1 |  : | R1 |  | R2 |  | R3 |  | R4 |  :
                  +----+  : +----+  +----+  +----+  +----+  :
                     |    :    |       |       |       |    :
                     | 23 :    |       | 31    | 32    | 33 :
                     |    :    |       |       |       |    :
                     |    :    |    +----+  +----+  +----+  :
                     |    :    |    | C1 |  | C2 |  | L2 |  :
                     |    :    |    +----+  +----+  +----+  :
                     |    :    |       |       |       |    :
                     +---------+-------+-------+-------+-------- Rz --- 0
                          :                                 :
                          ...................................

        R0 and C0 may be omitted and B:V+ input connected directly to
        node 12.

    B{Note}: R0 and C0 form an LPF with a time constant of ts, which
    may help convergence. But the author is not yet certain whether
    it's really that realistic or helpful to include. Low-pass filting
    here delays and limits high-frequency responsiveness to the effect
    of core saturation, which may or may not be true to the underlying
    physics of magnetic dipoles in ferrous material. To omit and have
    the + input of B:V connected directly to node 12, set my I{no_lpf}
    attribute C{True}.
    
    B{Note}: Components R1-4, C1-2, and L2, inside the dotted box, are
    for modeling high-frequency core loss per Edward Herbert's "Core
    Loss Modeling" presentations. It may be possible to determine
    their values, along with I{mu} and the exponent for L{expr_V13},
    by making this a L{ParameterFinder} and comparing actual
    measurements of sample devices to simulations with ADE. Probably
    not trivial, so this remains a big B{TODO} for now.
    
    In addition to inductance I{L}, also defines series resistance
    I{R}, a defined self-resonant frequency I{fsr}, and core
    saturation with inductance at I{Idc} dropping to 90% its
    zero-current value.

    The inductor retains 90% of its zero-current (maximum) inductance
    when there is I{Idc} Amps of DC current flowing through it. Set
    I{Idc} to I{None} to have no inductor core saturation.

    Core saturation is modeled in accordance with Ben-yaakov and
    Peretz, "Simulation bits: a SPICE behavioral model of non-linear
    inductors," IEEE Power Electronics Society Newsletter (Q4
    2003). When the DC current reaches I{Idc}, the effective
    inductance drops to 90% its full zero-bias amount. L0 implements
    the miminum fully-saturated inductance, when the coil is
    effectively just an air-core inductor.

    The function for the behavioral voltage source I{B:V} is::

        1 + 1/9*(|I|/Idc)^3
    
    This coil is simulation-friendly: If the pingspice simulation
    parameter I{ts} is defined, the coil will have a default
    self-resonant frequency of 2/ts, in the absence of a defined
    I{fsr} or if that is less than I{fsr}.

    B{Note:} The parallel (inter-winding capacitance) C and its
    damping resistance Rp are connected across the air-core
    fully-saturated equivalent inductance L0. This isn't exactly
    accurate, as the capacitance resonates with the much larger
    overall inductance. But having the capacitance across the overall
    inductance causes oscillations due to the behavioral sources. The
    capacitance is adjusted (made larger) to account for this.
    
    B{TODO:} Make this a L{ParameterFinder} with I{c} and the exponent
    determined via paramfinding on sample device measurements with a
    pulse input, and (non-trivial!) maybe include hysteresis in the
    B:V with its two unknown hysteresis parameters as well.

    @ivar R: Effective series resistance (ESR), Ohms. (Default is
        zero, but that's not realistic.)

    @ivar fsr: Self-resonant frequency, Hz.

    @ivar Q: The quality factor of the inductance in parallel with its
        winding capacitance. (Default is 50. Toroidal iron-powder
        power inductors have a Q of around 30-35.)

    @ivar Idc: DC current at which inductance drops to 90% of its
        zero-current value.

    @ivar mu: The initial (zero-current) relative permeability of the
        core. This is used to calculate the lower limit of
        inductance. Real-world values range from 20-130, with higher
        values resulting in lower fully saturated inductance values,
        since at that point the core adds nothing to the air-core
        inductance. Default is 50, which is mid-range for iron but low
        for Ferrite.

    @ivar pdiss: Set C{True} if a 'pdiss' (power dissipation) node is
        desired. Setting this with no non-zero I{R} defined raises an
        exception. The 'pdiss' node will come after the second
        inductor node.
    
    @ivar ic: Initial transient analysis current, Amps. (Default is
        C{None}, to use SPICE-computed initial conditions.)

    @ivar no_lpf: Set C{True} to omit the RC lowpass filtering in the
        current loop that simulates inductor saturation. The author is
        not yet certain whether it's really that realistic or helpful,
        though it is presently the default. (The default value of
        I{no_lpf} is C{False}.)
    """
    R           = 0
    fsr         = None
    Q           = 40
    Idc         = None
    mu          = 50
    ic          = None
    no_lpf      = False
    
    nodes = ['a', 'b']

    def expr_V13(self, n1):
        """
        Returns a B-source expression for the voltage at node I{n1}::

            V = V(n1, 'b') * (1 + 1/9*(|I(Vs1)|/Idc)^3)
        
        """
        ex = expressions.Expressionist()
        # First term
        ex.ap("V({}, 'b')", n1)
        # Second term
        ex.ap("(1 + {:f}*(abs(I(Vs1))/{:f})^3)", 1.0/9, self.Idc)
        return ex.ep("*")
    
    def setup(self, f):
        # Some keywords defining characterstics of the inductor primitive(s)
        kw = {}
        ts = f.get(self, 'ts')
        if ts: kw['ts'] = ts
        if self.ic is not None: kw['ic'] = self.ic
        # Series (winding) resistance
        f.R('a', 11, self.R)
        # Self-resonant frequency (maybe)
        fsr = 2.0/ts if ts else None
        if self.fsr and fsr and self.fsr < fsr: fsr = self.fsr
        if fsr:
            # 2*pi*fsr = sqrt(1/(LC) - (R/L)^2)
            w = 2*math.pi*fsr
            C = 1.0 / (self.L * (w**2 + (self.R/self.L)**2))
            f.C('a', 'b', C)
            Rp = 2*math.pi*fsr*self.L*self.Q
            f.R('a', 'b', Rp)
        # Saturation (maybe)
        if self.Idc:
            f.L0(11, 12, self.L/self.mu, **kw)
            f.Vs1(12, 13, 0)
            f.F(13, 'b', 'Vs2', 1.0)
            if ts and not self.no_lpf:
                R_lpf = 1e3
                f.R(12, 14, R_lpf)
                f.C(14, 'b', ts/R_lpf)
                n1 = 14
            else: n1 = 12
            f.B(21, 0, V=self.expr_V13(n1))
            f.Vs2(21, 22, 0)
            f.L1(22, 23, self.L*(1-1.0/self.mu), **kw)
            f.Rz(23, 0, RMIN)
        else: f.L(11, 'b', self.L, **kw)


class Lss(Subcircuit):
    """
    Simulation-friendly Inductor, as a subcircuit.

    B{Note:} This is included for explanatory purposes, but you can
    just specify a I{ts} keyword in a C{f.L} call to do the same thing
    much more easily.

    I have a small amount of parallel capacitance added, just enough
    to limit unit voltage rise time to simulation step time I{ts} if
    there is a discontinuous change in current. I also have just
    enough parallel resistance added to keep LC at critical damping,
    so there isn't any ringing.

    You'll appreciate how significant this is if you've struggled for
    hours with mysterious "time step too small" errors.

    The inductance is a parameter I{L} because it will likely be
    different each time you call an instance of me with a new node
    pair. So you use me something like this::

        ...
        L = Lss(f, ts=10E-9)
        L(1, 2, L=1E-6)
        f.R(2, 0, 1E3)
        L(2, 3, L=1.5E-6)
        f.R(3, 0, 2E3)
        ...

    If you want to define I{L} as an attribute, fixed for all calls to
    an instance of me, you can do that instead. Like so::

        Lss(f, ts=10E-9, L=1E-6)(1, 2)
        f.R(2, 0, 1E3)
        Lss(f, ts=10E-9, L=1.5E-6)(2, 3)
        f.R(3, 0, 2E3)

    @see: L{Lsi} for a version that includes the circuitry instead of
        putting it in a subcircuit.
    """
    L = None
    params = {'L': 0}
    nodes = ['a', 'b']
    
    def setup(self, f):
        # Doubled step time is more likely to get the job done
        ts = 2*f.get(self, 'ts')
        # C = 1/L * (ts/pi)^2
        # R = pi*L / (2*ts)
        if self.L is None:
            f('L', 'a', 'b', "{l}")
            C = sub("{{{:g}^2/9.86960440109/l}}", ts)
            f.C('a', 'b', C)
            R = sub("{{1.57079632679*l/{:g}}}", ts)
            f.R('a', 'b', R)
            return
        f('L', 'a', 'b', self.L)
        C = (ts / math.pi)**2 / self.L
        f.C('a', 'b', C)
        R = math.pi * self.L / (2*ts)
        f.R('a', 'b', R)


class Lsi(Include):
    """
    Simulation-friendly Inductor, as an included chunk of netlist.

    B{Note:} This is included for explanatory purposes, but you can
    just specify a I{ts} keyword in a C{f.L} call to do the same thing
    much more easily.
    
    I have a small amount of parallel capacitance added, just enough
    to limit unit voltage rise time to simulation step time I{ts} if
    there is a discontinuous change in current. I also have just
    enough parallel resistance added to keep LC at critical damping,
    so there isn't any ringing.

    You use me something like this::

        ...
        Lsi(f, 1, 2, ts=10E-9, L=1E-6)
        f.R(2, 0, 1E3)
        Lsi(f, 2, 3, ts=10E-9, L=1.5E-6)
        f.R(3, 0, 2E3)
        ...

    You can't alter subcircuit parameters, so this is used for
    L{analysis.param.ParameterFinder} setups instead of L{Lss}. Also,
    it produces less netlist lines and recursion for just one device
    instance.
    """
    def setup(self, f, a, b):
        ts = f.get(self, 'ts')
        if ts is None:
            raise RuntimeError(sub(
                "You must define a time step 'ts' in {} or {}!", self, f))
        # C = 1/L * (ts/pi)^2
        # R = pi*L / ts
        refDes = f('L', a, b, self.L)
        # AV compatible
        C = self.L**-1 * (ts / math.pi)**2
        f("C_"+refDes, a, b, C)
        # AV compatible
        R = self.L * math.pi / ts
        f("R_"+refDes, a, b, R)


class Wire(Subcircuit):
    """
    A wire with a particular I{awg} gauge and I{length}, in meters
    unless I{inches} is set C{True}.

    Various class methods support both an individual L{Wire} and a
    L{WirePair}.

    Inductors often cause convergence errors in SPICE because they
    create ringing that needs to be tracked by the stepwise
    simulation, often at much higher frequencies than you're really
    interested in. To ignore the inductance (and capacitance, in a
    L{WirePair}), set I{R_only} C{True}.
    """
    rhoCopper   = 1.68E-8
    muZero      = math.pi * 4E-7
    # Ignore inductance, capacitance
    R_only      = False
    # Use backward American units
    inches      = False

    @classmethod
    def mmArea(cls, awg):
        """
        Returns the copper cross-sectional area (mm2) of a wire given the
        American Wire Gauge (an integer). An I{awg} of 0 will select
        4/0 battery cable.

        References: NEC 2017 Ch. 9, Tables 5A, 8.
        """
        return {
            0:  107.2,
            1:  42.41, 
            2:  33.62,
            3:  26.67,
            4:  21.15,
            6:	13.30,
            8:	8.367,
            10:	5.261,
            12:	3.31,
            14:	2.08,
            16: 1.31,
            18: 0.823,
        }[awg]

    @classmethod
    def mmDia(cls, awg, insulation=False):
        """
        Returns the overall conductor or THHN insulated diameter (mm) of a
        wire given the American Wire Gauge (an integer). An I{awg} of
        0 will select 4/0 battery cable.

        The conductor diameter includes voids between strands. Use
        L{mmArea} to calculate wire resistance.

        Set I{insulation} to C{True} to include the insulation.

        References: NEC 2017 Ch. 9, Tables 5, 5A.
        """
        return {
            0:  (13.41, 16.31),
            1:  (8.43, 11.33), 
            2:  (7.42, 9.754),
            3:  (6.60, 8.941),
            4:  (5.89, 8.230),
            6:	(4.67, 6.452),
            8:	(3.71, 5.486),
            10:	(2.95, 4.166),
            12:	(2.32, 3.302),
            14:	(1.85, 2.819),
            16: (1.46, 2.4), # Insulated OD guesstimated
            18: (1.16, 2.0), # Insulated OD measured
        }[awg][int(insulation)]

    nodes = ('a', 'b')

    @property
    def meters(self):
        if self.inches:
            return 2.54E-2 * self.length
        return self.length
    
    def skinDepth(self, f=120):
        """
        Returns the skin depth in meters of an I{awg} gauge conductor for
        a signal of I{f} Hertz (default: 120 Hz).

        This is included for completeness but not used in resistance
        calculation because skin effect at 120 Hz only reduces
        cross-sectional area by about 1% on a 4/0 AWG wire.
        """
        conductivityCopper = 5.98E7 # S/m
        x =  1.0 / conductivityCopper
        x /= math.pi * f * self.muZero
        return math.sqrt(x)

    def L_internal(self, r):
        """
        Returns the internal inductance (Henries) per meter of a wire of
        the specified radius I{r} in mm.

        Included (and used) for completeness but not a realistic factor.
        """
        sd = self.skinDepth()
        x  = self.muZero * sd * (2*r - sd)
        x /= 8 * math.pi * r**2
        return x

    @property
    def L(self):
        """
        Returns inductance (Henries) of my I{length} of a single wire of
        my gauge I{awg}.
        """
        if self.R_only: return 0
        length = self.meters
        r = 0.5*self.mmDia(self.awg)
        x  = math.asinh(length / r)
        x -= math.sqrt(1 + (r / length)**2)
        x += r / length
        L = self.muZero / (2*math.pi) * x
        return length * (L + self.L_internal(r))

    def R(self, awg, unitLength=False):
        """
        Returns the room-temperature resistance (Ohms) of my I{length} of
        copper wire of the specified gauge I{awg}.

        Skin effect is negligible for DC and AC power frequencies and
        is not accounted for.
        """
        length = 1.0 if unitLength else self.meters
        squareMeters = 1E-6 * self.mmArea(awg)
        return self.rhoCopper * length / squareMeters
    
    def setup(self, f):
        R = self.R(self.awg)
        L = self.L
        if L:
            f.L('a', 1, L, ts=f.get(self, 'ts'))
            f.R(1, 'b', R)
        else: f.R('a', 'b', R)


class WirePair(Wire):
    """
    A wire pair with a particular I{awg} gauge and I{length} in meters
    (unless I{inches} is set C{True}), optionally with an additional
    I{gap} (in mm) between the wires::

        a0 <--- R - L ---> a1
        b0 <--- R - L ---> b1

    This is mostly for modeling high-current behavior at relatively
    low frequencies.

    If you want to use a ground reference on both ends, just set
    I{gndRef} C{True} and the single pair of nodes 'a0', 'a1'
    will have the R and L for both wires.

    Inductors often cause convergence errors in SPICE. To ignore the
    inductance (and capacitance) of the wire pair, set I{R_only}
    C{True}.
    """
    # Vacuum permittivity
    E0 = 8.8541878176E-12
    # Default relative permittivity: THHN, mostly PVC with a thin
    # nylon sheath
    Er = 3.3

    # Ignore insulation when computing separation? (In that case, gap
    # is the only distance.)
    ignoreInsulation = False
    # Use transmission line model if possible (TRAN analysis only!)
    useTxLine = False
    # Number of lumped RLC stages to use, if not transmission line
    # model. More will better approximate the wire pair's
    # transmission-line effects, but smaller RLC time constants will
    # cause more simulation headaches.
    N_lumps = 3

    # Air gap (mm) between insulation of each conductor (zero if
    # touching)
    gap = 0
    # American wire gauge of each conductor. You can also specify
    # I{awg} for each having the same gauge.
    awgs = None
    awg = None
    # Use ground reference and double R, L of single connection
    # between two nodes instead of four.
    gndRef = False
    

    @property
    def nodes(self):
        result = ['a0', 'a1']
        if not self.gndRef:
            result.extend(['b0', 'b1'])
        return result

    @property
    def _awgs(self):
        if self.awgs is None:
            if self.awg is None:
                raise ValueError(
                    "You must specify wire gauges or a common wire gauge")
            return [self.awg]*2
        return self.awgs
    
    @property
    def sep(self):
        rList = [0.5*self.mmDia(
            x, insulation=not self.ignoreInsulation) for x in self._awgs]
        return sum(rList) + self.gap
    
    @property
    def L(self):
        """
        Returns inductance (Henries) per meter of two adjacent wires given
        their wire gauges.

        You can include an additional air I{gap} (in mm) between the
        wires, on average. For example, use gap=4 for loosely bundled
        heavy wires.
        """
        if self.R_only: return 0
        rList = [0.5*self.mmDia(x) for x in self._awgs]
        x = self.sep**2 - rList[0]**2 - rList[1]**2
        x /= 2 * rList[0] * rList[1]
        L = 0.5 * self.muZero / math.pi * math.acosh(x)
        for r in rList:
            L += self.L_internal(r)
        return L

    @property
    def C(self):
        """
        Returns capacitance (Farads) per meter between two adjacent wires
        given their common I{length} in meters (unless I{inches} is
        set) and wire gauges.

        You can include an additional air I{gap} (in mm) between the
        wires, on average. For example, use gap=4 for loosely bundled
        heavy wires.

        An average radius of the two wires is used, which may not be
        accurate if they are very different.
        """
        if self.R_only: return 0
        sep = self.sep
        rAvg = 0.5*sum([0.5*self.mmDia(x) for x in self._awgs])
        C = math.pi * self.Er * self.E0
        extraTerm = math.sqrt(sep**2 / (4*rAvg**2) - 1.0)
        C /= math.log(sep/(2*rAvg) + extraTerm)
        return C

    def txLine(self, f):
        """
        Lossy transmission line.
        """
        R = sum([self.R(x, unitLength=True) for x in self._awgs])
        wirepair = f.MODEL(
            'wirepair', 'ltra', R=R, L=self.L, C=self.C, LEN=self.meters)
        if self.gndRef:
            f.O('a0', 0, 'a1', 0, wirepair)
        else: f.O('a0', 'b0', 'a1', 'b1', wirepair)

    def RLC_unbal(self, f, L, R, C, na0, *na1):
        n1 = self.iNode()
        f.L(na0, n1, L, ts=f.get(self, 'ts'))
        n2 = na1[0] if na1 else self.iNode()
        f.R(n1, n2, R)
        if C: f.C(n2, 0, C)
        return n2

    def RLC_bal(self, f, L, R, C, na0, nb0, *nab1):
        R /= 2
        nList = []
        n2List = nab1 if nab1 else [self.iNode()]*2
        for k, n0 in enumerate((na0, nb0)):
            n1 = self.iNode()
            f.L(n0, n1, L, ts=f.get(self, 'ts'))
            n2 = n2List[k]
            f.R(n1, n2, R)
            nList.append(n2)
        if C: f.C(nList[0], nList[1], C)
        return nList

    def setup(self, f):
        R_list = [self.R(x) for x in self._awgs]
        if self.R_only:
            if self.gndRef:
                R = sum(R_list)
                f.R('a0', 'a1', R)
                return
            f.R('a0', 'a1', R_list[0])
            f.R('b0', 'b1', R_list[1])
            return
        if self.useTxLine:
            self.txLine(f)
            return
        length = self.meters
        Lk = length/self.N_lumps * self.L
        Rk = length/self.N_lumps * sum(
            [self.R(x, unitLength=True) for x in self._awgs])
        Ck = length/(self.N_lumps-1) * self.C
        if self.gndRef:
            n0 = 'a0'
            for k in range(self.N_lumps-1):
                n0 = self.RLC_unbal(f, Lk, Rk, Ck, n0)
            self.RLC_unbal(f, Lk, Rk, 0, n0, 'a1')
            return
        # The inductance won't be the same for each wire if the gauges
        # are different, but it doesn't matter for almost all uses.
        na0, nb0 = 'a0', 'b0'
        for k in range(self.N_lumps-1):
            n0 = self.RLC_bal(f, 0.5*Lk, Rk, Ck, na0, nb0)
        self.RLC_bal(f, 0.5*Lk, Rk, 0, na0, nb0, 'a1', 'b1')
