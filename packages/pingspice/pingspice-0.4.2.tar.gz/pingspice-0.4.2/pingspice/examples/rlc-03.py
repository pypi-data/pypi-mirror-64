#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.
#
# See (lack of) warranty in header to other source files.

"""
Tutorial, Part 3

Does AC and TRAN simulations on a single-stage passive RLC lowpass
filter, in parallel using two separate Ngspice processes. Includes
errbacks, following good asynchronous programming practice. Uses a
I{nameList} to get both 'src' and 'load' vectors from the analyses.
"""

from cStringIO import StringIO

import numpy as np
from twisted.internet import reactor, defer

from yampex.plot import Plotter

from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Netlist
from pingspice.ngspice.runner import NgspiceRunner
from pingspice.analysis.sim import AC, TRAN
from pingspice.util import sub, oops, msg, Config


class RLC(object):
    """
    I represent an RLC circuit, with a load resistance and a voltage
    source that also has transient behavior.
    """
    R = 100     # 100 Ohms
    L = 22E-6   # 22 Microhenries
    C = 47E-6   # 47 Microfarads
    R_load = 1E3

    # This name list will be provided to each Analysis object to
    # indicate which simulation vectors should be fetched from Ngspice
    # and loaded into an analysis.sim.Vectors object.
    nameList = ['src', 'load']
    
    def __init__(self):
        # This time, we are letting the Netlist object write to
        # itself. We will get the netlist text from it by coercing it
        # to a string.
        self.n = Netlist(None, "RCL-03")
        with self.n() as f:
            self.make(f)

    def make(self, f):
        # Now we also have a transient voltage as well, defined with
        # help from a wrappers.Paren convenience object
        f.V('src', 0, 'DC', 1, 'AC', 1, Paren('PULSE', 0, 1, 0, 2E-3))
        f.R('src', 1, self.R)
        f.L(1, 'load', self.L)
        f.C('load', 0, self.C)
        # There's now also an output load resistance
        f.R('load', 0, self.R_load)


class Runner(object):
    """
    I run an Ngspice Analysis, constructing a netlist and
    NgspiceRunner.

    @cvar details: Set C{True} to see what happens on STDIO between
        Python and Ngspice.
    """
    fMax = 1000
    tMax = 0.1
    details = True

    def __init__(self):
        # The msg function lets you have messages go to the console or
        # a log file.
        msg(True)
        self.ckt = RLC()
        self.p = Plotter(2, width=8, height=6)
        self.p.use_grid()
        # The config may have one of its options set.
        self.cfg = Config(spew=self.details)

    def plot_AC(self, sp, V):
        """
        Does an AC subplot of the circuit's frequency response.
        """
        def annotate(freq):
            k = np.searchsorted(F, freq)
            sp.add_annotation(k, "{:.1f} Hz: {:+.1f} dB", F[k], dB[k])

        sp.plot_semilogx()
        sp.set_xlabel("Hz")
        sp.set_ylabel("dB")
        F = np.abs(V.frequency)
        dB = 20*np.log10(np.real(np.abs(V.load/V.src)))
        for freq in (10, 40, 80):
            annotate(freq)
        sp.set_title("Frequency Response")
        sp(F, dB)

    def plot_TRAN(self, sp, V):
        """
        Does a time-domain subplot of the circuit's transient response to
        a step input. Places an annotation on the output ('load') node
        voltage at one total system time constant.
        """
        Y = V.load
        k = np.searchsorted(Y, Y[-1]/np.sqrt(2))
        sp.add_axvline(k)
        sp.add_annotation(k, "Time Constant", kVector=0)
        sp.use_timex()
        sp.set_title("Step Response")
        sp(V.time, V.load, V.src)
        
    @defer.inlineCallbacks
    def _run(self):
        dList = []
        for klass, args in (
                (AC, ['lin', 1000, 1, self.fMax]),
                (TRAN, [self.tMax/1000, self.tMax])):
            r = NgspiceRunner(self.cfg)
            d = klass(r, self.ckt.nameList, *args)(str(self.ckt.n))
            d.addErrback(oops)
            dList.append(d)
        # Wait (in a non-blocking manner) for the results of both analyses
        Vs = yield defer.gatherResults(dList)
        # Plot the results
        with self.p as sp:
            self.plot_AC(sp, Vs[0])
            self.plot_TRAN(sp, Vs[1])
        self.p.show()
        reactor.stop()

    def run(self):
        """
        Runs an AC analysis and a transient analysis in a non-blocking
        asynchronous manner and using two separate Ngspice processes
        running in parallel.

        Does a subplot of each result and exits when the plot is
        closed.

        This is all accomplished by calling my L{_run} method, with an
        error callback added to the resulting C{Deferred} object. This
        is good Twisted programming practice to deal with the
        inevitable errors that occurr during program development.
        """
        return self._run().addErrback(oops)


# Set up things to run under control of Twisted's reactor
reactor.callWhenRunning(Runner().run)
# Start Twisted's reactor and everything goes from there
reactor.run()

        



