#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.

"""
Tutorial, the beginning: Simplest usage example for the
I{pingspice} package.

Does an AC simulation on a single-stage passive RLC lowpass
filter. Prints the frequencies and dB output levels to the
console. Nothing object oriented yet.

The generated netlist is written to and read from a file.
"""

import numpy as np
from twisted.internet import reactor, defer

from pingspice.circuit.netlist import Netlist
from pingspice.ngspice.runner import NgspiceRunner
from pingspice.util import sub, Config

# For providing some limited info about unhandled Deferred
# failures. You'll be far better off adding errbacks to all your
# deferreds, but we'll get to that later.
from twisted.logger import globalLogPublisher
from twisted.logger._levels import LogLevel
def analyze(event):
    if event.get("log_level") == LogLevel.critical:
        print sub("\nERROR: {}\n", event)
globalLogPublisher.addObserver(analyze)


R = 100     # 100 Ohms
L = 22E-6   # 22 Microhenries
C = 47E-6   # 47 Microfarads

FILEPATH = "rlc-01.cir"

@defer.inlineCallbacks
def run():
    # A configuration object with only defaults
    cfg = Config()
    # Construct an NgspiceRunner, the fundamental object
    r = NgspiceRunner(cfg)
    # Have it source the netlist file that was created before the
    # reactor started
    yield r.source(FILEPATH)
    # Do the AC analysis
    yield r.ac('lin', 11, 1, 101)
    # Get the frequency and output vectors and print them
    F, V3 = yield r.get('frequency', 'V(3)')
    for f, dB in zip(np.abs(F), 20*np.log10(np.abs(V3))):
        print(sub("{:5.1f} Hz: {:+.2f} dB", f, dB))
    # All done, stop the reactor and the program exits.
    reactor.stop()

# Build the netlist
with Netlist(FILEPATH)() as f:
    f.V(1, 0, 'DC', 1, 'AC', 1)
    f.R(1, 2, R)
    f.L(2, 3, L)
    f.C(3, 0, C)
# Set up things to run under control of Twisted's reactor
reactor.callWhenRunning(run)
# Start Twisted's reactor and everything goes from there
reactor.run()

        



