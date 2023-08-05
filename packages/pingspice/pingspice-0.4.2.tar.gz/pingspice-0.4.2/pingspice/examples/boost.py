#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.

"""
A switch-mode boost converter supplying current from a 12V battery
to a 48V one.
"""

from copy import copy
from cStringIO import StringIO
from contextlib import contextmanager

import numpy as np
from twisted.internet import reactor, defer

from yampex.plot import Plotter
from yampex.tools import clipOutliers

from pingspice.circuit.wrappers import Paren, Array
from pingspice.circuit.netlist import Netlist, Subcircuit, Include
from pingspice.ngspice import NgspiceRunner
from pingspice.analysis.sim import TRAN
from pingspice.analysis.vectors import Vectors_File
from pingspice.analysis.capacitance import Capacitance
from pingspice.analysis.tools import SwitchmodeTools
from pingspice.util import *

# Electronic Components
from pingspice.lib import mosfets, diodes
from pingspice.lib.passive import Wire, WirePair, Coil, Capacitor
from pingspice.lib.active import PWM, FileSource
from pingspice.lib.current import Ammeter, InrushLimiter
from pingspice.lib.thermal import TO247, WV_T247


#--- FUNCTIONS ----------------------------------------------------------------

def dtt(f, *args, **kw):
    """
    Runs the function I{f} with I{args} and I{kw} in a thread,
    returning a C{Deferred} that fires with the eventual
    result. If there's an error, calls L{oops}.
    """
    return deferToThread(f, *args, **kw).addErrback(oops)


#--- CONFIGURATION ------------------------------------------------------------
# Your configuration of how the simulation runs should all be set here.

# Ngspice options, if non-default. SPICE is an old and fragile
# matrix-solution simulation algorithm that was never intended for the
# complexity of circuitry it's being asked to handle here. Sometimes
# it requires you to relax its runtime options a bit to avoid
# convergence errors, unfortunately.
OPTS = {}
# Omit the inrush limiters?
NO_IRL = True
# Ignore inductance of wires connecting to the boost converter circuit
# board?
IGNORE_WIRE_L = False
# Ignore component lead inductance?
IGNORE_LEAD_L = False
# Ignore inductor saturation?
IGNORE_SATURATION = False
# If modeling inductor saturation, omit LPF in saturation response?
# The author is not yet sure if the LPF helps realism or convergence.
NO_SATURATION_LPF = False


#--- LIBRARY ------------------------------------------------------------------
# Components not provided in pingspice's modest standard library

class CeramicCapacitor(Subcircuit):
    """
    10 nF ceramic capacitor to ground for RF filtering, with very
    small ESL. ESR is wild-ass guess based on Kemet's capacitor tool,
    center of 4-30 MHz range
    """
    nodes = ['a', 'b']

    def setup(self, f):
        f.C('a', 1, 10E-9)
        f.R(1, 'b', 15E-3)


#--- CIRCUIT ------------------------------------------------------------------
# The boost converter circuit board, the overall circuit, and a
# thermal equivalent circuit

class Boost(Subcircuit):
    """
    The boost converter circuit board.

    For the sake of simplicity and avoiding a non-convergence
    nightmare, the ground for this subcircuit is the perfect
    simulation ground (node 0). Some realism is sacrificed for this,
    of course, because the copper foil used as a ground plane in the
    actual circuit has non-zero impedance and that lumps of that
    impedance are present between leads of components ostensibly
    connected to "ground."

    @ivar thermal: A dict containing entries that define some
        temperatures, all in degrees C: 'ambient'; 'tca0-mosfet'
        (initital MOSFET case temp); 'tca0-diode' (initital diode case
        temp).

    @ivar ti: The time you should set aside for my initialization of
        MOSFET and diode case temperatures at the beginning of your
        TRAN simulation. (Read-only.)
    """
    tRiseFall = 25e-9
    MOSFET = mosfets.STW75NF20
    Diode = diodes.MBR40250

    def setup(self, f):
        """
        Sets up the circuit for the boost converter.
        """
        V0 = self.Vout if self.Vout else self.Vin
        ambient = self.thermal['ambient']
        
        A = Ammeter(f)

        #--- Define some library component subcircuits ------------------------
        Idc = None if IGNORE_SATURATION else 26.3 
        L = Coil(
            f, L=10E-6, R=6E-3, fsr=10E6, Idc=Idc, no_lpf=NO_SATURATION_LPF)
        kw = {
            'ignoreL': self.ignoreL,
            'ambient': ambient,
        }
        kw['tca0'] = self.thermal['tca0-mosfet']
        # MOSFET has an Ohmite WV-T247-101E heatsink
        kw['heatsink'] = WV_T247
        Q = self.MOSFET(f, **kw)
        # No heatsink necessary on diode
        kw['tca0'] = self.thermal['tca0-diode']
        D = self.Diode(f, **kw)
        # Al-Polymer 16V with great ESR (APSG160ELL152MJ16S)
        C1 = Capacitor(
            f, C=1500E-6, ESR=8E-3,
            leadSpacing=5.0, pdiss=True, V_max=16)
        # Electrolytic, 80V, great ESR (EGPD800ELL162MM40H)
        C2 = Capacitor(
            f, C=1600E-6, ESR=21E-9,
            leadSpacing=7.5, pdiss=True, V_max=80)
        #  Film, 250V with df ~ 2% @ 400kHz (ECQ-E2106KF)
        C3 = Capacitor(
            f, C=0.1E-6, df=(0.02, 400E3), ESL=6E-9, pdiss=True)
        C4 = CeramicCapacitor(f)
        # End of longest inital-voltage charge interval
        self.ti = max([x.ti for x in Q, D if x.ti is not None])
        #--- Input capacitors, possibly with inrush limiter on big ones -------
        C4('inp', 0) # Ceramic right at power input
        if NO_IRL:
            # No inrush limiter
            f.R('inp', 15, 1e-4)
            f.V('pd_il1', 0, 0)
        else:
            # Inrush limiter for input caps (CL-11)
            InrushLimiter(
                f, tc=100.0, timeWarp=2000,
                df=25.0, Iss=12.0, Ta=ambient,
                R0=0.7, R25=0.14, R50=0.06, R75=0.04, R100=0.03)(
                    'inp', 15, 'pd_il1')
        # Big electrolytics, with current flow monitoring on one of them
        C1(15, 10, 'pd_c1')
        A(10, 0, 'amps_c1')
        C1(15, 0)
        #--- Inductor, w/ current flow monitoring & oscillation damping -------
        A(*npr(15, 20, 'amps_l'))
        L(20, 'drain')
        f.R(15, 'drain', 22E3)
        #--- PWM -> driver -> MOSFET ------------------------------------------
        PWM(f, fs=self.fs,
            tRiseFall=self.tRiseFall, t0=self.ti,
            Vhigh=self.Vin, Vlow=0.2)('duty', 'pwm', 0)
        # External gate resistance
        Rg = 10.0
        f.R('pwm', 'gate', Rg)
        # The switching MOSFET
        Q('drain', 'gate', 0, 'pd_mosfet', 'tj', 'tc', ambient=ambient)
        # Vgs pulldown
        f.R('gate', 0, 1.5e3)
        #--- Output diode -----------------------------------------------------
        D('drain', 40, ambient=ambient)
        #--- Output caps ------------------------------------------------------
        # Bigger ones between output inrush limiter ("inrush" would be
        # from a battery connected at the output)
        C2(40, 42, 'pd_c2'); A(42, 0, 'amps_c2')
        C3(40, 44, 'pd_c3'); A(44, 0, 'amps_c3')
        if NO_IRL:
            # No inrush limiter
            f.R(40, 'out', 1e-4)
            f.V('pd_il2', 0, 0)
        else:
            # Inrush limiter for output caps (CL-170)
            InrushLimiter(
                f, tc=110.0, timeWarp=2000,
                df=15.0, Iss=2.7, Ta=ambient,
                R0=16.0, R25=1.95, R50=0.80, R75=0.48, R100=0.33)(
                    40, 'out', 'pd_il2')
        # Smaller caps, right at output
        C3('out', 0)
        C4('out', 0)


class Circuit(Include):
    """
    The overall simulated circuit, including connecting wires and a
    duty cycle control voltage source.

    For the sake of simplicity and avoiding a non-convergence
    nightmare, the ground for this circuit is the perfect simulation
    ground (node 0). Some realism is sacrificed for this, of course,
    because the copper foil used as a ground plane in the actual
    circuit has non-zero impedance and that lumps of that impedance
    are present between leads of components ostensibly connected to
    "ground."

    B{Note}: There are two additional nodes in the circuit that will
    be examined and post-simulation analysis: 'amps_in' and
    'amps_out'. These nodes are not included in my constructor
    arguments because those are passed on as-is to the L{Boost}
    subcircuit. It doesn't matter what additional nodes are defined in
    my L{setup} method and whether they are examined or not, because
    B{all} nodes in an L{Include} are considered "public."

    There are two purposes of defining nodes in a constructor, or as a
    class attribute I{nodes}, of an I{Include}. The first is to pass
    them on to the L{setup} method as arguments following the
    circuit-building tool I{f}. That makes it convenient to define
    local variables in the method. See
    L{analysis.capacitance.FastChargeCap} and
    L{analysis.capacitance.Initializer} for examples.

    The second purpose is to allow pingspice to check that all the
    predefined nodes are actually connected. An exception is raised if
    any node defined in the constructor or I{nodes} class attribute
    are not connected in some way by the L{setup} method. This is
    valuable because failure to do so can result in some Ngspice
    convergence problems that are B{very} difficult to troubleshoot.
    
    @cvar L_out: Parasitic inductance of output resistor (if present).

    @ivar thermal: A dict containing entries that define some
        temperatures, all in degrees C: 'ambient'; 'tca0-mosfet'
        (initital MOSFET case temp); 'tca0-diode' (initital diode case
        temp).
    
    @ivar dc0: Starting duty cycle.
    @ivar dc1: Ending duty cycle.
    @ivar tt: Transition time (seconds) from dc0 to dc1.

    @ivar ti: The time you should set aside for my initialization of
        MOSFET and diode case temperatures at the beginning of your
        TRAN simulation. (Read-only.)
    """
    L_out = 0.5e-6

    def setup(self, f, *nodes):
        A = Ammeter(f)
        
        # 12V battery with 60 mOhm resistance connected via 2x2 ft of
        # 12 AWG wire (pair treated as a single wire)
        n1, n2, n3 = f.iNode('inp', 3)
        f.R(n1, n2, 0.060)
        WirePair(
            f, gndRef=True, inches=True,
            R_only=IGNORE_WIRE_L, awg=12, length=12*2*2)(n2, n3)
        A(n3, 'inp', 'amps_in')
        # The boost converter
        kw = {
            'fs': self.fs, 'nodes': nodes,
            'Vin': self.Vin, 'Vout': self.Vout,
            'ignoreL': IGNORE_LEAD_L, 'thermal': self.thermal
        }
        boost = Boost(f, **kw)(*nodes)
        self.ti = boost.ti
        # The load, connected via 2x6 ft of 18 AWG (pair treated as a
        # single wire)
        n3, n4 = f.iNode('out', 2)
        A('out', n3, 'amps_out')
        WirePair(
            f, gndRef=True, inches=True,
            R_only=IGNORE_WIRE_L, awg=18, length=12*2*6)(n3, n4)
        if self.Vout:
            f.V(n4, 0, self.Vout)
        if self.R_out:
            n5 = f.iNode('out')
            f.R(n4, n5, self.R_out)
            f.L(n5, 0, self.L_out, ts=f.get(self, 'ts'))
        # The input (12V battery voltage)
        ts = f.get(self, 'ts')
        f.V(n1, 0, 'DC', self.Vin, PULSE=[0, self.Vin, 0, self.ti, ts])
        # Control for the duty cycle
        f.V('duty', 0, DC=0, PULSE=[self.dc0, self.dc1, 0.20*self.tt, self.tt])


class ThermalConfig(object):
    """
    Call an instance of me with appropriate arguments to get a dict
    suitable for use as the 'thermal' attribute of L{Circuit}.
    """
    # MOSFET Heatsink thermal resistance
    rth_hs = 12.0
    # MOSFET Heatsink thermal capacitance
    # Specific heat of Al times mass
    cth_hs = 0.902 * 12.0

    def __init__(self, ambient):
        self.thermal = {
            'ambient': ambient,
            'rth_hs': self.rth_hs,
            'cth_hs': self.cth_hs
        }
    
    def tca0(self, name, caseTemp):
        ambient = self.thermal['ambient']
        if caseTemp is None:
            caseTemp = ambient
        if caseTemp < ambient:
            raise ValueError(sub(
                "Case temperature of {:+.1f} is lower than ambient temp "+\
                "of {:+.1f}", caseTemp, ambient))
        self.thermal[name] = caseTemp - ambient
    
    def __call__(self, tc0_mosfet, tc0_diode):
        self.tca0('tca0-mosfet', tc0_mosfet)
        self.tca0('tca0-diode', tc0_diode)
        return self.thermal


class CircuitBuilder(object):
    """
    I build the netlist for your circuit.

    There are three constructor arguments, which are all temperatures
    in degrees C:

        1. ambient
        2. MOSFET case, initial
        3. Diode case, initial

    @keyword verbose: Set C{True} to have detailed info about node
        connections logged.
    """
    nodes_basic = [
        # Duty cycle for MOSFET shorting inductor to ground
        'duty',
        # Input and output
        'inp', 'out',
        # MOSFET terminals (source tied to ground)
        'gate', 'drain',
        # MOSFET junction and case temperature
        'tj', 'tc',
        # Current flow through each input cap, inductor, and output caps
        'amps_c1', 'amps_l', 'amps_c2', 'amps_c3',
        # Power dissipation of components that run hot
        'pd_mosfet', 'pd_c1', 'pd_c2', 'pd_c3',
    ]
    nodes_irl = [
        # Power dissipation of inrush limiters
        'pd_il1', 'pd_il2',
    ]

    def __init__(self, ambient, tc0_mosfet, tc0_diode, verbose=False):
        self.nodes = self.nodes_basic
        if not NO_IRL:
            self.nodes += self.nodes_irl
        self.thermal = ThermalConfig(ambient)(tc0_mosfet, tc0_diode)
        self.verbose = verbose

    def build(self, name, **kw):
        """
        Call this with the name of your circuit and any keywords you want
        to supply to the constructor of L{Circuit}.

        Returns a 2-tuple with (1) the initial-charging time interval
        I{ti} for getting the case temperatures where you want them to
        start, and (2) a string containing the full netlist.
        """
        kw['thermal'] = self.thermal
        fh = StringIO()
        with Netlist(
                fh, name,
                ts=kw.pop('ts', None),
                timeWarp=kw.pop('timeWarp', 1.0),
                fiti=kw.pop('fiti', None), debug=self.verbose)() as f:
            ckt = Circuit(f, *self.nodes, **kw)
        netlist = fh.getvalue()
        fh.close()
        return ckt.ti, netlist


#--- SIMULATION ---------------------------------------------------------------


class ResultsPlotter(object):
    """
    Construct an instance of me to intialize a C{yampex.plot.Plotter}
    object for a new Matplotlib C{Figure} window. Then call my various
    methods on that instance to plot results.

    Constructor arguments are the total number of subplots, or the
    number of columns and then rows of subplots.

    Each call accepts at least one argument, a 2-sequence
    containing the initial charging interval and the Ngspice results
    L{Vectors_Ngspice} object.

    Additional optional arguments are (2) the minimum TIME value to
    include in the subplot (default is to include the earliest) and
    (3) the maximum TIME value to include (default is to include the
    latest).

    You can specify a particular subplot with its integer index by
    setting the keyword I{k} to that index in the call.

    Call my L{done} method with no arguments when done setting up all
    subplots.

    @keyword dims: The desired dimensions of the figure as a string
        with "x" separating width from height.
    
    @keyword xy: Set C{True} if these are xy plots and not having time
        as the x-axis variable. In that case, supply a third or fourth
        argument to any call will raise an exception.

    @keyword timeWarp: Set to a non-unity value if there was a thermal
        timeWarp in the simulation.

    @keyword fiti: The initial time allocated for fast initial
        temperature increase, for irregular but simulation-friendly
        initial warm-up. The default is C{None} for no such irregular
        warm-up. B{Note:} I{timeWarp}, if any, still applies.

    @keyword fs: The switching frequency (Hz).

    @keyword dc0: The starting (or only) duty cycle (fractional, 0-1).

    @keyword dc1: The ending duty cycle (fractional, 0-1), when ramped
        from I{dc0}.
    """
    infoLocations = {
        'timeWarp':     "N",
        'temp':         "NW",
        'voltage':      "NW",
        'power':        "NW",
        'efficiency':   "NW",
    }
    
    def __init__(self, *args, **kw):
        self.xy = kw.pop('xy', False)
        self.timeWarp = kw.pop('timeWarp', 1)
        for name in ('fiti', 'fs', 'dc0', 'dc1'):
            setattr(self, name, kw.pop(name, None))
        dims = kw.pop('dims', None)
        if dims:
            figSize = [float(x)/Plotter.DPI for x in dims.split('x')]
        else: figSize = None
        if figSize: kw['figSize'] = figSize
        p = Plotter(*args, **kw)
        p.use_grid()
        p.use_minorTicks('x')
        p.use_minorTicks('y')
        if not self.xy: p.use_timex()
        self.sp = p.start()

    def __getattr__(self, name):
        """
        If the I{name} matches, returns a wrapper function that calls the
        named one of my underscored subplotting methods with an
        initial time interval I{ti} and a possibly trimmed I{V}.

        The wrapper function (which is what you actually call) takes a
        single argument I{ti_V}, a 2-sequence containing I{ti} and the
        untrimmed I{V}. It accepts keywords I{tMin} and I{tMax} for
        time trimming and I{k} for specifying which subplot to use if
        not the default progression.

        If my I{xy} attribute is set I{True} for xy plots, there is no
        time trimming of I{V} and specifying I{tMin} or I{tMax} raises
        an exception.
        """
        def wrapper(tMin=None, tMax=None, k=None):
            ti, V = self.ti, self.V
            if self.xy:
                if tMin is not None or tMax is not None:
                    raise ValueError(
                        "You can't specify tMin or tMax for an XY plot!")
            else:
                V = V.trimmedCopy(tMin, tMax)
                if ti and ti > V.time[0] and ti < V.time[-1]:
                    self.sp.add_axvline(ti)                    
            return f(ti, V, self.sp, k=k)
        
        if name.startswith("plot_"):
            suffix = "_".join(name.split('_')[1:])
            f = getattr(self, sub("_{}", suffix))
            return wrapper

    def setResult(self, ti_V):
        self.ti, self.V = ti_V
        
    def done(self):
        """
        Call this with no args when done plotting and I can draw my
        C{Figure} with all subplots.
        """
        self.sp.done()

    def power(self, V, in_or_out):
        """
        Given a C{Vectors} object I{V} and a string I{in_or_out} that is
        either 'in' or 'out', returns the input or output power.
        """
        if in_or_out == 'in':
            VV = V['inp']
            VI = V['amps_in']
        elif in_or_out == 'out':
            VV = V['out']
            VI = V['amps_out']
        else: raise ValueError("Must be 'in' or 'out'!")
        return VV*VI
    
    def timeWarpInfo(self):
        """
        Adds info to the next subplot about the thermal I{timeWarp} that
        was used, and possibly also the I{fiti}. (Both are attributes
        set up from constructor keywords.)
        """
        parts = [sub("Thermal Timewarp: {:d}x", self.timeWarp)]
        if self.fiti:
            parts.append(sub(
                "with {:d}x more for the first {:.5g} seconds",
                Capacitance.faster, self.fiti))
        self.sp.add_textBox(self.infoLocations['timeWarp'], ", ".join(parts))

    def tempInfo(self, name, Tmean, Tmax, Tslope):
        """
        For the temperature with the supplied I{name}, adds to the next
        subplot info about its average I{Tmean} and maximum I{Tmax} in
        degrees C, and its slope I{Tslope} in deg/seg.

        Relies on the value of my I{timeWarp} attribute, set via that
        constructor keyword.
        """
        parts = []
        parts.append(sub("Mean {:.1f} deg C", Tmean))
        parts.append(sub("Max {:.1f}", Tmax))
        parts.append(sub("Warming by {:+.1f} deg/sec", Tslope/self.timeWarp))
        self.sp.add_textBox(
            self.infoLocations['temp'],
            "{}: {}", name.capitalize(), ", ".join(parts))

    def voltageInfo(self, V):
        """
        Adds info about the time-averaged input and output voltages, my
        switching frequency I{fs} and, if specified, my start and
        ending duty cycles I{dc0}, I{dc1}.
        """
        def add(proto, *args):
            textParts.append(sub(proto, *args))
        
        textParts = []
        add("{:.1f} V --> {:.1f} V", V.avg('inp'), V.avg('out'))
        if self.fs:
            add("{:.1f} kHz switching", self.fs)
        if self.dc0 is not None:
            dc0 = 100*self.dc0
            if self.dc1 is not None:
                dc1 = 100*self.dc1
                add("{:.1f}% -> {:.1f}% duty cycle", dc0, dc1)
            else: add("{:.1f}% duty cycle", dc0)
        self.sp.add_textBox(
            self.infoLocations['voltage'], ", ".join(textParts))
    
    def _voltages(self, ti, V, sp, k=None):
        """
        Plots the input and output voltages.
        """
        sp.set_ylabel("Volts")
        sp.set_legend("Input", "Output")
        self.voltageInfo(V)
        return sp(V, 'time', 'inp', 'out', k=k)
        
    def _voltages_internal(self, ti, V, sp, k=None):
        """
        Plots the MOSFET terminal voltages, plus the output.
        """
        sp.set_ylabel("Volts")
        sp.set_legend("Gate", "Drain", "Output")
        return sp(V, 'time', 'gate', 'drain', 'out', k=k)

    def _currents(self, ti, V, sp, k=None):
        """
        Plots the input and output current (Amps).
        """
        sp.set_ylabel("Amps")
        sp.set_legend("Input", "Output")
        sp.add_annotation(-1, "{:.1f} A", V.amps_out[-1], kVector=1)
        return sp(V, 'time', 'amps_in', 'amps_out', k=k)

    def _currents_internal(self, ti, V, sp, k=None):
        """
        Plots the current (Amps) in the most important internal current
        paths.
        """
        sp.set_ylabel("Amps")
        sp.set_legend("C1", "L", "C2", "C3")
        return sp(V, 'time', 'amps_c1', 'amps_l', 'amps_c2', 'amps_c3', k=k)

    def _temps(self, ti, V, sp, k=None):
        """
        Plots the MOSFET junction and case temperatures.
        """
        sp.set_ylabel("Degrees C")
        sp.set_legend("Tj", "Tc")
        return sp(V, 'time', 'tj', 'tc', k=k)

    def _power(self, ti, V, sp, k=None):
        """
        Plots the power in vs out, and also power dissipated in the inrush
        limiters if they are present.
        """
        sp.add_legend("Input")
        sp.add_legend("Output")
        text = "Power In, Out"
        powerList = [V.time, self.power(V, 'in'), self.power(V, 'out')]
        for name, label in (('pd_il1', "Input IRL"), ('pd_il2', "Output IRL")):
            if name in V:
                sp.add_legend(label)
                powerList.append(V[name])
        if len(powerList) > 3:
            text += ", Inrush Limiter Dissipation"
        sp.add_textBox(self.infoLocations['power'], text)
        return sp(*powerList)

    def _efficiency(self, ti, V, sp, k=None):
        """
        Plots the converter efficiency vs duty cycle.
        """
        sp.add_textBox(
            self.infoLocations['efficiency'],
            "Converter Efficiency vs. Duty Cycle")
        sp.set_xlabel("Duty Cycle")
        sp.set_ylabel("%")
        E = 100*np.clip(self.power(V, 'out') / self.power(V, 'in'))
        return sp(V.duty, E)


class Sim(object):
    """
    I run a simulation for a switchmode boost converter. Construct an
    instance of a subclass of me with an L{Args} object containing
    your command-line arguments and options.

    Then you can call the instance to get a C{Deferred} that fires
    with the L{Vector_Ngspice} object I{V} when I have prepared (but
    not yet shown) a Matplotlib C{Figure} with my results.

    @cvar Nc: The number of columns in the Matplotlib C{Figure} that
        shows results.

    @cvar Nr: The number of rows in the Matplotlib C{Figure} that
        shows results.

    @cvar timeWarp: The thermal timewarp.
    @cvar fastWarmup: Set C{True} to use an initial fast warmup.

    @cvar N_ts: Set > 1 if convergence problems; that will increase
        circuit ts vs that of TRAN timestep

    @ivar M: Set to a multiple of 1 to do decimation on the output,
        i.e., have internal Ngspice timestep be that multiple of the
        nominal time between samples produced.
    
    @ivar name: The name to use for my circuit.
    @ivar names: A list of Ngspice result vector names to obtain.
    @ivar t0: The time to start obtaining simulation results.
    @ivar t1: The end time for the simulation.
    """
    Nc = 1
    Nr = 1
    timeWarp = 1

    N_ts = 2
    M = 1

    @classmethod
    def setArgs(cls, args):
        """
        All instances will share the same command-line I{args}, analysis
        L{Config} object I{cfg}, L{SwitchmodeTools} object I{smct},
        and L{CircuitBuilder} object I{cb}.
        """
        if not args.o and not args.R:
            print("WARNING: No output voltage or load resistance specified!")
        cls.args = args
        cls.cfg = Config('verbose', waitmsg=True, chatty=args.v, spew=args.V)
        cls.smct = SwitchmodeTools(args.f)
        cls.cb = CircuitBuilder(args.A, args.M, args.D, verbose=args.V)

    def __init__(self):
        """
        C{Sim()}

        Each instance of me has its own L{ResultsPlotter} object I{rp}.
        """
        self.fs = self.args.f
        self.ts = self.args.t
        self.tRamp = self.args.p
        self.t_switching = 1.0 / self.fs
        self.rp = ResultsPlotter(
            self.Nc, self.Nr, dims=self.args.d, timeWarp=self.timeWarp)

    @property
    def dutyCycles(self):
        """
        Property: Start and end duty cycle, as floats from 0-1.
        """
        def arg2fraction(k):
            return 0.01*float(self.args[k])

        dc0 = arg2fraction(0) if self.args else 0.2
        dc1 = arg2fraction(1) if len(self.args) > 1 else dc0
        return dc0, dc1

    @property
    def tranArgs(self):
        """
        Property: A list with the arguments to the L{TRAN} instance call
        that follow the reference to an L{NgspiceRunner} instance.
        """
        tmax = self.ts / self.N_ts
        tstep = self.M * tmax
        args = [self.names, tstep, self.t1, self.t0]
        if tmax < tstep:
            args.append(tmax)
        for opt in OPTS:
            args.append((opt, OPTS[opt]))
        return args

    @property
    def vectorsFile(self):
        """
        Property: The name of an C{.npz} file for saving or loading a
        transient analysis with my I{name}.
        """
        return self.name + ".npz"
        
    def tran(self):
        """
        Performs a transient analysis from my time I{t0} to time I{t1}.

        Returns a C{Deferred} that fires with (1) the case temperature
        initialization time to set aside at the beginning of your TRAN
        simulation, and (2) an instance of C{analysis.sim.Vectors}
        populated with the vector I{names} supplied as additional
        arguments.
        """
        args = self.args
        Vin = args.i
        Vout = None if not args.o else args.o
        R_out = None if not args.R else args.R
        dc0, dc1 = self.dutyCycles
        # Build the circuit/netlist. This blocks, but not for very long
        ti, netlist = self.cb.build(
            self.name,
            fs=self.fs, Vin=Vin,
            Vout=Vout, R_out=R_out,
            dc0=dc0, dc1=dc1, tt=self.tRamp,
            ts=self.ts, timeWarp=self.timeWarp)
        if args.L:
            # Instead of running simulation, load a previously saved one
            d = defer.succeed(Vectors_File(self.vectorsFile))
        else:
            # Run the simulation with the netlist (non-blocking!)
            r = NgspiceRunner(self.cfg, timeout=None)
            a = TRAN(r, *self.tranArgs)
            filePath = sub(
                "~/{}.cir", self.name) if self.name and self.args.c else False
            d = a(netlist, study=filePath, overwrite=True)
        d.addCallback(lambda x: (ti, x))
        d.addErrback(oops)
        return d
        
    def setup(self):
        """
        You can implement this in your subclass to do setup stuff before I
        call my I{tran} object.
        """
        
    def plot(self, rp):
        """
        You must implement this in your subclass to plot results.
        """
        raise NotImplementedError("You must define this in your subclass!")
        
    def __call__(self):
        """
        Call an instance of a subclass of me to run a transient
        simulation, plot the results as defined by your L{plot}
        method, and return the (deferred) L{Vectors_Ngspice} object.

        First calls any L{setup} method you have defined in the
        subclass.
        """
        def done(ti_V):
            if self.args.S:
                ti_V[1].save(self.vectorsFile)
            self.rp.setResult(ti_V)
            self.plot(self.rp)
            self.rp.done()
            return self.rp.V

        self.setup()
        return self.tran().addCallbacks(done, oops)


class Startup(Sim):
    """
    I run a startup simulation for a switchmode boost converter.

    @cvar N_cycles: The number of switching cycles to simulate.

    @cvar timeWarp: The thermal timewarp.
    """
    Nc, Nr = 2, 3
    
    timeWarp = 200
    name = "boost-startup"
    names = [
        'inp', 'out',
        'gate', 'drain',
        'amps_c1', 'amps_l', 'amps_c2', 'amps_c3',
        'tj', 'tc',
    ]

    N_cycles = 100

    def setup(self):
        self.t0 = 0
        self.t1 = self.N_cycles*self.t_switching
    
    def plot(self, rp):
        N = min([20, self.N_cycles])
        # Very first simulation samples
        tMax = N*self.t_switching+2*self.ts
        rp.plot_voltages_internal(tMax=tMax)
        rp.plot_currents_internal(tMax=tMax)
        # After a few switching cycles
        tMin = (self.N_cycles-1)*self.t_switching - 2*self.ts
        rp.plot_voltages_internal(tMin)
        rp.plot_currents_internal(tMin)
        # Full-length stuff
        rp.plot_voltages()
        rp.timeWarpInfo()
        rp.plot_temps()


class Switching(Sim):
    """
    I run a warmed-up switching simulation for a switchmode boost
    converter.

    @cvar timeWarp: The thermal timewarp.
    """
    Nc, Nr = 2, 3

    timeWarp = 200
    name = "boost-switching"
    names = [
        'inp', 'out',
        'gate', 'drain',
        'amps_in', 'amps_c1', 'amps_l', 'amps_c2', 'amps_c3', 'amps_out',
    ]

    def setup(self):
        N_ramps = self.args.N
        self.M = max([20, N_ramps])
        totalRampTime = N_ramps * self.tRamp
        self.t0 = N_ramps*self.tRamp + 10.0*self.t_switching
        self.t1 = self.t0 + 5*self.t_switching

    def plot(self, rp):
        sp = rp.sp
        # Voltage
        rp.plot_voltages_internal()
        # Current
        rp.timeWarpInfo()
        #sp.add_textBox("NW", "Annotated with average in & out current")
        #for k, kVector, name in ((0, 4, 'amps_in'), (-1, 5, 'amps_out')):
        #    I_avg = V.avg(name)
        #    sp.add_annotation(k, "{:.2f} A", I_avg, kVector=k, y=True)
        sp.set_zeroLine()
        rp.plot_currents_internal()
        

class RampUp(Sim):
    """
    I run a ramp-up simulation for a switchmode boost converter.

    @cvar timeWarp: The thermal timewarp.
    """
    Nc = 1

    timeWarp = 200
    name = "boost-rampup"
    names = ['duty', 'inp', 'out', 'amps_in', 'amps_out']
    if not NO_IRL:
        names.extend(['pd_il1', 'pd_il2'])

    @property
    def Nr(self):
        """
        Property: The number of rows (and subplots) in the
        C{Figure}. Three if duty cycle is not fixed, otherwise just
        two.
        """
        dc0, dc1 = self.dutyCycles
        return 2 if dc0 == dc1 else 3
        
    def setup(self):
        N_ramps = self.args.N
        self.M = max([20, N_ramps])
        totalRampTime = N_ramps * self.tRamp
        self.t0, self.t1 = [x*totalRampTime for x in (0.1, 1.3)]

    @defer.inlineCallbacks
    def plot(self, rp):
        sp = rp.sp
        # Decimation and outlier clipping
        V = self.V = yield dtt(self.smct.smoothed, self.V)
        V['amps_in'] = clipOutliers(sp, V.amps_in, 3.0, "A", annEnd=True)
        # Ramp-up current
        sp.add_textBox(
            "NW", "Ramping from {:.1f}% to {:.1f}% duty cycle",
            *[np.round(100*x) for x in self.dutyCycles])
        ax = rp.plot_currents_external()
        ax.plot(
            V.time,
            V.duty*np.max(V.amps_in)/self.dutyCycles[1], '--', linewidth=1)
        # Power out vs Dissipated
        rp.plot_power()
        # Efficiency vs. Duty Cycle
        if self.Nr > 2:
            rp.plot_efficiency()


#------------------------------------------------------------------------------

def run(args):
    def done(null):
        Plotter.showAll()
        # All done, stop the reactor and the program exits.
        reactor.stop()

    dList = []
    doAll = args.a
    Sim.setArgs(args)
    if doAll or args.u:
        dList.append(Startup()().addErrback(oops))
    if doAll or args.s:
        dList.append(Switching()().addErrback(oops))
    #if doAll or args.m:
    #    dList.append(Thermal().addErrback(oops))
    return defer.DeferredList(dList).addCallbacks(done, oops)

def main():
    msg(True)
    # Set up things to run under control of Twisted's reactor
    reactor.callWhenRunning(run, args)
    # Start Twisted's reactor and everything goes from there
    reactor.run()

args = Args(
    """
    Switch-mode DC-DC boost converter.

    Starts at duty cycle dc0 (percentage). If dc1 is provided as a
    second argument, ramps up to dc1.

    Simulation step time (-t) is very important. Setting it higher
    than 10 nS (the default) is not recommended.

    CAUTION: Specify either -o or -R unless you want to see what it
    does with no load.

    With -S, -L options, vector object is saved/loaded to/from file in
    local (runtime) directory with name boost-startup.npz,
    boost-switching.npz, etc., depending on the simulation(s)
    done.

    Using the -L option skips the time-consuming simulation process
    and just loads what has been simulated before, unless the
    appropriate file is not found. B{Caution}: No checking is done to
    make sure that the options are the same as when simulation was
    done, so it's possible that annotations to plots may be incorrect. 
    """
)
args('-c', '--cir',
     "Write Ngspice .cir files for each analysis (overwrites existing)")
args('-v', '--verbose', "A bit more chatty")
args('-V', '--very-verbose', "Very chatty, starting with node connections")
args('-u', '--startup', "Include startup simulation (very fast)")
args('-s', '--switching', "Include stabilized switching simulation (slow)")
args('-r', '--rampup', "Include ramp-up simulation (very slow)")
args('-m', '--thermal', "Include thermal warm-up simulation (very slow)")
args('-a', '--all', "Include all simulations (very slow)")
args('-i', '--input-V', 12.0, "Input battery voltage")
args('-o', '--output-V', 0.0, "Output battery voltage")
args('-R', '--output-R', 0.0, "Output load resistance")
args('-p', '--ramp-time', 10E-3, "Ramp time from dc0 to dc1")
args('-N', '--ramps', 8, "Number of dc0-dc1 ramp times for sim to run")
args('-f', '--freq', 25E3, "Switching frequency")
args('-t', '--timestep', 10E-9, "Simulation time step")
args('-M', '--tc-mosfet', 25.0, "MOSFET starting case-ambient temperature")
args('-D', '--tc-diode', 25.0, "Diode starting case-ambient temperature")
args('-A', '--ambient', 25.0, "Ambient temperature")
args('-d', '--plot-dims', "",
     "Plot dims (e.g., '800x600') if not screen size")
args('-S', '--save', "Save vector object(s) to boost-XXX.npz file(s)")
args('-L', '--load', "Load vector object(s) from boost-XXX.npz file(s)")
args("[dc0 [dc1]]: Default 20%%")
args(main)
