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
Stuff that wants to be like MicroChip when it grows up.

B{Not endorsed by or in any way connected with Microchip Technology, Inc.}
"""

import math

from pingspice.wrappers import Paren
from pingspice.netlist import Subcircuit


class OpAmp(Subcircuit):
    """
    Behaviorally modeled op amp sort of like the MCP6281.

    I attempt to model op-amp behavior with offset voltage, bias
    current (opposite and equal amounts for each input), common and
    differential mode input resistance and capacitance, a large but
    finite DC open-loop gain, gain-bandwith product, and output slew
    rate. Also has a second 1/RC pole that implements a 45-degree
    phase margin frequency.

    My internal voltages never go within I{hr0} volts of I{vcc} and
    ground. I have a low but finite output impedance that increases
    that headroom with higher output source or sink current.

    My default attributes are aimed at matching the Microchip
    MCP6281. Subclass me with your own attributes, or set different
    ones with constructor keywords, for a different op amp.
    """
    vcc =    5.0   # Supply voltage
    voff = +1.2e-3 # input offset voltage
    ioff = +1e-12  # input offset current
    ib =   2e-12   # input bias current (worst case: opposite for inp, inn)
                     
    rdm =  10e13   # input resistance, differential mode
    cdm =  3e-12   # input capacitance, differential mode
    rcm =  10e13   # input resistance, common mode
    cdm =  3e-12   # input resistance, common mode
                   
    gdb =    110   # db open-loop gain at dc
    gbp =    5e6   # gain-bandwidth product (hz)
    p45 =   12E6   # 45-degree phase margin frequency
                   
    hr0 =  0.012   # Output voltage headroom from +/- rail
    rout =  19.4   # Est. from output headroom reduction w/ higher current
    sr =   2.5E6   # Output slew rate, V/sec

    nodes = ['inp', 'inn', 'out']

    @staticmethod
    def capValueUnity(R, f0, gDC):
        """
        Returns the capacitance value for a single RC pole with I{R} when
        unity gain is at I{f}, with DC gain of I{gDC}.
        """
        # F(f) = gDC / (1 + f*R*C)
        # F(f0) = 1
        # gDC = 1 + f0*R*C
        # f0*R*C = gDC - 1
        # f0*C = (gDC - 1) / R
        return (gDC - 1) / (R*f0)
    
    @staticmethod
    def capValue45deg(R, f):
        """
        Returns the capacitance value for a single RC pole with I{R} when
        there is a 45 degree phase shift at I{f}.
        """
        # atan(45deg) = 2*pi*f*R*C
        # C = 1.0/(2*pi*f*R)
        return 1.0 / (2*math.pi*f*R)
    
    def setup(self, f):
        # ESD diodes
        esd = f.model('esd', 'D', IS=5E-12, BV=6, IBV=1E-3)
        f.D(0, 'inp', esd)
        f.D(0, 'inn', esd)
        # Input impedance and offset...
        f.V('inp', 1, -self.voff)
        # ... common mode
        for sign, pin in ((+1, 1), (-1, 'inn')):
            f.R(pin, 0, 10E13)
            f.C(pin, 0, 6E-12)
            f.I(pin, 0, sign*self.ib)
        # ... differential mode
        f.R(1, 'inn', 10E13)
        f.C(1, 'inn', 3E-12)
        f.I(1, 0, self.ioff)
        # Open-loop gain amplifier with realistic rail-to-rail limits
        # and an RC pole for the gain-bandwidth product
        g = 10**(0.05*self.gdb)
        f.E(2, 0, 1, 'inn', g)
        rails = f.model('rails', Paren(
            'limit', fraction=False, gain=1.0,
            out_lower_limit=0, out_upper_limit=self.vcc,
            limit_range=self.hr0))
        f.A(2, 3, rails)
        C = capValueUnity(1.0, self.gbp, g)
        f.R(3, 0, 1.0)
        f.C(3, 0, C)
        # Unity-gain buffer with a second pole at 45-degree phase
        # margin frequency
        f.G(0, 4, 3, 0, 1.0)
        f.R(4, 0, 1.0)
        C = capValue45deg(1.0, self.p45)
        f.C(4, 0, C)
        # Unity-gain output buffer with low impedance and limited slew
        # rate (using default soft transition of 0.1V)
        slew = f.model('slew', Paren(
            'slew', rise_slope=self.sr, fall_slope= self.sr))
        f.A(4, 5, slew)
        f.R(5, 'out', self.rout)


class MCP3204(Subcircuit):
    """
    One input of the an A/D converter sort of like the Microchip
    MCP3204 12-bit A/D.
    """
    # Setting this 1/1000 for sim purposes
    fScale = 0.001
    fclk = fScale * 2E6
    nodes = ['in', 'sample', 'ctrl']
    
    def setup(self, f):
        # Capacitance and leakage current from datasheet, Figure 4-1
        f.C('in', 0, 7E-12)
        f.I('in', 0, 1E-9)
        # Sample-and-hold switch and capacitor
        sh = f.model(
            'sh', 'aswitch',
            cntl_off=0, cntl_on=1, r_off=1E9, r_on=10E3, log='FALSE')
        f.A('ctrl', Paren(None, 'in', 'sample'), sh)
        f.A('ctrl_not', Paren(None, 'sample', 0), sh)
        f.R('in', 'sample', 1E3)
        # Scale C up when fclk has been scaled down
        f.C('sample', 0, 20E-12 / self.fScale)
        # Switch control
        pulseWidth = 1.5/self.fclk
        f.V('ctrl', 0, Paren(
            'PULSE', 0, 1,
            0,               # |
            0.01*pulseWidth, # \
            0.01*pulseWidth, # /
            9   *pulseWidth, #  |
            10  *pulseWidth, # |
        ))
        f.E('ctrl_not', 0, value='{1-V(ctrl)}')
