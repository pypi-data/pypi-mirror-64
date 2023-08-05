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
Python-only simulations.
"""

import re

import numpy as np
from twisted.internet import defer, reactor

from pingspice.circuit.av import AV, AV_Error
from pingspice.analysis.names import ParameterNamer
from pingspice.analysis.vectors import Vectors_Python
from pingspice.analysis.sim import AnalyzerBase
from pingspice.util import *


class Analyzer(AnalyzerBase):
    """
    I am an analyzer for simulating results with a Python callable, in
    those cases where there's no need for Ngspice simulation.

    No constructor is used; your subclass is welcome to have one,
    e.g., L{lib.thermal.SeriesResistanceAnalyzer.__init__}.
    
    Before using me, you can define AV objects I use with a call to
    L{avDefine}. It accepts as a single argument instance of
    L{av.AV_Maker}, with the very useful C{f.av} method. Then,
    also before using me, set me up with a call to L{setup}.

    The callable you override my L{func} method with must accept as
    its arguments a Numpy array for each independent vector I produce
    for it, and as its keywords all current parameter values from the
    avList, determined from the values that are supplied to each call
    of my instance. It must return either a single SSE scalar or a
    tuple with one Numpy array for each vector represented by the
    names in I{vectorNames}, excluding any independent vectors.

    @ivar timeout: Defines how long I will wait for a result from my
        (subclassed) evaluation L{func}, run in a thread.

    @ivar absVals: Set to a sequence with the names of all vectors
        whose raw vector values are always treated as positive
        numbers. See L{VectorsBase}.
    """
    @property
    def V(self):
        if not hasattr(self, '_V'):
            self._V = Vectors_Python(self)
        return self._V
    
    @defer.inlineCallbacks
    def setup(self, ID, vectorNames, avList, *sweeps):
        """
        Call this before using me. Returns a C{Deferred} that fires when
        I'm ready, with a reference to me if all went OK or C{None} if
        not.

        @param ID: An integer ID for the analysis setup I am handling.

        @param vectorNames: A list of the vector names I am handling.

        @param avList: A reference to a shared list of AV objects.

        @param sweeps: Triads of values (not tuples) defining DC-style
            sweeps of values for each independent vector: I{start},
            I{stop}, I{increment}.
        """
        self.ID = ID
        self.V.nm.add(vectorNames)
        self.avList = avList
        status = Bag(True)
        for k, name in enumerate(getattr(self, 'toSweep', [])):
            try:
                sweep = sweeps[3*k:3*(k+1)]
            except:
                status(False)
                break
            if sweep:
                d = deferToThread(self.V.doSweep, name, *sweep)
                d.addErrback(lambda _: status(False))
                yield d
        # Ready for business
        if self.dLock.locked: self.dLock.release()
        defer.returnValue(self if status() else None)

    def addName(self, name, k=None):
        """
        Call after L{setup} to adds a vector with I{name} to my
        L{Vectors_Python} object I{V}.

        Returns a C{Deferred} that fires immediately. (This is for
        consistency with L{sim.Analyzer.addName}, which may have to
        talk with Ngspice when adding a vector name.)

        @keyword k: Set this to an integer to have the name inserted
            at a specific position in the names list of my
            L{Vectors_Python} object's L{NameManager} rather than
            appended. The order isn't usually important, but does
            affect the result of a call to L{VectorsBase.array}.
        """
        if not hasattr(self, 'ID'):
            raise RuntimeError("Call only after setup has run ")
        self.V.addName(name, k)
        return defer.succeed(None)
        
    def shutdown(self):
        return self.dLock.acquire().addCallback(lambda _: self.dLock.release())
    
    def __repr__(self):
        return sub("<Python Analyzer {}>", self.__class__.__name__)

    def __getstate__(self):
        return {'toSweep': getattr(self, 'toSweep', [])}

    def __setstate__(self, state):
        for name in state:
            setattr(self, name, state[name])
    
    def avDefine(self, f):
        raise NotImplemented()

    def func(self, *args, **kw):
        raise NotImplemented()

    def scheduleSweep(self, name):
        """
        Call this with the name of each independent vector and, during
        setup, I'll do a sweep for it based on the next three values
        in my stash of unused sweep args
        """
        if not hasattr(self, 'toSweep'):
            self.toSweep = []
        self.toSweep.append(name)
        
    @defer.inlineCallbacks
    def __call__(self, *args, **kw):
        """
        Call my instance with a list of float values (or sub-lists of
        floats in the case of vector values) to populate my
        L{Vectors_Python} object I{V} with vectors from Python-only
        analysis.

        The total number of items in the list must equal the total
        number of names supplied to those setup method calls. If no
        alterables have been defined, then an empty list is what's
        acceptable (the default if no arg is supplied).

        After I alter these values and/or parameters and I do the
        analysis, the returned C{Deferred} will fire with a reference
        to my L{Vectors_Python} instance. It will contain the
        resulting Numpy vectors, unless the value is out of a defined
        range or produced a Numpy error.

        Any keywords supplied are ignored.
        """
        def timedOut(failureObj, *args):
            self.V.error(failureObj)
            
        def null(*args):
            pass
            
        def fAV(av, value):
            if av.isParent():
                name = av.name
                if name in params:
                    if value == params[name]: return
                    raise AV_Error(
                        "Tried redefining the value for parameter '{}' from "+\
                        "{} to {}", name, params[name], value)
                params[name] = value

        if len(args) > 1:
            raise ValueError(sub(
                "Call a {} instance with zero or one arg", self))
        yield self.dLock.acquire()
        # Process the alterable values (if any) in the proper order
        values = args[0] if args else []
        self.checkValues(values)
        params = {}
        yield self.alterations(values, null, null, fAV)
        d = self.V(params)
        if self.maxWait:
            d.addTimeout(self.maxWait, reactor, onTimeoutCancel=timedOut)
        yield d
        # Get and "return" the results
        if not self.V:
            paramNames = params.keys()
            pn = ParameterNamer(paramNames)
            msg(-1, pn.prettyValues(
                [params[name] for name in paramNames],
                "WARNING: Bogus result from {} with", self))
        V = self.V.copy()
        self.dLock.release()
        defer.returnValue(V)
