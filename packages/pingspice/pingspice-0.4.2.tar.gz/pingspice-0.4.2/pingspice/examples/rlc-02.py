#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.

"""
Tutorial, Part 2

Does two AC simulations on a single-stage passive RLC lowpass filter
using an object-oriented approach. The generated netlist is written to
a string instead of a file and re-used for each AC analysis.
"""

from cStringIO import StringIO

import numpy as np
from twisted.internet import reactor, defer

from yampex.plot import Plotter

from pingspice.circuit.netlist import Netlist
from pingspice.ngspice.runner import NgspiceRunner
from pingspice.analysis.sim import AC
from pingspice.util import sub, Config

from twisted.logger import globalLogPublisher
from twisted.logger._levels import LogLevel
def analyze(event):
    if event.get("log_level") == LogLevel.critical:
        print sub("\nERROR: {}\n", event)
globalLogPublisher.addObserver(analyze)


class RLC(object):
    """
    I represent an RLC circuit. My L{make} method defines it, using
    the baton (an instance of C{elements.Elements}) that gets passed
    from a context call to a C{netlist.Netlist} instance.
    """
    R = 100     # 100 Ohms
    L = 22E-6   # 22 Microhenries
    C = 47E-6   # 47 Microfarads

    def __init__(self):
        # This time, we are using a file-like string object instead of
        # a file for the netlist
        fh = StringIO()
        with Netlist(fh, "RCL-02")() as f:
            self.make(f)
        self.netlist = fh.getvalue()
        fh.close()

    def make(self, f):
        f.V(1, 0, 'DC', 1, 'AC', 1)
        f.R(1, 2, self.R)
        f.L(2, 3, self.L)
        f.C(3, 0, self.C)


class Runner(object):
    """
    I run an Ngspice Analysis, constructing a netlist and
    Plotter. My L{run} method does an analysis and plots the
    results.
    """
    fMax = (101, 10E3)

    def __init__(self):
        self.netlist = RLC().netlist
        self.p = Plotter(len(self.fMax), width=8, height=5)
        self.p.use_grid()
        self.p.plot_semilogx()
        self.p.set_xlabel("Hz")
        self.p.set_ylabel("dB")

    def plot(self, sp, V):
        """
        Does an AC plot of the circuit's frequency response, over two
        frequency ranges. Places annotations at harmonics of 10 Hz.
        """
        def annotate(freq):
            k = np.searchsorted(F, freq)
            sp.add_annotation(k, "{:.1f} Hz: {:+.1f} dB", F[k], dB[k])

        # The vectors 'frequency' and 'V(3)' are accessed as
        # attributes of an analysis.sim.Vectors object.
        F = np.abs(V.frequency)
        dB = 20*np.log10(np.real(np.abs(V.V3)))
        for freq in (10, 40, 80):
            annotate(freq)
        sp(F, dB)

    @defer.inlineCallbacks
    def run(self):
        """
        Runs two AC analyses in a non-blocking asynchronous manner, doing
        a subplot of each result. Exits when the plot is closed.
        """
        cfg = Config()
        with self.p as sp:
            # An AC analysis and subplot for each fMax
            for fMax in self.fMax:
                # An NgspiceRunner and instance of analysis.sim.AC is
                # constructed for each frequency range and called with
                # the circuit's netlist text. We yield the resulting
                # Twisted Deferred object to wait for it in a
                # non-blocking manner, and eventually obtain an
                # analysis.sim.Vectors object.
                r = NgspiceRunner(cfg)
                V = yield AC(r, ['V3'], 'lin', 1000, 1, fMax)(self.netlist)
                self.plot(sp, V)
        self.p.show()
        reactor.stop()


# Set up things to run under control of Twisted's reactor
reactor.callWhenRunning(Runner().run)
# Start Twisted's reactor and everything goes from there
reactor.run()

        



