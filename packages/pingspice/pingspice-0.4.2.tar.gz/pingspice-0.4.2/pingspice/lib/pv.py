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
Solar panel and components.
"""

import math

from pingspice import netlist as nt
from pingspice.util import sub


class VocProvider:
    def clear(self):
        self.VocList = []
        
    def setSubordinate(self, fVoc):
        self.Voc_sub = fVoc
        self.callbacks.append(self.another)

    def another(self, f, params):
        if not hasattr(self, 'VocList'):
            self.VocList = []
        self.VocList.append(params['sp'])
    
    def Voc(self, sp=None):
        """
        """
        result = 0
        for spThis in self.VocList:
            if spThis == 'sp':
                spThis = sp
            result += self.Voc_sub(spThis)
        return result


class PV(nt.Subcircuit, VocProvider):
    """
    A ~9A PV cell from a large ~200W 60-cell rooftop panel.
    """
    k = 1.3806485E-23
    q = 1.6021766E-19
    diodeParams = {
        'N':    1.5,
        'IS':   5E-7,
        'Cjo':  50E-6,
        'Tnom': 25,
    }
    Isc = 9.4
    Rs = 0.001
    Rp = 10000
    
    nodes = ('A', 'K')
    params = {'sp': 1000}
    
    def setup(self, f):
        self.setSubordinate(self.Voc_bottomLevel)
        cell = f.MODEL('cell', 'D', **self.diodeParams)
        f.D(1, 'K', cell)
        expr = sub("{{-{}*sp/1000}}", self.Isc)
        f.I(1, 'K', expr)
        f.R(1, 'A', self.Rs)
        f.R('A', 'K', self.Rp)

        
    def Voc_bottomLevel(self, sp):
        """
        """
        N, IS = [self.diodeParams[x] for x in ('N', 'IS')]
        V = N*self.k*300 / self.q
        ID = self.Isc*sp / 1000
        V *= math.log(ID/IS)
        return V


class String(nt.Subcircuit, VocProvider):
    """
    A string of L{PV} cells with a bypass diode.
    """
    VFT1045BP = {
        # Vishay VFT 1045BP Shottky diode
        'BV':  45,
        'Cjo': 100E-12,
        'EG':  0.69,
        'XTI': 2,
        'N':   1.7,
        'IS':  1E-4,
        'RS':  0.008,
    }

    nodes = ('A', 'K')
    params = {'sp': 1000}

    def setup(self, f):
        pv = PV(f)
        self.setSubordinate(pv.Voc)
        # First cell
        pv('A', 1, sp='sp')
        # Eighteen more
        for k in range(18):
            pv(k+1, k+2, sp='sp')
        # Last cell, total of 20
        pv(k+2, 'K', sp='sp')
        bypass = f.MODEL('bypass', 'D', **self.VFT1045BP)
        f.D('K', 'A', bypass)


class SolarPanel(nt.Subcircuit, VocProvider):
    """
    A complete ~200W rooftop solar panel with three strings of PV
    cells in series and a small amount of inductance and resistance in
    the wire leads.
    """
    leadLength = 3.0 # feet, between panel centers
    considerLeadInductance = True

    nodes = ('pos', 'neg')
    params = {'sp': 1000}

    def setup(self, f):
        string = String(f)
        self.setSubordinate(string.Voc)
        for k in range(3):
            string(k+2, k+1, sp='sp')
        for k, node in enumerate((k+2, 1)):
            if self.considerLeadInductance:
                iNode = self.iNode(node)
                f.R(node, iNode, 1.0E-3 * self.leadLength)
                # There is some significant inductance because leads
                # in a string are not in pairs
                f.L(iNode, self.nodes[k], 1.85E-7 * self.leadLength)
            else:
                f.R(node, self.nodes[k], 1.0E-3 * self.leadLength)


class Cable(nt.Subcircuit):
    """
    Twisted pair of PV wires, modeled with RLC lumps. Tried using
    NgSpice's transmission line models; slow, non-converging.
    """
    mPerFt = 12.0*25.4/1000
    muZeroVsPi = 4E-7
    epsZero = 8.85418782E-12
    
    AWG = 10
    OD = 6.6E-3 # meters
    lengthFeet = 30
    mmAirGap = 1.0
    # More for higher accuracy, less for faster sim
    N_lumps = 50

    nodes = ['pvi', 'pvo']

    @classmethod
    def mmDia(cls, AWG):
        return {
            6:	4.115,
            7:	3.665,
            8:	3.264,
            9:	2.906,
            10:	2.588,
            11:	2.304,
            12:	2.052,
        }[AWG]

    @classmethod
    def mmSeparation(cls, AWG, OD):
        return 1000.0 * OD - cls.mmDia(AWG)

    @classmethod
    def R(cls, AWG, lengthFeet=None):
        """
        Returns Ohms per meter of BOTH wires for the given wire gauge, or
        total Ohms if a length in feet is provided.
        """
        mOhmsPerFt = {
            6:	0.40,
            7:	0.50,
            8:	0.63,
            9:	0.79,
            10:	1.00,
            11:	1.26,
            12:	1.59,
        }[AWG]
        cableOhmsPerFt = 2 * 10E-3 * mOhmsPerFt
        if lengthFeet:
            return lengthFeet * cableOhmsPerFt
        return cableOhmsPerFt / cls.mPerFt

    @classmethod
    def L(cls, AWG, OD=None, mmSep=None):
        """
        Returns Henries per meter of BOTH wires for the given wire gauge
        and outside diameter (in meters).
        """
        if OD: mmSep = cls.mmSeparation(AWG, OD)
        return cls.muZeroVsPi * (
            math.log(2*mmSep / cls.mmDia(AWG)) + 0.25)

    @classmethod
    def C(cls, AWG, OD=None, mmAirGap=None, usingPVC=True):
        dia = cls.mmDia(AWG)
        dielectricConstant = 3.5 if usingPVC else 2
        if mmAirGap is None:
            sep = cls.mmSeparation(AWG, OD)
            perm = cls.epsZero * math.sqrt(
                cls.mmAirGap * dielectricConstant*sep)
        else:
            sep = mmAirGap
            perm = cls.epsZero * mmAirGap
        num = math.pi*perm
        den = math.log(
            sep/dia + math.sqrt(sep**2/dia**2 - 1.0))
        return num / den
    
    def setup(self, f):
        AWG, OD = self.AWG, self.OD
        lengthMeters = getattr(self, 'lengthMeters', None)
        if lengthMeters is None:
            lengthMeters = self.lengthFeet * self.mPerFt
        R = self.R(AWG) / lengthMeters
        L = self.L(self.AWG, self.OD) / lengthMeters
        C = self.C(self.AWG, self.OD) / lengthMeters
        # Sanity- (and convergence-) preserving capacitor at input
        f.C('pvi', 0, 20*C)
        # The lumps
        for k in range(self.N_lumps):
            n0 = 'pvi' if k == 0 else n1
            n1 = self.iNode(n0)
            n2 = self.iNode(n1) if k < self.N_lumps-1 else 'pvo'
            f.R(n0, n1, R)
            f.L(n1, n2, L)
            f.C(n2, 0, C, IC=0)
