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
Diodes, including power diodes with evolved parameters.

These aim to fill a huge void in Ngspice and open-source circuit
simulation generally. There's been almost nothing freely available for
modeling power semiconductors.

See the source at
U{pingspice.analysis.diode<edsuom.com/pingspice/pingspice.analysis.diode.py>}
to appreciate how much effort went into trying to accurately simulate
the complexity of self-heating power diode behavior. There is modeling
of voltage-dependent junction capacitance, forward and reverse
biasing, reverse recovery, and lead impedance.

And self-heating! The model estimates power dissipation and, in
conjunction with a Cauer thermal network for the package and any
attached heatsink, applies that to estimate junction and case
temperature over time.

Of course, it bears repeating from the license terms: I{pingspice} is
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied. And B{none of these models is
endorsed or in any way connected with} the manufacturer of the devices
whose behavior they are attempting to simulate.

@see: L{pingspice.analysis.diode}.
"""

from pingspice.circuit import netlist
from pingspice.circuit.wrappers import Paren
from pingspice.circuit.netlist import RawInclude, Subcircuit
from pingspice.lib.semiconductor import PowerSemiconductor
from pingspice.analysis.diode import *


class PowerDiode(PowerSemiconductor):
    """
    Base class for power diode subcircuits.

    @cvar Die: The subclass of L{analysis.diode.Diode} that models
        your device's semiconductor die. Technically, it's not just a
        die since it also models lead impedances, and diodes are
        usually just big junctions. But the point is that it doesn't
        include package thermal behavior.

    @cvar package: The name (not FQN) of the package subcircuit in
        L{lib.thermal}, a subclass of L{lib.thermal.Package}.
    @type package: str

    @ivar heatsink: A 2-sequence (or callable that returns a
        2-sequence) containing values for I{rth_ca} and I{cth_c} of my
        package with a heatsink attached.
    
    @ivar rth_ca: Thermal resistance, case (package) to
        ambient. Should only be defined if I{heatsink} is not.
    
    @ivar cth_c: Thermal capacitance of case (package). Should only be
        defined if I{heatsink} is not.
    
    @see: L{PowerSemiconductor} for an explanation of the subcircuit
        param B{ambient} and the use of nodes 'tc' and 'tca0'.
    """
    nodes = ['anode', 'cathode', 'pdiss', 'tj', 'tc', 'tca0']


class _DO201_Diode(PowerDiode):
    """
    Subcircuit for a diode with the DO201 package.

    No heatsink attaches to this package, so I have no I{rth_hs} or
    I{cth_hs} attribute.
    """
    package = "DO201"

class _TO220_Diode(PowerDiode):
    """Subcircuit for a diode with TO-220 package."""
    package = "TO220"


#--- MBR40250 -----------------------------------------------------------------
    
class _MBR40250_Setups(Diode_Setups):
    specs = "MBR40250.specs"
    goals = "MBR40250.goals"

class MBR40250_Finder(Diode_Finder):
    """
    Parameter finder for the MBR40250 power diode.
    
    To try to find better parameters than what's currently in
    L{MBR40250_Die}, call this with::

        pf [options] pingspice.lib.diodes.MBR40250_Finder
    """
    Setups = _MBR40250_Setups
    package = "TO220"

class MBR40250_Die(Diode):
    """
    The semiconductor die for the L{MBR40250} without any package.
    """
    Finder = MBR40250_Finder
    finderParams = {
        # Finder = pingspice.lib.diodes.MBR40250_Finder
        # SSE = 121.9 after 41338 evaluations
        # Commit following #4ea27fce, 2020-01-27
        'Rp': 19.536,
        'T_chl': -2.01061,
        'cp': -13.9099,
        'd_cjo': 6.93232e-10,
        'd_ikr': -10.045,
        'd_is': -3.0217,
        'd_m': 0.459211,
        'd_n': 0.483935,
        'd_rs': -2.84907,
        'd_tt': -9.28358,
        'd_vj': 0.607592,
        'if_hca': -16.8184,
        'if_hcb': -4.77063,
        'l': 9.97664e-09,
        'vf_lca': -2.72242,
    }

class MBR40250(_TO220_Diode):
    """
    B{MBR40250}: 250 V, 40 A switch-mode Schottky power rectifier,
    TO220 package.

    Fairchild/ON Semiconductor.
    """
    Die = MBR40250_Die


#--- MUR420 -------------------------------------------------------------------

class _MUR420_Setups(Diode_Setups):
    specs = "MUR420.specs"
    goals = "MUR420.goals"

class MUR420_Finder(Diode_Finder):
    """
    Parameter finder for the MUR420 power diode.
    
    To try to find better parameters than what's currently in
    L{MUR420_Die}, call this with::

        pf [options] pingspice.lib.diodes.MUR420_Finder
    """
    Setups = _MUR420_Setups

class MUR420_Die(Diode):
    Finder = MUR420_Finder
    finderParams = {
        # Finder = pingspice.lib.diodes.MUR420_Finder
        # SSE = 173.8 after 17745 evaluations
        # Commit #f4f24c6a, 2020-01-24
        'Rp': 10.5751,
        'T_chl': -5.1685,
        'cp': -10.9266,
        'd_cjo': 1.76957e-10,
        'd_ikr': -11.167,
        'd_is': -5.58346,
        'd_m': 0.411885,
        'd_n': 0.350188,
        'd_rs': -2.36733,
        'd_tt': -7.72936,
        'd_vj': 0.158565,
        'if_hca': -15.5414,
        'if_hcb': -4.63562,
        'l': 2.69348e-09,
        'vf_lca': -2.95575,
    }
    
class MUR420(_DO201_Diode):
    """
    On Semiconductor ultrafast rectifier, 200V, 4.0 A.
    """
    Die = MUR420_Die


#--- D1N5240 ------------------------------------------------------------------

class D1N5240(Subcircuit):
    """
    1N5240 10V Zener. No self-heating is modeled for this device.
    """
    nodes = ['anode', 'cathode']

    def setup(self, f):
        f.C('anode', 'cathode', 40E-12)
        model = f.MODEL(
            '1N5240', 'zener',
            v_breakdown=10.0, i_breakdown=20E-3, r_breakdown=17, i_rev=3E-6)
        f.A('anode', 'cathode', model)
