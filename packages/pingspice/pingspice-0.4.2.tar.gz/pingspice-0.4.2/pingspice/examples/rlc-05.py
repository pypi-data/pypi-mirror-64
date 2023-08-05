#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.

"""
Tutorial, Part 5
"""

from cStringIO import StringIO

import numpy as np
from twisted.internet import reactor, defer

from yampex.plot import Plotter

from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Netlist, Subcircuit
from pingspice.ngspice import NgspiceRunner
from pingspice.analysis.sim import AC, TRAN
from pingspice.analysis import param
from pingspice.util import sub, oops


class RLC_Finder(param.ParameterFinder):
    """
    I am a trimmed-down version of the C{RLC_Finder} from
    C{rlc-04.py}, Part 4 of the RLC Tutorial. The stuff required for
    parameter finding is omitted for clarity in this example
    file. However, as it does no harm to leave in, you would almost
    always to just put your subcircuit below a fully functional
    subclass of L{param.ParameterFinder} in the same module as you
    used to do the parameter finding.
    """
    def setup(self, f):
        # Stage #1
        f.R('rlc_in', 1, f.av("R1", 1E3, 100E3))
        f.L(1, 2, f.av("L1", 1E-6, 100E-6))
        f.C(2, 0, f.av("C1", 100E-9, 100E-6))
        # Stage #2
        f.R(2, 3, f.av("R2", 1E3, 100E3))
        f.L(3, 'rlc_out', f.av("L2", 100E-9, 10E-6))
        f.C('rlc_out', 0, f.av("C2", 10E-9, 10E-6))
            

class RLC(Subcircuit):
    """
    I represent a subcircuit with values found by ADE with L{RLC_Finder}.
    """
    Finder = RLC_Finder
    nodes = ['rlc_in', 'rlc_out']
    finderParams = {
        # Finder = __main__.RLC_Finder
        # SSE = 2.6 after 1653 evaluations
        'C1': 7.76878e-06,
        'C2': 1.84552e-08,
        'L1': 2.86834e-05,
        'L2': 7.00176e-06,
        'R1': 2082.89,
        'R2': 41347.4,
    }


class Circuit(object):
    """
    I represent a simple circuit using the L{RLC} subcircuit with
    known parameters.
    """
    nameList = ['src', 'load']

    def __init__(self):
        fh = StringIO()
        with Netlist(fh, "RCL-05")() as f:
            f.V('src', 0, 'DC', 1, 'AC', 1, Paren('PULSE', 0, 1, 0, 2E-3))
            # This next line is how you use the RLC subcircuit. Note
            # that the f baton is passed to the subcircuit
            # constructor.
            RLC(f)('src', 'load')
            f.R('load', 0, 11.2E3)
        self.netlist = fh.getvalue()
        fh.close()


class Runner(object):
    fMax = 1000
    tMax = 0.1

    def __init__(self):
        self.ckt = Circuit()
        self.p = Plotter(2, width=10, height=8)
        self.p.set_grid()

    def plot_AC(self, sp, V):
        def annotate(f):
            k = np.searchsorted(F, f)
            sp.add_annotation(k, "{:.1f} Hz: {:+.1f} dB", F[k], dB[k])

        sp.set_semilogx()
        sp.set_xlabel("Hz")
        sp.set_ylabel("dB")
        F = V.frequency
        dB = 20*np.log10(np.real(np.abs(V.load/V.src)))
        for f in (1, 5, 100):
            annotate(f)
        sp(F, dB)

    def plot_TRAN(self, sp, V):
        sp.set_timex()
        sp.set_zeroLine(0.2)
        sp(V.time, V.load)
        
    @defer.inlineCallbacks
    def _run(self):
        dList = []
        for klass, args in (
                (AC, ['lin', 1000, 1, self.fMax]),
                (TRAN, [self.tMax/1000, self.tMax])):
            r = NgspiceRunner()
            d = klass(r, self.ckt.nameList, *args)(self.ckt.netlist)
            d.addErrback(oops)
            dList.append(d)
        Vs = yield defer.gatherResults(dList)
        with self.p as sp:
            self.plot_AC(sp, Vs[0])
            self.plot_TRAN(sp, Vs[1])
        self.p.show()
        reactor.stop()

    def run(self):
        return self._run().addErrback(oops)


reactor.callWhenRunning(Runner().run)
reactor.run()
