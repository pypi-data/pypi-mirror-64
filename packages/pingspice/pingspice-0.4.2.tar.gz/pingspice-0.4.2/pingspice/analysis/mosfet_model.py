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
A power MOSFET model with evolved parameters.

@see: L{pingspice.lib.mosfets} and L{pingspice.analysis.diode}.
"""

import numpy as np

from pingspice.circuit.av import AV
from pingspice.analysis import diode, expressions
from pingspice.util import *


class ArchOpts(object):
    """
    I store an architecture configuration and provide methods for
    convenient abstracting of different MOSFET architecture options.

    @ivar architecture: A dict set from the device spec, containing
        entries I{N_channel}, I{LDD}, I{vertical}, and I{Rp}.
    """
    def __init__(self, architecture):
        self.architecture = architecture

    @property
    def N_channel(self):
        """
        Property: C{True} if N-channel (NMOS), C{False} if P-channel
        (PMOS).
        """
        return self.architecture.get('N_channel', False)

    @property
    def P_channel(self):
        """
        Property: C{True} if P-channel (NMOS), C{False} if N-channel
        (PMOS).
        """
        return not self.architecture.get('N_channel', False)
    
    @property
    def has_ldd(self):
        """
        Property: C{True} if includes a lightly doped drift region.
        """
        return self.architecture.get('LDD', False)

    @property
    def has_jfet(self):
        """
        Property: C{True} if includes a JFET region.
        """
        return \
            self.has_ldd \
            and self.architecture.get('vertical', False) \
            and not self.architecture.get('trench', False)

    @property
    def has_Rp(self):
        """
        Property: C{True} if there is enough baseline drain-source leakage
        to warrant having a fixed resistor in parallel with the MOS3
        primitive modeling the channel.
        """
        return self.architecture.get('Rp', False)
    
    def npi(self, x):
        """
        Returns the unchanged input if N-channel, else the "inverted"
        value of the input. "Inverted" means different things for
        different object types:
        
          - B{string:} Prepends a '-' onto the string, or removes a
            '-' if there was one.

          - B{float} or B{int}: Makes the value negative if it was
            positive, leaves it alone if it was already negative.

          - B{AV} object or anything else: Inverts it.
        """
        if self.N_channel:
            return x
        if isinstance(x, str):
            return x[1:] if x.startswith('-') else "-"+x
        if isinstance(x, (int, float)):
            return -abs(x)
        return -x

    def npp(self, x, y, forceFirst=False):
        """
        Returns the first arg if N channel, else the second one.

        Set the keyword I{forceFirst} C{True} to force return of the
        first arg.
        """
        return x if self.N_channel or forceFirst else y

    def npr(self, x, y, *args):
        """
        Returns the args, except with the first two reversed if P Channel.
        """
        newArgs = [x, y] + list(args)
        if not self.N_channel:
            x = newArgs[0]
            newArgs[0] = newArgs[1]
            newArgs[1] = x
        return newArgs


class MOSFET_Physics(ArchOpts):
    """
    I model a few physical aspects of a MOSFET cell. My
    L{MOSFET_Model} subclass does much more.
    """
    # Degrees K for 0 deg C
    Tc2k = 273.15
    # Nominal (room) temperature, deg C
    Tnc = 25
    # Boltzmann's constant
    k = 1.38064853e-23
    # Electron charge
    q = 1.60217663e-19
    # Bandgap energy of silicon (V), from Ravindra & Srivastava
    # (1979).
    Eg = 1.111
    # Intrinsic carrier concentration of Si
    ni = 1.015e10
    # Electron affinity of Si (V), T&M p. 28.
    Chi = 4.05
    # Permittivity of free space
    e0 = 8.854e-16 # F/m
    # Dielectric constant of silicon and silicon dioxide
    ks = 11.9; kso2 = 3.9
    # Interface charge density (C/cm^2). Roughly midrange guess from
    # T&M pp. 70-71, set to Example 2.2 value.
    Qd0 = 1e-8
    # Metal gate work function potential (leave at None for
    # polysilicon gate).
    PM = None
    
    # AVC = Weird-looking arithmetic done for AV compatibility
    
    def __init__(self, **kw):
        ArchOpts.__init__(self, kw.pop('arch', {}))
        # Keywords -> attributes
        for name in kw:
            setattr(self, name, kw[name])
        # Nominal (room) temperature in deg C
        self.Tnk = self.Tnc + self.Tc2k
        # Thermal voltage
        self.Pt = self.k*self.Tnk/self.q
        # Degeneracy upper limit for acceptor and donor concentrations
        self.N_upperLimit = self.ni*np.exp(self.Eg/(2*self.Pt))
        # A term for use in calculating the Fermi potential PF,
        # equivalent to dividing N by ni inside the logarithm
        self.PF_ni = -self.Pt*np.log(self.ni)
        # A term for use in calculating the body effect coefficient
        # gamma, which includes a factor of 10 due to es being in F/m
        # instead of F/cm
        self.sqrt_2qe = 10*np.sqrt(2*self.q*self.e0*self.ks)
        
    def lowerLimit(self, A, X, limit=None, test=None):
        """
        Returns I{X} with a soft lower limit of I{limit}, using an
        expression that is numerically robust for all unlimited values
        and for modestly lower-limited values.

        The limiter output is log(2)/A when I{X} equals I{limit}.

        @see: T&M (10.4.6) p. 612. The B-source expression counterpart
            to this is L{Expressionist.lowerLimit}.
        """
        # TODO: Make work with large positive
        Y = A*(limit - X)
        Y = np.log(1 + np.exp(Y))
        return X + Y/A
        
    def Cdox(self, tox):
        """
        Given oxide thickness I{tox} (m), returns the oxide capacitance
        per unit area (F/cm^2). AV compatible.
        """
        eox = self.kso2 * self.e0
        return (tox**-1)*eox # AVC

    def PF(self, N):
        """
        Given acceptor or donor concentration I{N}, returns the
        substrate (bulk) Fermi potential PF (phi_F) at nominal
        temperature. AV compatible.

        B{Note}: You have to ensure that I{N} does not exceed the
        upper degeneracy limit.

        @see: T&M pp. 9-10.
        """
        x = N.ln()*self.Pt if isinstance(N, AV) else self.Pt*np.log(float(N))
        return x + self.PF_ni

    def Vfb(self, tox, NA, NG=None):
        """
        Given oxide thickness I{tox}, acceptor concentration I{NA}, and
        donor concentration I{NG} of polysilicon gate, returns the
        flatband voltage. AV compatible.

        If I{NG} is I{None}, 0, or not specified, then my I{PM}
        attribute must be set to a metal gate contact potential.

        The calculation is fairly involved, and is derived from the
        metal-substrate (gate-bulk) voltage I{PMS} that is required to
        cancel the total gate-oxide-bulk contact potential. A small
        correction term is subtracted from that difference [T&M
        (2.2.6) p. 71].

        M{PMS = PM - PS} where I{PM} is the gate ("metal") contact
        potential and I{PS} is the bulk ("substrate") contact
        potential. If the gate and bulk are doped exactly the same or
        are both degenerate (one being n- and the other p+), then
        I{PMS} will be twice the gate's (negative) Fermi potential.
        
        I{PMS} is a float or child L{AV} object derived from the
        result of a call to L{PF} for the p+ bulk and the Fermi
        potential of the n- polysilicon gate, which is calculated from
        the work function potential I{PM} of a polysilicon gate based
        on I{NG}. But if my I{PM} (phi_M) attribute was set in my
        constructor, its value (which may be expressed as an L{AV}
        object) is used directly as the work function potential I{PM}
        for a metal gate.

        B{TODO}: Because of the complexity of the computation, a
        repeated call with the same arguments will return a cached
        result.

        Calls L{PF} and L{Cdox}.
        """
        def PW(PF):
            # Not including q in the denominator of the second term
            # (see T&M p. 28) because Eg is specified in V.
            return PF + (self.Chi + self.Eg/2) # AVC

        # TODO: Cache result, re-calculate only on change to tox, NA,
        # NG. That should work fine with AV objects, too.
        PM = PW(-self.PF(NG)) if NG else self.PM
        PS = PW(self.PF(NA))
        return -PS - ((self.Cdox(tox)**-1) * self.Qd0) + PM # AVC
    
    def gamma(self, tox, NA):
        """
        Given oxide thickness I{tox} and acceptor concentration I{NA},
        returns the body effect coefficient. AV compatible.

        An issue with units is addressed during my constructor's
        one-time calculation of I{sqrt_2qe}: I{es} is in F/m, but
        I{m_NA} is in cm^-3 and I{Cdox} is in F/cm^2.

        Scaling the latter two to meters rather than centimeters
        multiplies I{m_NA} by 1e6 and I{Cdox} by 1e4. This results in
        a numerator (after the square root of 1e6) that is 1e3 times
        as big, and a denominator that is 1e4 times as big. Thus, the
        T&M formula (2.4.26a) needs to have a constant scalar of 10
        included in the numerator.

        Calls I{Cdox}.
        """
        return NA**0.5 / self.Cdox(tox) * self.sqrt_2qe # AVC

    def VT(self, tox, NA, NG=None):
        """
        Given oxide thickness I{tox}, acceptor concentration I{NA}, and
        donor concentration I{NG} of polysilicon gate, returns the
        threshold voltage. AV compatible.

        If I{NG} is I{None}, 0, or not specified, then my I{PM}
        attribute must be set to a metal gate contact potential.

        Calls L{PF}, L{Vfb}, and L{gamma}.
        """
        P0 = self.PF(NA)*2 + 6*self.Pt # AVC
        x = self.Vfb(tox, NA, NG) + P0
        x += self.gamma(tox, NA)*(P0**0.5) # AVC
        return x

    def Vgsm(self, gamma, Vgs0):
        """
        Returns the lower limit of Vgs for computing I{n}.

        Call L{gamma} and L{Vgs0} to get the two argument values.
        """
        return (gamma**2 * 0.25) - Vgs0 # AVC
    
    def mu(self, N, sma=0.45, N_forced=False):
        """
        Given doping concentration I{N}, returns the approximate surface
        mobility of silicon. AV compatible.

        The material is N- for N_channel architecture, or if the
        keyword I{N_forced} is set C{True}. Otherwise it is P+, with
        hole mobility.

        The calculation of I{muBulk} was adapted from
        U{http://ecee.colorado.edu/~bart/book/mobility.htm},
        2.9.1. Units are cm^2/(V*s).

        You can force the value to be for bulk mobility by setting the
        I{sma} keyword to 1.0.

        Surface vs Bulk Mobility
        ========================
        
            With the default value of the I{sma} keyword (which may be
            an L{AV} object as well as I{NA}), the result is assumed
            to be 0.45 of I{muBulk}. That's the best info I have, from
            T&M p. 159; p. 217 ["may be roughly half of the bulk
            mobility (as evaluated for lightly doped substrates), or
            less for heavily doped substrates"], and p. 245
            ["significantly lower than the bulk mobility (e.g., by a
            factor of 2)"].
    
            Mason
            U{https://www.egr.msu.edu/classes/ece410/mason/files/Ch6.pdf}
            in his ECE 410 lecture notes 6.19 cites typical N- surface
            mobility as 500-580 cm^2/(V*s), and "typical" bulk
            mobility (6.3) as 1360. That works out to a fraction of
            0.37 - 0.43.
    
            Sergio Franco in Analog Circuit Design: Discrete and
            Integrated (p. 407) says mobility at the surface is
            "somewhere in the neighborhood of one-half to one-third of
            its bulk value."
        """
        mu_min = self.npp(60, 45, N_forced)
        mu_max = self.npp(1415, 471, N_forced)
        # The value of Nr for N-channel is an average for Arsenic and
        # Phosphorus. For P-channel, it's the value for Boron.
        Nr = self.npp(9.45e16, 2.23e17, N_forced)
        # The value of alpha for N-channel is an average for Arsenic
        # and Phosphorus. For P-channel, it's the value for Boron.
        alpha = self.npp(0.70, 0.719, N_forced)
        # Build the child AV object with mods
        muBulk = (N / Nr)**alpha + 1
        muBulk = (muBulk**-1 * (mu_max - mu_min)) + mu_min
        # This gets scaled down to convert bulk to surface
        # mobility. More scaling with higher N, which should get
        # reflected in the value of m_sma.
        return muBulk * sma

    def Kp(self, W, L, NA, tox):
        """
        Given channel width I{W} and length I{L}, acceptor concentration
        I{NA}, and oxide thickness I{tox}, returns the transconductance
        parameter I{Kp}. AV compatible.

        The all-region model [T&M (4.9.1) p. 209] for Ids is::

            Ids = Kp*Pt^2*2*n*(a^2 - b^2)
              where
                Kp =  W/L*mu*Cdox
                a = log(1 + exp(Vgst/(2*n*Pt)))
                b = log(1 + exp((Vgst-n*Vds)/(2*n*Pt)))
        
        Everything to the left of I{n} is dependent only on constants
        and parameters, so you can also define a I{scale} for (4.9.1)
        as follows::
        
            scale = Kp * Pt**2 * 2

        Then the expression becomes::

            Ids = scale*n*(a^2 - b^2)

        The channel "width" parameter I{W} is just for a single
        cell. Since there can be thousands of cells in a power MOSFET,
        overall device I{Kp} is likely to be much bigger than the
        result.

        Calls L{mu} and L{Cdox}.
        """
        return (W / L) * self.mu(NA) * self.Cdox(tox)

    def theta(self, Bt, tox):
        """
        Given the mobility reduction coefficient factor I{Bt} and oxide
        thickness I{tox}, returns the coefficient I{theta} for the
        Vgs-induced reduction in effective mobility. AV compatible.

        Effective mobility is then calculated as follows::

            mu_eff = mu / (1 + theta*(Vgs - VT))

        Computing theta is a simple matter of factoring in the effect
        of I{tox} so that I{Bt} can be relatively free of size
        effects::

            theta = Bt / tox

        T&M (p. 220) introduce this term as C{Beta_sub_theta} and
        suggest its range is "typically 0.5 to 2 nm * V^-1." A value
        of zero would entirely eliminate the effect of higher Vgs
        reducing mu.

        Also used in computing a different theta for accumulation in
        drift. For that, I{Bt} may be smaller due to the oxide being
        thickened partway along the drift path (LDMOS) or the gate
        being far away for much of the drift path (VDMOS).
        """
        return Bt / tox

    def Lpn(self, xj, L, tox):
        """
        Given junction depth I{xj}, channel length L{L}, and oxide
        thickness I{tox} (all in meters), returns the nominal length
        of the pinchoff region L{Lpn} relative to the channel
        length. AV compatible.

        It is calculated as follows::

            Lpn = La / L
              where
                La = sqrt(3 * tox * xj)
        
        The junction depth I{xj} is an absolute (not relative) value
        that is anywhere from a low percentage of the channel length
        I{L} to a bit bigger than it.

        The result I{Lpn} is a "nominal length" because it's the
        (relative) length of the pinchoff region when Vds just exceeds
        the onset of saturation. More precisely, it is the fractional
        length of the channel that is "lost" from inversion when
        M{log(1+(Vds-Vds_prime)/VE) = 1}. I{Vds_prime} is the
        drain-source (or source-drain) voltage at the onset of
        saturation, very close to M{Vgst/n}. I{VE} is a fitting
        parameter with a value in the general neighborhood of 1.0.

        With I{VE} equal to 1.0, I{Lpn} is the pinchoff region length
        when Vds is 1.718 times I{Vds_prime}. The pinchoff region
        doubles (again, with I{VE} equal to 1.0) when Vds quadruples
        from that point. And when Vds is 11x times greater, the
        pinchoff region will have tripled in length. So, considering
        how much greater the operating range of a power MOSFET is
        beyond saturation, I{Lpn} must be kept well below L{L}.

        The simplest constraint to impose on I{Lpn} is to assume
        I{Vds_prime} is zero (a conservative lower limit, since it
        would require Vgst=0). Then, at breakdown voltage M{Vds =
        Vds_BV} and requiring that M{Lpn*log(1+Vds/VE) < L},::

            Lpn < L/log(1 + Vds_BV/VE)
        """
        La = (tox * xj * 3)**0.5 # AVC
        return La / L
    
    def n(self, VGS, tox, NA, NG=None):
        """
        Given I{VGS} (may be a Numpy array), oxide thickness I{tox},
        acceptor concentration I{NA}, and donor concentration I{NG} of
        polysilicon gate, returns I{n}. NOT AV compatible!

        The term I{n} is used in the all-region model [T&M (4.9.1)
        p. 209] and is treated as the equivalent of the more commonly
        used "alpha." It is the inverse of the first derivative of the
        surface potential deep in depletion vs Vgs.

        If I{NG} is I{None}, 0, or not specified, then my I{PM}
        attribute must be set to a metal gate contact potential. (The
        Hspice simulator's implementation of MOS3 assumes NG=1e18.)
        
        This method is B{NOT} AV compatible, because the result relies
        on I{VGS}, a float (or Numpy array).
        """
        gamma = self.gamma(tox, NA)
        Vgs0 = 0.25*gamma**2 - self.Vfb(tox, NA, NG)
        VGSP = self.lowerLimit(100, VGS, self.Vgsm(gamma, Vgs0))
        denom = -gamma + 2*np.sqrt(Vgs0 + VGSP)
        return 1 + (gamma / denom)


class MOSFET_Model(MOSFET_Physics, diode.DiodeMixin):
    """
    I implement the MOSFET model, everything on the silicon die, from
    source pad to drain connection. My methods define the circuitry
    for everything inside (but not including) the package leads::
                                             
        15 >--+-- Rd --+----------+------------- 16 ----------+
              |        |          |                           |
              |     +------+  +------+                        |
              |     | Cgso |  | Crss |                        |
              |     +------+  +------+                        V
              |         |         |                           |
              |         |         |                           |
              |         +---------+                           |
              |                   |           +----------+    |
              |                   |  +-------<|-        +|<---+
              |                   |  |        |  Drift   |
              |                   +--|-------x|    +     |       
              |              +----|--|-------x|   temp   |       
              |              |    |  |        +----------+       
        25 >--|--- Rg --+----|----+  |        
              |         |    |    |  |             +---------+
              |-        |    |    |  +------ 19 -->|D        |
            +---+       |    |    |                |         |
            | D |       |    |    +--------- 29 --x|G        |
            +---+       |    |                     |         |
              |+        |    |                     |         |
              |     +------+ |                     |  MOS3   |
              |     | Cgso | |                     |   +     |
              |     +------+ |                     |  temp   |
              |         |    |                     |         |
              |         |    |                     |         |
        35 <--+-- Rs ---+----+-------------- 39 --<|SB       |
                                                   +---------+

    This is a huge class, but attempts to split it into two parts were
    unsatisfactory. Everything here is connected intricately.
    
    The exponential I{vs_n} is my (Ed's) own empirical figure (not
    AV-compatible, alas), not mentioned in T&M, since the
    excess-current reduction approach isn't. Would still expect the
    exponentials to be near or at 2.0 and 1.0, matching the gradual vd
    vs vd_max curves for electron and holes, respectively (T&M
    p. 249).

    @ivar vd_max: Maximum carrier velocity (cm/s), electrons &
        holes. From Quay et al. (2000). See also T&M p. 245.
    @type vd_max: tuple
    """
    Tj_max = 200 # Deg C, will burn up at this point
    
    # vd_max, vs_A from Quay et al. (2000)
    vd_max = (1.02e7,   0.72e7  )
    vs_A =   (0.74,     0.37    )
    vs_n =   (2.0,      1.0     )
    tpg = +1

    def __init__(self, specs, **kw):
        self.s = specs
        self.ex = expressions.Expressionist()
        self.mms = {}
        kw['arch'] = self.s.get('architecture')
        MOSFET_Physics.__init__(self, **kw)
        # Tempsens parallel current path goes unstable (?) when
        # T_chm*((Tnk/Tjk)^1.5 - 1) < -1
        #
        # So upper limit is T_chm = -1 / ((Tnk/Tj_max_ever)^1.5 - 1)
        self.Tm_max = -1.0 / ((self.Tnk/(self.Tj_max+self.Tc2k))**1.5 - 1)
    
    def params(self, f):
        """
        Defines fundamental parameter L{AV} objects:

            - I{m_L}: Channel length (m).

            - I{m_L2xj}: Multiplier to go from channel length I{m_L}
              to junction depth. T&M p. 257.

            - I{m_L2W}: Multiplier to go from channel length to
              width. Power MOSFETs can have literally meters of
              channel width inside the package, in the form of
              thousands of strips (e.g., ST Microelectronics's
              StripFET), repeated honeycomb structures (e.g.,
              Infinion's HexFET), or conventional VDMOS
              cells. Narrow-channel effects are not modeled, so
              there's no need to separate out individual cell widths,
              if there is even such a structure in the device.

            - I{m_tox}: Oxide thickness (m).

            - I{m_Bt}: Coefficient of Vgst/tox in denominator of
              effective channel mobility equation. T&M (p. 220)
              introduce this term as Beta_sub_theta and suggest its
              range is "typically 0.5 to 2 nm * V^-1." A value of zero
              would entirely eliminate the effect of higher Vgs
              reducing mu.
        
            - I{m_vsa}: Fitting factor for modest adjustment of
              maximum carrier velocity. "Most MOSFET models allow the
              value of |vd|max, and/or that of the 'critical field'
              Ec, to be chosen for best fit of model predictions to
              measured drain current values. The reason for this is
              that these parameters are difficult to measure. Also, in
              MOS transistor work, these theories are often applied in
              a simplified manner anyway, and this fact can be
              compensated to some degree by choosing parameter values
              for best fit with measurements" (T&M p. 246).

            - I{m_kappa}: Fitting factor for channel length
              modulation. The MOS3 model multiplies excess Vds (over
              Vds_sat), then calculates the hypotenuse of that with a
              voltage of some kind (?) that is expected at the nominal
              pinchoff point. T.H.Lee (2001), p. 27.

            - {m_NA}: The acceptor concentration (doping atoms per
              cm^3), of the P+ substrate (bulk).
        
        With I{tempsens} enabled for temperature sensitivity, the
        following are also defined, in L{channel}:

            - I{T_chm}: Scaling of channel mobility temperature
              dependence relative to non-saturated theoretical with
              1.5 power.

            - I{T_chv}: Coefficient for linear threshold voltage
              decrease with higher temperature.

        With an LDD, two more temperature sensitivity parameters are
        also defined, I{T_drm} and I{T_drs}. See L{drift_region}.

        @see: T&M pp. 9-10.
        """
        # -- Dimensions -------------------------------------------------------
        # T&M p. 45: "The channel width W and length L of individual
        # transistors can vary greatly (from a few tens of nanometers
        # to several hundred micrometers)."
        # Channel length (m)
        self.m_L = f.av('m_L', -8, -4, 'log')
        # The parameter m_L2W is the total channel width for all
        # cells, as a multiple of length. The AV object mm_W is the
        # total channel width in meters. The common usage of "length"
        # and "width" is misleading; channels are wider than they are
        # long, tens of millions of times wider in some power
        # MOSFETs. And power MOSFETS with approximately rectangular
        # gates repeat the channel structure in thousands of cells,
        # effectively multiplying the width.
        self.mm_W = f.av('m_L2W', +0, +8, 'log') * self.m_L
        self.mm_xj = f.av('m_L2xj', -2.1, +0.3, 'log') * self.m_L
        # 100 nm oxide thickness is ancient technology, but maybe
        # still used in power MOSFETS?
        self.m_tox = f.av('m_tox', -9.7, -6.9, 'log', 'hard')
        # -- Threshold and sub-threshold --------------------------------------
        self.m_eta = f.av('m_eta', -20, -1, 'log')
        self.m_nfs = f.av('m_nfs', -12, +13.5, 'log')
        # -- Secondary channel effects ----------------------------------------
        self.m_Bt = f.av('m_Bt', -28, -5, 'log')
        self.mm_vdmax = f.av('m_vsa', 0.5, 2.0) * self.npp(*self.vd_max)
        self.m_kappa = f.av('m_kappa', -7, +7, 'log')
        # -- Doping -----------------------------------------------------------
        # Intrinsic for Si is 1e10, lowest doping I've seen mentioned
        # is 1e14
        lower = +14
        # Transform degeneracy upper limit since this AV object will
        # be in log (actually log10) space
        upper = np.log10(self.N_upperLimit)
        self.m_NA = f.av('m_NA', lower, upper, 'log', 'hard')
        # ---------------------------------------------------------------------

    def _sameSuffix(self, suffix, thing):
        """
        Returns I{True} if I've already made a voltage source for the
        specified I{suffix}, with the same characteristic I{thing}. If
        so but with a different thing, raises an exception.
        """
        if suffix in self.mms:
            if self.mms[suffix] != thing:
                raise Exception(
                    "Can't define the same voltage source twice, differently")
            return True
    
    def mv_vacc(self, f):
        """
        Makes a voltage source I{mv_vacc} for an accumulation effect on
        the drift. Add to 1.0 to form the denominator of a variable
        drift resistance. Here's a schematic view of what happens::

                    +-------------------------------+
                    |       Accumulation part       |
            17 >--->|>>+>>>>>>>>>>>>>>>>>>>>>>>>>+>>|>----> 18
                    |  |     of drift region     |  |
                    +--|-------------------------|--+
                       |                         |
                       |  +------+     +------+  |
                       +->|-     |     |     -|<-+
                          | Diff |-+ +-| Diff |
                      +-->|+     | | | |     +|<--+
                      |   +------+ | | +------+   |
                      |            | |            |
            291 >-----+------------|-|------------+
                                   | |
                                   V V      
                                 +-----+    +----------+ 
                                 | Avg |--->| -V(m_aV) |---+
                                 +-----+    +----------+   |
                                                           |
                                   +--<---- mv_vgat ---<---+
                                   |
                                   |     +--------------+            
                                   +---->| V(m_aK)*()^2 |---> mv_vacc
                                         +--------------+
        
        Increases from 0.0 with I{m_aK} times the square of increasing
        gate voltage relative to accumulation region midpoint after
        threshold I{m_aV} is reached.

        For PMOS, the (negative) gate voltage relative to accumulation
        region midpoint is inverted. So, with the slightly negative
        drain voltage (relative to source) of a P-channel MOSFET in
        strong inversion, making the gate voltage more negative causes
        I{mv_vacc} to B{increase}, just as it would with more positive
        gate voltage gets the more positive internally.
        """
        if 'vacc' in self.mms: return
        self.mms['vacc'] = True
        expr_vga = sub("{}(V(291,17)+V(291,18))/2", self.npp('', '-'))
        f.ve('mv_vgat', "{}-V(m_aV)", expr_vga)
        self.ex.ap("V(mv_vgat) > 0")
        self.ex.ap("? V(m_aK)*(V(mv_vgat)^2)")
        self.ex.ap(": 0")
        f.ve('mv_vacc', self.ex.ep(" "))

    def mi_vsat(self, f, nmc, nto, nfrom, shunt):
        """
        Makes a B-source producing reverse current from node I{nfrom} to
        I{nto} to counteract current approaching or exceeding the
        saturation current limit defined by max-current node I{nmc}.

        Note that this does B{not} reduce the current flowing through
        the semiconductor region. Instead, it makes the region's
        resistance (between node I{nfrom} and I{nto}) B{appear} higher
        by limiting the net current flow between those terminals. The
        node I{nto} is named because current goes "to" the
        current-limiting circuitry, and gets pulled "from"
        it at node I{nfrom}.

        For PMOS, I{nfrom} and I{nto} are simply reversed,
        internally. The call to this method remains the same. You will
        have to reverse your shunt, however.

        Pre-limited current is measured through zero-valued voltage
        source with name I{shunt}.

        Here's how it works (direction of current flow for NMOS)::

                      +---------+       
            nto --+-->|+ shunt -|>--------------+
                  |   +---------+               |
                  |        |                    |
                  ^        |                    |
                  |        x                    |
                  |   +----------+              V
                  +--<|- B:Isat +|<--+   +---------------+
                      +----------+   |   |               |
                           x x       |   | Semiconductor |
                           | |       |   |  region       |
            nmc -----------+ |       ^   |               |
                             |       |   +---------------+
            Tj --------------+       |          V
                                     |          |
            nfrom <------------------+----<-----+

        When current through I{shunt} is much lower than maximum, as
        defined by the voltage at node I{nmc}, B:Isat produces very
        little reverse current. As the I{shunt} current approaches
        maximum, the reverse current through B:sat increases to more
        fully counteract the shunt current. The limit of the reverse
        current is the forward current minus the saturation
        current. Thus the upper limit of effective current flow is the
        saturation current.
        
        If temperature sensitivity is enabled, makes a voltage source
        that reduces the voltage at I{nmc} with higher temperature and
        uses that as the current limit.
        """
        nfrom, nto = self.npr(nfrom, nto)
        thing = (nfrom, nto, shunt)
        if self._sameSuffix(nmc, thing): return
        self.mms[nmc] = thing
        if self.s.ge('tempsens'):
            A = self.npp(*self.vs_A)
            mv = sub("mv_{}", nmc.lstrip('m_'))
            proto = "V({})/({:g}+{:g}*((V(tj)+{:g})/{:g}))"
            f.ve(mv, proto, nmc, 1-A, A, self.Tc2k, self.Tnk)
        else: mv = nmc
        expr_Imax = sub("V({})", mv)
        vs_n = self.npp(*self.vs_n)
        # Avoid errors due to negative currents, trial or
        # otherwise. Lots of them (setup 212 and ?) without this!
        self.ex.ap("i({}) < 0 ? 0 :", shunt)
        # Avoid errors due to huge trial currents during OP calculations
        self.ex.ap("i({}) > 1000*{}", shunt, expr_Imax)
        self.ex.ap("? i({}) - {}", shunt, expr_Imax)
        # This part is 2 at Imax, and with vs_n=2, is 5 at 2*Imax
        #                                |
        #                                |
        #                      /-------------------\
        proto = ": i({})*(1 - ((1 + (i({})/{})^{:g})^{:g}))"
        #                     \--------------------------/
        #                                  |
        #                                  |
        # With vs_n = 2, this part = 0.707 at Imax and 0.447 at 2*Imax.
        #
        # Thus the reverse current is 0.293 at Imax and 0.553 at 2*Imax.
        #
        # Thus the effective current is 70.7% of Imax with shunt
        # current = Imax, and is 89.4% of Imax with shunt current of
        # 2*Imax. With shunt current 10x Imax, effective current is
        # 99.5% of Imax.
        self.ex.ap(proto, shunt, shunt, expr_Imax, vs_n, -1.0/vs_n)
        # The Ngspice convention is for the current to go from the
        # left (first) node, through the source, to the right (second)
        # node. Left to right, like reading English.
        f.B(nfrom, nto, I=self.ex.ep(" "))
    
    def expr_temp_mu(self, Tm):
        """
        Returns an expression for the relative current in a parallel
        current path implementing temperature sensitivity of
        semiconductor mobility, based on the voltage source at node
        I{Tm}.

        The source at node I{Tm} defines the scaling of channel
        mobility temperature dependence relative to the
        (non-saturated) theoretical relationship::

            mu(Tj) = mu(Tn)*A*(Tn/Tj)^1.5

        where I{Tj} and I{Tn} are the junction and nominal (room)
        temperatures in Kelvin, and I{A} is the value of the source at
        node I{Tm}. If I{A} is 1.0, then exactly the theoretical
        1.5-power value is used (T.H. Lee 2001).

        The behavioral expression for the current in the parallel
        path, relative to the current in the primary path, is::

            I_rel = V(Tm)*((Tn/Tj)^1.5 - 1), when Tj < Tj_max
            otherwise I_rel = V(Tm)*((Tn/Tj_max)^1.5 - 1)
        """
        # Ratio, with lower limit at Tj_max
        self.ex.ap("{:g}", self.Tnk)
        self.ex.ap("(V(tj)+{:g})", self.Tc2k)
        expr_ratio = self.ex.ep("/")
        ratio_min = self.Tnk / (self.Tj_max + self.Tc2k)
        expr_ratio = self.ex.ifelse(
            expr_ratio, ratio_min, "V(tj) < {:g}", self.Tj_max)
        # Full expression
        self.ex.ap("V({})", Tm)
        self.ex.ap("(({})^1.5-1)", expr_ratio)
        return self.ex.ep("*")

    def expr_temp_vt(self, Tv):
        """
        Returns an expression for a voltage source to reduce threshold
        voltage with increased temperature based on the voltage source
        at node I{Tv}.

        The source at node I{Tv} defines the scaling of the
        reduction, a linear relationship to junction temperature in
        degrees C above nominal. (Or below, in which case the
        reduction becomes an increase.) T&M p. 225.

        Because the effect of increased temperature is to B{reduce}
        the threshold voltage, the voltage of a source using this
        expression is B{negative} with temperatures above nominal. It
        may be more clear to picture the source developing positive
        voltage drop to "soak up" some of the applied Vgs with
        temperatures colder than nominal, which increases effective
        threshold voltage. See the diagrams for L{drift_region} and
        L{channel} to see how the voltage source is inserted into the
        gate circuit.

        For PMOS, the voltage source is inverted, i.e., made
        B{positive} with temperatures above normal. That's because the
        effect of increased temperature is always to reduce the
        B{magnitude} of the threshold voltage, whether in NMOS or
        PMOS. A positive voltage source in series with the gate
        terminal of a P-channel MOSFET will make the gate more
        negative, thus reducing how negative the external gate
        terminal needs to be.
        """
        proto = self.npp("V({})*({:g}-V(tj))", "V({})*(V(tj)-{:g})")
        return sub(proto, Tv, self.Tnc)
    
    def body_diode(self, f):
        """
        Body diode, connected from source region to drain, or to N+
        epitaxial region for VDMOS::

            >-- 15 ----+
                       |-   
                      Diode*
                       |+   
                       |    
            <-- 35 ----+
        
        Only forward-biased diode behavior is modeled
        here. Reverse-bias behavior, including breakdown voltage, is
        modeled as leakage current in L{channel}.
        
        @see: L{diode.DiodeMixin}.
        """
        nc, na = self.npr(15, 35)
        self.sc_diode_fwd(f, na, nc, self.s.ge('transient'))

    def resistance(self, f):
        """
        Fixed resistances surrounding the MOSFET primitive::

                         +-----------------+
                         | { capacitance } |
                         +-----------------+
                              |    |    |
                              |    |    |              
            --> 15 -- Rd ---+-+----|----|---------> 16 
                            |      |    | 
                            |      |    | 
                            |      |    | 
            --> 25 -- Rg ---|----+-+----|---------> 29 
                            |    |      |              
                            | Rgs_leak  |              
                            |    |      |              
            <-- 35 -- Rs ---|--+-+------+---------< 39
                            |  |                       
                        +-----------+
                        | { diode } |
                        +-----------+

        Rs vs Rd
        ========

            Rd is the drain resistance, not drift resistance.
        
            For power MOSFETS, Rs is kept from being too much of a
            fraction of Rd. Not only do electrons have to travel much
            farther in the drift region for Rd, but the light doping
            there (<10% of NA in p+ region) makes its resistivity much
            higher than that of the p+ source region for Rs. The fact
            that it has more cross-sectional area than the source
            region does not compensate much for those two factors.
    
            Zheng Yang ("Power MOSFET," ECE442 handout) has VDMOS
            source plus source contact resistivity at 0.06 mOhm/cm^2,
            with most of that being from the contact, and drift plus
            substrate plus drain contact (all part of I{rd}) being
            0.41 mOhm/cm^2. (That doesn't include accumulation
            resistance he puts at 0.66 mOhm/cm^2 and JFET resistance
            at 0.19 mOhm/cm^2.) This corresponds to an I{rs}/I{rd}
            ratio of about 15%.
    
            For UMOS, Zheng Yang has source plus contact at 0.0505
            mOhm/cm^2, with the source part vanishingly small. Drift
            plus substrate drain contact is 0.27 mOhm/cm^2 (not
            including accumulation resistance he puts at 0.055
            mOhm/cm^2). This corresponds to an I{rs}/I{rd} ratio of
            about 19%.

        Gate Leakage
        ============
        
            Modeling gate leakage would require integrating gate
            current density vs channel position (T&M pp. 297-98). Not
            gonna happen. The next obvious answer is to use very high
            value resistances, from gate to drain and gate to source,
            to do a rough modeling. But the problem there is that the
            resistances would provide a conduction path from drain to
            source, swamping the drain-source leakage current.

            Thus a single resistance, from gate to source, is used,
            and no gate-drain leakage current is modeled, current at
            I{Vgs_max} being a multiple of actual rated I{Ig_leakage}
            to slightly compensate for log-space behavior of actual
            leakage vs Vgs.
        
        """
        # -- Gate series resistance and leakage -------------------------------
        Rg = f.av('rg', 0.5, 40) if self.s.ge('transient') else 1.0
        f.R(25, 29, Rg)
        f.R(29, 39, 0.1*self.Rg_leakage) # Gate to source only
        # -- Source and drain -------------------------------------------------
        rsVSrd = 0.15 if self.has_ldd else 0.5
        # Ohmic drain resistance, mostly from N- drift region near drain.
        Rd = f.av('rd', 0.0, 0.6*self.Rds_on)
        f.R(15, 16, Rd)
        # Source resistance to channel. For components with higher
        # voltage ratings, the drift region (part of drain resistance)
        # almost entirely dominates.
        Rs = f.av('rs', 0.0, 0.5*self.Rds_on)
        f.R(35, 39, Rs)
        # ---------------------------------------------------------------------
        
    def capacitance(self, f):
        """
        Drain-gate capacitance::
                                                     
            --> 16 ---------+-----------+------------+-----+
                            |           |            |     |            
                            |           ^            ^     |            
                            |        +-----+      +-----+  |               
                         ------      |  +  |      |  +  |  | 
                          Cgdo   +--x| FI1 |  +--x| FI2 |  |         
                         ------  |   |  -  |  |   |  -  |  |   +-----+   
                            |    |   +-----+  |   +-----+  |   |     |   
                            |    |      ^     |      ^     +--x|+   +|--+  
                            |    |      |     |      |         |  E  |  |        
            --> 29 ---------+----|------+-----|------+--------x|-    |  |
                                 |            |                |     |  |
                                 |            +-----------+    +-----+  |
                                 |                        |             | 
                  +------+-------|------- 210 ---+--------|-------------+ 
                  |      |       |               |        |                
                  |    ------    |             +---+      |                
                  |     Crss     |             | R |      |                
                  |    ------    |             +---+      |                
                +---+    |       |               |        |                
                | R |   211      |           205 +--------|-------+        
                +---+    |       |               |        |       |        
                  |      ^       |            +-----+     |    +-----+     
                  |   +------+   |            |  -  |     |    |  -  |     
                  |   |  -   |   |            |  D3 |     |    |  D2 |     
                  |   | VFI1 |---+            |  +  |     |    |  +  |     
                  |   |  +   |                +-----+     |    +-----+     
                  |   +------+                   |        |       |
                  |      ^                       |   +--------+   |    
                  |      |     +------+          +-->|+ VFI2 -|>--+ 204 
                  +------+---->|- D4 +|>---------+   +--------+ 
                     206       +------+          |                                 
                                                 0
        
        Adapted from App. Note AND9033, On Semiconductor.

        Conventional current flow: v#branch is + if current ENTERS
        its + terminal, i.e., making its + terminal more positive.
                                                              
        """
        # -- Fixed capacitances -----------------------------------------------
        # Crss = Cgd
        Cgd = f.av('mt_cgdo', 0.0, 3.0*self.Crss_min)
        f.C(29, 16, Cgd)
        # -- Variable part of Cgd ---------------------------------------------
        diode_ideal = f.MODEL('ideal', 'D', N=0.005, IS=1E-13, IKR=1E-15)
        # Adapted from App. Note AND9033, On Semiconductor
        # Conventional current flow: v#branch is + if current ENTERS
        # its + terminal, i.e., making its + terminal more positive.
        # Non-linear capacitors (Figure 1)
        f.FI1(29, 16, 'vfi1', 1.0) # Current entering shunt vfi -> Igd
        f.FI2(29, 16, 'vfi2', 1.0)
        # Control circuit for non-linear caps (Figure 4).
        f.E(210, 0, 16, 29, 1.0) # Eq. 7
        f.D4(*self.npr(0, 206, diode_ideal))
        # With Vgs > Vds, current enters vfi1
        f('vfi1', 206, 211, 0)
        av = f.av('mt_crss', 0.05*self.Crss_max, 4.0*self.Crss_max)
        f.C(211, 210, av)
        f.R(206, 210, 1.0)
        f.R(210, 205, 1.0)
        ts = f.get(self, 'ts')
        if ts: f.C(205, 0, ts)
        f.D3(*self.npr(0, 205, diode_ideal))
        f('vfi2', 0, 204, 0)
        # NOTE: Maximum M is 0.9; SPICE limits beyond that
        diode_md1 = f.MODEL(
            'md1', 'D', CJP=0,
            CJO=av, FC=0.5, RS=1E-6,
            VJ=f.av('mt_vj', 0.01, 1.0)*1.999999,
            M=f.av('mt_m', 0.1, 0.9))
        f.D2(*self.npr(204, 205, diode_md1))

    def drift_region(self, f):
        """
        Lightly doped drift region, which adds quasi-saturation and
        Vgs-independent current limiting behavior (separate velocity
        saturation) to power MOSFETs.

        Modeled with a behavioral voltage source for accumulation
        region, a JFET for quasi-saturation, an inner current feedback
        path for mobility reduction with increased temperature, and an
        outer current feedback path for velocity saturation::
                                             
                     +--------+          +--------+       
            16 --+-->|+ Vsh1 -|>-----+-->|+ Vsh2 -|>------------- 17 -----+
                 |   +--------+      |   +--------+                       |
                 |       |          167     |                             V
                 ^       |           |      |        +--------+   291  +------+
            29 --|-------|-----------|------|-------x| B:dVt +|-------x| B:Ra |
                 |       |           |      |        |       -|--+     |      |
                 |       |           |      |        +--------+  |     +------+
                 |       |           V      x              x     0         V
                 |       |           |   +---------+       |               |
                 |       |           +-->| B:Itemp |>--+   |               |   
                 |       |               +---------+   |   |    +----+  18 |
                 |       |                      x      +--------| Rp |-----+
                 |       x                      |      |   |    +----+     |
                 |   +--------+               +-|---<--+   |               V
                 +--<| B:Isat |<--+           | +----------+          +--------+
                     +--------+   |           |            |          |    D   |
                          x       |   +-----+ | 391 +---+  |  392     |        |
            39 -----------|-------|--x| E  +|-|-----| R |--|----+----x|G  JFET |
                          |       +--x| x1 -|-+     +---+  |    |     |        |
                          |       |   +-----+ |            |  +---+   |    S   |
                          |       |           |            |  | C |   +--------+
            Tj -----------+-------|-----------|------------+  +---+        V
                                  |           |                 |          |
                                  |           |                 |          | 
            19 -------------------+-----------+-----------------+----------+

        B{Note}: There really is supposed to be a negative sign at the
        output of the zero-volt shunts. This is consistent with the
        Ngspice convention for a current-controlled source: "The
        direction of positive controlling current flow is from the
        positive node, through the [voltage] source, to the negative
        node" (4.2.4).
        
        The idea behind the JFET is that excessive voltage V(19,39)
        across the intrinsic MOSFET channel will raise the JFET's
        source voltage with respect to its gate voltage, reducing its
        Vgs. That will drop more voltage across the JFET in
        compensation.

        Adds the following parameters:

            - I{m_aK}: Accumulation effect of gate voltage reducing
              Ra. One plus twice the square of I{m_aK} is how much the
              average gate voltage (minus I{m_aV}), referenced to the
              midpoint of the accumulation region (Vga), reduces Ra.

            - I{m_aR}: Zero-bias drift region resistance Ra in the
              accumulation region, between the channel and JFET
              region, in Ohms. This will typically be much higher than
              I{Rds_on}; the accumulation of electrons in the lightly
              doped drift region under the gate (Vga) causes it to be
              much more conductive when it is under a gate voltage at
              which I{Rds_on} is rated.
        
            - I{m_aV}: Threshold gate-source voltage at which
              accumulation effect begins. Vga at or below this has no
              effect. (Depletion perhaps should be modeled, but isn't.)
        
            - I{m_dB}: Scaling up or down of JFET's nominal Beta
              value, given the computed Kp. The (somewhat implausible)
              lower limit of zero equals no JFET effect at all, with
              all the current going through the parallel resistance
              defined by I{m_dR}.

            - I{m_dI}: Maximum (velocity saturated) Ids, regardless of
              Vgs.

            - I{m_dL}: JFET LAMBDA parameter, relative to the
              intrinsic MOSFET's I{m_kappa} channel-length modulation
              parameter.

            - I{m_dR}: Drain region resistance Rp in parallel with and
              unaffected by JFET behavior. Relative to I{Rds_on}. For
              a vertical architecture with no JFET effect, i.e.,
              trench VMOS, this region is still present and the
              parameter has an effect.
        
            - I{m_dV}: Scaling up or down of JFET's nominal VTO value,
              given the maximum Ids.

        With I{tempsens} enabled for temperature sensitivity, the
        following is also defined:
        
            - I{T_drm}: Scaling of drift region mobility temperature
              dependence relative to non-saturated theoretical with
              1.5 power.

            - I{T_drv}: Coefficient for linear accumulation threshold
              voltage decrease with higher temperature.
        
        See, Robert S. Scott, Garhard A. Franz, and Jennifer
        L. Johnson (1991); Canzhong He, James Victory, et al. (2017).

        For temperature dependence of semiconductor saturation
        velocity, R. Quay, C. Moglestue, et al. (2000).
        """
        f.vav('m_aK', -9.0, +0.6, 'log')
        f.vav('m_aR', 0.0, 5*self.Rds_on)
        f.vav('m_aV', -11.0, 8.0) # TODO: Tie to specs?
        I_max = self.s.g.Id_max
        if not I_max:
            raise ValueError(
                "Maximum simulated drain current Id_max must be specified")
        m_dI = f.vav('m_dI', I_max, 2.5*I_max)
        # Reversing Vsh1 for PMOS is necessary because mi_vsat does
        # unidirectional current limiting
        f.Vsh1(*self.npr(16, 167, 0))
        # Not necessary to reverse Vsh2 for PMOS because it's only
        # used for bidirectional stuff
        f.Vsh2(167, 17, 0)
        if self.s.ge('tempsens'):
            # -- B:Itemp ---------------------------------
            f.vav('T_drm', 0.4, self.Tm_max, 'hard')
            expr = self.expr_temp_mu('T_drm')
            # Unfortunately, this can go unstable and shove a ton of
            # current backwards into node 167, causing drain voltage
            # to spike up to BV.
            f.B(167, 19, I=sub("i(vsh2)*{}", expr))
            # -- B:dVt -----------------------------------
            f.vav('T_drv', 2e-4, 1.5e-2)
            expr = self.expr_temp_vt('T_drv')
            f.ve(291, "V(29)-{}", expr)
            f.R(291, 0, 1)
            # --------------------------------------------
        else: f.R(29, 291, 0)
        # -- B:Ra -------------------------------------------------------------
        self.mv_vacc(f)
        f.B(17, 18, V="i(vsh2)*V(m_aR)/(1+V(mv_vacc))")
        f.R(17, 18, 1)
        # -- B:Isat -----------------------------------------------------------
        self.mi_vsat(f, 'm_dI', 16, 19, 'vsh1')
        # -- Vertical drift region --------------------------------------------
        m_dR = f.av('m_dR', -2.5, +0.7, 'log')
        # Fixed resistance, in parallel with any JFET, modeling
        # silicon region subject to velocity saturation but free of
        # JFET effect
        f.R(18, 19, m_dR*self.Rds_on)
        if not self.has_jfet:
            return
        # Isolate JFET drain-gate leakage path
        f.E(391, 19, 39, 19, 1)
        # Gate LPF for SCA if ts defined
        ts = f.get(self, 'ts')
        if ts:
            ng = 392
            # LPF for SCA, JFET area seems particularly fussy for SPICE
            f.R(391, 392, 1.0)
            f.C(392, 19, ts)
        else: ng = 391
        # The JFET
        m_dB = f.av('m_dB', -2.5, +3.0, 'log')
        m_dL = f.av('m_dL', -15, +2, 'log')
        m_dV = f.av('m_dV', -1.4, +0.3, 'log')
        Beta = self.Kp(self.mm_W, self.m_L, self.m_NA, self.m_tox)
        VTO = Beta**-0.5 * m_dI**0.5 # AVC, does not need to be negative
        model = f.MODEL(
            'drift_jfet', self.npp('njf', 'pjf'),
            level=1, BETA=m_dB*Beta, VTO=m_dV*VTO, LAMBDA=m_dL*self.m_kappa)
        #    D   G   S
        f.J(18, ng, 19, model)
        # ---------------------------------------------------------------------
        
    def channel(self, f):
        """
        Drain-source current through the channel, modeled with a Level 3
        MOSFET primitive and parallel current source modeling
        temperature sensitivity::

                     +------+          
            19 --+-->| Vsh3 |>-- 191 --------------------------------+------+
                 |   +------+                                        |      |
                 |       |                                           |   +----+
                 |       x                                           |   | Rp |
                 |   +----------+                                    |   +----+
                 +-->|+ B:temp -|>--+                                V      |
                     +----------+   |                          +---------+  |
                           x        |                          |     D   |  |
                           |        |   +---------+            |         |  |
            29 ------------|--------|-->|+ B:dVt -|>-- 292 ---x|G   MOS3 |  |
                           |        |   +---------+            |         |  |
                           |        |        x                 |     S   |  |
                           |        |        |                 +---------+  |
            Tj ------------+--------|--------+                       V      |
                                    |                                |      |
            39 ---------------------+--------------------------------+------+

        The B-source I{B:dVt} drops voltage on the way from the gate
        to the MOSFET primitive's gate terminal. Since its voltage is
        positive when temperature is lower than nominal, it has the
        effect of increasing threshold of a cold device. It has
        negative voltage when temperature is warming than nominal,
        effectively decreasing threshold of a hot device.

        An ideal voltage-mode B-source has zero impedance, so the
        capacitance modeled by the MOS3 primitive from node 292 to
        nodes 191 and 39 will still be "seen" at node 29.

        The B-source I{B:temp} adjusts the total channel current based
        on I{tj} to model (1) the reduction in mobility with
        temperature, and (2) the increase in leakage current with
        temperature.

        Rp sets a floor for drain-source leakage current. Still
        included (for SCA), but only as a very high fixed value, if my
        I{has_Rp} property is not C{True}.
        """
        f.Vsh3(19, 191, 0)
        if self.s.ge('tempsens'):
            # -- B:temp -------------------------------------------------------
            # Current adjustment to model reduction in channel
            # mobility with higher tj
            f.vav('T_chm', 0.2, self.Tm_max, 'hard')
            self.ex.ap("i(vsh3)*{}", self.expr_temp_mu('T_chm'))
            # Current increase over baseline leakage to model increase
            # with higher tj (this simply adds to baseline leakage
            # without caring what it is)
            f.vav('T_chl', -8, -2, 'log')
            # If your MOSFET is running hotter than +200 degrees C,
            # you have a problem
            self.ex.ap(
                "V(19,39)*V(T_chl)*(V(tj) > 200 ? 1 : exp(0.08*(V(tj)-200)))")
            # Linear combination
            f.B(19, 39, I=self.ex.ep(" + "))
            # -- B:dVt --------------------------------------------------------
            # Voltage adjustment to model reduction in threshold with higher tj
            f.vav('T_chv', 1e-3, 2e-2)
            f.B(29, 292, V=self.expr_temp_vt('T_chv'))
            f.R(29, 292, 1) # SCA
            # -----------------------------------------------------------------
        else: f.V(29, 292, 0)
        kw = {
            'level':    3,
            'tpg':      +1, # N- polysilicon gate (or N+ for PMOS)
            'tox':      self.m_tox,
            'nsub':     self.m_NA,
            'nfs':      self.m_nfs,
            'xj':       self.mm_xj,
            'uo':       self.mu(self.m_NA),
            'vmax':     self.mm_vdmax,
            'theta':    self.theta(self.m_Bt, self.m_tox), # T&M p. 220
            'eta':      self.m_eta,
            'kappa':    self.m_kappa,
        }
        if self.s.ge('transient'):
            # Wi is the inverse (reciprocal) of total channel width
            Wi = self.mm_W**-1
            kw['cbd'] = f.av('mt_cbd', 0, 7.0) * self.Cj_min
            kw['cgso'] = f.av('mt_cgso', 0, 3.0) * Wi * self.Ciss_min
        primitive = f.MODEL('channel', self.npp('nmos', 'pmos'), **kw)
        #     D    G   S   B  
        f.M(191, 292, 39, 39, primitive, L=self.m_L, W=self.mm_W)
        Rp = f.av('m_Rp', +8, +19.9, 'log') if self.has_Rp else 1e22
        f.R(191, 39, Rp)
    
    def setup(self, f):
        """
        Call this to construct a circuit with all my stuff.
        """
        self.params(f)
        # Body diode: Bypasses source resistance, channel,
        # accumulation, and JFET regions, and, when forward-biased,
        # drift resistance
        if self.s.ge('body_diode'):
            self.body_diode(f)
        # Drain, gate, and source static resistance
        self.resistance(f)
        # Drain-gate cpacitance, modeled separately due to intervening
        # drift region stuff
        if self.s.ge('transient'):
            self.capacitance(f)
        # Shunt for measuring drain current
        # Drift region
        if self.has_ldd:
            self.drift_region(f)
        else: f.R(16, 19, 0)
        # Finally, the channel
        self.channel(f)
