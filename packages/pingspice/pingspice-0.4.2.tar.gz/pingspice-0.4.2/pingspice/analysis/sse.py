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
With the L{ErrorTabulator} and support staff, this module does the
nuts and bolts of computing a sum-of-squared-error fitness metric SSE.

The SSE indicates how close a particular combination of component
values and device parameters functions compared to the circuit's
stated goals. See L{ErrorTabulator.add} for a discussion of goals and
the different forms they can take.
"""

import numpy as np
from twisted.internet import reactor, defer, task

from pingspice.util import *


class Run(object):
    """
    I hold the static results of an evaluation run for a single setup
    ID.

    The I{X} attribute of my L{evalSpec} deserves some discussion. It
    is the 2-D Numpy array of goal points that L{ErrorTabulator} used
    in comparing simulation results to what they should have been. The
    independent vs. dependent vector coordinates in the array are
    plotted with "X" symbols. There is an "X" symbol for each
    combination of independent value and dependent value. For example,
    if X has shape (4,3), with two dependent vectors, there will be
    eight "X" points.

    However, the columns for dependent vectors in the X array can have
    C{nan} values, which indicates to the plotter that what is desired
    is instead a vertical line indicating the independent vector value
    and a circle symbol where the line intersects the dependent vector
    value that is specified.

    @ivar nameList: A list of names of vectors obtained from this run.

    @ivar SSE: The sum of squared errors for the evaluation in this
        run.

    @ivar X: A 2-D Numpy array of goal points for the evaluation.
    
    @ivar evalSpec: An instance of L{EvalSpec} for the setup.

    @ivar V: A copy of the instance of a L{VectorsBase}
        subclass that got populated with simulation
        results. Significantly, this is a B{copy}, not the original,
        because the original will probably get updated with results of
        another simulation.
    """
    X = None

    def __nonzero__(self):
        return self.X is not None
    

class Result(object):
    """
    I hold comprehensive results of a multi-setup evaluation in my
    I{runs} dict, with each element being an instance of L{Run}.

    Significantly, I store a B{copy} of the L{VectorBase} subclass
    instance from each setup's simulation because the original will
    likely get overwritten soon.

    Use L{Result_SSE} instead if all you will ever need is the total
    SSE.
    """
    def __init__(self, nameLists):
        self.nameLists = nameLists
        self.runs = {}
        self._cached_SSE = None
        self._SSE0 = 0
    
    @property
    def SSE(self):
        """
        Property: My SSE is the sum of SSEs for all runs, unless one of
        them is negative or C{None}.

        A run with a negative SSE gives me an SSE of -1. A run with an
        SSE of C{None} gives me an infinite SSE.
        """
        if self._cached_SSE is not None:
            return self._cached_SSE
        total = self._SSE0
        for run in self.runs.values():
            if run.SSE is None:
                return float('+inf')
            if run.SSE < 0:
                return -1
            total += run.SSE
        self._cached_SSE = total
        return total

    def __contains__(self, ID):
        return ID in self.runs
    
    def __len__(self):
        return len(self.runs)
        
    def __iter__(self):
        for ID in sorted(self.runs.keys()):
            yield ID, self.runs[ID]

    def __getitem__(self, ID):
        return self.runs[ID]

    def nameList(self, ID):
        return self.nameLists[ID] if ID in self else []

    def makeBogus(self):
        self._SSE0 = float('+inf')
    
    def __call__(self, ID, SSE, *args):
        """
        Call my instance with a setup I{ID} and I{SSE}. If not an SSE-only
        analysis, also include the setup's goal array I{X} and
        L{EvalSpec} object, and the simulation result's C{Vectors}
        instance I{V}. Creates a L{Run} with results for that setup.

        Critically, the new run object's I{V} attribute is a copy of
        I{V}, not the supplied object itself. That way, other things
        can modify I{V} without messing up the results of this run.

        This is the only valid way to modify my I{runs} dict.
        """
        if SSE: self._cached_SSE = None
        run = self.runs[ID] = Run()
        run.nameList = self.nameLists[ID]
        run.SSE = SSE
        if not args: return
        run.X = args[0]
        run.evalSpec = args[1]
        # Critical that it be a copy!
        run.V = args[2].copy()


class Result_SSE(object):
    """
    A stripped-down stand-in for L{Result}.

    Used by L{ErrorTabulator} if it is constructed without a populated
    nameList.
    """
    __slots__ = ('SSE',)
    
    def __init__(self):
        self.SSE = 0

    def __contains__(self, ID):
        """
        I contain no setup runs.
        """
        return False

    def __len__(self):
        return 0

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration
    
    def nameList(self, ID):
        return []

    def makeBogus(self):
        self.SSE = float('+inf')
    
    def __call__(self, ID, SSE, *args):
        """
        I have the same call pattern as L{Result} for compatibility but
        all I actually need is the SSE.
        """
        self.SSE += SSE


class ErrorTabulator(object):
    """
    I tabulate the sum of squared errors between a simulated result
    and the goals you'd set for that simulation.

    Construct me with a dict of I{nameLists}, optionally, a dict of
    I{transforms} with callables keyed by vector name. If all that
    will ever be asked of me is the total SSE, you can omit the
    I{nameLists}. (For remote evaluations, only the total SSE will
    ever be required.)

    I am a disposable object. Use me once and throw away, to avoid
    concurrency problems.

    @ivar bogus: C{True} if an error occurred while producing my
        result, or if I've been told to abort tabulation.
    """
    __slots__ = [
        '_bogus', 'transforms', 'result', 'notRunning', 'dLock', 'SSE']
    
    def __init__(self, nameLists=None, transforms={}):
        """
        C{ErrorTabulator(nameLists=None, transforms={})}
        """
        self.result = Result_SSE() if nameLists is None else Result(nameLists)
        self.transforms = transforms
        self.dLock = defer.DeferredLock()
        self.notRunning = False
        self._bogus = False

    @property
    def bogus(self):
        return self._bogus
    @bogus.setter
    def bogus(self, yes):
        if yes: self.result.makeBogus()
        self._bogus = yes

    def __nonzero__(self):
        """
        I am C{True} if I'm not bogus, i.e., no errors occurred while
        producing my result, and I haven't been told to abort
        tabulation.
        """
        return not self.bogus
        
    def __float__(self):
        SSE = self.total()
        return float('+inf' if SSE is None else SSE)
    
    def __lt__(self, other):
        return float(self) < float(other)

    def __le__(self, other):
        return float(self) <= float(other)

    def __gt__(self, other):
        return float(self) > float(other)

    def __ge__(self, other):
        return float(self) >= float(other)

    def __eq__(self, other):
        return float(self) == float(other)

    def __ne__(self, other):
        return float(self) != float(other)

    def __sub__(self, other):
        return float(self) - float(other)
    
    def __div__(self, other):
        return float(self) / float(other)

    def __str__(self):
        return str(float(self))

    def __repr__(self):
        lines = [sub(
            "<ErrorTabulator at {}> with SSE={:.4g}:",
            hex(id(self)), self.total())]
        for ID, run in self.result:
            if len(lines) == 1: lines.append("-"*70)
            nameList = ", ".join(self.result.nameList(ID))
            lines.append(sub("{:03d}  {:7.4g}  {}", ID, run.SSE, nameList))
        return "\n".join(lines)
    
    def maybeLog(self, x, evalSpec, name):
        """
        If the vector I{x} with the specified I{name} is to be evaluated
        in logspace, returns its base-10 (common) logarithm.

        Any values less than or equal to zero are converted to 1/10
        the minimum positive non-zero value or to 1e-30 if there are
        no positive non-zero values.
        """
        if name.lstrip('+-') in evalSpec.logValues:
            K = np.flatnonzero(x <= 0)
            if len(K):
                K_gz = np.flatnonzero(x > 0)
                xMin = np.min(x[K_gz]) if len(K_gz) else 1e-29
                x[K] = 0.1*xMin
            return np.log10(x)
        return x
    
    def total(self):
        """
        Returns my total SSE of all evals done.
        """
        return self.result.SSE

    def biggestDiff(self, other):
        """
        Identifies the biggest per-setup SSE difference between my results
        and the results of another instance of me I{other}.

        Returns 3-tuple with (1) the setup ID for the biggest SSE
        difference, (2) my SSE for that setup, and (3) the SSE of
        I{other} for that setup. If no SSE difference was found,
        returns C{None}.
        """ 
        ID = None
        max_diff_SSE = 0
        for thisID, run in self.result:
            diff_SSE = abs(run.SSE - other.result[thisID].SSE)
            if diff_SSE > max_diff_SSE:
                ID = thisID
                max_diff_SSE = diff_SSE
        if ID is None:
            return None, self.total(), other.total()
        return ID, self.result[ID].SSE, other.result[ID].SSE
    
    def closenessToIndepInterpolated(self, X, Y, evalSpec):
        """
        Call this when you have a single non-enumerable independent vector
        that is increasing in values.

        That will usually be the case. This method's way of evaluating
        is more efficient and gives a more accurate result, so use it
        whenever you can.

        Each dependent vector value is linearly interpolated to find
        what its value would have been (an estimate, but a pretty
        close one) for each independent vector value. Then those
        interpolated dependent values are compared to what they are
        expected to be for each independent value, all in one
        sum-of-squares operation for each dependent vector value.

        The weight of the independent vector is disregarded for this
        type of closeness calculation. That's because the difference
        between observed and expected dependent vector values is
        calculated at the dependent vector's exact values, not some
        close-by point as with L{closenessToIndep} and
        L{closenessToAll}.

        If there is also an enumerable independent vector, the
        calculation is repeated for each unique value of that vector,
        with a subset of rows of I{X} and I{Y} where that vector has
        an exact match with particular unique value.
        """
        def K_allRows(Z):
            return np.ravel(np.indices([Z.shape[0]]))
        
        def calculate(kDep, KX, KY):
            """
            Calculates SSE for simulated vs expected values of the dependent
            at the specified column index I{kDep} of goal array I{X}
            and simulation array I{Y}.

            I{KX} is a 1-D Numpy array of indices for a subset (or the whole
            thing) of rows for B{goal values} of the continuous
            independent and dependent vectors, and of the
            corresponding rows of the weights array.

            I{KY} is a 1-D Numpy array of indices for a subset (or the whole
            thing) of rows for B{simulation values} of the continuous
            independent and dependent vectors.
            """
            # Independent vector X (expected) and Y (actual)
            # values. Confusingly, these are not related to the x-axis and y-axis
            # of the Numpy interp function.
            Xi = X[KX,kInterp]
            Yi = Y[KY,kInterp]
            # The expected dependent values
            Xd = X[KX,kDep]
            # The actual dependent values
            Yd = Y[KY,kDep]
            # The interpolated dependent values at each expected
            # independent value. This is the opposite of what you
            # might think! We are interpolating to come up with an
            # interpolated simulated dependent value as it would have
            # occured at the exact same independent-vector value as
            # the expected dependent value.
            try:
                Yinterp = np.interp(Xi, Yi, Yd)
                # The error is between each interpolated ACTUAL
                # dependent value and its respective EXPECTED
                # dependent value. Scaled by weight of each
                # independent value times weight of its corresponding
                # dependent value.
                SSE = np.sum(evalSpec.W[KX,kDep] * np.square(Yinterp - Xd))
            except:
                # If Numpy interp complains for any reason, bogus (infinite) SSE
                SSE = float('+inf')
            # Add to the running SSE total
            self.SSE += SSE

        ivm = evalSpec.ivm
        kInterp = ivm.kInterp
        if ivm.noEnumerables():
            # No enumerable independents to deal with; use all
            # simulation rows
            for kDep in ivm.dependerator():
                yield calculate(kDep, K_allRows(X), K_allRows(Y))
        else:
            for kCol in ivm.enumerableator():
                for KX, KY in ivm.subseterator(kCol, kCol, X, kCol, Y):
                    for kDep in ivm.dependerator():
                        yield calculate(kDep, KX, KY)
    
    def closenessToIndep(self, X, Y, evalSpec):
        """
        SSE of the closest points in I{Y} to each combination of
        independent values (as selected by the I{I} index list/vector)
        in the 2-D array I{X}.

        Weights I{W} are of the same dimensions as X. Weights of
        independent vector values are considered along with dependent
        vector values, because the SSE of each point is partially
        dependent on how close the selected goal point is to the
        simulated point.

        If I manage to select a goal point whose independent-vector
        value(s) exactly match the simulated independent-vector
        values, then the independent vector value weight will be
        multiplied by zero (as part of the vector product) and thus
        irrelevant. But only in that case, for this closeness
        computation method. If you will have an exact match between
        simulation and goal at every point, for all of your
        independent vectors except at most one, use
        L{closenessToIndepInterpolated} instead.

        Except where there are just one or two goal points,
        independent values in X that exceed the range of independent
        values in Y will be disregarded. For best results, make sure
        your Y more than covers the range of X.
        """
        N = Y.shape[0]
        kkE = {0, N}
        W = evalSpec.W
        I = list(evalSpec.ivm)
        Yi = Y[:,I]
        for k, ePoint in enumerate(X):
            kk = np.argmin(np.sum(
                np.square(ePoint[I] - Yi), axis=1), axis=0)
            if len(kkE) > 2 and kk in kkE:
                # There aren't dependent Y values on both sides of
                # this goal point, or this kk value was already used,
                # so we must skip this goal point
                continue
            # If there are too few Y points for all the nearby X goal
            # points, at least don't compound the SSE penalty by
            # counting distance to the same Y point multiple times
            kkE.add(kk)
            self.SSE += np.sum(W[k,:] * np.square(ePoint - Y[kk,:]))
            yield
            if self.bogus: break

    def closenessToAll(self, X, Y, evalSpec):
        """
        Call this instead of L{closenessToIndep} in the unlikely case that
        there are no independent column vectors in I{X}.

        The SSE will be the minimum distance between each goal point
        in I{X} and all points in I{Y}, with weighting by I{W}. The W
        array must be of the same dimensions as X, with one weight
        combo for each goal point.

        You will probably never use this. When will you have a
        situation where there is no independent variable?
        """
        W = evalSpec.W
        for k, ePoint in enumerate(X):
            E = W[k,:] * np.square(ePoint - Y)
            self.SSE += np.sum(E, axis=1).min()
            yield
            if self.bogus: break
    
    def closenesserator(self, ID, X, V, evalSpec):
        """
        Iterator for doing math-intensive simulation post-processing in a
        Twisted-friendly manner.

        All the yielding involved doesn't seem to incur any noticeable
        performance hit.

        Updates my I{SSE} attribute in place.
        """
        vectors = []
        for k, name in enumerate(evalSpec.nameList):
            if not self: break
            stuff = self.transforms.get(name, None)
            if stuff and callable(stuff[0]):
                transform = stuff[0]
                args = [ID]
                for arg in stuff[1:]:
                    if isinstance(arg, str) and arg in V:
                        args.append(V[arg])
                        continue
                    if callable(arg):
                        args.append(arg())
                        continue
                    args.append(arg)
                try:
                    Vk = transform(*args)
                except:
                    Vk = None
                    self.bogus = True
                    print sub(
                        "TRANSFORM ERROR with {}({}):\n",
                        transform.__name__, ", ".join(stuff[1:]))
                    import pdb; pdb.set_trace()
                if Vk is not None: V.addVector(name, Vk)
            elif name not in V:
                self.bogus = True
            else: Vk = V[name]
            if self.bogus: break
            try: Vk_max = Vk.max()
            except: Vk_max = 1E10
            if Vk_max > 1E9:
                self.bogus = True
                break
            vectors.append(self.maybeLog(Vk, evalSpec, name))
        else:
            # This block is executed only there was no error inducing
            # me break out of the for loop
            Y = np.column_stack(vectors)
            #SSE0 = self.SSE # For debugging only
            if evalSpec.canInterpolate():
                func = self.closenessToIndepInterpolated
            elif evalSpec.ivm:
                func = self.closenessToIndep
            else: func = self.closenessToAll
            for null in func(X, Y, evalSpec):
                yield
            #print SSE0, self.SSE
    
    @defer.inlineCallbacks
    def add(self, ID, V, evalSpec):
        """
        Call this with a L{vectors.Vectors_Ngspice} or
        L{vectors.Vectors_Python} instance populated with simulation
        result vectors, an I{ID}, and an instance of L{EvalSpec}.

        It will contain at a minimum a I{nameList} of vector names for
        this simulation setup, and a callable or 2-D Numpy array I{X}
        of goal points.

        Callable Goals
        ==============
        
            If I{X} is a callable, it must accept one 1-D Numpy array
            for each vector in the I{nameList} and return a 2-tuple
            with (1) a real-valued (pre-weighted) fitness metric
            equivalent to the sum of squared error and (2) a 2-D array
            of goal points that the vector coordinates were evaluated
            against.

            As an example, see L{analysis.mosfet.RevCurrentEvaluator}
            and the L{MOSFET_Setups.Xs} method that defines it as a
            goal callable along with two other callable class
            instances.
    
            A callable X may return a C{Deferred}, but it has to have
            a I{dr} attribute set C{True} if that is the case. The
            preferred form of a callable goal is a class instance with
            a C{__call__} method, and obviously there's no problem
            with setting an attribute I{dr} of a class or
            instance. You can set attributes of unbound functions, so
            something like this is acceptable, too::
    
                def goal_deferred(t, X):
                    t2 = np.square(t)
                    SSE = np.square(np.sum(X-t2))
                    return defer.succeed((SSE, t2))
                goal_deferred.dr = True
    
            There is no weight applied to a callable goal. You simply
            scale up the SSE result it provides as much as you want it
            weighted.

        Array Goals
        ===========
        
            If X is a 2-D array, the evalSpec will also contain a 2-D
            array I{W} of the same dimensions as X with real-valued
            weights for each goal point value.
    
            B{NOTE:} The logValues setting is only applicable to the
            array form of I{X} and is disregarded during evaluation of
            a callable I{X}.

        Independent Vectors
        ===================
        
            If (as will be typical) there are independent variables in
            each goal point in X, the evalSpec will also include a
            list I{indieFlags} of the same length as each goal point
            coordinate. Each list element will be C{True} for an
            independent variable or C{False} otherwise.

        @see: L{Evaluator._gotV}, which is called by public methods
            L{Evaluator.evaluate} and L{Evaluator.evaluateSSE}.
        """
        if ID in self.result:
            raise RuntimeError(sub(
                "Attempt to reuse ID {:d} in {}", ID, self))
        # The use of dLock fixed an SSE inconsistency problem that
        # vexed me for days
        yield self.dLock.acquire()
        SSE = None
        if self:
            if V is None:
                # When does this ever happen?
                SSE = float('+inf')
            elif V.error():
                # Error = worst possible SSE and quit ASAP
                SSE = float('+inf')
                self.bogus = True
            elif None in V:
                # SSE-only Python-only analysis
                SSE = V[None]
        if SSE is not None:
            self.result(ID, SSE)
        elif callable(evalSpec.X):
            # Ngspice analysis with callable goal
            if evalSpec.q and not evalSpec.q.isRunning():
                self.notRunning = True
            else:
                args = []
                for name in evalSpec.nameList:
                    args.append(self.maybeLog(V[name], evalSpec, name))
                if evalSpec.q:
                    SSE, X = yield evalSpec.q.call(evalSpec.X, *args)
                else: SSE, X = yield evalSpec.X(*args)
            if self: self.result(ID, SSE, X, evalSpec, V)
        else:
            # Ngspice analysis with array goal
            self.SSE = 0
            X = evalSpec.X
            yield task.cooperate(
                self.closenesserator(ID, X, V, evalSpec)).whenDone()
            N = X.shape[0]
            if N: self.SSE /= N
            if self: self.result(ID, self.SSE, X, evalSpec, V)
        # The lock release must be the VERY LAST THING DONE!!!!
        self.dLock.release()
