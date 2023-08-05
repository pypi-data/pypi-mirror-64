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
Parameter finding with differential evolution.

Define a L{Subcircuit} subclass with a I{Finder} class attribute set
to a subclass of L{ParameterFinder}. Then use the L{paramfind} script
via the C{pf} entry point (console command) to get a dict for the
subclass's I{finderParams} class attribute. See
L{lib.mosfets.ST75NF20_Die} for an example.
"""

import os.path, re, shelve, inspect
from StringIO import StringIO
import cPickle as pickle
from copy import copy

import numpy as np
from twisted.internet import defer
from twisted.python import reflect

from pingspice.circuit.netlist import Netlist
from pingspice.circuit.av import AV_Maker, AV_Manager
from pingspice.analysis.evaluate import Enumerable, Evaluator
from pingspice.analysis.solver import Solver
from pingspice.util import *


# Set this to the full path of a pickle of the fully loaded specs
# object. The only time this should be necessary or useful is to
# update unit tests.
PICKLE_PATH = None # Always leave this alone
# Uncomment to update N-channel unit tests
#PICKLE_PATH = "~/git/pingspice/pingspice/test/specs-NMOS.dat"
# Uncomment to update P-channel unit tests
#PICKLE_PATH = "~/git/pingspice/pingspice/test/specs-PMOS.dat"


def pStrip(nameList):
    """
    Returns a copy of the supplied I{nameList} with any preceding '+'
    chars stripped off.
    """
    return [x.lstrip('+') for x in nameList]


class ParserBase(object):
    """
    Base class for parsing data and specs from text or text files.
    """
    def __init__(self, setups, attrName):
        self.setups = setups
        self.lines = getattr(setups, attrName).split('\n')
        if len(self.lines) < 2:
            self.lines = self.readLines(self.lines[0])
        if len(self.lines) < 2:
            raise ValueError(sub(
                "You must set '{}' to either text or a valid filePath",
                attrName))

    def readLines(self, filePath):
        if not os.path.exists(filePath):
            klass = getattr(self.setups, '__class__', type)
            if klass == type:
                klass = self.setups
            modulePath = inspect.getfile(klass)
            filePath = os.path.join(os.path.dirname(modulePath), filePath)
        if os.path.exists(filePath):
            with open(filePath) as fh:
                lines = fh.readlines()
                msg("Read {:d} lines from {}", len(lines), filePath)
        else: raise OSError(sub("File '{}' not found", filePath))
        return lines


class DataParser(ParserBase):
    """
    I parse text or text files with columnar data defining the goals
    for a device's performance.

    Construct me with an instance of L{Setups} and call the instance
    of me (not of L{Setups}) to obtain an I{Xs} dict keyed by setup
    ID. This dict will be the I{Xs} dict already present in the setups
    instance, updated with the entries I add to it.
    
    Comments (lines beginning with '#', or portions of a line after a
    '#' following a space) and blank lines are ignored.

    Setups are identified by C{ID = <int>}.

    Array columns containing only constant values are set by::
    
        <name> = <value>

    Array columns are defined by their names, separated by space,
    followed by a line beginning with two or more hyphens ('-------'),
    followed by one or more lines of space-delimited real numbers. All
    of the numbers in a column may be negated by proceeding the column
    name with a '-'.

    Values in a column may be scaled with::

        scale <name> <scaling factor>
    
    An example that produces, for ID=1, an array with three columns
    and four rows, i.e., four goal points of three values each, with
    one of the values (for 'gate') being a constant::

        ID = 1
        gate = 5
        drain          -vds#branch   
        --------------------------------
        0.51763632950  6.72268907563
        0.99683484885  11.7647058824
        1.51425659183  15.7983193277
        1.95499047772  18.8235294118

    If another table is found with the same ID and column names but,
    say, C{gate = 10}, its entries will be included in the array for
    ID=1 with the 'gate' value set to 10 instead of 5.
    
    If just certain setups are desired, provide a list of setup
    I{IDs}. The returned list will contain the 2-D goal point array(s)
    in the order of the IDs provided. You can also specify one or more
    I{skippedIDs}.
    """
    reEquals = re.compile(
        r'^([a-zA-Z][\(\)a-zA-Z0-9\#]*)\s*=\s*([\+\-]?[0-9\.]+)')

    def __init__(self, setups):
        """
        C{DataParser(setups)}
        """
        self.Xs = setups.Xs
        self.nameLists = {}
        for ID in setups.nameLists:
            self.nameLists[ID] = pStrip(setups.nameLists[ID])
        self.valueLists = {}
        super(DataParser, self).__init__(setups, 'goals')
    
    def assembleXs(self):
        """
        Assembles and returns a dict of 2-D arrays keyed by ID, each
        containing a column vector for each name in its respective
        nameList.
        """
        Xs = {}
        for ID in self.nameLists:
            nameList = self.nameLists[ID]
            vectorList = [
                self.valueLists[ID][name] for name in nameList
                if name in self.valueLists.get(ID, {})]
            if vectorList:
                Xs[ID] = np.column_stack(vectorList)
        return Xs
    
    def __call__(self):
        """
        Call to get a dict of 2-D goal point arrays, keyed by setup
        ID. This method does not store the dict anywhere.
        """
        def appendValue(value, scale):
            self.valueLists.setdefault(
                ID, {}).setdefault(
                    name, []).append(float(value)*scale)

        ID = None
        skipping = False
        signs = {}; constants = {}; scales = {}
        # Build up the lists of values from relevant lines, ignoring
        # lines that are not part of setup IDs we want.
        for k, line in enumerate(self.lines):
            line = line.strip()
            if line.startswith('#') or line.startswith('--'):
                continue
            if not line:
                skipping = False
                continue
            if line.lower() == 'skip':
                skipping = True
            if skipping:
                continue
            match = self.reEquals.match(line)
            if match:
                name, value = match.groups()
                if name == 'ID':
                    ID = int(value)
                    if ID not in self.nameLists:
                        msg("WARNING: Ignoring ID {:d}", ID)
                elif name not in self.nameLists.get(ID, []):
                    msg("WARNING: Ignoring unknown vector name '{}'", name)
                else: constants.setdefault(ID, {})[name] = value
                continue
            parts = line.split()
            if parts[0] == 'scale':
                scales.setdefault(ID, {})[parts[1]] = float(parts[2])
                continue
            if ID is None:
                raise ValueError(
                    "The first line of a setup goal definition must be "+\
                    "the setup ID")
            if ID not in self.nameLists:
                continue
            if len(self.lines) > k+1 and \
               self.lines[k+1].strip().startswith('--'):
                vectorNames = line.split()
                for kk, name in enumerate(vectorNames):
                    if name.startswith('-'):
                        name = name[1:]
                        vectorNames[kk] = name
                        sign = -1
                    else:
                        sign = +1
                    signs.setdefault(ID, {})[name] = sign
                continue
            theseSigns = signs.get(ID, {})
            for name, value in zip(vectorNames, line.split()):
                appendValue(
                    value, theseSigns.get(
                        name, +1) * scales.get(ID, {}).get(name, 1.0))
            for name in constants.get(ID, {}):
                appendValue(constants[ID][name], 1.0)
        return self.assembleXs()


class AttrGetter(object):
    """
    I am a convenience helper for an instance of L{Specs} to allow
    accessing its attributes and returning an integer zero ("0") as a
    default value for attributes that are not set.

    With me, you can do this: C{s.g.foo} and get 0 if 'foo' is not
    set.
    """
    __slots__ = ['s']
    
    def __init__(self, specs):
        self.s = specs

    def __getstate__(self):
        return {'s': self.s}

    def __setstate__(self, state):
        self.s = state['s']
    
    def __getattr__(self, name):
        return getattr(self.s, name, 0)

    
class Specs(object):
    """
    I am a simple object that lets you access device specifications as
    my attributes.
    """
    params = {}
    _properties = {'g', 'enumerable'}

    @property
    def g(self):
        """
        Property: Returns an instance of L{AttrGetter}, creating it if
        necessary, for shorthand access to attributes with zero-value
        defaults.
        """
        if '_g' not in dir(self):
            self._g = AttrGetter(self)
        return self._g
    @g.setter
    def g(self, value):
        self._g = value

    @property
    def enumerable(self):
        """
        Property: Returns an instance of L{Enumerable}, creating it if
        necessary, for obtaining the unique values of a vector if it
        is considered enumerable.
        """
        if '_enumerable' not in dir(self):
            self._enumerable = Enumerable()
        return self._enumerable
    
    def __getstate__(self):
        """
        Neither properties nor their underlying objects are pickled. The
        unpickled version can just re-create them.
        """
        state = {}
        for name in dir(self):
            if name.startswith('_') or name in self._properties:
                continue
            state[name] = getattr(self, name)
        return state

    def __setstate__(self, state):
        for name in state:
            setattr(self, name, state[name])
        
    def add(self, name, value):
        """
        Sets an attribute with I{name} to the specified I{value}.
        """
        setattr(self, name, value)

    def setdefault(self, name, value):
        """
        If no attribute with I{name} is present, assigns it the specified
        I{value}. Returns the value that the attribute ultimately has.

        Same behavior as running the C{setdefault} on a dictionary for
        one of its entries.
        """
        if name not in dir(self):
            self.add(name, value)
        return getattr(self, name)
        
    def _remove(self, name):
        delattr(self, name)

    def get(self, *names, **kw):
        """
        Returns the named entry of the named entry ... of the named dict,
        with the names in top-first order. Returns a 0 entry if it
        doesn't exist, or the value of I{default} if that keyword is
        set to something.

        An empty top-level dict is returned if only that is requested
        (no entry keys specified), even if it doesn't exist.
        """
        names = list(names)
        first = names.pop(0)
        if 'dct' in kw:
            dct = kw['dct']
            if first in dct:
                obj = dct[first]
                if names and isinstance(obj, dict):
                    kw['dct'] = obj
                    return self.get(*names, **kw)
                return obj
            return kw.get('default', 0)
        obj = getattr(self, first, {})
        if names and isinstance(obj, dict):
            kw['dct'] = obj
            return self.get(*names, **kw)
        return obj

    def ge(self, name):
        """
        Returns C{True} if there is no active (value = 1) entry with the
        specified I{name} in the 'disabled' dict.
        """
        return not self.get('disabled', name, False)
    
    def gp(self, ID, *names, **kw):
        """
        Returns a list of the named entries of the sub-dict of the
        'params' dict for the specified setup I{ID}.

        The list item for any entry not defined will have a zero
        value, unless the I{default} keyword is set, in which case
        that will be used as the default for any missing values.

        If you supply just one name, then a single value will be
        returned instead of a list.
        """
        default = kw.get('default', 0)
        result = [self.get('params', ID, x, default=default) for x in names]
        return result[0] if len(names) == 1 else result

    def gperator(self, ID, name):
        """
        If there is a named entry of the sub-dict of the 'params' dict for
        the specified setup I{ID}, yields the value of that entry in a
        single iteration. If not, doesn't iterate at all.

        Use this to selectively execute code using parameter value if
        it's been defined.
        """
        value = self.get('params', ID, name, default=None)
        if value is not None:
            yield value
    
    def _name2k(self, ID, name):
        """
        Returns the column index for parameter I{name} in my 2-D Numpy
        goals array for the specified setup I{ID}.
        """
        for k, thisName in enumerate(self.nameLists[ID]):
            if thisName.lstrip('+') == name:
                return k
        raise ValueError(sub("Name '{}' not in {}", name, self.nameLists[ID]))

    def _subset(self, ID, name, value):
        """
        Returns a subset of my 2-D Numpy goals array for the specified
        setup I{ID} with rows selected such that the values in the
        column for parameter I{name} are closest to I{value}.

        The column vector in the area must be an enumerable
        vector. (Independent, too, although this is not checked.) See
        L{IV_Manager} to understand what it means for a vector to be
        "enumerable."

        The enumerated values are examined and the closest one to
        I{value} is used for the row selection criterion. If there are
        enumerated values for the column for the parameter specified
        with I{name} that exactly equal I{value}, then of course an
        array with exactly those values in the column will be
        returned. Otherwise, the array will have the rows with the
        closest enumerated value for that parameter.
        """
        X = self.Xs[ID]
        kCol = self._name2k(ID, name)
        Z = X[:,kCol]
        uv = self.enumerable(Z)
        if uv is None:
            raise ValueError(
                sub("The vector '{}' is not enumerable", name))
        k = np.argmin(np.abs(uv-value))
        value = uv[k]
        K = np.flatnonzero(np.equal(X[:,kCol], value))
        return X[K,:]
    
    def _getX(self, ID, kw):
        """
        Returns my 2-D Numpy goals array for the specified setup I{ID} or,
        if there is a single keyword in I{kw} referencing an
        enumerable column vector in that array, a subset thereof.
        """
        if kw:
            if len(kw) > 1:
                raise ValueError("You can only specify one enumerable vector")
            name = kw.keys()[0]
            return self._subset(ID, name, kw[name])
        return self.Xs[ID]

    def Xmax(self, name, *IDs, **kw):
        """
        Returns the maximum value of the goal points of vector I{name} for
        all setup IDs listed as subsequent arguments.

        With a keyword, you can specify the name and desired value of
        an enumerable vector. Then, only the goal points having the
        value closest to that will be considered.
        """
        maxValue = None
        for ID in IDs:
            if ID not in self.Xs or callable(self.Xs[ID]): continue
            X = self._getX(ID, kw)
            thisMax = X[:,self._name2k(ID, name)].max()
            if maxValue is None or thisMax > maxValue:
                maxValue = thisMax
        return maxValue
    
    def Xrange(self, ID, name, **kw):
        """
        Returns a 1-D Numpy array of sorted unique values of the goal
        points of vector I{name} for setup I{ID}.

        If there are no goal points for this setup or it has a
        callable goal, returns C{None}.

        With a keyword, you can specify the name and desired value of
        an enumerable vector. Then, only the goal points having the
        value closest to that will be considered.
        """
        if ID not in self.Xs or callable(self.Xs[ID]): return
        X = self._getX(ID, kw)
        V = X[:,self._name2k(ID, name)]
        return np.unique(V)

    def XYmax(self, ID, xName, *args, **kw):
        """
        Returns a list with the maximum value of the goal points of vector
        I{xName} for setup I{ID} followed by the value for the
        corresponding goal point of each vector named as an additional
        argument.

        If there are no goal points for this setup or it has a
        callable goal, returns C{None}.

        With a keyword, you can specify the name and desired value of
        an enumerable vector. Then, only the goal points having the
        value closest to that will be considered.
        """
        if ID not in self.Xs or callable(self.Xs[ID]): return
        X = self._getX(ID, kw)
        Vx = X[:,self._name2k(ID, xName)]
        k = np.argmax(Vx)
        result = [Vx[k]]
        for yName in args:
            kc = self._name2k(ID, yName)
            if kc < X.shape[1]:
                x = X[k, kc]
            else:
                import pdb; pdb.set_trace() 
            result.append(x)
        return result


class DictStack(object):
    """
    Dictionaries within a dictionary, for L{Specs}.
    """
    def __init__(self, s):
        self.s = s
        self.names = []

    def __nonzero__(self):
        """
        I am C{True} if I've been started since construction or a call to
        L{done}.
        """
        return bool(self.names)
        
    def add(self, name):
        """
        Call to add a new dictionary or sub-dictionary with I{name}.
        
        The first time this is called after construction or a call to
        L{done}, starts a new dictionary to hold sub-dictionaries and
        records I{name} as its name. Thereafter, before L{done} is
        called, adds a new sub-dictionary to the dictionary, keyed by
        I{name}.

        I will hold onto the dictionary name, or sub-dictionary key,
        as my I{currentName}.
        """
        if name.isdigit():
            name = int(name)
        self.currentName = name
        if name in self.names:
            return
        if self.names:
            self.dct[name] = {}
        else: self.dct = {}
        self.names.append(name)

    def entry(self, key, value):
        """
        Sets a dictionary or sub-dictionary entry.
        
        If L{add} has only been called once since construction or the
        last L{done}, sets an entry under I{key} of my dictionary to
        I{value}. Otherwise, sets an entry to the sub-dictionary that
        I{currentName} points to, under I{key} with I{value}.
        """
        if key.isdigit():
            key = int(key)
        if len(self.names) > 1:
            self.dct[self.currentName][key] = value
            return
        self.dct[key] = value
        
    def done(self):
        """
        Sets my dictionary as an attribute of my parent L{Specs} object
        I{s}, using the dictionary's name as the attribute name.

        Clears things out for another call or series of calls to
        L{add} and L{entry}.
        """
        if not self.dct:
            # TODO: Allow for empty dicts with nothing but perhaps a
            # comment between two lines of hyphens
            return
        self.s.add(self.names[0], self.dct)
        self.names = []
        del self.dct


class SpecsParser(ParserBase):
    """
    I parse text or text files defining the specifications of a
    device.

    A single attribute value is defined with the construct C{name =
    value} or C{name value}.

    A dict of values is defined with just the dict C{name} on a line
    by itself followed by a line of hyphens, e.g., C{-----}. Then,
    after the hyphens, one or more C{key value} lines. (Zero lines
    should make an empty dict, but is not supported.) Then another
    line of hyphens.

    But dicts can be stacked! If a I{key} has two parts separated by a
    colon, the first part is an entry in the top-level dict that is
    actually another dict, and the second part is an entry in I{that}
    dict. The file I{RFP12N10L.specs} included in the L{lib}
    sub-package uses this for its I{params} dict::

        params
        -------------------------------------------
        351:Rg        990
        351:ttrig     2E-4
        351:Vbatt     62.7
        
        361:Rg        82000
        361:ttrig     2E-4
        361:Vbatt     63.343
        
        371:ttrig     2E-3
        371:Vbatt     63.42
        -------------------------------------------

    There are three sub-dicts inside I{params}, accessible with the
    keys I{351}, I{361}, and I{371}.

    Construct me with an instance of L{Setups} and call my instance
    to obtain a L{Specs} object with the specifications as its
    attributes.
    
    Comments (lines beginning with '#', and trailing parts of a line
    after a '#') and blank lines are ignored.
    """
    reNum = re.compile(r'[\+\-]?[0-9]+(\.[0-9]+)?([e][\+\-]?[0-9]+)?$')
    
    def __init__(self, setups):
        self.s = Specs()
        self.ds = DictStack(self.s)
        super(SpecsParser, self).__init__(setups, 'specs')
    
    def parseName(self, tokens):
        """
        I call this when I encounter a line defining a new entry, with the
        first and possibly only token being the entry's name.
        """
        first = tokens.pop(0).replace("'", "")
        parts = [x.strip() for x in first.split(':')]
        if len(parts) == 1:
            return parts[0], None
        if len(parts) > 2:
            raise ValueError(
                "A name can only be by itself or with one key")
        if not self.ds:
            raise ValueError(
                "The name:key format is only for dicts inside a dict")
        return parts
    
    def parse(self, value):
        """
        I call this when I encounter a line defining just one or more
        space-delimited values, once per value.
        """
        value = value.lower()
        for string, assignedValue in (
                ('none', None), ('true', True), ('false', False)):
            if value == string:
                return assignedValue
        match = self.reNum.match(value)
        if match:
            return float(value)
        return value
    
    def add(self, name, key, value):
        """
        Adds something to my L{Specs} instance I{s}. There are three
        possibilities.
        
            1. If I{key} is C{None} and I have no L{DictStack} in
               progress, adds an attribute I{name} with I{value} to my
               L{Specs} object.

            2. If I{key} is C{None} and I have a L{DictStack} in
               progress, adds an entry to its top level, referenced by I{name}
               with the I{value}.

            3. With a I{key}, adds a new sub-dict to my L{DictStack}
               (one must be in progress) and an entry to that,
               referenced by I{key} with the I{value}.
        """
        if key:
            self.ds.add(name)
            self.ds.entry(key, value)
            return
        if self.ds:
            self.ds.entry(name, value)
            return
        self.s.add(name, value)

    def __call__(self):
        """
        Returns a new populated instance of L{Specs}.
        """
        for k, line in enumerate(self.lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('--'):
                if self.ds: self.ds.done()
                continue
            tokens = line.split()
            name, key = self.parseName(tokens)
            if not tokens:
                # A standalone name is the start of a dict definition
                self.ds.add(name)
                continue
            if tokens[0] == "=":
                tokens.pop(0)
            seq = []
            for token in tokens:
                if token.startswith('#'):
                    break
                seq.append(self.parse(token.rstrip(',')))
            if len(seq) == 1:
                seq = seq[0]
            self.add(name, key, seq)
        return self.s


class RelationsChecker(object):
    """
    Checks that the linear relation between two parameters is within
    the limits imposed by the 'relations' dict-of-dicts specification.
    """
    def __init__(self, relations):
        self.relations = relations

    def __call__(self, params):
        for xName in self.relations:
            x = params[xName]
            ys = self.relations[xName]
            for yName in ys:
                y = params[yName]
                m, b, yMaxErr = ys[yName]
                yr = m*x + b
                if abs(yr-y) > yMaxErr:
                    return False
        return True
                
    
class Setups(object):
    """
    Include an instance of your subclass of me, with my class
    attributes defined, as the I{setups} attribute to your
    L{ParameterFinder} subclass.

    If your subclass of me has a L{setup} method, it will be called at
    the beginning of my init, right after L{setdefaults} and
    construction of an L{EvalHelper}.

    The goal values for the parameter finder are in my dict I{Xs}, one
    2-D Numpy array per setup ID. If you don't want to specify all
    those numbers in your subclass, set the I{goals} attribute to
    text, or a path of a file containing text, of goals readable by
    L{DataParser}.

    The class attributes I{analyzers}, I{independents}, I{Xs}, are
    dicts, keyed by setup ID, or callables that take a L{Specs} object
    as the sole argument and return a dict. Be sure to order your
    setups with the least CPU-intensive ones numbered lowest because
    evaluations returning huge SSEs can prevent ones from
    higher-numbered setups from even bothering to run.

    The class attributes I{weights} and I{transforms} are dicts keyed
    by vector name.

    @cvar goals: Text or a text file defining the device's performance
        goals. Parsed by L{DataParser}.

    @cvar specs: Text or a text file defining the device's
        specifications. Parsed by L{SpecsParser}.

    @cvar EvalHelper: A class with a constructor that takes a L{Specs}
        instance as its sole argument. I automatically construct it
        right away if you define the class and you can refer to the
        instance via my I{eh} attribute.
    
    @cvar nameLists: A dict of lists of vector names to retrieve after
        each analysis, each keyed by setup ID.

    @cvar plotSpecs: (Optional) A setup ID-keyed dict of plot
        specificiations, if parameter-fit plotting is desired. For
        each setup: C{None} if no plot for that setup, or a list
        with::

        [<plot title>, <x-axis vector name>, <y-axis vector name(s)>]
    
    @cvar analyzers: A setup ID-keyed dict of lists defining
        analyzers. The first item in each is a subclass of
        L{sim.Analyzer} or an instance of L{psim.Analyzer} followed by
        its setup args.

    @cvar independents: A setup ID-keyed dict of lists of names of the
        vectors that are independent variables.

    @cvar Xs: A setup ID-keyed dict of lists of goals that were not
        otherwise defined with I{goals}. Items can be either a 2-D
        Numpy array of expected goal values or a callable. An array
        must have one column for each vector name listed in the
        I{nameLists} list for that setup. A callable must accept the
        vectors named in the I{nameLists} list as 1-D Numpy arrays and
        return a real-valued sum-of-squared error based on how closely
        the values in those vectors conform to some user-defined
        goal. If there is no Xs entry for a given setup ID (after I
        populate it from parsing I{goals}, no analysis for that setup
        will be included.
    
    @cvar weights: A dict of weights (real values or single-argument
        callables) to apply to the value from each vector, keyed by
        the names found in nameLists. A callable must take two args,
        the integer ID of the series being evaluated and a 1-D Numpy
        array of values from the vector, and return a positive
        real-valued weight.

    @cvar transforms: A dict, keyed by the name of a
        transform-produced vector, of callables that each transform
        one or more vectors from the Ngspice simulation into a vector
        listed in I{nameLists} but not included in the Ngspice
        simulation. The result of the transform (which must be a 1-D
        Numpy array) will be added to the C{V} object under the name
        by which the transform is keyed in this dict.

    @cvar logValues: A set of vector names that should be evaluated
        and plotted in log space rather than linear. I will
        log-transform any goal points in I{X} corresponding to such
        vector names. It's up to whoever uses me to do the same log
        transformation on simulation results.

    @cvar defaultSpecs: A dict of default values for attributes that
        don't appear in a given subclass's specs.
    
    @ivar netlists: A setup ID-keyed dict of netlist file paths or
        text. Usually populated by L{ParameterFinder}.
    """
    _possiblyCallable = {
        'nameLists', 'plotSpecs', 'analyzers',
        'independents', 'weights', 'transforms', 'constraints'}

    goals = None
    specs = None
    EvalHelper = None

    Xs = {}
    knowns = {}
    constraints = []
    logValues = set()
    defaultSpecs = {}

    IDs = []
    skippedIDs = []

    @classmethod
    def setdefaults(cls, *args):
        """
        Examines my class (or subclass), or an object if supplied as a
        sole argument, for attributes named in my I{defaultSpecs}
        dict. Those not found are set to the default values.
        """
        obj = args[0] if args else cls
        for name in cls.defaultSpecs:
            if not hasattr(obj, name):
                setattr(obj, name, cls.defaultSpecs[name])
    
    def __init__(self, **kw):
        """
        C{Setups(**kw)}

        You can set an instance's attributes with constructor
        keywords.
        """
        self.netlists = {}
        for name in kw:
            setattr(self, name, kw[name])
        s = Specs() if self.specs is None else SpecsParser(self)()
        self.setdefaults(s)
        if self.EvalHelper:
            s.eh = self.EvalHelper(s)
        # Do user-defined setup, if any
        self.setup(s)
        for name in dir(s):
            if name.startswith('_'):
                continue
            setattr(self, name, getattr(s, name))
        self._setupDicts(s)
        self.IDs, self.nameLists = self._prune()
        msg("IDs enabled: [{}]", ', '.join([str(x) for x in self.IDs]))
        for ID in self:
            ads = self.analyzers.get(ID, None)
            if not hasattr(ads, '__iter__'):
                msg("WARNING: No analyzer definition sequence for ID {:d}", ID)
                self.IDs.remove(ID)
                del self.nameLists[ID]
                continue
            if not isinstance(ads, list):
                self.analyzers[ID] = list(ads)
            self.plotSpecs.setdefault(ID, None)
        if self.weights:
            self._checkWeights()
        for func in self.constraints:
            if not callable(func):
                raise ValueError("Constraints must be callables!")
        # If there is a relations dict-of-dicts, add a constraint for it
        relations = s.get('relations')
        if relations: self.constraints.append(RelationsChecker(relations))
        try:
            self._finalizeXs()
        except:
            print "ERROR setting up goals! Fix it."
            import sys, traceback, pdb
            type, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
        # Prune unused plotSpecs so we don't get empty unused subplots
        toDelete = set()
        for ID in self.plotSpecs:
            if ID not in self:
                toDelete.add(ID)
        for ID in toDelete:
            del self.plotSpecs[ID]
        # If PICKLE_PATH is set, save a pickle of my Specs instance to
        # that file
        if PICKLE_PATH:
            with open(os.path.expanduser(PICKLE_PATH), 'wb') as fh:
                pickle.dump(s, fh)

    def __contains__(self, ID):
        """
        I contain a setup ID if it's for a setup I run.
        """
        return ID in self.IDs
        
    def __len__(self):
        """
        My length is the number of setups I run.
        """
        return len(self.IDs)
        
    def __iter__(self):
        """
        I iterate over my setup IDs. You can change my I{IDs} attribute
        during iteration if you want.
        """
        IDs = copy(self.IDs)
        for ID in IDs:
            yield ID

    def __getstate__(self):
        """
        For pickling during wire evaluation.
        """
        state = {}
        names = {
            'specs', 'netlists', 'nameLists', 'IDs',
            'nameLists', 'plotSpecs', 'analyzers',
            'independents', 'Xs', 'weights', 'constraints',
            'transforms', 'logValues', 'avList',}
        for name in names:
            if hasattr(self, name):
                state[name] = getattr(self, name)
        return state

    def __setstate__(self, state):
        """
        For unpickling during wire evaluation.
        """
        for name in state:
            setattr(self, name, state[name])

    def setup(self, s):
        """
        Override this if you want custom setup at the beginning of my
        standard setup, right after L{setdefaults} gets called and an
        L{EvalHelper} instance is constructed.
        """
        pass

    def _setupDicts(self, s):
        """
        Called by my constructor with a L{Specs} object to replace any
        dict-producing callable attributes with their results.

        The I{nameLists} dict/callable gets done first, with a
        reference to it included in I{s} so that each setup's vector
        names are available to the others.
        
        The I{Xs} dict/callable gets done second, with my I{goals}
        string/file parsed and a reference to it included in I{s} so
        that its values are available to the others.
        """
        if callable(self.nameLists): self.nameLists = self.nameLists(s)
        s.nameLists = self.nameLists
        if callable(self.Xs): self.Xs = self.Xs(s)
        if self.goals: self.Xs.update(DataParser(self)())
        s.Xs = self.Xs
        for name in self._possiblyCallable:
            thing = getattr(self, name, {})
            if callable(thing):
                thing = thing(s)
            setattr(self, name, thing)
        
    def _prune(self):
        """
        Called by my constructor to get (1) a sorted copy of my class-wide
        I{IDs} list and (2) a pruned version of I{nameLists}
        containing just entries for the enabled IDs.

        If my I{IDs} list is empty, (1) contains all IDs of all keys in
        I{nameLists}, still sorted, and (2) contains entries for all IDs.

        B{Except:} Any ID appearing in my I{skippedIDs} list is always
        omitted.
        """
        IDs = []
        nameLists = {}
        for ID in sorted(self.IDs if self.IDs else self.nameLists.keys()):
            if ID in self.skippedIDs:
                continue
            if ID not in self.nameLists:
                raise ValueError("Invalid setup ID in your 'IDs' list")
            IDs.append(ID)
            nameLists[ID] = self.nameLists[ID]
        return IDs, nameLists
        
    def _checkWeights(self):
        """
        Called by my constructor to make sure my I{weights} dict is legit.
        """
        for key in self.weights:
            if not isinstance(key, str) or not key[0].isalpha():
                raise ValueError(
                    "Each key of 'weights' must be a "+\
                    "potential vector name")
            for nameList in self.nameLists.values():
                nameList = pStrip(nameList)
                if key in nameList: break
            else:
                msg("WARNING: weight "+\
                    "'{}' for vector not in any nameList!", key)
            value = self.weights[key]
            if not callable(value) and not isinstance(value, (float, int)):
                raise ValueError(
                    "Each value of 'weights' must be a callable "+\
                    "or real-valued constant")

    def _finalizeXs(self):
        """
        Called by my constructor to finalize the setting up of a dict of
        evaluation goals, one Numpy 2-D array or callable evaluator
        per setup I{ID}.

            - Removes IDs of setups with no goals defined.

            - Sorts independent variables in ascending order so that
              L{sse.ErrorTabulator.closenessToIndepInterpolated} may be
              used.

            - Log-transforms any log-space goal values (as indicated
              by presence of their vector name in my I{logValues} set)
              into linear space.
        """
        omittedIDs = set()
        for ID in self:
            if hasattr(self.analyzers[ID][0], 'avDefine'):
                # Python-only analyzer defines its own goal
                continue
            nameList = pStrip(self.nameLists[ID])
            X = self.Xs.get(ID, None)
            if callable(X):
                # Callable X's can't be sorted or log-transformed, and
                # have no goals since each one defines its goal
                continue
            if X is None:
                omittedIDs.add(ID)
                continue
            if len(getattr(X, 'shape', [])) == 2:
                independents = self.independents[ID]
                if len(independents) == 1:
                    # Just one independent variable, make sure sorted
                    # ascending so we can use
                    # sse.ErrorTabulator.closenessToIndepInterpolated
                    k = nameList.index(independents[0])
                    I = np.argsort(X[:,k])
                    self.Xs[ID] = X[I,:]
            for k, name in enumerate(nameList):
                # Log tranformations (if any) of goals are done just
                # once, up front
                if name in self.logValues:
                    try:
                        self.Xs[ID][:,k] = np.log10(self.Xs[ID][:,k])
                    except:
                        msg(-1,
                            "Problem doing log transformation of goals "+\
                            "for setup {:d}!", ID)
                        import pdb; pdb.set_trace() 
        if omittedIDs:
            msg("WARNING: Omitting {} {} since no goals defined",
                plural("setup", omittedIDs), ", ".join(
                    [str(x) for x in omittedIDs]))
            for ID in omittedIDs:
                del self.nameLists[ID]
                self.IDs.remove(ID)


class ParameterFinder(object):
    """
    Model parameter evolver.
    
    I use Differential Evolution to identify an optimum combination of
    alterable values and device or model parameters in a circuit for
    fitting its simulated behavior to goal points you specify in your
    subclass of L{Setups} that you supply to your subclass of me with
    the I{Setups} class attribute.

    Define the alterable values in your L{setup} method with::

        f.av(name, <dev|model>, [<param>], min, max)

    For the differential evolution algorithm used, you MUST define min
    and max bounds for each alterable.

    If you set the I{params} keyword to a dict of parameter values
    keyed by their names, or a string from which I can parse such a
    dict, I will just serve as a structure for my L{setup} method to
    be used by a L{netlist.Subcircuit}, with no parameter-finding
    being done.

    You can set attributes for the L{Setups} instance with keywords
    not listed here as reserved for my own use. The most useful is
    I{IDs}, a list of setup IDs for restricted parameter finding.

    @keyword params: Parameter values from a previous parameter
        finding session. If this keyword is present and not C{None},
        all of the other keywords will be ignored.
    @type params: dict
    
    @keyword N_cores: The number of CPU cores my solver should use for
        evaluations.

    @keyword wire: Set C{True} for my solver to use a WireEvaluator.

    @keyword tcp: Set to a TCP host:port endpoint for the
        WireEvaluator (B{TODO}).

    @keyword debug: Set C{True} for a debugging mode with more verbose
        output and opportunities to fix stuff.

    @keyword spew: Set C{True} for an extremely verbose mode that
        spews out the communications between Python and Ngspice.

    @keyword console: Set C{True} to drop to an interactive Ngspice
        console if Ngspice has an error.

    @keyword autoUIC: Set C{True} to have TRAN analysis done with the
        'uic' option if any netlist item has I{ic} set to
        something. this isn't that useful as Ngspice's uic option is
        very hard to tame.

    @keyword plotFile: Set to the full path of a PNG file that will
        update with plots showing the progress of parameter
        finding. The default is C{~/pfinder.png}.

    @keyword plotDims: Set to a 2-sequence of ints with the pixel
        width and height of the plot, or to C{None} if the default
        defined in L{Plotter} is to be used.
    
    @keyword logFile: The path of a file for logging output (CAUTION:
        File gets truncated, i.e., overwritten). Logs to STDOUT if not
        provided.

    @keyword knowns: A dict of known parameter values. This is of the
        same type as the I{params} keyword, but doesn't cause my
        instance to skip parameter finding. It also doesn't need to
        have all (or even any) parameter values defined.

    @keyword twp: A percentage for varying known value(s) +/- as
        bounds. Default is C{None}, but note that it's rarely a good
        idea for parameter values to not be subject to any parameter
        modification at all during parameter finding.
    
    @cvar Setups: A subclass of L{Setups} that you define to specify
        parameter names, analyzers, independent vectors, goal points,
        etc.
    
    @ivar s: An instance that I construct of the L{Setups} subclass
        referenced in your subclass of me.

    @cvar setup: The Ngspice circuit setup for the parameter-finding
        testbed. The similarity of names is regretted.

    """
    kwAttrs = {
        'N_cores':      None,
        'wire':         False,
        'tcp':          [],
        'debug':        False,
        'verbose':      False,
        'spew':         False,
        'console':      False,
        'autoUIC':      False,
        'plotDims':     None,
        'plotFile':     "~/pfinder.png",
    }
    subCircuit = None
    logFile = None
    showNetlists = []
    class _EmptySetups:
        specs = None

    def __init__(self, *args, **kw):
        """
        There are two different call patterns. One is for using
        Differential Evolution to find parameter values::

            ParameterFinder(
                cfg,
                N_cores=None, wire=False,
                debug=False, spew=False, console=False,
                autoUIC=False, plotFile=~/pfinder.png, plotDims=None,
                logFile=None, knowns={}, twp=None)

        The other is for using all-known parameter values to do an
        actual simulation in a circuit or subcircuit::

            ParameterFinder(params={...})
        
        """
        params = kw.pop('params', None)
        if params:
            # With parameters supplied, no parameter finding analysis
            # is done. In this mode, I just act as a structure for a
            # Subcircuit to run my setup method.
            setups = getattr(self, 'Setups', self._EmptySetups)
            self.s = setups if setups.specs is None else SpecsParser(setups)()
            setups.setdefaults(self.s)
            self.avm = AV_Manager()
            if not isinstance(params, dict):
                params = self.avm.paramsFromText(params)
            self.avm.knowns = params
            # That's it for this mode
            return
        if not args or not isinstance(args[0], Config):
            raise ValueError(
                "Must provide a Config instance when doing parameter finding")
        self.__init_pf(args[0], **kw)

    def __init_pf(self, cfg, **kw):
        """
        My constructor calls this to do the full initialization in
        paramfinding mode, when no parameters are supplied.
        """
        self.cfg = cfg
        for name in self.kwAttrs:
            value = kw.pop(name, None)
            if value is None:
                value = self.kwAttrs[name]
            setattr(self, name, value)
        if self.cfg.quiet:
            self.logHandle = None
        else:
            logFile = kw.pop('logFile', None)
            if logFile:
                self.logHandle = open(os.path.expanduser(logFile), 'w')
            else: self.logHandle = True
        msg(self.logHandle)
        if self.N_cores is None:
            import multiprocessing as mp
            self.N_cores = mp.cpu_count() - 1
        if not hasattr(self, 'Setups'):
            raise NotImplementedError("No 'Setups' class supplied!")
        knowns = kw.pop('knowns', None)
        knownTwiddlePercentage = kw.pop('twp', None)
        self.s = self.Setups(**kw)
        # Now configured and ready to get started
        if knowns is None: knowns = self.s.knowns
        self.avm = AV_Manager(
            knowns, twp=knownTwiddlePercentage, verbose=self.cfg.chatty)
            
    def __getattr__(self, name):
        """
        Looks to my subcircuit "parent" and then my L{Setups} object I{s}
        for attributes that I lack.
        """
        if self.subCircuit and hasattr(self.subCircuit, name):
            return getattr(self.subCircuit, name) 
        if name != 's':
            if hasattr(self.s, name):
                return getattr(self.s, name)
            raise AttributeError(sub(
                "Neither {} nor its setups object {} has '{}'",
                self, self.s, name))
    
    def tableSources(self, f, ID):
        """
        Called by L{analyzerPrep} for each setup I{ID} to possibly
        generate one or more TABLE sources.
        
        If the specified setup I{ID} has more than one independent vector
        and it's not a dual-sweep DC analysis, constructs a TABLE
        Ngspice voltage source for each secondary independent vector
        whose output is based on the primary independent vector.

        This allows analyses based on real test circuits where
        multiple voltage vectors are acquired whose values are
        dependent on a primary test signal rather than behavior of the
        device under test.
        """
        ads = self.s.analyzers[ID]
        k0_indep = 2 if ads[0].fName == 'dc' and len(ads) > 5 else 1
        independents = self.s.independents[ID]
        if k0_indep >= len(independents):
            return
        X = self.Xs[ID]
        if callable(X):
            return
        nameList = pStrip(self.nameLists[ID])
        for k, name in enumerate(independents):
            if k == 0:
                xName = name
                X_pi = X[:,nameList.index(xName)]
            if k < k0_indep:
                continue
            expr = "{time}" if xName == 'time' else sub("{{V({})}}", xName)
            tokens = ['TABLE', expr, '=']
            Y = X[:,nameList.index(name)]
            for x, y in zip(X_pi, Y):
                tokens.append(sub("({}, {})", x, y))
            f.E(name, 0, *tokens)
        
    def analyzerPrep(self, ID):
        """
        Call this with a setup I{ID} to provide what the C{Analyzer} for
        that setup will need when it is activated.

        Returns C{True} if the analyzer got prepared without any
        problems. In particular, if calling your subclass's override of
        L{setupTestCircuit} with this ID didn't raise an exception.
        """
        def describe(name):
            if self.cfg.chatty:
                if len(ads) > 1:
                    msg(2, "{}: {}", name, " ".join([str(x) for x in ads[1:]]))
                else: msg(2, name)
                    
        msg("Setup {:d} ...", ID)
        self.avm.setSetupID(ID)
        ads = self.s.analyzers[ID]
        aco = ads[0]
        if hasattr(aco, 'avDefine'):
            self.netlists[ID] = None
            f = AV_Maker(self.avm)
            aco.avDefine(f)
            for independentVectorName in self.s.independents.get(ID, []):
                aco.scheduleSweep(independentVectorName)
            describe(aco.__class__.__name__)
            return True
        if isinstance(aco, type) and hasattr(aco, 'fName'):
            # Look Ma, no files!
            fh = StringIO()
            n = Netlist(
                fh,
                sub("PF-setup-{:02d}", ID), self.avm,
                keep=self.cfg.keep, debug=self.cfg.nodes)
            n.uic(False)
            with n() as f:
                # Do this first in case test circuit modifies setup
                # for param finding purposes
                if self.cfg.nodes:
                    # Don't trap node-checking errors when logging them
                    self.setupTestCircuit(f, ID)
                else:
                    try:
                        self.setupTestCircuit(f, ID)
                    except:
                        msg(-1, "Couldn't setup test circuit for ID {:d}", ID)
                        if self.cfg.verbose:
                            import traceback; traceback.print_exc()
                            msg('-')
                        return
                self.setup(f)
                self.tableSources(f, ID)
            if self.autoUIC and aco.fName == 'tran':
                if f.uic() and 'uic' not in ads[1:]:
                    ads.append('uic')
            # Can only getvalue after n() context ends!
            self.netlists[ID] = fh.getvalue()
            fh.close()
            if ID in self.showNetlists:
                text = self.netlists[ID].replace("{", "{{").replace("}", "}}")
                msg(-1, text, -1)
            describe(aco.fName.upper())
            return True
        import pdb; pdb.set_trace()
        raise TypeError(sub(
            "Object '{}' is not a sim.Analyzer "+\
            "subclass or a psim.Analyzer subclass instance", aco))

    @defer.inlineCallbacks
    def __call__(self, **kw):
        """
        Call this to find best-fit alterable values for the circuit you've
        defined with your L{setup} override method.

        Sets my I{params} attribute to a dict of alterable values,
        keyed by their names as defined with the C{f.av(<name>, ...)}
        calls in that setup method.

        Any keywords supplied will be passed on to the constructor of
        L{Solver} when I make my own instance of it.

        Returns a C{Deferred} that fires with a reference to a dict of
        the best params and my C{ade.Population} instance in its final
        state.
        """
        skipped = set()
        for ID in self.s:
            if not self.analyzerPrep(ID):
                skipped.add(ID)
        self.avm.finalize()
        # The toolkit
        wire = self.tcp if self.tcp else True if self.wire else False
        popsize = kw.pop('popsize', None)
        sv = Solver(
            self.cfg, self.avm, self.s, self.N_cores,
            wire=wire, popsize=popsize,
            logHandle=self.logHandle,
            picklePath=kw.pop('picklePath', None),
            savePicklePath=kw.pop('savePicklePath', None))
        if self.s.plotSpecs:
            from pingspice.analysis import plot
            plotter = plot.Plotter(
                self.s.plotSpecs, self.s.logValues,
                os.path.expanduser(self.plotFile), self.plotDims)
            sv.addCallback(plotter)
        yield sv.setup(
            uniform=kw.pop('uniform', False), skipIDs=skipped)
        # At last, we run the solver
        p = yield sv(**kw).addErrback(oops)
        msg(-1, "Final population after {:d} evaluations", p.counter, '-')
        msg(repr(p), -1)
        iBest = p.best()
        if iBest is None:
            params = None
        else:
            params = self.avm.knownParams()
            for name, value in zip(sv.names, iBest.values):
                params[name] = value
            msg(4, "finderParams = {{")
            msg(8, "# Finder = {}", reflect.fullyQualifiedName(self.__class__))
            msg(8, "# SSE = {:.1f} after {:d} evaluations",
                float(p.best().SSE), p.counter)
            names = sorted(params.keys())
            for name in names:
                msg(8, "'{}': {:g},", name, params[name])
            msg(4, "}}", -1)
        msg("Providing final Population to caller")
        # We're just about done, so turn off logging, closing any open
        # logfile
        msg(None)
        # The last thing I do is "return" a reference to the params
        # (or None) and final population
        defer.returnValue((params, p))
    
    def setupTestCircuit(self):
        """
        You must override this to define test circuitry for one or more
        setups.
        """
        raise NotImplementedError("Define test circuits in your subclass!")
