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
A base class for power semiconductor subcircuits, which have
almost nonexistent built-in model support in Ngspice.
"""

import numpy as np
from copy import copy

from pingspice.util import *
from pingspice.circuit.netlist import Include, Subcircuit
from pingspice.lib import thermal


class SemiconductorError(Exception):
    def __init__(self, proto, *args):
        Exception.__init__(self, sub(proto, *args))


class PowerSemiconductor(Subcircuit):
    """
    I am a base class for a self-heating power semiconductor
    subcircuit. My junction temperature node 'tj' starts at ambient
    temperature unless I{steadyState} is C{True}.

    You can scale down all thermal capacitances in my package and
    heatsink by setting the pingspice-only simulation option
    I{timeWarp} > 1 where stuff heats up x times faster. You should
    keep I{timeWarp} consistent for all thermal subcircuits in a given
    simulation, and it's preferred to set this option (as with all
    pingspice-only simulation options) via a L{Netlist} constructor
    keyword.

    The sole subcircuit param is I{ambient}, the ambient temperature
    of the air surrounding the package. Default: 25 deg C.

    You must define my I{nodes} list in your subclass. It must end
    with the temperature nodes 'tc', 'tj', and 'tca0', representing my
    die and case temperatures and an input node 'tca0' that specifies
    an initial case-ambient temperature. The 'tca0' node is a
    high-impedance input that floats to zero, so if you'll never want
    the case to start out with a higher temperature than ambient, just
    leave it disconnected.

    The other items must match the nodes expected by the I{Die}
    subclass you specify.

    So, unless you specify an initial case-ambient temperature
    difference with attribute I{tca0}, your nodes list pattern must
    match the following::

        [<Die, without 'tj'>] + ['tj', 'tc', 'tca0']

    For the semiconductor device models provide by pingspice, the
    patterns are as follows::

        ['drain', 'gate', 'source', 'pdiss', 'tj', 'tc', 'tca0']
        ['anode', 'cathode', 'pdiss', 'tj', 'tc', 'tca0']

    @cvar Die: The subclass of L{analysis.mosfet.MOSFET} that models
        your device's semiconductor die. (Technically not just a die
        since it also models lead impedances. But not package thermal
        behavior.)

    @cvar package: The name (not FQN) of the package subcircuit in
        L{lib.thermal}, a subclass of L{lib.thermal.Package}.
    @type package: str

    @ivar heatsink: A 2-sequence (or callable that returns a
        2-sequence) containing values for I{rth_ca} and I{cth_c} of a
        heatsink attached to my package.
    
    @ivar rth_ca: Thermal resistance, case (package) to
        ambient. Should only be defined if I{heatsink} is not.
    
    @ivar cth_c: Thermal capacitance of case (package). Should only be
        defined if I{heatsink} is not.

    @ivar tca0: Set this to an initial case-ambient temperature
        difference. I will set up an extra node internally with that
        "voltage" for its thermal capacitance to be fast-charged to so
        you don't have to supply the node. (If I{tca0} is set to
        something, supplying the 'tca0' node will raise an exception.)
    
    @ivar ignoreL: Set this C{True} to ignore lead
        inductance. Inductors cause convergence errors in SPICE
        because they create ringing that needs to be tracked by the
        stepwise simulation, often at much higher frequencies than
        you're really interested in. That's been mitigated by the use
        of simulation-friendly inductors, though, so you probably
        won't need to set this.
    """
    Die = None
    package = None
    heatsink = None
    rth_ca = None; cth_c = None; tca0 = None;
    ignoreL = False
    params = {'ambient':25.0}
    nodes = None
    ti = None

    def checkNodes(self, nodes):
        """
        Raises an exception if the supplied list of I{nodes} isn't
        appropriate.
        """
        has_pdiss = False
        while nodes:
            node = nodes.pop(0)
            if node == 'pdiss':
                has_pdiss = True
                continue
            if node != 'tj':
                continue
            if self.tca0 is not None and len(nodes) > 2:
                raise SemiconductorError(
                    "You specified tca0 as an attribute but also\n"+\
                    "provided {:d} nodes", len(nodes))
            if nodes != ['tc', 'tca0']:
                raise SemiconductorError(
                    "Error with subclass '{}'\nnodes '{}':\n'tj' must be "+\
                    "followed by 'tc' and 'tca0'", self.__class__, self.nodes)
        if not has_pdiss:
            raise SemiconductorError("Your nodes list must include 'pdiss'")

    def setup(self, f):
        if self.Die is None:
            raise NotImplementedError(
                "You must define your Die subclass in a subclass of me")
        if self.package is None:
            raise NotImplementedError(
                "You must define the name of a Package subclass")
        if self.nodes is None:
            raise NotImplementedError(
                "You must define your nodes list in a subclass of me")
        nodes = list(self.nodes)
        self.checkNodes(nodes)
        if self.tca0 is not None:
            f.V('tca0', 0, self.tca0)
            nodes.append('tca0')
        if getattr(self, 'finderParams', None):
            self.Die.finderParams = self.finderParams
        # The semiconductor die, connected to all nodes except tc and tca0
        self.Die(f, ignoreL=self.ignoreL)(*self.nodes[:-2])
        # The package, connected to tj, tc, and tca0
        kw = {}
        for name in ('heatsink', 'rth_ca', 'cth_c'):
            value = getattr(self, name, None)
            if value: kw[name] = value
        PackageClass = getattr(thermal, self.package)
        pkg = PackageClass(f, **kw)
        pkg('tj', 'tc', 'ta', 'tca0')
        self.ti = pkg.setupResults['ti']
        # Power dissipated -> "current" through thermal network. Note
        # that you will need some thermal capacitance connected
        # directly to tj to avoid convergence problems.
        f.G(0, 'tj', 'pdiss', 0, 1000.0)
        # This very high value resistance across the current output
        # avoids some convergence problems and doesn't affect
        # simulation accuracy
        f.R(0, 'tj', 1e6) # SCA
        # Terminate the package with ambient temperature
        f.V('ta', 0, "{ambient}")
        f.R('ta', 0, 1) # SCA
        return {'ti': self.ti}


class PowerSemiconductorInclude(Include):
    """
    An L{Include} version of L{PowerSemiconductor} for use in a
    parameter-finding test fixture.

    @cvar package: The name (not FQN) of the package subcircuit in
        L{lib.thermal}, a subclass of L{lib.thermal.Package}.
    @type package: str

    @ivar ambient: The ambient temperature in degrees C. If left
        C{None} (the default), you must provide the ambient
        temperature as a voltage on node 'ta'.

    @ivar heatsink: A 2-sequence (or callable that returns a
        2-sequence) containing values for I{rth_ca} and I{cth_c} of my
        package with a heatsink attached.
    """
    ambient = None
    heatsink = None

    def setup(self, f, tj, pdiss):
        packageClass = getattr(thermal, self.package)
        pkgSubcircuit = packageClass(f, heatsink=self.heatsink)
        pkgSubcircuit(tj, 'tc', 'ta', 'tca0')
        # Power dissipated -> "current" through thermal network. Note
        # that you will need some thermal capacitance connected
        # directly to tj to avoid convergence problems.
        f.G(0, tj, pdiss, 0, 1.0)
        # If ambient temperature is defined, terminate the package
        # with a voltage defining it
        if self.ambient is not None:
            f.V('ta', 0, self.ambient)
            f.R('ta', 0, 1) # SCA
