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
Power MOSFETs with evolved parameters.

These aim to fill a huge void in Ngspice and open-source circuit
simulation generally. There's been almost nothing freely available for
modeling power MOSFETs.

See the source at
U{pingspice.analysis.mosfet<edsuom.com/pingspice/pingspice.analysis.mosfet.py>}
to appreciate how much effort went into trying to accurately simulate
the behavior of these important devices. There is modeling of
voltage-dependent junction capacitance, gate threshold, Vds saturation
curves, forward and reverse biasing of the body diode, and lead
impedance.

And self-heating! The model estimates power dissipation and, in
conjunction with a Cauer thermal network for the package and any
attached heatsink, applies that to estimate junction and case
temperature over time.

Of course, it bears repeating from the license terms: I{pingspice} is
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied. And B{none of these models is
endorsed or in any way connected with} the manufacturer of the devices
whose behavior they are attempting to simulate.

@see: L{pingspice.analysis.mosfet}.
"""

from pingspice.circuit.netlist import Subcircuit
from pingspice.lib.semiconductor import PowerSemiconductor
from pingspice.analysis.mosfet import *


class PowerMOSFET(PowerSemiconductor):
    """
    Base class for power MOSFET subcircuits.

    @cvar Die: The subclass of L{analysis.mosfet.MOSFET} that models
        your device's semiconductor die. (Technically not just a die
        since it also models lead impedances. But not package thermal
        behavior.)

    @cvar package: The name (not FQN) of the package subcircuit in
        L{lib.thermal}, a subclass of L{lib.thermal.Package}.
    @type package: str

    @ivar heatsink: A 2-sequence (or callable that returns a
        2-sequence) containing values for I{rth_ca} and I{cth_c} of my
        package with any heatsink attached.
    
    @ivar rth_ca: Thermal resistance, case (package) to
        ambient. Should only be defined if I{heatsink} is not.
    
    @ivar cth_c: Thermal capacitance of case (package). Should only be
        defined if I{heatsink} is not.
    
    @see: L{PowerSemiconductor} for an explanation of the subcircuit
        param B{ambient} and the use of nodes 'tc' and 'tca0'.
    """
    nodes = ['drain', 'gate', 'source', 'pdiss', 'tj', 'tc', 'tca0']


class _TO220_MOSFET(PowerMOSFET):
    """Subcircuit for a power MOSFET with TO-220 package."""
    package = "TO220"

class _TO220F_MOSFET(PowerMOSFET):
    """Subcircuit for a power MOSFET with TO-220F plastic package."""
    package = "TO220F"
    
class _TO247_MOSFET(PowerMOSFET):
    """Subcircuit for a power MOSFET with TO-247 package."""
    package = "TO247"


#--- FQP32N20C ----------------------------------------------------------------

class _FQP32N20C_Setups(MOSFET_Setups):
    skippedIDs = [121, 222]
    specs = "FQP32N20C.specs"
    goals = "FQP32N20C.goals"

class FQP32N20C_Finder(MOSFET_Finder):
    """
    Parameter finder for the FQP32N20C series of N-channel power
    MOSFETs.
    
    To try to find better parameters than what's currently in
    L{FQP32N20C_Die}, call this with::

        pf [options] pingspice.lib.mosfets.FQP32N20C_Finder
    """
    Setups = _FQP32N20C_Setups
    package = "TO220"

class FQP32N20C_Die(MOSFET):
    """
    The semiconductor die for the L{FQP32N20C} and L{FQPF32N20C},
    without any package.
    """
    Finder = FQP32N20C_Finder
    finderParams = {
        # Finder = pingspice.lib.mosfets.FQP32N20C_Finder
        # SSE = 4179.3 after 5847 evaluations
        # Commit #4084b40, 2020-02-27
        'T_chl': -6.54554,
        'T_chm': 0.455221,
        'T_chv': 0.0037376,
        'T_drm': 1.50424,
        'T_drv': 0.00415382,
        'd_cjo': 1.05085e-09,
        'd_ikr': -99,
        'd_is': -11.121,
        'd_m': 0.708998,
        'd_n': 0.041009,
        'd_rs': -2.17888,
        'd_tt': -12.5278,
        'd_vj': 0.706697,
        'if_hca': -7.21902,
        'if_hcb': -8.61559,
        'ld': 6.32116e-09,
        'lgs_vs_ld': 2.96889,
        'm_Bt': -12.7641,
        'm_L': -6.28884,
        'm_L2W': 6.235,
        'm_L2xj': -0.557024,
        'm_NA': 17.5872,
        'm_Rp': 13.1443,
        'm_aK': -3.90103,
        'm_aR': 0.0686445,
        'm_aV': 8.50296,
        'm_dB': 1.79741,
        'm_dI': 93.5049,
        'm_dL': -99,
        'm_dR': -2.01083,
        'm_dV': -0.304644,
        'm_eta': -7.8853,
        'm_kappa': -5.56719,
        'm_nfs': 11.6978,
        'm_tox': -7.38583,
        'm_vsa': 1.04034,
        'mt_cbd': 3.09812,
        'mt_cgdo': 2.42953e-11,
        'mt_cgso': 0.848027,
        'mt_crss': 4.33258e-09,
        'mt_m': 0.891399,
        'mt_vj': 0.565493,
        'rd': 0.00363044,
        'rg': 0.492656,
        'rs': 0.0032074,
        'tca0': 10,
        'vf_lca': -2.83589,
    }

class FQP32N20C(_TO220F_MOSFET):
    """
    B{FQP32N20C}: N-Channel 200V, 0.082 Ohm, TO220 package.

    Fairchild/ON Semiconductor power MOSFET, rated at 28A.
    """
    Die = FQP32N20C_Die

class FQPF32N20C(_TO220F_MOSFET):
    """
    B{FQP32N20C}: N-Channel 200V, 0.082 Ohm, TO220F package.

    Fairchild/ON Semiconductor power MOSFET, rated at 28A.
    """
    Die = FQP32N20C_Die

    
#--- ST75NF20 -----------------------------------------------------------------

class _ST75NF20_Setups(MOSFET_Setups):
    skippedIDs = [121, 222]
    specs = "ST75NF20.specs"
    goals = "ST75NF20.goals"

class ST75NF20_Finder(MOSFET_Finder):
    """
    Parameter finder for the ST75NF20 series of N-channel power
    MOSFETs.
    
    To try to find better parameters than what's currently in
    L{ST75NF20_Die}, call this with::

        pf [options] pingspice.lib.mosfets.ST75NF20_Finder

    Assumes that a TO247 package was used to obtain transient data in
    datasheet, a reasonable assumption that doesn't affect whether you
    use the L{STP75NF20} or the L{STW75NF20} in your actual simulation.
    """
    Setups = _ST75NF20_Setups
    package = "TO247"

class ST75NF20_Die(MOSFET):
    """
    The die for the L{STP75NF20} and L{STW75NF20}, without any
    package.
    """
    Finder = ST75NF20_Finder
    finderParams = {
        # Finder = pingspice.lib.mosfets.ST75NF20_Finder
        # SSE = 4204.5 after 5904 evaluations
        # Commit following #a3565d1c, 2020-02-26
        'T_chl': -5.96276,
        'T_chm': 1.14928,
        'T_chv': 0.00628177,
        'T_drm': 1.35649,
        'T_drv': 0.0023024,
        'd_cjo': 1.04679e-08,
        'd_ikr': -99,
        'd_is': -11.2447,
        'd_m': 0.855679,
        'd_n': -4.00737e-05,
        'd_rs': -2.60605,
        'd_tt': -6.60918,
        'd_vj': 0.382868,
        'if_hca': -7.47928,
        'if_hcb': -8.28741,
        'ld': 1.70798e-09,
        'lgs_vs_ld': 1.21723,
        'm_Bt': -99,
        'm_L': -6.82094,
        'm_L2W': 6.28052,
        'm_L2xj': -1.0279,
        'm_NA': 19.2286,
        'm_Rp': 18.7899,
        'm_aK': -1.17367,
        'm_aR': 0.0281293,
        'm_aV': 5.7473,
        'm_dB': 0.861728,
        'm_dI': 218.099,
        'm_dL': -11.5932,
        'm_dR': -0.599271,
        'm_dV': -0.155393,
        'm_eta': -99,
        'm_kappa': 0,
        'm_nfs': 12.606,
        'm_tox': -8.29778,
        'm_vsa': 1,
        'mt_cbd': 1.48171,
        'mt_cgdo': 7.35398e-11,
        'mt_cgso': 0.815395,
        'mt_crss': 4.54434e-09,
        'mt_m': 0.883096,
        'mt_vj': 0.193175,
        'rd': 0.00291177,
        'rg': 3.04812,
        'rs': 0.000737872,
        'tca0': 10,
        'vf_lca': -2.77789,
    }
    
class STP75NF20(_TO220_MOSFET):
    """
    B{STP75NF20}: N-Channel 200V, 0.028 Ohm, TO220 package.

    ST Microelectronics power MOSFET, rated at 75A.
    """
    Die = ST75NF20_Die

class STW75NF20(_TO247_MOSFET):
    """
    B{STP75NF20}: N-Channel 200V, 0.028 Ohm, TO247 package.

    ST Microelectronics power MOSFET, rated at 75A.
    """
    Die = ST75NF20_Die


#--- STP60NF06 ----------------------------------------------------------------

class _STP60NF06_Setups(MOSFET_Setups):
    skippedIDs = [222]
    specs = "STP60NF06.specs"
    goals = "STP60NF06.goals"

class STP60NF06_Finder(MOSFET_Finder):
    """
    Parameter finder for the STP60NF06 series of N-channel power
    MOSFETs.
    
    To try to find better parameters than what's currently in
    L{STP60NF06_Die}, call this with::

        pf [options] pingspice.lib.mosfets.STP60NF06_Finder
    """
    Setups = _STP60NF06_Setups
    package = "TO220"

class STP60NF06_Die(MOSFET):
    """
    The L{STP60NF06} die, without any package
    """
    Finder = STP60NF06_Finder
    finderParams = {
        # Finder = pingspice.lib.mosfets.STP60NF06_Finder
        # SSE = 4524.5 after 11067 evaluations
        # Commit #836ae165, 2020-02-27
        'T_chl': -5.77924,
        'T_chm': 1.67761,
        'T_chv': 0.00760595,
        'T_drm': 1.41643,
        'T_drv': 0.00728825,
        'd_cjo': 5.95244e-09,
        'd_ikr': -32.5902,
        'd_is': -12.4304,
        'd_m': 0.883396,
        'd_n': 0.00311866,
        'd_rs': -2.49503,
        'd_tt': -7.28909,
        'd_vj': 0.135905,
        'if_hca': -7.22298,
        'if_hcb': -10.7926,
        'ld': 3.49957e-09,
        'lgs_vs_ld': 1.11627,
        'm_Bt': -13.9905,
        'm_L': -6.44797,
        'm_L2W': 6.65037,
        'm_L2xj': -0.614747,
        'm_NA': 17.7348,
        'm_aK': -2.24893,
        'm_aR': 0.00899299,
        'm_aV': -4.33823,
        'm_dB': -0.669992,
        'm_dI': 181.004,
        'm_dL': -2.25245,
        'm_dR': -1.16913,
        'm_dV': -1.06826,
        'm_eta': -3.2922,
        'm_kappa': 0.789533,
        'm_nfs': 6.59758,
        'm_tox': -7.42785,
        'm_vsa': 1.14554,
        'mt_cbd': 0.369454,
        'mt_cgdo': 4.73151e-10,
        'mt_cgso': 0.429777,
        'mt_crss': 9.27808e-10,
        'mt_m': 0.873958,
        'mt_vj': 0.50839,
        'rd': 0.00335311,
        'rg': 2.72178,
        'rs': 0.00260544,
        'tca0': 10,
        'vf_lca': -2.65947,
    }

class STP60NF06(_TO220_MOSFET):
    """
    B{STP60NF06}: N-Channel 60V, 0.016 Ohm, TO220 package.

    ST Microelectronics power MOSFET, rated at 60A.
    """
    Die = STP60NF06_Die


#--- RFP12N10L ----------------------------------------------------------------

class _RFP12N10L_Setups(MOSFET_Setups):
    # Component has no specs/goals defined for setups 231, 321
    skippedIDs = [220, 231, 321]
    specs = "RFP12N10L.specs"
    goals = "RFP12N10L.goals"

class RFP12N10L_Finder(MOSFET_Finder):
    """
    Parameter finder for the RFP12N10L N-channel power MOSFET.

    To try to find better parameters than what's currently in
    L{RFP12N10L_Die}, call this with::

        pf [options] pingspice.lib.mosfets.RFP12N10L_Finder

    @cvar package: The package for the device used in actual device
        testing ("TO220").
    """
    Setups = _RFP12N10L_Setups
    package = "TO220"

class RFP12N10L_Die(MOSFET):
    """
    The L{RFP12N10L} die, without any package
    """
    Finder = RFP12N10L_Finder
    finderParams = {
        # Finder = pingspice.lib.mosfets.RFP12N10L_Finder
        # SSE = 1793.1 after 8334 evaluations
        # Commit following #507f5e28, 2020-01-15
        'T_chl': -6.22577,
        'T_chm': 1.62441,
        'T_chv': 0.00386641,
        'T_drm': 0.946266,
        'T_drv': -0.0298239,
        'd_cjo': 1.21028e-09,
        'd_ikr': -99,
        'd_is': -10.9016,
        'd_m': 0.518306,
        'd_n': 0.0630756,
        'd_rs': -1.90075,
        'd_tt': -6.94267,
        'd_vj': 0.284159,
        'if_hca': -7.52992,
        'if_hcb': -8.03599,
        'ld': 1.23173e-08,
        'lgs_vs_ld': 1.9815,
        'm_Bt': -20.2123,
        'm_L': -6.44794,
        'm_L2W': 5.35201,
        'm_L2xj': -1.63664,
        'm_NA': 19.3164,
        'm_aK': -1.17264,
        'm_aR': 0.0524999,
        'm_aV': 1.01584,
        'm_dB': -0.929837,
        'm_dI': 35.179,
        'm_dL': -1.95776,
        'm_dR': -0.731366,
        'm_dV': 0.156154,
        'm_eta': -31.4898,
        'm_kappa': -13.0986,
        'm_nfs': -12.0082,
        'm_tox': -8.66886,
        'm_vsa': 1,
        'mt_cbd': 0.0221993,
        'mt_cgdo': 1.29618e-11,
        'mt_cgso': 0.0271408,
        'mt_crss': 2.48465e-09,
        'mt_m': 0.897222,
        'mt_vj': 0.0853106,
        'rd': 0.035689,
        'rg': 18.5574,
        'rs': 0.0350526,
        'vf_lca': -2.77822,
    }

class RFP12N10L(_TO220_MOSFET):
    """
    B{RFP12N10L}: N-Channel 100V, 0.200 Ohm, TO220 package

    ON Semiconductor (formerly Fairchild) power MOSFET, rated at 12A.
    """
    Die = RFP12N10L_Die
    

#--- IRF9Z34NPbF -----------------------------------------------------------------

class _IRF9Z34NPbF_Setups(MOSFET_Setups):
    # Component has no specs/goals defined for setup 272
    skippedIDs = [272]
    goals = "IRF9Z34NPbF.goals"
    specs = "IRF9Z34NPbF.specs"
    
class IRF9Z34NPbF_Finder(MOSFET_Finder):
    """
    Parameter finder for the IRF9Z34NPbF P-channel power MOSFET.
    
    To try to find better parameters than what's currently in
    L{IRF9Z34NPbF_Die}, call this with::

        pf [options] pingspice.lib.mosfets.IRF9Z34NPbF_Finder
    """
    Setups = _IRF9Z34NPbF_Setups
    package = "TO220"

class IRF9Z34NPbF_Die(MOSFET):
    """
    The L{IRF9Z34NPbF} die, without any package.
    """
    Finder = IRF9Z34NPbF_Finder
    finderParams = {
        # Finder = pingspice.lib.mosfets.IRF9Z34NPbF_Finder
        # SSE = 1432.3 after 9264 evaluations
        # Commit #4084b40, 2020-02-27
        'T_chl': -6.85815,
        'T_chm': 0.700231,
        'T_chv': 0.00231376,
        'T_drm': 1.46768,
        'T_drv': 0.0122538,
        'd_cjo': 1.65111e-09,
        'd_ikr': -99,
        'd_is': -11.2249,
        'd_m': 0.718521,
        'd_n': 0.0464368,
        'd_rs': -1.81848,
        'd_tt': -7.57985,
        'd_vj': 0.0556662,
        'if_hca': -15.7306,
        'if_hcb': -11.5665,
        'ld': 4.5e-09,
        'lgs_vs_ld': 1.667,
        'm_Bt': -99,
        'm_L': -7.38814,
        'm_L2W': 5.2806,
        'm_L2xj': -1.96576,
        'm_NA': 18.8859,
        'm_aK': -8.92073,
        'm_aR': 0.018158,
        'm_aV': 6.39917,
        'm_dB': -0.162616,
        'm_dI': 108.651,
        'm_dL': 6.55572,
        'm_dR': -1.51768,
        'm_dV': 0.184459,
        'm_eta': -7.68536,
        'm_kappa': -1.71624,
        'm_nfs': 12.2377,
        'm_tox': -8.20691,
        'm_vsa': 0.186406,
        'mt_cbd': 3.07829,
        'mt_cgdo': 9.82665e-12,
        'mt_cgso': 0.894925,
        'mt_crss': 8.33834e-10,
        'mt_m': 0.578918,
        'mt_vj': 0.979857,
        'rd': 0.0119141,
        'rg': 5.31015,
        'rs': 0.00574262,
        'tca0': 10,
        'vf_lca': -2.7455,
    }

class IRF9Z34NPbF(_TO220_MOSFET):
    """
    B{IRF9Z34NPbF}: P-Channel 55V, 0.10 Ohm, TO220 package.

    IR Power MOSFET, rated at 19A.
    """
    Die = IRF9Z34NPbF_Die


#--- IXT26P20 -----------------------------------------------------------------

class _IXT26P20_Setups(MOSFET_Setups):
    # Component has no specs/goals defined for setup 272. Setup 411 is
    # disabled because excessive oscillation messes up analyzer
    skippedIDs = [272, 411]
    goals = "IXT26P20.goals"
    specs = "IXT26P20.specs"
    
class IXT26P20_Finder(MOSFET_Finder):
    """
    Parameter finder for the IXT26P20 P-channel power MOSFET.
    
    To try to find better parameters than what's currently in
    L{IXT26P20_Die}, call this with::

        pf [options] pingspice.lib.mosfets.IXT26P20_Finder
    """
    Setups = _IXT26P20_Setups
    package = "TO220"

class IXT26P20_Die(MOSFET):
    """
    The L{IXTP26P20P} die, without any package.
    """
    Finder = IXT26P20_Finder
    finderParams = {
        # Finder = pingspice.lib.mosfets.IXT26P20_Finder
        # SSE = 4157.7 after 20886 evaluations
        # Commit #16c9f1af, 2019-12-17
        'T_chl': -5.71832,
        'T_chm': 0.759895,
        'T_chv': 0.00216509,
        'T_drm': 1.65969,
        'T_drv': 0.0324412,
        'd_cjo': 6.10008e-09,
        'd_ikr': -99,
        'd_is': -10.4691,
        'd_m': 0.872025,
        'd_n': 0.570743,
        'd_rs': -1.66483,
        'd_tt': -5.64408,
        'd_vj': 0.237006,
        'if_hca': -18.2,
        'if_hcb': -19.5,
        'ld': 1e-09,
        'lgs_vs_ld': 1.02724,
        'm_Bt': -12.5,
        'm_L': -6.15017,
        'm_L2W': 6.75555,
        'm_L2xj': -1.52567,
        'm_NA': 17.7735,
        'm_aK': -2.29003,
        'm_aR': 0.0959384,
        'm_aV': -3.98653,
        'm_dB': -0.6,
        'm_dI': 196.792,
        'm_dL': -99,
        'm_dR': -0.817024,
        'm_dV': 0.65154,
        'm_eta': -2.81012,
        'm_kappa': 4,
        'm_nfs': 10.0148,
        'm_tox': -7.43865,
        'm_vsa': 1,
        'mt_cbd': 4.30637,
        'mt_cgdo': 2.6441e-12,
        'mt_cgso': 2.41615,
        'mt_crss': 1.30119e-09,
        'mt_m': 0.81725,
        'mt_vj': 1,
        'rd': 0.0446136,
        'rg': 5.58939,
        'rs': 0.015701,
        'vf_lca': -2.24115,
    }

class IXTP26P20P(_TO220_MOSFET):
    """
    B{IXTP26P20P}: P-Channel 200V, 0.170 Ohm, TO220 package.

    IXYS Power MOSFET, rated at 26A.
    """
    Die = IXT26P20_Die


#--- IXTH130N10T --------------------------------------------------------------

class _IXTH130N10T_Setups(MOSFET_Setups):
    goals = "IXTH130N10T.goals"
    specs = "IXTH130N10T.specs"
    
class IXTH130N10T_Finder(MOSFET_Finder):
    """
    Parameter finder for the IXTH130N10T N-channel power MOSFET.
    
    To try to find better parameters than what's currently in
    L{IXTH130N10T_Die}, call this with::

        pf [options] pingspice.lib.mosfets.IXTH130N10T_Finder
    
    """
    Setups = _IXTH130N10T_Setups
    package = "TO247"

class IXTH130N10T_Die(MOSFET):
    """
    The L{IXTH130N10T} die, without any package.
    """
    Finder = IXTH130N10T_Finder
    finderParams = {
        # Finder = pingspice.lib.mosfets.IXTH130N10T_Finder
        # SSE = 4511.9 after 18286 evaluations
        # Commit #049ffe7a, 2019-12-19
        'T_chl': -3.85415,
        'T_chm': 1.08297,
        'T_chv': 0.00451678,
        'T_drm': 1.76538,
        'T_drv': 0.0149837,
        'd_cjo': 1.23833e-09,
        'd_ikr': -99,
        'd_is': -9.98014,
        'd_m': 0.705952,
        'd_n': 0.0498954,
        'd_rs': -2.85067,
        'd_tt': -7.31703,
        'd_vj': 0.526626,
        'if_hca': -7.59108,
        'if_hcb': -13.1478,
        'ld': 1e-09,
        'lgs_vs_ld': 1.14359,
        'm_Bt': -13.9755,
        'm_L': -6.45882,
        'm_L2W': 6.98614,
        'm_L2xj': -2.04495,
        'm_NA': 17.6371,
        'm_aK': -8.37154,
        'm_aR': 0.00112536,
        'm_aV': 1.05774,
        'm_dI': 538.343,
        'm_dR': -0.723201,
        'm_eta': -99,
        'm_kappa': -99,
        'm_nfs': 12.1659,
        'm_tox': -7.33077,
        'm_vsa': 1,
        'mt_cbd': 4.117,
        'mt_cgdo': 7.19476e-12,
        'mt_cgso': 1.02278,
        'mt_crss': 8.97046e-10,
        'mt_m': 0.267529,
        'mt_vj': 0.0230701,
        'rd': 0.00182304,
        'rg': 7.19332,
        'rs': 0.00176982,
        'vf_lca': -2.78347,
    }

class IXTH130N10T(_TO247_MOSFET):
    """
    B{IXTH130N10T}: N-Channel 100V, ..., TO247 package.

    IXYS Power MOSFET, rated at ....
    """
    Die = IXTH130N10T_Die


# --- PSMN9R5-100PS -----------------------------------------------------------

class _PSMN9R5_100PS_Setups(MOSFET_Setups):
    goals = "PSMN9R5_100PS.goals"
    specs = "PSMN9R5_100PS.specs"
    
class PSMN9R5_100PS_Finder(MOSFET_Finder):
    """
    Parameter finder for the PSMN9R5-100PS N-channel power MOSFET.
    
    To try to find better parameters than what's currently in
    L{PSMN9R5_100PS_Die}, call this with::

        pf [options] pingspice.lib.mosfets.PSMN9R5_100PS_Finder
    """
    Setups = _PSMN9R5_100PS_Setups
    package = "TO220"

class PSMN9R5_100PS_Die(MOSFET):
    """
    The L{PSMN9R5_100PS} die, without any package.
    """
    Finder = PSMN9R5_100PS_Finder
    finderParams = {
        # Finder = pingspice.lib.mosfets.PSMN9R5_100PS_Finder
        # SSE = 4097.7 after 7324 evaluations
        # Commit #2f58fc265f, 2019-12-26
        'T_chl': -4.10298,
        'T_chm': 1.57083,
        'T_chv': 0.00723474,
        'T_drm': 1.74508,
        'T_drv': 0.00943368,
        'd_cjo': 1.8199e-09,
        'd_ikr': -99,
        'd_is': -7.90833,
        'd_m': 0.641237,
        'd_n': 0.138533,
        'd_rs': -2.8286,
        'd_tt': -7.2656,
        'd_vj': 0.164127,
        'if_hca': -20.3086,
        'if_hcb': -8.53516,
        'ld': 5.52322e-10,
        'lgs_vs_ld': 1.777,
        'm_Bt': -99,
        'm_L': -7.14425,
        'm_L2W': 7.03308,
        'm_L2xj': -1.80228,
        'm_NA': 19.3797,
        'm_Rp': 14.3798,
        'm_aK': -6.94754,
        'm_aR': 0.00383555,
        'm_aV': 1.67286,
        'm_dI': 917.382,
        'm_dR': -2.18706,
        'm_eta': -4.3381,
        'm_kappa': 0.559481,
        'm_nfs': 6.92592,
        'm_tox': -8.32363,
        'm_vsa': 1,
        'mt_cbd': 3.11244,
        'mt_cgdo': 1.32599e-10,
        'mt_cgso': 0.866816,
        'mt_crss': 1.55467e-09,
        'mt_m': 0.745171,
        'mt_vj': 0.6073,
        'rd': 0.00268098,
        'rg': 0.91015,
        'rs': 0.000207985,
        'vf_lca': -2.90935,
    }

class PSMN9R5_100PS(_TO220_MOSFET):
    """
    B{PSMN9R5_100PS}: N-Channel 100V, 9.6 mOhm, TO220 package.

    Nexperia Power MOSFET, rated at 89 A.
    """
    Die = PSMN9R5_100PS_Die
