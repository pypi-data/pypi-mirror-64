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
Semiconductor packages and heatsinks.
"""

from pingspice.circuit.netlist import Subcircuit
from pingspice.analysis.thermal import Package_Setups, Package_Finder, Heatsink


class TO220_Setups(Package_Setups):
    """
    Setups for TO220.

    I{rth_ca} and I{cth_c} from On/Fairchild App Note AN-7516, Table 3.
    """
    specs = "TO220.specs"
    goals = "TO220.goals"

class TO220_Finder(Package_Finder):
    Setups = TO220_Setups


class TO220F_Setups(Package_Setups):
    """
    Setups for TO220F.

    I{rth_ca} and I{cth_c} for TO220 from On/Fairchild App Note
    AN-7516, Table 3. Assuming I{rth_ca} is the same for TO220F, based
    on FQPF32N20C/FQP32N20C datasheet citing the same junction-ambient
    thermal resistance. However, plastic package is clearly going to
    have less I{cth_c}; guesstimated.
    """
    specs = "TO220F.specs"
    goals = "TO220F.goals"

class TO220F_Finder(Package_Finder):
    Setups = TO220F_Setups

    
class TO247_Setups(Package_Setups):
    """
    Setups for TO247.

    I{rth_ca} and I{cth_c} from On/Fairchild App Note AN-7516, Table 3.
    """
    specs = "TO247.specs"
    goals = "TO247.goals"

class TO247_Finder(Package_Finder):
    Setups = TO247_Setups


class Package(Subcircuit):
    """
    Base class for all packages.
    """
    heatsink = None

    @property
    def nodes(self):
        nodeList = ['tj', 'tc', 'ta']
        if getattr(self, 'tca0', None) is None:
            nodeList.append('tca0')
        return nodeList


class TO220(Package):
    Finder = TO220_Finder
    finderParams = {
        # Finder = pingspice.lib.thermal.TO220_Finder
        # SSE = 0.6 after 11421 evaluations
        # Commit following #2e53fad8, 2020-02-04
        'r0': 0.000943157,
        'r1': 0.00233872,
        'r2': 0.00451352,
        'r3': 0.0121583,
        'r4': 0.0495757,
        'r5': 0.117001,
        'r6': 0.240832,
        'r7': 0.232638,
        'rc0': 7.28304e-08,
        'rc1': 2.36293e-07,
        'rc2': 6.48294e-06,
        'rc3': 0.000122674,
        'rc4': 0.00128113,
        'rc5': 0.00590619,
        'rc6': 0.0801029,
        'rc7': 0.322834,
    }

class TO220F(Package):
    Finder = TO220F_Finder
    finderParams = {
        # Finder = pingspice.lib.thermal.TO220F_Finder
        # SSE = 0.3 after 36188 evaluations
        # Commit following #2e53fad8, 2020-02-04
        'r0': 0.00474246,
        'r1': 0.00977687,
        'r2': 0.0276389,
        'r3': 0.0803195,
        'r4': 0.26769,
        'r5': 0.812942,
        'r6': 0.840893,
        'r7': 0.46607,
        'rc0': 1.56291e-07,
        'rc1': 1.64548e-06,
        'rc2': 1.17913e-05,
        'rc3': 7.65891e-05,
        'rc4': 0.000697949,
        'rc5': 0.0111051,
        'rc6': 0.0627305,
        'rc7': 0.403229,
    }

class TO247(Package):
    Finder = TO247_Finder
    finderParams = {
        # Finder = pingspice.lib.thermal.TO247_Finder
        # SSE = 0.6 after 24271 evaluations
        # Commit following #2e53fad8, 2020-02-04
        'r0': 0.00015499,
        'r1': 0.000476674,
        'r2': 0.00263443,
        'r3': 0.0103457,
        'r4': 0.0419523,
        'r5': 0.0741154,
        'r6': 0.374733,
        'r7': 0.15561,
        'rc0': 3.46816e-08,
        'rc1': 9.12158e-08,
        'rc2': 4.23619e-07,
        'rc3': 2.80446e-05,
        'rc4': 0.000299413,
        'rc5': 0.00310954,
        'rc6': 0.0547089,
        'rc7': 0.325556,
    }

class DO201(Package):
    """
    A DO-201 (Axial case 267) diode package. Rth with short leads
    soldered to PCB with small copper area available, from On
    Semiconductor datasheet for MUR420.

    This package model (naively) assumes no thermal capacitance or
    junction-case resistance.
    """
    def setup(self, f):
        f.R('tj', 'tc', 0)
        f.R('tc', 'ta', 51.0)

    
class WV_T247(Heatsink):
    """
    Ohmite WV-T247-101E, a small clip-on aluminum heatsink for the TO247
    package.
    """
    rth = 12.0
    mass = 12.0
