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
The L{Constraints} base class makes it easier for you to enforce
parameter constraints.
"""

import numpy as np
from pingspice.util import *


class Constraints(object):
    """
    Subclass me and define one or more constraint-checking
    methods.

    Register the methods to be used with a given instance of that
    subclass by defining a I{registry} dict in your subclass, keyed by
    method name. Each entry must have a 2-sequence, with the first
    item being linear parameter names (or C{None}) and log-space
    parameter names (or C{None}) for the constraint method.

    You can define instance attributes via constructor keywords.

    To just add a raw constraint function that gets called without any
    parameter transformations, use L{append}.

    @cvar debug: Set C{True} to have failing constraints shown with
        parameters. (Debugging only.)
    """
    debug = False
    
    def __init__(self, **kw):
        for name in kw:
            setattr(self, name, kw[name])
        self.cList = []
        for methodName in self.registry:
            func = getattr(self, methodName)
            self.cList.append([func]+list(self.registry[methodName]))
        self.fList = []
    
    def __len__(self):
        return len(self.cList) + len(self.fList)

    def __nonzero__(self):
        return bool(self.cList) or bool(self.fList)
    
    def __iter__(self):
        """
        Iterating over an instance of me yields wrappers of my
        constraint-checking functions registered in my I{cList}, plus
        any raw functions registered in my I{fList} with calls to
        I{append}.

        Each wrapper automatically transforms any log parameters into
        their linear values before calling the wrapped
        constraint-checking function with a revised parameter
        dict. Also, if a parameter is not present, forces a C{True}
        "constraint satisfied" result so that setting a parameter to
        known doesn't cause bogus constraint checking.

        @see: L{analysis.param.Setups}, whose constructor treats an
            instance of me like a list, using iteration and appending.
        """
        def wrapper(params):
            if linearParams:
                if not linearParams.issubset(params):
                    return True
                for name in linearParams:
                    if name not in newParams:
                        newParams[name] = params[name]
            if logParams:
                if not logParams.issubset(params):
                    return True
                for name in logParams:
                    if name not in newParams:
                        newParams[name] = np.power(10.0, params[name])
            result = func(newParams)
            if self.debug:
                print sub("BOGUS: {}, {}", func.__name__, newParams)
            return result
        
        newParams = {}
        for func, linearParams, logParams in self.cList:
            yield wrapper
        for func in self.fList:
            yield func

    def append(self, func):
        self.fList.append(func)
