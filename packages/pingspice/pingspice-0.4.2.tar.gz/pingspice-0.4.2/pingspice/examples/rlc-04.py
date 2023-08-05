#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.

"""
Tutorial, Part 4
"""

import numpy as np

from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Netlist
from pingspice.analysis.sim import AC, TRAN
from pingspice.analysis import param
from pingspice.util import sub

from twisted.logger import globalLogPublisher
from twisted.logger._levels import LogLevel
def analyze(event):
    if event.get("log_level") == LogLevel.critical:
        print sub("\nERROR: {}\n", event)
globalLogPublisher.addObserver(analyze)


RLC_SPECS = """
# Points per decade of AC sweep
N_AC    = 10
# Max AC sweep frequency
fMax    = 100
# Max TRAN time
tMax    = 0.3
# Load resistance
R_load = 11.2E3
"""

RLC_GOALS = """
# Frequency Response
ID = 11
freq            dB
-------------------------------------------------------------
1               -14
5               -14
100             -30

# Step Response
ID = 21
time            rlc_out
-------------------------------------------------------------
100E-3          0.20
150E-3          0.20
200E-3          0.20
250E-3          0.20
"""


class RLC_Setups(param.Setups):
    specs = RLC_SPECS
    goals = RLC_GOALS
    
    nameLists = {
        # AC Sweep
        11:['freq', 'dB'],
        # TRAN step response
        21:['time', 'rlc_out'],
    }

    plotSpecs = {
        11:("Frequency Response", 'freq', 'dB'),
        21:("Step Response", 'time', 'rlc_out'),
    }

    def analyzers(self, s):
        x = {}
        x[11] = [AC, 'dec', s.N_AC, 1, s.fMax]
        x[21] = [TRAN, s.tMax/1000, s.tMax]
        return x

    independents = {
        11:['freq'],
        21:['time'],
    }

    weights = {
        'dB':           100.0,
        'rlc_out':      2e6,
    }
    
    def transforms(self, s):
        def dB(ID, inputValue, outputValue):
            """
            Transforms I{inputValue} vs I{outputValue} into gain, in dB.
            """
            outputValue = np.clip(outputValue, 1E-12, None)
            result = np.abs(outputValue)/(np.abs(inputValue) + 1e-9)
            result = 20*np.log10(result)
            return result
        def freq(ID, frequency):
            """
            Transforms complex frequency from AC analysis into real by just
            discarding the imaginary (phase) part.
            """
            return np.real(frequency)
        # Assign the two functions above as transforms
        return {
            'freq': [freq, 'frequency'],
            'dB': [dB, 'rlc_in', 'rlc_out'],
        }


class RLC_Finder(param.ParameterFinder):
    Setups = RLC_Setups

    def setup(self, f):
        # Stage #1
        f.R('rlc_in', 1, f.av('R1', 20000, 50000))
        f.L(1, 2, f.av('L1', 1e-7, 1e-5))
        f.C(2, 0, f.av('C1', 500e-9, 3e-6))
        # Stage #2
        f.R(2, 3, f.av('R2', 2000, 20000))
        f.L(3, 'rlc_out', f.av('L2', 1e-8, 3e-6))
        f.C('rlc_out', 0, f.av('C2', 1e-11, 1e-7))

    def setupTestCircuit(self, f, ID):
        if ID == 11:
            f.V('rlc_in', 0, 'DC', 1, 'AC', 1)
        else: f.V('rlc_in', 0, 'DC', 1, Paren('PULSE', 0, 1, 0, 2E-3))
        f.R('rlc_out', 0, self.R_load)
            

from pingspice.scripts import paramfind
# Write to STDOUT instead of logfile
paramfind.args.s = True
# Verbose output, with some Ngspice warnings and failures
paramfind.args.v = True
# Midway between DE/best/1 and DE/rand/1
paramfind.args.r = 0.5
# Set size of plotfile at ~/pfinder.png
paramfind.args.g = "1200x1200"
# Go!
paramfind.main(RLC_Finder)

        



