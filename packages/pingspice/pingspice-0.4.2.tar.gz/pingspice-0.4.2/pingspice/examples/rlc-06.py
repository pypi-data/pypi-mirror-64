#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.

"""
Tutorial, Part 6: RLC lowpass filter, fourth order. With a
Pythonic circuit set up and realistic component values.
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


RLC_SPECS = """
# Points per decade of AC sweep
N_AC    = 10
# Max AC sweep frequency
fMax    = 1000
# Max TRAN time
tMax    = 0.3
# Load resistance
R_load = 11.2E3
"""

RLC_GOALS = """
# Frequency Response
ID = 11
frequency       dB
-------------------------------------------------------------
1               -14
5               -14
100             -35


# Step Response
ID = 21
time            rlc_out
-------------------------------------------------------------
75E-3           0.20
100E-3          0.20
125E-3          0.20
150E-3          0.20
200E-3          0.20
250E-3          0.20
"""


class RLC_Setups(param.Setups):
    """
    This is identical to RLC_Setups in rlc-04.py except that there is
    now a constraint.
    """
    specs = RLC_SPECS
    goals = RLC_GOALS
    
    nameLists = {
        # AC Sweep
        11:['frequency', 'dB'],
        # TRAN step response
        21:['time', 'rlc_out'],
    }

    plotSpecs = {
        11:("Frequency Response", 'frequency', 'dB'),
        21:("Step Response", 'time', 'rlc_out'),
    }

    def analyzers(self, s):
        x = {}
        x[11] = [AC, 'dec', s.N_AC, 1, s.fMax]
        x[21] = [TRAN, s.tMax/1000, s.tMax]
        return x

    independents = {
        11:['frequency'],
        21:['time'],
    }

    def weights(self, s):
        def weight_frequency(ID, f):
            return 1.0 if f < 10 else 0.1
        def weight_time(ID, t):
            return 100*(20*t)**2
        w = {}
        w['frequency'] = weight_frequency
        w['time'] = weight_time
        return w
    
    def transforms(self, s):
        def dB(ID, inputValue, outputValue):
            outputValue = np.clip(outputValue, 1E-12, None)
            return 20*np.log10(np.real(np.abs(outputValue/inputValue)))
        return {'dB': [dB, 'rlc_in', 'rlc_out']}


class RLC_Finder(param.ParameterFinder):
    """
    This RLC_Finder builds up stages in a more Pythonic manner,
    allowing you to decide filter order (within reason). Also
    constrains L, C values to commonly available values.
    """
    Setups = RLC_Setups

    N_stages = 3
    commonMantissas = [
        0.1, 0.12, 0.15, 0.18, 0.22, 0.27, 0.33, 0.39, 0.47, 0.56, 0.68, 0.82]
    
    def setup(self, f):
        def aname(prefix, kk=None):
            if kk is None:
                return sub("{}{:d}", prefix, k)
            return sub("{}{:d}_{:d}", prefix, k, kk)

        def expList(x, y):
            return np.logspace(x, y, y-x+1)
        
        for k in range(self.N_stages):
            # Nodes for this stage
            n0 = 'rlc_in' if k == 0 else 2*k
            n1 = 2*k+1
            n2 = 'rlc_out' if k == self.N_stages-1 else 2*k+2
            # Resistance
            f.R(n0, n1, f.av(aname("R"), 10, 100E3))
            # Inductance (100 nH - 100 uH)
            Lm = f.av(aname("Lm"), self.commonMantissas)
            Le = f.av(aname("Le"), expList(-6, -4))
            f.L(n1, n2, Lm*Le)
            # Capacitance (100 pF - 10 uF)
            Cm = f.av(aname("Cm"), self.commonMantissas)
            Ce = f.av(aname("Ce"), expList(-9, -5))
            f.C(n1, 0, Cm*Ce)

    def setupTestCircuit(self, f, ID):
        if ID == 11:
            f.V('rlc_in', 0, 'DC', 1, 'AC', 1)
        else:
            f.V('rlc_in', 0, 'DC', 1, Paren('PULSE', 0, 1, 0, 2E-3))
        f.R('rlc_out', 0, self.R_load)
            

class RLC(Subcircuit):
    """
    I represent a more complex RLC circuit using commonly available
    inductor and capacitor values.
    """
    Finder = RLC_Finder
    nodes = ['rlc_in', 'rlc_out']


from pingspice.scripts import paramfind
paramfind.args.s = True
paramfind.args.v = True
paramfind.main(RLC_Finder)

        



