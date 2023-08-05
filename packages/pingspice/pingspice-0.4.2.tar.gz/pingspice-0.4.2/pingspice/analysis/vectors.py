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
Vectors containers for simulation analysis.
"""

import re, os.path

import numpy as np
from twisted.internet import defer, reactor

from asynqueue.iteration import Delay

from pingspice.circuit.av import AV, AV_Error, AV_ListHolder
from pingspice.ngspice.runner import NgspiceRunner
from pingspice.ngspice.misc import ShuttingDownToken, NgspiceError
from pingspice.util import *


class NameManager(object):
    """
    I manage your vector names.

    This can be a bit of a hassle, considering Ngspice's
    fussiness. Also, I allow for a '+' prefix in front of a name,
    which indicates that its absolute value is what the analysis is
    concerned with.

    @see: L{Formatter}.
    """
    fmt = Formatter()

    def __init__(self):
        """
        C{NameManager()}
        """
        self.names = []
        self.cnames = {}
        self.absVals = set()

    def __call__(self, name):
        """
        Call my instance with a name to get the canonical version of it
        (which may be the same).
        """
        if name in self.cnames:
            return self.cnames[name]
        return self.fmt.toCanonical(name)

    def cnameList(self):
        """
        Returns the canonical versions of my I{names}. The list is ordered
        in the order that names were added with calls to L{add}.
        """
        return [self.cnames.get(x, x) for x in self.names]
    
    def add(self, nameOrNames, k=None):
        """
        Adds the the supplied vector name or sequence of names to my list
        of I{names}. Also adds an entry for the canonical name to my
        I{cnames} dict, keyed by the original name.

        Returns the canonical version(s) of the name(s).

        If a name is already present in my list, it will not be
        added. (But it will have its canonical name registered in my
        I{cnames} dict; doing that repeatedely does no harm.) Repeated
        calls with the same argument has no additional effect, even if
        you specify a different list position I{k}.

        @keyword k: Set this to an integer to have the name inserted
            at a specific position in my names list rather than
            appended.
        """
        names = [nameOrNames] \
          if isinstance(nameOrNames, str) else nameOrNames
        for name in names:
            if name in self.cnames:
                continue
            cname = self.fmt.toCanonical(name)
            if name.startswith('+'):
                self.absVals.add(cname)
            if cname not in self.names:
                if k is None:
                    self.names.append(cname)
                else: self.names.insert(k, cname)
            self.cnames[name] = cname
        cnames = [self.cnames[x] for x in names]
        return cnames[0] if len(cnames) == 1 else cnames

    def isAbs(self, name):
        """
        Returns C{True} if the specified I{name} has been added with a
        call to L{add} and has a '+' prefix, indicating an absolute
        value.
        """
        return name in self.absVals


class VectorsBase(object):
    """
    I am an abstract base class for C{Vectors} that provides a
    convenient common interface for accessing both Python-only and
    Ngspice simulation results.

    Vectors (1-D Numpy arrays) can be accessed as my attributes, so
    long as their names don't include characters like "-" or "(" that
    are forbidden to Python variables, or as mapping-style elements.
    """
    @property
    def nm(self):
        """
        Property: My L{NameManager}, newly constructed if I did't have one
        yet.
        """
        if not hasattr(self, '_nm'):
            self._nm = NameManager()
        return self._nm
    @nm.setter
    def nm(self, x):
        self._nm = x
    @nm.deleter
    def nm(self):
        del self._nm
    
    def __contains__(self, name):
        """
        Dict-like access to my I{values}: Whether I{name} is included.
        """
        if name is None:
            return None in self.values
        return self.nm(name) in self.values
    
    def __len__(self):
        """
        Dict-like access to my I{values}: The number of vectors and
        perhaps +1 for a C{None} entry.
        """
        return len(self.values)

    def __iter__(self):
        """
        Dict-like access to my I{values}: Iterates over vector names plus
        perhaps C{None} for a L{psim.Analyzer} instance.
        """
        for name in self.values:
            yield name

    def __getitem__(self, name):
        """
        Dict-like access to my I{values}, with scaling done from unity
        except for a I{None} item, which is an SSE from a
        L{psim.Analyzer} instance.
        """
        def doScaling(name):
            coeff = 1.0
            if name.startswith('-'):
                coeff = -1.0
                name = name[1:]
            if '*' in name:
                scale, name = [x.strip() for x in name.split('*')]
                coeff *= float(scale)
            return name, coeff

        if name is None:
            return self.values[None]
        name, coeff = doScaling(name)
        name = self.nm(name)
        if name not in self.values:
            raise KeyError(sub(
                "{}: No vector '{}' among vectors {}",
                repr(self), name, ", ".join(self.values.keys())))
        if coeff != 1.0:
            # This consumes memory, so only do it for non-unity
            # coefficients
            return coeff * self.values[name]
        return self.values[name]

    def __setitem__(self, name, value):
        """
        Replace the existing numpy vector specified by I{name} with
        another.

        This is only for modifying my existing contents; raises an
        exception if you try to set a new vector with this mechanism.
        """
        name = self.nm(name)
        if name not in self.values:
            raise LookupError(sub("No existing vector '{}'!", name))
        self.values[name] = value
    
    def __getattr__(self, name):
        """
        A value can be accessed as an attribute if it has an
        attribute-friendly I{name}.
        """
        if name == '_error':
            return False
        return self[name]

    def avg(self, name):
        """
        Returns the time-weighted average value of my vector I{name},
        given my I{time} vector.
        """
        time = self['time']
        w = np.diff(time) / (time[-1] - time[0])
        return np.sum(w*self[name][1:])
    
    def error(self, *args):
        """
        Call this with something to tell me that I've had an error, or
        with nothing to find out if I've had an error.

        The "something" to call with can be an informative string or a
        C{twisted.python.failure.Failure} object.
        """
        if args: self._error = sub(*args)
        return self._error
    
    def setValue(self, x, cname):
        """
        Sets entry I{cname} in my I{values} dict to I{x}, or to its
        absolute value if I{cname} is an absolute value vector.

        Make sure I{cname} is either C{None} or a canonical name. Set
        it to C{None} to record the SSE from a L{psim.Analyzer} whose
        Python callable returns an SSE instead of computing and
        returning the values of one or more non-independent vectors.
        """
        if self.nm.isAbs(cname):
            x = np.abs(x)
        self.values[cname] = x

    def array(self, includeNames=False):
        """
        Returns my data as a 2-D Numpy array, with each of my I{values}
        (except a C{None} entry) appearing as a column vector.

        The columns are in the same order as the vector names were
        added, as indicated by the list returned from calling
        L{NameManager.cnameList}.

        If I have no values, C{None} is returned, followed by an empty
        list if I{includeNames} is set C{True}.

        @keyword includeNames: Set C{True} to have the canonical name
            list included. The result will then be a 2-tuple, with the
            array and then the names list.
        """
        Ys = []
        names = self.nm.cnameList()
        if not names:
            Ys = None
        else:
            for name in names:
                Ys.append(self[name])
            Ys = np.column_stack(Ys)
        if includeNames:
            return Ys, names
        return Ys
        
    def save(self, filePath):
        """
        Saves my current contents to a C{.npz} file at the specified
        I{filePath}, with any home directory symbol ("~") expanded.
        """
        filePath = os.path.expanduser(filePath)
        np.savez(filePath, **self.values)

    def copy(self):
        raise NotImplementedError("Your subclass must define a 'copy' method")
    
    def trimmedCopy(self, tMin=None, tMax=None):
        """
        Returns a copy of me, trimmed to omit values from TIME < I{tMin}
        and from TIME > I{tMax}.

        If I do not have a 'time' vector already loaded, an exception
        is raised.
        """
        if 'time' not in self:
            raise ValueError("No 'time' vector is already loaded!")
        V = self.copy()
        if tMin is None: tMin = V.time[0]
        if tMax is None: tMax = V.time[-1]
        K = np.flatnonzero(np.logical_and(
            np.greater_equal(V.time, tMin), np.less_equal(V.time, tMax)))
        for name in V.values:
            V.values[name] = V.values[name][K]
        return V
        
    
class Vectors_File(VectorsBase):
    """
    I am a Vectors object whose I{values} have been loaded from the
    C{.npz} file specified by the sole constructor argument.

    Presumably, the file was created by calling L{save} on an instance
    of a "live" L{Vectors_Ngspice} or L{Vectors_Python} object.
    """
    def __init__(self, filePath):
        self.filePath = filePath
        self.values = {}
        with np.load(filePath) as data:
            for cname in data.keys():
                self.nm.add(cname)
                self.values[cname] = data[cname]

    def copy(self):
        return Vectors_File(self.filePath)


class Vectors_Ngspice(VectorsBase):
    """
    I hold Ngspice results as Numpy vectors, accessible (read-only) as
    my attributes or as named items, dict-style.

    Construct me with an C{NgspiceRunner} and a list of names of nodes
    whose values I am to retrieve via the runner with each call to my
    instance. You can add names later via my Analyzer's I{addName}
    method.

    You can access a list of all my vector names (read-only, please)
    via my I{names} list.

    You can specify the difference between vectors in the usual way,
    i.e., C{V(2,1)} is the (canonical) name of C{V(2)} - C{V(1)}.

    A canonical name is a name that has been converted into format
    that Ngspice finds acceptable. Most of the time, the canonical
    name is the same as the given name. But sometimes, conversion is
    necessary, via an indirect call to
    L{util.Formatter.toCanonical}. I keep track of both versions.

    @ivar r: My L{NgspiceRunner}.

    @ivar addedLater: A list of Ngspice-canonical vector names that
        were added (via L{addVector}) after I got constructed.

    @ivar values: My underlying vector values, keyed by canonical
        name.
    @type values: dict
    """
    reDiffVector = re.compile(r'[vV]\(([^,]+),([^\)]+)\)')
    
    def __init__(self, r, names=[]):
        self.r = r
        self.addedLater = []
        self.values = {}
        self.nm.add(names)

    @property
    def cnames(self):
        """
        Property: A list of my names in Ngspice-canonical format.
        """
        return self.nm.cnameList()

    def addName(self, name, k=None):
        """
        Adds a I{name} to my L{NameManager} I{nm}.

        Doesn't add it to my I{addedLater} list, so calling this will
        cause I{name} to be included in the vectors fetched during my
        next call unless you add I{name} to I{addedLater} yourself.

        @keyword k: Set this to an integer to have the name inserted
            at a specific position in the names list of my
            L{NameManager} object I{nm} rather than appended. The
            order isn't usually important, but does affect the result
            of a call to L{array}.
        """
        return self.nm.add(name, k)
    
    def addVector(self, name, X):
        """
        Adds 1-D Numpy array I{X} as a later-added vector with I{name}.
        
        It will be included in my list of names but will not be
        included in the vectors fetched during my next call.

        The vector's name will be appended to the names list of my
        L{NameManager} object I{nm}.
        """
        cname = self.addName(name)
        self.addedLater.append(cname)
        self.setValue(X, cname)

    def copy(self):
        """
        Returns a copy of me with its own copies of my I{NgspiceRunner},
        Numpy vectors, and state as it all stands right now.

        This allows somebody like the L{plot.Plotter} to leisurely
        access my vectors without concern that my analyzer will call
        me again and overwrite them.
        """
        V2 = Vectors_Ngspice(self.r, self.nm.names)
        V2.addedLater = self.addedLater
        V2.values = self.values.copy()
        errMsg = self.error()
        if errMsg: V2.error(errMsg)
        return V2
        
    def __call__(self, *names):
        """
        Obtain the result vectors and set my read-only attributes (or
        pseudo-items) with them.

        Returns a C{Deferred} that fires (with C{None}) when I've
        attempted to set all the attributes. If I fail to set any, my
        error state gets set, checkable with a call to L{error}.
        """
        def gotVectors(X):
            def maybeAbs(kk):
                Xk = X[k+kk]
                if self.nm.isAbs(diffNames[kk]):
                    return np.abs(Xk)
                return Xk

            if not X:
                if X.error:
                    self.error(X.error)
                    return
                lines = [sub("Error getting {}", ", ".join(args))]
                stderr = getattr(X, 'stderr', [])
                for line in [X.error] + stderr:
                    line = line.strip()
                    if line: lines.append(sub("| {}", line))
                if len(lines) > 1:
                    lines[0] += ":"
                self.error("\n".join(lines))
                return
            if len(X) < len(args):
                self.error("Not enough vectors received")
                return
            k = 0
            while k < len(args):
                if k in diffs:
                    diffNames = diffs[k]
                    first, second = [self.nm(x) for x in diffNames]
                    name = sub("V({},{})", first, second)
                    self.values[name] = maybeAbs(0) - maybeAbs(1)
                    k += 1
                else:
                    if isinstance(X[k], ShuttingDownToken) or X[k] is None:
                        self.error("Shutting down")
                        return
                    name = args[k]
                    self.setValue(X[k], self.nm(name))
                k += 1
        
        if names: args = [self.nm(x) for x in names]
        else: args = [x for x in self.nm.names if x not in self.addedLater]
        k = 0; diffs = {}
        while k < len(args):
            arg = args[k]
            match = self.reDiffVector.match(arg)
            if match:
                v1, v2 = [x.strip() for x in match.groups()]
                diffs[k] = v1, v2
                args[k] = sub("V({})", v2) if v2.isdigit() else v2
                args.insert(k, sub("V({})", v1) if v1.isdigit() else v1)
                k += 1
            k += 1
        return self.r.get(*args).addCallbacks(gotVectors, self.error)


class Vectors_Python(VectorsBase):
    """
    I hold results of a Python-only simulatation as Numpy vectors,
    accessible (read-only) as my attributes or as named items,
    dict-style.

    Construct me with a callable for generating non-independent
    vectors and a list of vector names I am supposed to provide
    access to.
    """
    def __init__(self, analyzer):
        if not callable(analyzer.func):
            raise ValueError(sub("The supplied callable '{}' isn't!", func))
        self.analyzer = analyzer
        self.values = {}
        self.swept = set()
        
    def doSweep(self, name, start, stop, step):
        cname = self.nm.add(name)
        x = start
        values = []
        while x <= stop:
            values.append(x)
            x += step
        self.values[name] = np.array(values)
        self.swept.add(name)

    def addName(self, name, k=None):
        """
        Adds a I{name} to my L{NameManager} I{nm}.

        @keyword k: Set this to an integer to have the name inserted
            at a specific position in the names list of my
            L{NameManager} object I{nm} rather than appended. The
            order isn't usually important, but does affect the result
            of a call to L{array}.

        """
        return self.nm.add(name, k)
        
    def addVector(self, name, X):
        """
        Adds 1-D Numpy array I{X} as a vector with I{name}.
        """
        cname = self.addName(name)
        self.setValue(X, cname)

    def copy(self):
        """
        Returns a copy of me with its own copies of my I{analyzer} object,
        I{swept} set, and I{values} dict as they stand right now.

        This allows somebody like the C{Plotter} to leisurely access
        my vectors without concern that my analyzer will call me again
        and overwrite them.
        """
        V2 = Vectors_Python(self.analyzer)
        V2.nm = self.nm
        V2.swept = self.swept
        V2.values = self.values.copy()
        errMsg = self.error()
        if errMsg: V2.error(errMsg)
        return V2
        
    def __call__(self, params):
        """
        Obtains the result vectors and set my read-only attributes (or
        pseudo-items) with them.

        Returns a C{Deferred} that fires (with C{None}) when I've
        attempted to set all the attributes. If I fail to set any, my
        error state gets set, checkable with a call to L{error}.
        """
        def func():
            return deferToThread(self.analyzer.func, *args, **params)
        
        def done(result):
            if notseq(result):
                self.setValue(result, None)
                return
            if len(result) != len(I):
                self.error(
                    "Your callable did not generate a vector for each of [{}]",
                    ", ".join([cnames[i] for i in I]))
                return
            for k, Y in enumerate(result):
                cname = cnames[I[k]]
                self.setValue(Y, cname)

        args, I = [], []
        cnames = self.nm.cnameList()
        for k, cname in enumerate(cnames):
            if cname in self.swept:
                args.append(self.values[cname])
            else: I.append(k)
        return func().addCallbacks(done, self.error)
