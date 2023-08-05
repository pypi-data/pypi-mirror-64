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
Running multiple simulation processes at once.

The main character in this cast is L{Evaluator}.
"""

import sys
from collections import OrderedDict

import numpy as np
from twisted.internet import reactor, defer

import asynqueue
from ade.util import EvalTimer

from pingspice.analysis.msim import MultiRunner
from pingspice.analysis import sse
from pingspice.util import *


class Enumerable(object):
    """
    Call an instance of me to get the unique values of vector I{Z} if
    it is considered enumerable, or C{None} otherwise.
    
    @cvar maxUniqueVals: The maximum number of unique values an
        independent vector can have for it to be considered enumerable
        rather than continuous.
    """
    maxUniqueVals = 20

    def __call__(self, Z):
        uv, counts = np.unique(Z, return_counts=True)
        if len(uv) > self.maxUniqueVals: return
        if counts.min() == 1: return
        return uv


class IV_Manager(object):
    """
    I manage info about the independent vectors for a given
    setup.

    Construct me with a sequence I{indieFlags} of bools indicating
    whether each column in the 2-D goals array for that setup is for
    an independent vector.

    My I{kInterp} attribute is very important: It is set to an integer
    column index (which may be zero) of a non-enumerable independent
    vector B{if} you can use interpolation-based SSE calculation based
    on my setup's 2-D goals array and my I{indieFlags}. (It's set to
    C{None} otherwise.)

    That special vector, if it exists, is used as the x-axis argument
    for Numpy's C{interp} function. The
    L{ErrorTabulator.closenessToIndepInterpolated} method uses that
    instead of looking for the closest independent-vector points as
    L{ErrorTabulator.closenessToIndep} does or (worse yet) looking for
    the closest overall points as L{ErrorTabulator.closenessToAll}
    does.

    Using Numpy's C{interp} function is very efficient, but only
    possible if there is exactly one independent variable (not
    including independent vectors that contain a limited set of
    enumerated values) and if the values for that independent
    variable are in ascending order. That seems like a lot of
    conditions, but it usually should be the case.

    Regarding enumerated values: If there are multiple independent
    vectors but all except one have goal points that are in a limited
    set of enumerated values (e.g., all integers between 5 and 10),
    then I{closenessToIndepInterpolated} can still be used. It will
    run Numpy's C{interp} function on the sole non-enumerated
    independent vector with the values of the other independent
    vector(s) set to each enumerated value in turn. That's still more
    efficient than using I{closenessToIndep}, and more desirable
    because the vast majority of simulated points for dual DC sweeps
    can often be simply ignored.

    B{Note:} Due to combinatorial explosion and lack of use case, only
    1 enumerable indep vector is currently supported in combination
    with a non-enumerable vector. (Some of the code structure is here
    for using two of them.)

    @ivar kInterp: The integer column index of a single continuous
        (non-enumerable) independent vector with monotonically
        ascending values, or C{None} if there is not one and only one
        such vector.
    
    @ivar kcList: A list of column indices of continuous (non-enumerable)
        independent vectors.

    @ivar keList: A list of column indices of enumerable independent
        vectors.

    @ivar uvList: A list of 1-D arrays of the unique values for each
        enumerable independent vector.
    """    
    def __init__(self, indieFlags):
        """
        C{IV_Manager(indieFlags)}
        """
        self.indieFlags = indieFlags
        self.enumerable = Enumerable()
        self.clear()

    def __nonzero__(self):
        """
        I evaluate as C{True} if my setup has any independent
        vectors. (Almost always the case.)
        """
        return bool(self.indieFlags)
        
    def __iter__(self):
        """
        I iterate over the column indices of all of my setup's independent
        vectors.
        """
        for k, isIndep in enumerate(self.indieFlags):
            if isIndep:
                yield k

    def dependerator(self):
        """
        Yields the column index of each dependent vector. Sort of the
        opposite of iterating over me directly with L{__iter__}.
        """
        for kCol, isIndep in enumerate(self.indieFlags):
            if not isIndep:
                yield kCol

    def enumerableator(self):
        """
        Yields the column index of each enumerable independent vector, a
        subset of what you get from iterating over me directly with
        L{__iter__}, or possibly no iterations at all.

        B{Note:} Only at most one enumerable independent vector is
        currently supported, so this will only iterate once or not at
        all.
        """
        for kCol in self.keList:
            yield kCol
                
    def clear(self):
        self.kInterp = None
        self.kcList = []
        self.keList = []
        self.uvList = []

    def noEnumerables(self):
        return not self.keList

    def subseterator(self, kCol, *args):
        """
        For each unique value of the enumerable independent vector at the
        specified column index I{kCol}, yields indices of matching
        values at a specified column index of a supplied array.
 
        Provide at least one pair of arguments after I{kCol}: (1) the
        column index of the supplied array and (2) the array
        itself. Argument pairs may be added for additional
        arrays. The yielded outputs are lists of one or more subset
        arrays, one for each argument pair.

        Each subset array contains the row indices of a subset of the
        array where the values of the vector at the column index
        exactly equal the unique value. For a 1-D Numpy array, its
        column index must equal zero.
        """
        def pairs():
            for k in range(len(args)/2):
                yield args[2*k:2*k+2]
        
        if kCol not in self.keList:
            raise IndexError(sub(
                "No enumerable independent vector at column {:d}", kCol))
        k = self.keList.index(kCol)
        for value in self.uvList[k]:
            yield [np.flatnonzero(np.equal(X[:,kCol], value))
                   for kCol, X in pairs()]

    def _monotonic(self, Z):
        """
        Returns C{True} if vector I{Z} is monotonically increasing for all
        its values.
        """
        if max(Z.shape) < 2: return
        return np.all(np.diff(Z) > 0)

    def _canInterpolate(self, kCol, X):
        """
        Returns C{True} if I{kCol} points to a column vector of I{X} that
        you can use as the x-axis for a call to Numpy C{interp}.
        """
        if not self.keList:
            return self._monotonic(X[:,kCol])
        for keCol in self.keList:
            if keCol == kCol: continue
            # See if this vector is monotonically increasing for this
            # EIVs values
            for K in self.subseterator(keCol, keCol, X):
                if not self._monotonic(X[K,kCol]):
                    # Nope
                    return
        return True
    
    def _interpolatableEIV(self, X):
        """
        If one of my EIVs can be considered a CIV on which interpolation
        can be done, returns its records index. Otherwise, returns
        C{None}.

        Looks through my EIVs, starting with the one with the most
        unique values, for one whose subsets at each value of the
        other enumerable(s) are all monotonically increasing.
        """
        if len(self.keList) < 2:
            # No spare EIVs
            return
        for k in reversed(np.argsort([len(x) for x in self.uvList])):
            # Get the EIV column index for this records index
            kCol = self.keList[k]
            if self._canInterpolate(kCol, X):
                return k
    
    def setup(self, X):
        """
        To set me up, call this with a 2-D array of goal points I{X}.

        For each independent vector, processes its column of the goals
        array I{X}. If the vector is enumerable, adds its column index
        and unique values to my I{keList} and I{uvList},
        respectively. Otherwise, adds the index to my I{kcList} and
        maybe sets I{kInterp} to it.

        A vector is considered enumerable when it has no more than
        I{maxUniqueVals} unique values and there are at least two of
        each unique value.

        Sets my I{kInterp} attribute to the column index of a
        independent vector in I{X} if (1) it is not an enumerable
        independent vector, (2) each subset of its values is
        monotonically increasing for unique values of all EIVs in
        I{X}, or monotonically increasing across its entire range if
        there are no EIVs, and (3) it is the only non-enumerable
        (continuous) vector in I{X}. Otherwise, I{kInterp} remains
        C{None}, indicating that interpolation cannot be used.
        """
        self.clear()
        kCols = list(self)
        if not kCols:
            # Special case: No independent vector at all
            return
        for kCol in kCols:
            uv = self.enumerable(X[:,kCol])
            if uv is None:
                # Continuous (non-enumerable) independent vector
                self.kcList.append(kCol)
            else:
                # Enumerable independent vector
                self.keList.append(kCol)
                self.uvList.append(uv)
        if not self.kcList:
            # There is no CIV, so consider one EIV continuous if
            # interpolation could be done on it
            k = self._interpolatableEIV(X)
            if k is not None:
                self.kInterp = self.keList.pop(k)
                self.uvList.pop(k)
                self.kcList.append(k)
            return
        if len(self.kcList) == 1:
            # We have a single CIV, but need to check that its values
            # are monotonically increasing for each subset of any
            # enumerable independent before setting interpolation
            # column index to it
            kCol = self.kcList[0]
            if self._canInterpolate(kCol, X):
                # Yes, this works
                self.kInterp = kCol


class EvalSpec(object):
    """
    I hold all the information needed to specify evaluations for a
    given setup.

    Construct me with the following arguments:

        1. Integer setup I{ID},

        2. List I{nameList} of vector names,

        3. List I{indieFlags} of bools, one for each vector name,
           indicating if its vector is independent.

        4. Set I{logValues} (possibly empty) of vector names that are
           to be evaluated in log space rather than linear.

    You will need to run my L{setupX} method before using the
    instance. If I'm not using a callable goal, you also need to run
    L{setWeights}.

    @ivar ivm: An instance of L{IV_Manager} that manages records about
        the independent vectors for my setup's goal points.
    
    @see: L{ErrorTabulator.add}.
    """
    def __init__(self, ID, nameList, indieFlags, logValues):
        self.ID = ID
        self.nameList = nameList
        if indieFlags and len(indieFlags) != len(nameList):
            raise ValueError(
                "With indieFlags, there must be one per vector name")
        self.ivm = IV_Manager(indieFlags)
        self.logValues = logValues
        self.q = None

    def __repr__(self):
        return sub(
            "<EvalSpec ID={:d} for {} at {}>",
            self.ID, ", ".join(self.nameList), hex(id(self)))

    def canInterpolate(self):
        """
        Returns C{True} if you can use interpolation-based SSE calculation
        for my setup.

        @see: L{IV_Manager}.
        """
        return self.ivm.kInterp is not None
    
    def setupX(self, X, q=None):
        """
        L{Evaluator.setup} calls this with a reference I{X} to a goal
        callable or 2-D array of goal points and a reference I{q} to
        its local task queue.

        I set my I{X} attribute to the goal object. I will set my I{q}
        attribute to the queue if the goal is callable and doesn't
        return a deferred result. That way the goal can run in a
        thread without blocking.

        If the callable says it returns a C{Deferred} by having a
        I{dr} attribute set C{True}, then I will leave the I{q}
        attribute at C{None} and trust that the callable won't block.

        If there is no goal for my setup, set the I{X} arg to C{None},
        although that seems kind of pointless.
        """
        if X is None:
            self.N = 1
        elif callable(X):
            self.N = 1
            if not getattr(X, 'dr', False):
                self.q = q
        else:
            Nc = X.shape[1]
            if len(self.nameList) != Nc:
                #--- Uncomment for DEBUG -----------------
                #import pdb; pdb.set_trace()
                #-----------------------------------------
                raise ValueError(
                    "There must be one column of X for each item "+\
                    "of vectorNames")
            self.N = X.shape[0]
            self.ivm.setup(X)
        self.X = X
        
    def setWeights(self, weights):
        """
        Call this with a dict of I{weights}, one entry keyed by each name
        in my I{nameList}.

        If there isn't an entry for a particular name, it will be
        given a default weight of one.

        If the entry is a callable, it must accept an integer ID and
        scalar values of its vector and return a scalar weight. In a
        one-time setup operation, I will call it with my I{ID} and
        each goal value of its vector, and assign a weight to that
        goal value for my setup.

        Returns a string describing the weights.
        """
        def summary(X):
            if isinstance(X, np.ndarray):
                if len(X) == 1: X = X[0]
                else:
                    Xmin = X.min()
                    Xmax = X.max()
                    if Xmin == Xmax: X = X[0]
                    else:
                        return sub(
                            "ARRAY[{:.3g}-{:.3g}, min={:.3g}, max={:.3g}]",
                            X[0], X[-1], X.min(), X.max())
            return "Unity" if X == 1 else sub("{:g}", X)
        
        W_cols = []
        lines = [sub("Weights for Setup {:03d}:", self.ID)]
        if self.X is None:
            return lines[0] + " (None)"
        if callable(self.X):
            return lines[0] + " (Callable goal)"
        lines.append("-"*100)
        for k, name in enumerate(self.nameList):
            name = name.lstrip('+')
            Xc = self.X[:,k]
            if name not in weights:
                Wc = np.ones(self.N)
                info = "Unity"
            else:
                x = weights[name]
                if callable(x):
                    Wc = tryCall(x, self.ID, Xc)
                    if not isinstance(Wc, np.ndarray) or len(Wc) == 1:
                        Wc *= np.ones(self.N)
                    info = sub(
                        "{}({}) -> {}", x.__name__, summary(Xc), summary(Wc))
                else:
                    Wc = x * np.ones(self.N)
                    info = sub("{}", summary(Wc))
            lines.append(sub("{:>12s}  {}", name, info))
            if np.any(np.equal(Wc, None)):
                raise ValueError(sub(
                    "Vector '{}' has 'None' in weight!", name))
            W_cols.append(Wc)
        if W_cols:
            self.W = tryCall(np.column_stack, W_cols)
        return "\n".join(lines)


class Evaluator(object):
    """
    I perform evaluations using a L{MultiRunner} and one or more goal
    setups.
    
    Construct me with a list I{avList} of AV objects, parents and
    children, known and unknown, for all setups.

    Then, when you can wait on a C{Deferred}, call my L{Setup} method
    with the following dicts keyed by setup ID with one entry for each
    setup:

      1. I{nameLists} with lists of vector names,
    
      2. I{analyzers} with sequences that define the analysis to be
         done, each beginning with either a subclass of an Ngspice
         Analyzer or an instance of a Python analyzer,

      3. I{Xs} with evaluation goals,

      4. I{netlists} of text for Ngspice Analyzers or C{None} for Python
         Analyzers,

      5. I{indies} with lists of the vector names in each list of
         I{nameLists} that are independent, and

    @see: L{Setup} for further details. For a TCP-based counterpart,
        see L{WireEvaluator}.

    @keyword transforms: You can provide a dict of sequences that each
        contain a callable and the names of vectors whose values it
        will accept as arguments. Before an evaluation that includes a
        vector name with an entry in I{transforms}, each transforming
        callable for such a name takes the setup I{ID} followed by
        vector values resulting from a call to my C{MultiRunner} and
        produces a vector value for the name under which it was keyed
        in I{transforms}.

    @keyword logValues: You can provide a set of vector names that are
        to be evaluated in log space rather than linear.
    
    @keyword N_cores: The number of that analyzers that my
        L{MultiRunner} maintains for each setup.

    @keyword verbose: Set C{True} to include info about Ngspice
        failures in the output. Otherwise, failures are only indicated
        by a "#" character.

    @keyword spew: Set C{True} to include warnings from
        Ngspice in the output. This can make things pretty messy.
    """
    def __init__(
            self, cfg, avList, transforms={}, logValues=set(), N_cores=None):
        """Constructor"""
        self.cfg = cfg
        self.avList = avList
        self.transforms = transforms
        self.logValues = logValues
        self.N_cores = N_cores
        self.mr = None
        self.qLocal = asynqueue.ThreadQueue(raw=True)
        self.skipped = set()
        self.running = None
        self.etimer = EvalTimer(0)

    @defer.inlineCallbacks
    def shutdown(self):
        """
        Shuts down my L{MultiRunner} and then my local ThreadQueue.

        Returns a C{Deferred} that fires when I'm done shutting down.
        """
        if self.running:
            self.running = False
            fhPrev = 999 if self.cfg.verbose else msg(False)
            msg("Shutting down Evaluator")
            if self.mr is not None:
                yield self.mr.shutdown()
                msg(2, "MultiRunner is shut down")
                self.mr = None
            if self.qLocal is not None:
                yield self.qLocal.shutdown()
                msg(2, "Local ThreadQueue is shut down")
                self.qLocal = None
            if fhPrev is not 999:
                msg(fhPrev)

    @defer.inlineCallbacks
    def setup(
            self, nameLists, analyzers, Xs, netlists, indies,
            weights={}, skipIDs=[]):
        """
        Sets up evaluation for each of my setups.

        Parameter Notes
        ===============
        
            Each sequence in I{analyzers} begins with either a
            subclass of L{sim.Analyzer} or an object constructed from
            L{psim.Analyzer}, and is followed by one or more args used
            in the construction or setup, respectively, of that
            analyzer.
            
            Each entry in I{Xs} is either a 2-D Numpy array of
            expected goal values for the points in the vectors for its
            set up, or a callable (TODO: Describe). Each row of that
            array represents one point in the N-dimensional simulation
            result space for that setup, where N is the length of the
            vector name list for that setup.

            Post-simulation evaluation time will scale somewhat with
            the number of rows in each I{X}, so pick your points
            judiciously.
    
            There almost always will be at least one (and usually one)
            independent vector. However, it is not an error to supply
            an empty list for any entry of I{indies}.

        Call Parameters
        ===============

            Call with the following dicts keyed by setup ID with one
            entry for each setup:
        
        @param nameLists: Lists of vector names.
        
        @param analyzers: Sequences that define the analysis to be
           done, each beginning with either a subclass of an Ngspice
           Analyzer or an instance of a Python analyzer, followed by
           args for the constructor or C{setup} method of the
           analyzer, as the case may be.

        @param Xs: Evaluation goals.
        
        @param netlists: Text for Ngspice Analyzers (entries may be
            omitted or set to C{None} for Python Analyzers).
        
        @param indies: Lists of the vector names in each list of
            I{nameLists} that are independent.

        @keyword weights: You can provide a dict (keyed by parameter
            name, for all IDs) to give non-unity weight to values in
            the evaluations.

        @keyword skipIDs: An optional list or set of setup IDs to
            skip, in addition to any I've already been told to skip.
        """
        for ID in nameLists:
            if ID not in analyzers:
                raise KeyError(sub(
                    "No analyzer sequence for ID {:d}", ID))
            if ID not in Xs:
                aco = analyzers[ID][0]
                if not isinstance(aco, type) and hasattr(aco, 'avDefine'):
                    Xs[ID] = None
                else:
                    raise KeyError(sub(
                        "No X goal callable or array for ID {:d}", ID))
            if self.cfg.verbose and ID not in indies:
                msg("WARNING: You probably want to define at least one "+\
                    "independent vector for each setup!")
        self.evalSpecs = {}
        if self.mr is not None:
            yield self.mr.shutdown()
        # I'll have multiple ones of these later, used via AsynQueue.wire
        self.mr = MultiRunner(self.cfg, self.avList, self.N_cores)            
        self.nameLists = {}
        self.skipped = self.skipped.union(set(skipIDs))
        for ID in nameLists:
            if ID in self.skipped:
                continue
            vectorNames = []
            nameList = nameLists[ID]
            snameList = self.nameLists[ID] = []
            for name in nameList:
                sname = name.lstrip('+')
                snameList.append(sname)
                if sname in self.transforms:
                    # A transform callable was found that produces
                    # this vector; instead of asking the MultiRunner
                    # to produce this vector directly, make sure it
                    # produces all vectors needed for the transform
                    # arguments
                    for tname in self.transforms[sname][1:]:
                        if tname not in vectorNames:
                            # This is the unstripped name, so you
                            # can specify that an input to the
                            # transform be provided as an absolute
                            # value by preceding it with the + sign,
                            # just as with a regular item of the
                            # nameLists
                            vectorNames.append(tname)
                    continue
                if name not in vectorNames:
                    # This is just a regular vector produced directly
                    # by the MultiRunner. Note that this is the
                    # unstripped name, which may be preceded by a "+"
                    # to indicate absolute value.
                    vectorNames.append(name)
            if self.mr is not None:
                # Not aborting, proceed
                yield self.mr.addSetup(
                    ID, vectorNames, analyzers[ID], netlists.get(ID, None))
                X = Xs[ID]
                indieFlags = [sname in indies.get(ID, []) for sname in snameList]
                evalSpec = EvalSpec(ID, nameList, indieFlags, self.logValues)
                yield evalSpec.setupX(X, self.qLocal)
                # We could just send the new evalSpec the weights of
                # vector names relevant to its setup, but it doesn't
                # really cost anything to just send them all every time.
                info = evalSpec.setWeights(weights)
                if self.cfg.chatty: msg(-1, info)
                self.evalSpecs[ID] = evalSpec
                self.running = True
    
    def __iter__(self):
        """
        I iterate over setup IDs that I started with and have not been
        told to L{skip}.

        No particular order.
        """
        for ID in self.evalSpecs:
            if ID not in self.skipped:
                yield ID
            
    def __len__(self):
        """
        My length is the number of eval specs I am actively managing.

        If I've been told (via L{skip}) to skip one or more setup IDs
        even if I started with and have evalSpecs for them, my length
        (and iterations) will omit those.
        """
        return len([1 for ID in self.evalSpecs if ID not in self.skipped])

    def skip(self, *IDs):
        """
        Call this to make me skip the supplied setup ID or IDs, even if I
        have evalSpecs for them.
        """
        for ID in IDs:
            self.skipped.add(ID)

    def _gotV(self, V, et, ID):
        """
        Called by L{evaluate} and L{evaluateSSE} to add simulation results
        in I{V} to the supplied L{ErrorTabulator} I{et}, for the
        specified setup I{ID}.

        Returns a C{Deferred} that fires when the results have been
        added, unless there was an Ngspice error.

        In that case, I{et} has its I{bogus} flag set to prevent it
        from wasting time completing other tabulations. Then, if the
        configuration I{cfg} calls for me to stop on errors, I call
        L{shutdown} and return the C{Deferred} from that. Otherwise, I
        then just return immediately.

        Yes, it is a real mess trying to get this unwieldy
        asynchronous beast to shut down properly.
        """
        if V is None or V.error():
            et.bogus = True
            if self.cfg.stop:
                return self.shutdown()
            return
        evalSpec = self.evalSpecs[ID]
        return et.add(ID, V, evalSpec)
    
    @defer.inlineCallbacks
    def evaluate(self, alterableValues, study=False, xSSE=None):
        """
        Runs an analysis with the supplied I{alterableValues} for all
        setup IDs.

        Returns a C{Deferred} that fires with an instance of
        L{ErrorTabulator} containing info about the analysis, most
        importantly I{SSE}, the sum of squared errors between the
        closest simulated point to each goal point previously
        established by a call to I{setup}.

        If one or more independent variables has been defined (almost
        always the case), the SSE is the sum of evaluations of each
        simulated point whose independent variable components are
        closest to each goal point defined by the independent
        variables. Otherwise, each evaluation is for the simulated
        point closest to each goal point. Weighting is used in either
        case.

        If the analysis fails or a needed vector is not present as an
        analysis's result, the "returned" SSE is set to C{None}. If
        pingspice is shutting down, the SSE is set to -1, which alerts
        C{ade} that it needs to abort.

        @keyword study: Set C{True} to have netlists of each setup
            written for study, even without an error and even if it
            means overwriting an existing netlist file.

        @keyword xSSE: Set to an SSE value of a target individual that
            the evaluation has to be in order to be considered a
            successful challenge. If the SSE reaches that value,
            evaluation will be aborted because it won't change any
            outcomes and the (partial) SSE won't be reported or used
            in any way.
        """
        # I need a new one of these for each evaluation because my
        # MultiRunner may have several analyzers for each setup.
        et = sse.ErrorTabulator(self.nameLists, self.transforms)
        # Evals are done in parallel, unless xSSE
        if xSSE is None:
            dList = []
            for ID in self:
                if self.mr is None:
                    break
                d = self.etimer(self.mr.run, ID, alterableValues, study)
                d.addCallback(self._gotV, et, ID)
                dList.append(d)
            if dList:
                yield defer.DeferredList(dList)
        else:
            # xSSE, do evals one at a time (yielding, of course),
            # sorted so fastest first
            for ID in self.etimer:
                if self.mr is None:
                    break
                d = self.etimer(self.mr.run, ID, alterableValues, study)
                d.addCallback(self._gotV, et, ID)
                yield d
                if et.total() > xSSE:
                    break
        # Careful about memory leaks! Every et reference keeps a
        # reference to a separate copy of V.
        defer.returnValue(et)

    @defer.inlineCallbacks
    def evaluateSSE(self, alterableValues, ID=None, xSSE=None):
        """
        Gets the SSE for the supplied I{alterableValues}, possibly only
        for a single specified setup I{ID}.

        Returns a C{Deferred} that fires with the SSE.

        If there was an error at any point during the evaluation(s),
        the SSE is set to infinite, unless I am configured to stop on
        error. In that case, the SSE is set to -1, which alerts
        upstream stuff that it's time to abort everything.

        @keyword ID: Set to a setup ID if evaluation is only desired
            for a single setup rather than all of them.
        
        @keyword xSSE: Set to a target SSE. Evaluations are allowed to
            quit early if they accumulate an SSE greater than
            this. With this set, the returned SSE is only be accurate
            to the extent that it exceeds I{xSSE} and thus a challenge
            based on the evaluation would fail.
        """
        if self.mr is None:
            # We must have either shut down or not been set up
            # yet. Either way, it's a fatal error
            result = -1
        else:
            if ID is None:
                # Evaluation for all setup IDs
                et = yield self.evaluate(alterableValues, xSSE=xSSE)
            else:
                # Evaluation for a single setup ID
                et = sse.ErrorTabulator(self.nameLists, self.transforms)
                d = self.etimer(self.mr.run, ID, alterableValues)
                d.addCallback(self._gotV, et, ID)
                yield d
            if et.bogus:
                # There was an error at some point
                result = -1 if self.cfg.stop else float('+inf')
            else: result = et.total()
        # Neither the I{et} object nor its copy of I{V} is referenced
        # after this point
        defer.returnValue(result)
    
    def evaluateAll(self, alterableValueLists):
        """
        Calls L{evaluateSSE} for each list of alterable values in the
        supplied list-of-lists.

        Returns a C{Deferred} that fires with a list of
        sum-of-squared-errors, one for each sub-list.

        If there is just one alterable value, you can supply a single
        list of those values.
        """
        dList = []
        if not hasattr(alterableValueLists[0], '__iter__'):
            if len(self.evalSpecs) == 1:
                dList = [self.evaluateSSE([x]) for x in alterableValueLists]
            else:
                raise ValueError(
                    "With more than one alterable value, you must"+\
                    "supply a list of lists.")
        if not dList:
            for alterableValues in alterableValueLists:
                dList.append(self.evaluateSSE(alterableValues))
        return defer.gatherResults(dList)
