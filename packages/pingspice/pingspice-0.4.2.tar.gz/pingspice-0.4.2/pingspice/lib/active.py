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
Some active building blocks.
"""

import os.path, shutil

import numpy as np
from scipy import signal, interpolate

from pingspice.circuit.av import AV
from pingspice.circuit.wrappers import Paren, Array, TABLE
from pingspice.circuit.netlist import Subcircuit
from pingspice.analysis.expressions import Expressionist
from pingspice.util import *


class PWM(Subcircuit):
    """
    PWM square wave oscillator with duty cycle controlled by an input
    ranging from 0-1, where 1 is 100% duty cycle.

    The nodes are:

        1. 'ctrl' - An inmput with voltage from 0 to 1, controlling
           the duty cycle.

        2. 'outp' - Positive output.

        3. 'outn' - Negative output (need not be tied to ground).
    
    @ivar Vhigh: The high output voltage.
    @ivar Vlow: The low output voltage.
    
    @ivar fs: The frequency (Hz).

    @ivar tt: The transition time from I{Vlow} to I{Vhigh} and vice
        versa.

    @ivar tRiseFall: Set to a rise/fall time in seconds to limit
        output slew rate for realism or convergence.

    @ivar t0: An optional delay (seconds) from TRAN start before the
        start of the pulse train.
    """
    Vhigh = 1.0
    Vlow = 0.0
    fs = 100E3
    # Default output rise/fall time
    tt = 0.005 / fs
    # Optional additional slew rate limiting
    tRiseFall = None
    # Optional delay
    t0 = 0

    nodes = ['ctrl', 'outp', 'outn']

    def setup_oscillator(self, f, ts, n1):
        """
        Constructs a triangle-wave oscillator with my frequency I{fs} and
        a ground-referenced output at n1.

        Returns the rise/fall time, which is a little bit less than
        half the period, owing to non-zero pulse width.
        """
        tp = 1.0 / self.fs
        # Ngspice chokes on pulse width exactly zero. Apparently, it
        # can't be too small.
        trf = 0.5*tp - ts
        f.V(n1, 0, 'DC', 0, Paren('PULSE', -0.5, +0.5,
        #     +------------------------------- Delay time
        #     |      +------------------------ Rise time
        #     |      |     +------------------ Fall time
        #     |      |     |     +------------ Pulse width (=ts)
        #     |      |     |     |        +--- Period
        #     |      |     |     |        |
        self.t0,   trf,  trf,   ts,      tp))
        return trf

    def setup_ctrl_atanh(self, f, a, b, n1, n2):
        """
        Constructs a TABLE E-source that implements the following
        function, which Ngspice seems to have trouble calculating
        consistently for some stupid reason::

            V(n2) = a*atanh(b*(V(n1)-0.5))

        The output voltage appears at node I{n2}. The voltage at input
        node I{n1} must be between 0 and 1. Both nodes are
        ground-referenced.
        """
        N = 20
        X = np.linspace(0, 1, N)
        Y = a*np.arctanh(b*(X-0.5))
        f.E(n2, 0, TABLE(n1, X, Y))
    
    def setup_comparator(self, f, ts, slopeGain, n1, n2, n3):
        """
        Constructs a smooth-edged comparator intended for use with a
        triangle wave on input I{n1} and a (relatively) constant
        voltage between 0 and 1 on input I{n2}.

        Specify the output rise/fall time by supplying a multiple of
        the triangle wave slope vs the output signal slope,
        I{slopeGain}.

        Input nodes I{n1} and I{n2} and output node I{n3} are all
        ground-referenced.

        The zero-state output voltage is set by my I{Vlow} attribute,
        and the one-state voltage by my I{Vhigh} attribute.
        """
        m = 0.5 * (self.Vhigh - self.Vlow)
        b = self.Vlow + m
        aGain = np.pi/2
        # V = b + m*tanh(tGain*({-0.5..+0.5} + ...
        #     ... aGain*atanh((1/aGain-2/tGain)*(ctrl-0.5))))
        ex = Expressionist()
        ex.ap("V({})", n1)
        n2b = self.iNode(n2)
        self.setup_ctrl_atanh(f, aGain, 1.0/aGain-2.0/slopeGain, n2, n2b)
        ex.ap("V({})", n2b)
        expr = ex.ep("+", paren=True, new=True)
        ex.ap("{:g}", slopeGain)
        ex.ep("*", paren="tanh", new=True)
        ex.ap("{:g}", m, joinWith="*", new=True)
        expr = ex.ap("{:g}", b, joinWith="+")
        f.B(n3, 0, V=expr)
    
    def setup(self, f):
        """
        Defines the subcircuit netlist for a PWM oscillator with
        simulation-friendly transitions from I{Vlow} to I{Vhigh} and
        back again.

        This is the output voltage expression, where C{X} is a
        triangle wave from -0.5 to +0.5 and C{ctrl} is an input node
        whose value can range from 0 (0% duty cycle) to 1.0 (100%):

        M{V = b + m*tanh(tGain*(X + aGain*atanh((1/aGain-2/tGain)*(ctrl-0.5))))}
        """
        ts = f.get(self, 'ts')
        trf = self.setup_oscillator(f, ts, 'tri')
        # Transition time can't be less than ts
        tt = self.tt if self.tt > ts else ts
        slopeGain = 3*trf/tt
        self.setup_comparator(f, ts, slopeGain, 'tri', 'ctrl', 10)
        if self.tRiseFall: tt = self.tRiseFall
        slope = (self.Vhigh - self.Vlow) / tt
        model = f.MODEL('slew', rise_slope=slope, fall_slope=slope)
        f.A(10, '%vd', 'outp', 'outn', model)


class FileSource(Subcircuit):
    """
    File source providing piecewise-linear source voltage values
    vs. time.

    Make your source waveform as complicated as you wish!
    
    @ivar t: A Numpy vector of increasing simulation time points.

    @ivar X: A Numpy vector with the same length as I{t} of source
        voltages.

    @ivar filePath: The full path of a file to be (over)written with
        I{t} and I{X} data. Any home directory symbol ("~") will be
        expanded. If C{None} (the default), a new, unique temporary
        file path will be used.
    
    @ivar keep: Set C{True} to keep the file after Python shuts
        down. The default is to automatically delete it, but you may
        want to keep it for study.

    @ivar gain: A scalar for amplifying the signal (default is 1.0).
    """
    filePath = None
    keep = False
    gain = 1.0

    nodes = ['a', 'b']
    
    def writeData(self, filePath, t, X):
        """
        Opens a new tempfile for writing and for Ngspice to read during
        this Python session. (Gets deleted when Python shuts down.)
        """
        if t.shape != X.shape:
            print "Shape mismatch between t, X. Fix it!"
            import pdb; pdb.set_trace()
        with open(filePath, 'w') as fh:
            for k, tk in enumerate(t):
                fh.write(sub("{:g} {:g}\n", tk, X[k]))
    
    def setup(self, f):
        keep = f.get(self, 'keep')
        if self.filePath is None:
            filePath = tempfile(".dat", keep=keep)
            self.writeData(filePath, self.t, self.X)
        else:
            # Ngspice seems too stupid to follow a lengthy file path,
            # so copy to home directory
            filePath = os.path.expanduser(
                "~/" + os.path.split(self.filePath)[-1])
            tempfile(filePath, register=not keep)
            shutil.copy(self.filePath, filePath)
        filesrc = f.MODEL(
            'filesrc', 'filesource',
            amploffset=[0], amplscale=[1], FILE=sub('\"{}\"', filePath))
        f.A("%vd([1 0])", filesrc)
        f.R(1, 2, 1.0)
        ts = f.get(self, 'ts')
        if ts: f.C(2, 0, ts)
        f.E('a', 'b', 2, 0, self.gain)
    

class Capacitance_Meter(Subcircuit):
    """
    Capacitance meter using a DC bias that ramps up and a sinusoidal
    signal source, with current sensing on return leg.

    Use this to measure capacitance of an active circuit, e.g., MOSFET
    ciss, coss, and crss.

    Construct and use only via the L{mc_addedBias} or
    L{mc_separateBias} class method.
    
    The subcircuit has six external subcircuit nodes:

        - I{npos}: The positive node at which AC (and possibly also DC
          bias) current emerges to the device under test.

        - I{nneg}: The negative node for return of the test current.

        - I{bias}: A positive node for DC bias output, ground
          referenced.

        - I{cap}: Output with voltage representing the calculated
          capacitance in Farads.

        - I{filt_in}: Input of an RC lowpass filter with the same
          S-response as the one used in the RMS current
          calculation. In most cases, you will short this to I{bias}.

        - I{filt_out}: Output of the RC lowpass filter. Use
          observations of this for the independent vector in
          dynamically measured capacitance setups.

        - I{xl}: Input with voltage representing the series inductance
          in Henries. Makes capacitance calculation more accurate if
          series inductance is at least partially known.

    @keyword fa: The AC signal frequency.
    @type fa: float
    
    @keyword Na: Number of AC signal cycles in the bias sweep.
    @type Na: int

    @keyword Nd: Number of AC signal cycles to delay before starting
        the bias sweep.
    @type Nd: int
    
    @keyword Vac: The AC signal voltage (peak-to-peak).
    @type Vac: float
    
    @keyword Vdc: A 2-sequence with (1) the starting and (2) ending DC
        bias voltage.

    @keyword bias_add: Set C{True} to have the DC bias voltage added
        to the AC signal at I{npos}. It will appear by itself, with no
        AC component, at the I{bias} terminal regardless. Default:
        C{False}.
    @type bias_add: bool

    @keyword Ls: If at least some of the series inductance is known,
        set this to it to make the capacitance calculation more
        accurate. AV compatible. Default: 0 Henries.

    @keyword invert_bias: Set C{True} to invert the voltage applied as
        bias, for P-channel MOSFETs. The I{bias} output remains
        positive.
    @type invert_bias: bool
    """
    nodes = [
        'npos', 'nneg',
        'bias', 'cap', 'filt_in', 'filt_out', 'xl']

    Cb = 0.1e-6
    Rb = 1000
    lpf_model = None

    bias_add = False
    invert_bias = False

    NS = np.array([
        [2,       0.99316],
        [3,       0.99314],
        [4,       0.99311],
        [5,       0.99306],
        [6,       0.99313],
        [7,       0.99309],
        [8,       0.99315],
        [9,       0.99312],
        [10,      0.99314],
        [12,      0.99312],
        [15,      0.99315],
        [18,      0.99305],
        [20,      0.99300],
        [25,      0.99257],
        [30,      0.99271],
        [35,      0.99316],
        [40,      0.99387],
        [45,      0.99468],
        [50,      0.99536],
        [60,      0.99651],
        [80,      0.99794],
        [100,     0.99868],
        [200,     0.99967],
        [300,     0.99985]])
    
    @classmethod
    def correct(cls, Ns):
        """
        Returns an approximate correction factor to account for high
        capacitance readings due to imperfect sampling of the AC test
        signal.

        Call with the number of Ngspice time steps per AC test signal cycle.
        """
        if not hasattr(cls, '_NS_interp'):
            cls._NS_interp = interpolate.interp1d(
                cls.NS[:,0], cls.NS[:,1],
                kind='linear', copy=False, assume_sorted=True)
        return cls._NS_interp(Ns)
    
    @classmethod
    def _xl(cls, f, kw):
        """
        Called by L{mc_addedBias} and L{mc_separateBias} to make voltage
        source I{cmv_xl}.
        """
        def v(n, value):
            if isinstance(value, AV):
                f.vav(n, value)
            else:
                f.V(n, 0, value)
                f.R(n, 0, 1)
                
        XL = kw.pop('Ls', 0) * 2*np.pi*kw['fa']
        v('cmv_xl', XL)
    
    @classmethod
    def mc_addedBias(cls, f, npos, nneg, bias, cap, **kw):
        """
        Makes an instance of me with bias added to the AC test signal and
        sent through the matching filter, and connects it to the
        specified nodes.

        Supply the circuit generation tool I{f} as the first argument,
        followed by the nodes I{npos}, I{nneg}, I{bias} (output,
        filtered) and I{cap} (output).

        Makes a voltage source I{cmv_xl} external to the subcircuit,
        with DC voltages based on the keyword I{Ls}. AV compatible.

        Only call this once per circuit.

        @keyword invert_bias: Set C{True} to invert voltage applied as
            bias, for P-channel MOSFETs. The I{bias} output remains
            positive.
        @type invert_bias: bool
        """
        cls._xl(f, kw)
        kw['bias_add'] = True
        cm = cls(f, **kw)
        cm(npos, nneg, 'bias', cap, 'bias', bias, 'cmv_xl')

    @classmethod
    def mc_separateBias(cls, f, npos, nneg, bias_out, cap, bias_m, bias, **kw):
        """
        Makes an instance of me with a separate bias output (also sent
        through the matching filter) and connects it to the specified 
        nodes.

        Supply the circuit generation tool I{f} as the first argument,
        followed by the nodes I{npos}, I{nneg}, I{bias_out} (output,
        non-filtered), I{bias_m} (measurement point, filter input),
        I{bias} (output, filtered), and I{cap} (output).

        Makes a voltage source I{cmv_xl} external to the subcircuit,
        with DC voltages based on the keyword I{Ls}. AV compatible.

        Only call this once per circuit.

        @keyword invert_bias: Set C{True} to invert voltage of
            I{bias_out}, for P-channel MOSFETs. The I{bias} output
            remains positive.
        @type invert_bias: bool
        """
        cls._xl(f, kw)
        kw['bias_add'] = False
        cm = cls(f, **kw)
        cm(npos, nneg, bias_out, cap, bias_m, bias, 'cmv_xl')
        
    def sources(self, f):
        if self.bias_add:
            nan = ndp = 'bias'
        else:
            nan = 0; ndp = 10
            f.Vshb(10, 'bias', 0)
            f.R('bias', 0, 1e20) # SCA
        f.Vac('npos', nan, DC=0, SIN=[0, self.Vac, self.fa])
        tStart = float(self.Nd) / self.fa
        tRamp = self.Na / self.fa
        Vdc = self.Vdc
        if self.invert_bias: Vdc = [-x for x in Vdc]
        f.Vdc(ndp, 0, DC=0, PULSE=[
            #   V1      V2      TD     TR     N/A       PW
            Vdc[0], Vdc[1], tStart, tRamp, tStart, 2*tRamp])
    
    def lpf(self, f, nin, nout):
        """
        Makes a lowpass filter following the cosine product and for the
        matched copy between I{filt_in} and I{filt_out}.

        The filter is Chebychev II. Its frequency response is
        monotonic in the passband and equiripple in the stopband,
        which begins at half the frequency of the AC test signal.
        """
        if self.lpf_model is None:
            # Filter order (Ngspice slows WAY down with higher order!)
            N = 2
            # Minimum Stopband attenuation (dB)
            dB_stop = 35
            # "For Type II filters, [f_stop] is the point in the
            # transition band at which the gain first reaches [dBa]."
            f_stop = 0.5*self.fa
            b, a = signal.cheby2(
                N, dB_stop, 2*np.pi*f_stop,
                btype='lowpass', output='ba', analog=True)
            self.lpf_model = f.MODEL(
                'lpf', 's_xfer',
                num_coeff=Array(None, b),
                den_coeff=Array(None, a),
                int_ic=Array(None, np.zeros_like(a)))
        f.A(nin, nout, self.lpf_model)

    def v_x(self, f, wa):
        """
        Makes a voltage source I{v_x} with the calculated reactance
        (90-degree current flow vs voltage), based on current through
        zero-voltage source I{Vsh}.

        If the bias is separate, its current is subtracted from what
        goes through I{Vsh}, improving accuracy.
        
        Internal nodes:

            - I{v_sc}: Behavioral voltage soruce for the current
              multiplied by (mixed with) a 90-degree phase-shifted
              version (cosine) of the AC test signal.

            - I{v_scf}: Lowpass filtered version of I{v_sc},
              substantially rejecting frequency components C{fa}
              (non-subtracted DC bias current after mixing) and
              C{2*fa} (the sum component of AC current with cosine
              "local oscillator").

        Called by, and only by, L{v_capacitance}.
        """
        expr_current = "i(vsh)" if self.bias_add else "(i(vsh)-i(vshb))"
        f.ve('v_sc', "{}*cos({:g}*time)", expr_current, wa)
        self.lpf(f, 'v_sc', 'v_scf')
        Vrms = self.Vac / np.sqrt(2)
        denom = Vrms
        f.ve('v_x', "{:g}/(V(v_scf) + 1e-30)", Vrms/np.sqrt(2))
        
    def v_capacitance(self, f):
        """
        Makes a voltage source I{cap} with calculated capacitance, based
        on squared impedance indicated at node I{z2} and known series
        resistance and inductance.
        """
        wa = 2*np.pi*self.fa
        self.v_x(f, wa)
        f.ve('cap', "1.0 / ({:g}*(V(xl)+V(v_x)))", wa)
    
    def setup(self, f):
        self.sources(f)
        f.Vsh('nneg', 0, 0)
        self.v_capacitance(f)
        if self.invert_bias:
            f.E('filt_out', 0, 20, 0, -1)
            self.lpf(f, 'filt_in', 20)
        else: self.lpf(f, 'filt_in', 'filt_out')
