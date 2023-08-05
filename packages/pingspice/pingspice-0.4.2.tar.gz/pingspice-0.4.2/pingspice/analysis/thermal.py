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
A semiconductor package thermally modeled with a Cauer network
having evolved parameters.
"""

import time, os.path, re

import numpy as np

from pingspice.util import *
from pingspice.circuit.av import AV
from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import Subcircuit
from pingspice.analysis.sim import TRAN
from pingspice.analysis import psim, param, constraints
from pingspice.analysis.capacitance import Capacitance


def N_range(s):
    """
    Returns a range with N iterations starting at zero, where N is the
    supplied spec object's I{N} attribute.
    """
    return range(int(s.N))


class SeriesResistanceAnalyzer(psim.Analyzer):
    """
    I analyze total series resistance in the Cauer thermal network.

    @see: L{func}.
    """
    weight = 1E5
    
    def __init__(self, s):
        """
        C{SeriesResistanceAnalyzer(s)}
        """
        self.s = s

    def rName(self, k):
        return "r" + str(k)
        
    def avDefine(self, f):
        for k in N_range(self.s):
            f.av(self.rName(k))

    def func(self, **kw):
        """
        Returns the weighted sum of squared error between (1) total series
        resistance of the Cauer network and (2) my spec's thermal
        resistance from junction to case I{rth_jc}.
        """
        R_total = 0
        for k in N_range(self.s):
            R_total += kw[self.rName(k)]
        return self.weight * (R_total - self.s.rth_jc)**2


class Constraints(constraints.Constraints):
    """
    I provide a simple constraint checker to make sure that each
    successive time constant in the Cauer network is increasing, thus
    avoiding overlap in the search space.
    """
    def __init__(self, N):
        """
        C{Constraints(N)}
        """
        self.N = int(N)
        self.registry = {
            'rc_increasing': [
                set(),                          # Linear
                None,                           # Log
            ],
        }
        rc_list = self.registry['rc_increasing'][0]
        for k in range(self.N):
            rc_list.add(self.rc(k))
        super(Constraints, self).__init__()

    def rc(self, k):
        return sub("rc{}", k)
            
    def rc_increasing(self, params):
        """
        Returns C{False} (and quits checking) if any RC is smaller than
        its predecessor in the Cauer network.
        """
        for k in range(1, self.N):
            if params[self.rc(k-1)] > params[self.rc(k)]:
                return False
        return True

    
class Package_Setups(param.Setups):
    """
    Setups for L{Package_Finder}.
    """
    weights = {'tj': 1E4}
    logValues = {'tj'}
    
    def setup(self, s):
        ID = 101
        tIntervals = [(5E-7, 1E-4), (1E-4, 0.01), (1E-3, 0.9)]
        self.plotSpecs = {ID:("Series Resistance",)}
        self.analyzers = {ID:[SeriesResistanceAnalyzer(s)]}
        self.nameLists = {ID:[]}
        self.independents = {ID:[]}
        for tMin, tMax in tIntervals:
            ID += 100
            title = sub("Tj vs time, {:g} - {:g} seconds", tMin, tMax)
            self.plotSpecs[ID] = (title, 'time', 'tj')
            self.analyzers[ID] = [TRAN, tMin, tMax, tMin]
            self.nameLists[ID] = ['time', 'tj']
            self.independents[ID] = ['time']

    def constraints(self, s):
        return Constraints(s.N)


class Package_Finder(param.ParameterFinder):
    """
    Finder for semiconductor packages, using a Cauer RC network to
    model thermal impedance::

                                         :
        tj ----+-- R1 ---+--- R2 ---+--- : ----+--- Rn ----+
               |         |          |    :     |           | 
            +----+    +----+     +----+  :  +----+         | 
            | C1 |    | C2 |     | C2 |  :  | Cn |         |
            +----+    +----+     +----+  :  +----+         | 
               |         |          |    :     |           | 
        tc ----+---------+----------+----:-----+------+----+-------+
                                         :            |            |
                                         :        +-------+    +--------+
        tca0 ------------------------------------x| cth_c |    | rth_ca | 
                                         :        +-------+    +--------+
                 #==========+            :            |            |
                 # timeWarp #            :            +------------+----- ta
                 # fiti     #
                 # ts       #
                 #==========#
    
    The Cauer RC network terminates in a first-order parallel RC for
    case-to-ambient heat dissipation with an R of I{rth_ca} and a C of
    I{cth_c}. If you have a heatsink, you can replace the package's
    defaults with its I{rth_ca} and I{cth_c}. In the unlikely event
    you connect another thermal network to the 'tc' node, set
    I{rth_ca} to something huge and I{cth_c} to zero.

    Implements the pingspice-only simulation option I{fiti}: Initial
    time allocated for fast initial temperature increase, for
    irregular but simulation-friendly initial warm-up. C{None} for no
    irregular warm-up. If set C{True} or to a value less than 100x
    I{ts}, will be forced to 100x I{ts}. B{Note:} I{timeWarp}, if any,
    still applies.

    You can set an initial case-ambient temperature differential with
    the input node 'tca0'.

    Pingspice-only simulation options used: I{ts}, I{timeWarp}, and
    I{fiti}.

    The time you should set aside for my initial and/or fast
    "charging" to desired case-ambient differential at the beginning
    of your TRAN simulation appears as the 'ti' entry of my
    I{setupResults}.

    
    Heatsinking
    ===========

        At the end of my L{setup} method, I check my I{heatsink}
        attribute to see if it was set to a callable. If so, it must
        return a 2-sequence with values for I{rth_ca} and I{cth_c}
        that override the class-wide defaults. If not, and it is a
        2-sequence, I will use that directly. If I{heatsink} is
        C{None} (the default), no heatsink is assumed to be attached.

        Set this with a L{Subcircuit} constructor keyword to "attach"
        a heatsink to a particular device and replace the package's
        I{rth_ca} and I{cth_c} with a heatsink's I{rth_ca} that is
        much lower and a I{cth_c} that is much higher.

        Remember, though: You don't set Python-instance attributes
        with keywords when calling the instance; those keywords are
        only for subcircuit parameters, which only Ngspice
        references. You'll need a separate Python instance for each
        device with a different I{heatsink} configuration, even if the
        devices use the same L{Subcircuit} subclass.

        Construct an instance of L{Heatsink} or a subclass of it for a
        callable object suitable for this.

    B{Note}: I have no class-wide defaults defined for instance
    variables I{heatsink}, I{rth_ca}, I{cth_c}, and I{tca0} because my
    custom L{ParameterFinder.__getattr__} needs to not find one or it
    won't go look for it in a package subcircuit. The default values
    for non-heatsinked packages are defined in each package's
    C{.specs} file, e.g., C{lib/TO247.specs}.

    @ivar heatsink: A 2-sequence (or callable that returns a
        2-sequence) containing values for I{rth_ca} and I{cth_c}.
    
    @ivar rth_ca: Thermal resistance, case (package) to
        ambient. Should only be defined if I{heatsink} is not.
    
    @ivar cth_c: Thermal capacitance of case (package). Should only be
        defined if I{heatsink} is not.
    
    @ivar tca0: Set to an initial case-ambient temperature difference
        to have me use XSPICE capacitance model with that as the
        initial voltage for my case/heatsink's thermal capacitance
        instead of constructing an internal 'tca0' node with a
        fast-charge initial voltage. Simpler, but may cause
        convergence problems.
    """
    def setup(self, f):
        """
        RC pairs of Cauer network, with time constants roughly a
        decade apart starting at around 0.1-10 microseconds.
        """
        N = int(self.s.N)
        scale_R = self.s.scale_R
        scale_RC = self.s.scale_RC
        R_nom = self.s.rth_jc * scale_R**(1-N)
        RC_nom = self.s.RC0
        R_nomPrev = 0.001*R_nom
        RC_nomPrev = 0.01*RC_nom
        ts = f.get(self, 'ts')
        if ts:
            # This only affects param finding, not runtime usage
            if ts > RC_nomPrev/scale_RC:
                # Must increase "previous" RC_nom so that lower end of
                # first (smallest) RC range is no smaller than ts
                RC_nomPrev = ts*scale_RC
                # Set upper end of first RC range to be like it had
                # been increased as usual from a fictitious previous
                # range
                RC_nom = RC_nomPrev*scale_RC
        timeWarp = f.get(self, 'timeWarp')
        fivi = f.get(self, 'fiti')
        for k in range(N):
            n0 = 'tj' if k == 0 else k
            n1 = 'tc' if k == N-1 else k+1
            Rname, RCname = [sub("{}{}", x, k) for x in ("r", "rc")]
            # Some overlap between resistance and time constant ranges
            Rk = f.av(Rname, R_nomPrev/scale_R, R_nom*scale_R)
            # The Rs all have to add up to 1.0, so there will be much
            # constraint-rejecting before any challenger gets to
            # simulate its parameters
            f.R(n0, n1, Rk)
            # The thermal inertia capacitance for each stage precedes
            # its resistance. Thus there will be some capacitance
            # right at the junction, smoothing tj from having
            # simulation-unfriendly nanosecond-range spikes.
            RCk = f.av(RCname, RC_nomPrev/scale_RC, RC_nom*scale_RC)
            kw = {}
            # The initial junction-case temp difference should
            # always be zero.
            Capacitance(
                f, n0, 'tc',
                C=(RCk/Rk).inf(0), V0=0,
                tcon=RCk, timeWarp=timeWarp, fivi=fivi)
            # The remainder of the loop only has effect during
            # parameter finding
            R_nomPrev = R_nom
            R_nom *= self.s.scale_R
            RC_nomPrev = RC_nom
            RC_nom *= scale_RC
        # Replace package's thermal resistance and capacitance with
        # that of a heatsink if one is attached. TODO: Add the
        # heatsink's capacitance to the package's, possibly also
        # parallel its resistance with the package's.
        heatsink = getattr(self, 'heatsink', None)
        if type(heatsink) == type:
            if issubclass(heatsink, Heatsink):
                heatsink = heatsink()
            else:
                raise TypeError(
                    "To specify 'heatsink' as a class, it must be a "+\
                    "subclass of lib.thermal.Heatsink.")
        if callable(heatsink): heatsink = heatsink()
        if heatsink: self.rth_ca, self.cth_c = heatsink
        f.R('tc', 'ta', self.rth_ca)
        nodes = ['tc', 'ta']
        kw = {
            'C': self.cth_c,
            'tcon': self.rth_ca*self.cth_c,
            'timeWarp': timeWarp,
            'fivi': fivi,
        }
        tca0 = getattr(self, 'tca0', None)
        if tca0 is None:
            nodes.append('tca0')
            # Node 'tca0' floats at zero with very high
            # impedance. Without input, the initial case-ambient temp
            # difference is zero.
            f.R('tca0', 0, 1e9)
        else: kw['V0'] = tca0
        cc = Capacitance(f, *nodes, **kw)
        return {'ti': cc.ti}
    
    def setupTestCircuit(self, f, ID):
        # Unit power as 1A current
        tRise = 1E-6
        # We short out the case's thermal network for test setups and
        # assume initial case and ambient temps of zero C.
        f.R('tc', 'ta', 0)
        f.V('ta', 0, 0)
        # Current is scaled to make limit(t->inf): tj = 1.0
        I = 1.0 / self.s.rth_jc
        f.Ip(0, 'tj', I, Paren('PULSE', 0, I, 0, tRise))


class Heatsink(object):
    """
    An aluminum heatsink. Default values are for 

    Subclass with a different value of I{rth_hs} and I{M} for a
    different heatsink.

    See L{Package_Finder} for usage info.

    @cvar rth: Thermal resistance, deg C/W (no default)
    @cvar material: Heatsink material (default: Al)
    @cvar mass: Heatsink grams (no default)
    """
    rth = None
    material = 'Al'
    mass = None

    def __call__(self):
        if self.rth is None:
            raise NotImplementedError(
                "Your subclass must define thermal resistance 'rth'")
        if self.material is None:
            raise NotImplementedError(
                "Your subclass must define heatsink 'material'")
        if self.mass is None:
            raise NotImplementedError(
                "Your subclass must define heatsink 'mass'")
        if self.material.lower().startswith('al'):
            specific_heat = 0.902
        else:
            raise ValueError(sub(
                "Unrecognized heatsink material '{}'", self.material))
        return self.rth, specific_heat*self.mass


