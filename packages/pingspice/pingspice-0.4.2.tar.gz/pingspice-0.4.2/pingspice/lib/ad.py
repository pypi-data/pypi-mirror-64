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
Stuff that wants to be like Analog Devices when it grows up.

B{Not endorsed by or in any way connected with Analog Devices, Inc.}
"""

from pingspice.wrappers import Paren
from pingspice.netlist import Subcircuit


class AD8293(Subcircuit):
    """
    Analog Devices instrumentation amplifier AD8293

    @cvar VCC: Positive supply, default 5.0 V.
    @cvar gain: 80x or 160x, default is 80.
    @cvar R1: Differential input I-to-V resistor, 4K.
    @cvar nodes: ['inp', 'inn', 'ref', 'adc_out', 'filt', 'out']
    """
    VCC = 5.0
    # The G80 version. Other option is G160.
    gain = 80 # 160
    # Differential input I-to-V resistor
    R1 = 4000
    # External nodes
    nodes = ['inp', 'inn', 'ref', 'adc_out', 'filt', 'out']
    
    def setup(self, f):
        # Input voltage-to-current conversion
        I_vs_V = 2.0 / self.R1
        f.G('filt', 0, 'inp', 'inn', I_vs_V)
        f.R('filt', 0, 1E6)
        # Differential mode impedance
        f.R('inp', 'inn', 50E6)
        f.C('inp', 'inn', 1E-12)
        # Common mode impedance
        for node in ('inp', 'inn'):
            f.R(node, 0, 10E9)
            f.C(node, 0, 10E-12)
        # Op-amp, clipped to worst-case Voh, Vol limits
        f.E(1, 0, 'ref', 'filt', 100E3)
        rails = f.model(Paren(
            'limit', fraction=False,
            out_lower_limit=0, out_upper_limit=self.VCC,
            limit_range=0.075))
        f.A(1, 'out', rails)
        # Internal resistors
        f.R('out', 'filt', 160E3)
        f.R('out', 'adc_out', 5E3)
        # Reference in
        # Max 1nA @1V
        f.R('ref', 0, 1E9)
