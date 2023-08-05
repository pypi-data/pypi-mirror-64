#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.

"""
Simple Op Amp example: A differential amplifier with some lowpass filtering.
"""

import numpy as np
from twisted.internet import reactor, defer

from yampex.plot import Plotter

from pingspice.wrappers import Paren, Array
from pingspice.netlist import Netlist
from pingspice.ngspice import NgspiceRunner
from pingspice.analysis.sim import AC, DC, TRAN
from pingspice.lib import mcp
from pingspice.util import sub, oops, msg


class Circuit(object):
    """
    I represent a differential amplifier circuit. My L{make} method
    defines it, using the baton (an instance of C{elements.Elements})
    that gets passed from a context call to a C{netlist.Netlist}
    instance.
    """
    filePath = "opamp-01.cir"

    Rs = 10E3
    Cp = 1E-6
    Rf = 100E3
    
    def __init__(self):
        with Netlist(self.filePath)() as f:
            self.make(f)

    def make(self, f):
        # Inputs
        f.Vcm('cm', 0, 'DC', 0, 'AC', 0, Paren('PULSE', -2, 0, 2E-5, 3E-5))
        f.Vdm('dm_p', 'dm_n', 'DC', 0, 'AC', 1, Paren('AM', 0.2, 0, 19E3, 400E3))
        f.R('dm_p', 0, 1E6)
        f.R('dm_n', 0, 1E6)
        offset = f.MODEL('offset', 'summer')
        f.A(Array(None, 'dm_p', 'cm'), 'pos_in', offset)
        f.A(Array(None, 'dm_n', 'cm'), 'neg_in', offset)
        # The circuit
        f.R('pos_in', 1, 1.001*self.Rs)
        f.R('neg_in', 2, 0.999*self.Rs)
        f.C(1, 2,  self.Cp)
        f.R(1, 10, 0.9996*self.Rf)
        f.R(2, 'out',  1.0003*self.Rf)
        opAmp = mcp.OpAmp(f)
        opAmp(1, 2, 'out')
        f.R(10, 12, 10)
        f.V(12, 0, 0.5*opAmp.vcc)
        f.R('out', 0, 1E3)


class Runner(object):
    def __init__(self):
        self.ckt = Circuit()

    @property
    def r(self):
        return NgspiceRunner(verbose=True, debug=True)

    @defer.inlineCallbacks
    def _run(self):
        # Analyzers
        analyzers = [
            DC(self.r, ['pos_in', 'neg_in', 'cm', 'out'],
               'Vdm', -0.5, +0.5, 0.005, 'Vcm', -1.5, +6, 0.5),
            TRAN(self.r, ['pos_in', 'neg_in', 'out'], 5E-9, 1E-4),
        ]
        dList = [x(self.ckt.filePath).addErrback(oops) for x in analyzers]
        Vs = yield defer.gatherResults(dList)
        # Plot results
        p = Plotter(2, width=11, height=12)
        p.set_grid()
        with p as sp:
            # DC
            V = Vs[0]
            sp.add_marker('.')
            sp(V.pos_in - V.neg_in, V.out+V.cm, markersize=1)
            # TRAN
            V = Vs[1]
            sp.set_timex()
            sp(V.time, V.pos_in, V.neg_in, V.out)
        p.show()
        # All done, stop the reactor and the program exits.
        reactor.stop()

    def run(self):
        return self._run().addErrback(oops)


msg(True)
# Set up things to run under control of Twisted's reactor
reactor.callWhenRunning(Runner().run)
# Start Twisted's reactor and everything goes from there
reactor.run()

        



