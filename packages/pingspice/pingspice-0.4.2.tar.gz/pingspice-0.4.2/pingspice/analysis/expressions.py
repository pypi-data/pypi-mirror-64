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

from pingspice.util import *


class Expressionist(object):
    """
    I help you build some complex B-source expressions. Used by
    L{MOSFET_Model}.
    """
    def __init__(self):
        self.eParts = []
    
    def ap(self, *args, **kw):
        """
        B{A}ppends a B{p}art to my list of expression parts I{eParts}.
        Call with a string, or a string prototype and args, to add an
        expression part.

        If I{joinWith} is specified, then the expression from my
        current list of parts (including the one from this method
        call) is built and returned, and the list is cleared. You can
        include the other keywords accepted by L{ep}.
        """
        self.eParts.append(sub(*args))
        joinWith = kw.get('joinWith', None)
        if joinWith:
            return self.ep(**kw)

    def ep(self, joinWith="", suffix=None, new=False, paren=None):
        """
        Build the expression from my list of parts I{eParts}, clears the
        list for another build, and returns the built expression.

        If I{new} is set C{True}, puts the new expression back into
        myself as the first part of a new list of expression
        parts. (It is still returned.)

        If I{paren} is set C{True}, the expression is wrapped inside
        parentheses. If I{paren} is set to a non-blank string, that
        string precedes the parentheses with no space.
        """
        expr = joinWith.join(self.eParts)
        del self.eParts[:]
        if suffix: expr += suffix
        if paren:
            prefix = "" if paren is True else paren
            expr = sub("{}({})", prefix, expr)
        if new: self.ap(expr)
        return expr

    def ifelse(self, expr_yes, expr_no, proto_test, *args):
        """
        Returns an expression for selecting I{expr_yes} if Ngspice
        evaluates I{expr_test} as C{True}, else I{expr_no}.
        """
        self.ap(proto_test, *args)
        self.ap("? {}", expr_yes)
        self.ap(": {}", expr_no)
        return self.ep(" ")
    
    def lowerLimit(self, A, expr_x, expr_limit=None, expr_test=None):
        """
        Returns an expression for an expression that is numerically robust
        and implements a soft lower limit, at I{expr_limit} if
        specified, otherwise zero.

        You must surround I{expr_x} with parentheses if it is a sum or
        difference.

        The limiter output is log(2)/A when the value of I{expr_x}
        equals that of I{expr_limit}.

        Uses different limiter expression depending on whether
        I{expr_test} is positive or negative. If I{expr_test} is not
        specified, M{expr_x - expr_limit} is used.

        @see: T&M (10.4.6) p. 612.
        """
        if expr_limit is None:
            expr = expr_x
        else: expr = sub("({}-{})", expr_x, expr_limit)
        self.ap(expr_x)
        self.ap("{:g}*log(1+exp({:g}*{}))", 1.0/A, -A, expr)
        expr_pos = self.ep("+")
        expr_neg = sub("({:g}*log(1+exp({:g}*{})))", 1.0/A, A, expr)
        return self.ifelse(
            expr_pos, expr_neg,
            "{} > 0", expr if expr_test is None else expr_test)
    
    def zeroLimit(self, A, expr_x, expr_test=None):
        """
        Returns an expression for a numerically robust expression that
        implements a soft lower limit at zero.

        The limiter output is log(2)/A when I{expr_x} is zero.

        @see: T&M (10.4.6) p. 612.
        """
        return self.lowerLimit(A, expr_x, expr_test=expr_test)
