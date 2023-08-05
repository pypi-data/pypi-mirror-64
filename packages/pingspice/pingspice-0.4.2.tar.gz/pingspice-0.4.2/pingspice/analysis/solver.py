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
Home of the L{Solver}, the workhorse that runs ADE with local or
TCP-connected analyzers to find a combination of component values and
device parameters that has minimum SSE with respect to the circuit's
stated goals.
"""

import sys

import numpy as np
from twisted.internet import defer

from asynqueue import TaskQueue
from asynqueue.util import DeferredTracker
from asynqueue.wire import o2p, WireWorker, ServerManager, ChunkyString

from ade.population import Population
from ade.de import DifferentialEvolution
# Need to use ADE's messenger to get it to print stuff
from ade.util import msg
# If console option selected, we need to disable ADE abort
from ade.abort import ignoreKeyboard

from pingspice.circuit.av import AV_ListHolder
from pingspice.analysis.names import ParameterNamer
from pingspice.analysis.sse import ErrorTabulator
from pingspice.analysis.evaluate import Evaluator
from pingspice.analysis.wire import WireEvaluator
from pingspice.util import sub, oops


class Rechecker(object):
    """
    L{Solver} uses an instance of me to compare a recomputed
    L{ErrorTabulator} with a reported SSE.

    I keep track of best-SSE reports and indicate when its own
    re-computation of the SSE differs from what the report said the
    SSE was.
    
    @keyword usingET: Set C{True} if L{Solver.evaluate} returns an
        instance of L{ErrorTabulator} as the SSE instead of a float.
    """
    tooDifferent = 0.02
    notableDifference = 0.001

    def __init__(self, verbose=False, usingET=False):
        self.verbose = verbose
        self.usingET = usingET
        self.N_reports = 0
        self.N_errors = 0
        self.SSE = float('+inf')

    def check(self, et, SSE):
        """
        Call this with a fully populated instance of L{ErrorTabulator}
        from a recomputation of SSE, along with a reported I{SSE}.

        Returns a 3-tuple with (1) the result that the L{Solver}
        instance I serve should return from its report callback, (2)
        the text that it should use as a prelude to its pretty-printed
        values if this is a legit report, and (3) the text, if any,
        that it should log after the reports are done being processed.

        Some details about the 3-tuple items:

            1. The result is (C{None} is there was not too much of an
               SSE difference. If there was, the result is the
               L{sse.Result} instance I{result} of I{et}.

            2. The prelude text is C{None} if this report should be
               ignored because it really isn't the best SSE I've seen
               yet, and there's no SSE discrepancy to talk about.

            3. The post-report text is C{None} unless
               L{ErrorTabulator} instances are being used for the
               reported SSEs and there is an SSE discrepancy to
               describe in detail.
        """
        def reldiff(x, y):
            if not y or np.isinf(y): return float('+inf')
            return abs(x-y)/y
        
        # Account for the report and figure out relative difference
        # between reported and recomputed SSEs, along with ID of the
        # biggest SSE difference if using an ErrorTabulator as SSE
        self.N_reports += 1
        if self.usingET:
            ID, rs_SSE, rpt_SSE = et.biggestDiff(SSE)
            rdSSE = reldiff(float(rs_SSE), float(rpt_SSE))
        else:
            ID, rs_SSE, rpt_SSE = None, et.total(), SSE
            rdSSE = reldiff(rs_SSE, rpt_SSE)
        # Set the result if the relative difference was too big, the
        # foreword if there should be a report, and the afterword if
        # there are SSE details to follow the report
        result, foreword, afterword = None, None, None
        if rdSSE > self.notableDifference:
            if ID is None:
                foreword = sub("SSE={:.2f} ({:.2f}) with", rpt_SSE, rs_SSE)
            else:
                foreword = sub(
                    "SSE={:.2f} for ID={:03d} but recomputed as "+\
                    "{:.2f}, with", rpt_SSE, ID, rs_SSE)
                afterword = "\n".join([
                    sub("Reported: {}", repr(SSE)),
                    sub("Recomputed: {}", repr(et)), ""])
            if rdSSE > self.tooDifferent:
                self.N_errors += 1
                result = et.result
        elif SSE < self.SSE:
            self.SSE = float(SSE)
            foreword = sub("SSE={:.2f} with", self.SSE)
        # Return results
        return result, foreword, afterword

    def processComplaint(self, i, result):
        """
        Called with an I{individual} I{i} and a discrepant result from the
        recomputation of that individual's values. Logs an error
        message about the discrepancy.
        """
        SSE = result.SSE
        return sub(
            "\n\nSSE ERROR #{:d} (of {:d} reports), "+\
            "{:g} on second analysis!",
            self.N_errors, self.N_reports, float(result.SSE))


class Solver(AV_ListHolder):
    """
    I solve for an optimum combination of alterable values to minimize
    the SSE result of my L{evaluate} method.
    
    Construct me with an instance of C{av.AV_Manager}, an instance of
    L{analysis.param.Setups}, and the number of CPU cores I am to
    use. I will report on the results as my iterative solution
    progresses.

    @keyword popsize: Set to the desired number of C{ade.Individual}
        objects in the population per parameter. Otherwise, ADE's
        default will be used. (Ignored if I{picklePath} is set.)
    
    @keyword wire: Set C{True} to offload evaluations (except for
        running callbacks) onto other Python interpreters that I spawn
        on this computer for that purpose. Set to a list of Twisted
        endpoint TCP descriptions to add workers on other computers as
        well.

    @keyword picklePath: The path of a compressed pickle of a previous
        C{ade.population.Population} instead, to be loaded and used
        instead of constructing and setting up a new one. Its names
        must match my list of I{names}. None of its C{Individual}
        objects should have values outside the bounds of my L{AV}
        objects. (Not checked!)

    @keyword savePicklePath: The path where a compressed pickle of my
        C{ade.population.Population} population should be
        automatically and periodically saved. When
        L{differential_evolution} is used (the default), that happens
        after each generation. Can be the same as I{picklePath}, if
        that is specified.
    """
    solvers = ['differential_evolution']
    N_maxParallel = 12

    def __init__(
            self, cfg, avm, setups, N_cores,
            wire=False, popsize=None, logHandle=None,
            picklePath=None, savePicklePath=None):
        """
        C{Solver(cfg, avm, setups, N_cores,}
        C{    wire=False, popsize=None, logHandle=None,}
        C{    picklePath=None, savePicklePath=None)}
        """
        self.cfg = cfg
        if cfg.console: ignoreKeyboard()
        if logHandle:
            msg(logHandle)
        elif cfg.verbose: msg(True)
        self.logHandle = logHandle
        self.savePicklePath = savePicklePath
        self.avList = avm.avList
        params = avm.knownParams()
        namesKnown = params.keys()
        names = self.names = []
        bounds = []
        for av in self.params:
            names.append(av.name)
            bounds.append(av.minMax)
        text =  sub("Solver with {:d} cores and ", N_cores)
        text += sub("{:d} alterables, ", len(self.avList))
        text += sub("{:d} of which are parameter bases.", len(names))
        if namesKnown:
            text = text[:-1] + sub(
                ", and {:d} are known.", len(namesKnown))
        msg(-1, text, '-')
        self.s = setups
        self.dLock = defer.DeferredLock()
        self.knownText = ParameterNamer(namesKnown).prettyValues([
            params[x] for x in namesKnown])
        if N_cores: self.N_maxParallel = N_cores
        if wire and not cfg.debug:
            self.s.avList = self.avList
            self.N_workers = N_cores
            self.wireDescriptions = [] if wire is True else wire
            N_cores = 1
        else: self.N_workers = None
        self.rc = Rechecker(cfg.verbose, cfg.et_sse)
        self.ev = Evaluator(
            cfg, self.avList,
            setups.transforms, setups.logValues, N_cores)
        if picklePath is None:
            self.p = Population(
                self.evaluate, names, bounds,
                constraints=setups.constraints,
                popsize=popsize,
                complaintCallback=self.rc.processComplaint)
        else:
            self.p = Population.load(
                picklePath,
                func=self.evaluate,
                complaintCallback=self.rc.processComplaint, bounds=bounds)
        self.callbacks = []
        self.funcList = [getattr(self, x) for x in self.solvers]
        info = "SSE evaluations and " + ", ".join(self.solvers)
        msg(-1, "Solving for {:d} setups with {}", len(setups), info, '-')
        self.pn = self.p.pm
        if cfg.verbose:
            for k, name in self.pn.sortedNamerator():
                low, high = bounds[k]
                msg(2, "{}: {:g} - {:g}", name, low, high)
            msg("")
        self.running = True
    
    @defer.inlineCallbacks
    def setup(self, uniform=False, blank=False, empty=False, skipIDs=[]):
        """
        Sets up my local Evaluator and, unless I{empty} is set C{True}, my
        Population.

        If I am running with one or more WireWorkers, sets up the
        C{TaskQueue} and various support objects for offloading
        evaluation to one or more other Python processes.

        @keyword uniform: Use uniform random variates instead of a
            Latin hypercube (LHS). Using LHS (the default) is usually
            better because initializes pseudorandom parameter values
            with minimal clustering. (Ignored if my I{Population}
            object I{p} was loaded from a compressed pickle.)

        @keyword blank: Set C{True} to give the initial individuals an
             infinite placeholder SSE instead of being
             evaluated. (Ignored if my I{p} was loaded from a
             compressed pickle.)
        
        @keyword empty: Set C{True} to have me start with an empty
            population. (Ignored if my I{p} was loaded from a
            compressed pickle.)
        
        @keyword skipIDs: An optional list or set of setup IDs to skip.
        """
        def addWorker(description):
            ww = WireWorker(wwu, description, N_concurrent=Nc)
            return self.qWire.attachWorker(ww)

        def done(i, k, SSE_prev):
            SSE = float(i.SSE)
            if not SSE or np.isinf(SSE_prev) or np.isinf(SSE):
                info = ": !!!"
            else:
                rd = (SSE-SSE_prev) / SSE_prev
                if abs(rd) > 1E-3:
                    info = sub(": {:+.1f}%", 100*rd)
                    iChanged.add(i)
                else: info = ""
            msg(2, "{:03d}  {:>8.1f} --> {:>8.1f}  {}", k, SSE_prev, SSE, info)
        
        self.addCallback(self.info)
        if self.N_workers:
            wwu = WireEvaluator()
            self.qWire = TaskQueue()
            self.smWire = ServerManager(
                "pingspice.analysis.wire.WireEvaluator")
            Nc = min([len(self.s.nameLists), 2])
            for k in range(self.N_workers):
                description = self.smWire.newSocket()
                yield self.smWire.spawn(description)
                yield addWorker(description)
            for description in self.wireDescriptions:
                yield addWorker(description)
            for chunk in ChunkyString(o2p(self.s)):
                yield self.qWire.update('send_chunk', chunk)
            yield self.qWire.update('setup', self.cfg, skipIDs=skipIDs)
        yield self.ev.setup(
            self.s.nameLists,
            self.s.analyzers,
            self.s.Xs,
            self.s.netlists,
            self.s.independents,
            self.s.weights, skipIDs)
        self.p.reporter.addCallback(self.runCallbacks)
        Np = len(self.p)
        if self.p.running is None and not empty:
            OK = yield self.p.setup(uniform, blank)
            if not OK:
                yield self.shutdown()
        elif Np:
            msg(-1, "Re-evaluating {:d} loaded Individuals...", Np, '-')
            iChanged = set()
            dt = DeferredTracker(interval=0.05)
            yield self.p.history.purgePop()
            for k, i in enumerate(self.p):
                SSE_prev = float(i.SSE)
                d = i.evaluate().addCallback(done, k, SSE_prev)
                dt.put(d)
                yield dt.deferUntilFewer(self.N_maxParallel)
            yield dt.deferToAll()
            if len(iChanged) > 0.5*len(self.p):
                # The amount of SSE changing indicates that something
                # fundamental has changed, so restart history with
                # re-evaluated population. Unfortunately, all the
                # history under the old SSE-evaluation regime is no
                # longer applicable and will be lost.
                yield self.p.history.clear()
            for i in self.p:
                yield self.p.history.add(i)
            self.p.initialize()
            msg("")
        else: self.p.initialize()
            
    @defer.inlineCallbacks
    def shutdown(self):
        """
        This should only get called once, by L{setup} if setup of my
        Population got aborted or by L{__call__} when it's done.
        """
        if self.running:
            self.running = False
            msg(-1, "Shutting down solver and its support staff...", '-')
            yield self.dLock.acquire()
            del self.callbacks[:]
            if self.N_workers:
                yield self.qWire.update('shutdown')
                yield self.qWire.shutdown()
                yield self.smWire.shutdown()
            yield self.ev.shutdown()
            msg("Solver is shut down...")
            self.dLock.release()

    def save(self, picklePath):
        """
        Saves a compressed pickle of my present population to a file at
        I{picklePath}.
        """
        self.p.save(picklePath)
            
    def info(self, result):
        """
        Prints info about the supplied L{sse.Result} object to the log or
        STDOUT, including the alterations made if in 'chatty' mode.
        """
        def msgDev(ref, value):
            if ref in done: return
            msg(" {} = {:.4g}", ref, value)
            done.add(ref)

        def msgModel(ref, param, value):
            if (ref, param) in done: return
            msg(" {}:{} = {:.4g}", ref, param, value)
            done.add((ref, param))

        done = set()
        if hasattr(result, 'counter') and hasattr(result, 'description'):
            # TODO: Reflow if longer than max line length
            msg(-1, "{:04d}: {}", result.counter, result.description, -1)
        if self.cfg.chatty:
            self.alterations(result.values, msgDev, msgModel)
            msg("")
        
    def addCallback(self, func, *args, **kw):
        """
        Call this to register as a callback a function that accepts a
        L{sse.Result} object, as well as any other arguments and
        keywords you provide.

        I will run all the callbacks whenever the population reporter
        calls my L{runCallbacks} method, which I register with it as
        its own callback.
        """
        if not callable(func):
            raise ValueError("You must supply a callable")
        self.callbacks.append((func, args, kw))

    def runCallbacks(self, values, evalCount, SSE):
        """
        Runs, with the supplied 1-D array of I{values}, all callbacks that
        have been registered via my L{addCallback} method.

        Any function-specific args and kw that were provided in the
        call to L{addCallback} are also included after the values.

        The primary use of this is displaying a plot of the current
        best set of parameters.

        I add the I{values} and a I{description} of this result to the
        L{sse.Result} object. Before doing any of this, I recompute
        the SSE with my local evaluator. If my recomputed SSE differs
        from the SSE supplied as a third argument, I complain to ADE
        by setting my C{Deferred} return value to the L{sse.Result}
        object from my local re-evaluation instead of running my own
        callbacks with it.
        """
        def evaluated(et):
            rs = et.result
            rs.values = values
            rs.counter = evalCount
            if not self.running or et.notRunning: return
            result, preludeText, afterword = self.rc.check(et, SSE)
            if preludeText:
                if self.knownText:
                    preludeText += sub(
                        " known params {} and unknown params",
                        self.knownText)
                rs.description = self.p.pm.prettyValues(
                    values, preludeText)
                for func, args, kw in self.callbacks:
                    func(rs, *args, **kw)
            if afterword: msg(afterword)
            self.dLock.release()
        
        def failed(failureObj):
            self.dLock.release()
            return self.shutdown().addCallback(lambda _: failureObj)
        
        if not self.running: return defer.succeed(None)
        d = self.dLock.acquire()
        d.addCallback(
            lambda _: self.ev.evaluate(values, study=self.cfg.study_best))
        d.addCallback(evaluated)
        d.addErrback(failed)
        return d
    
    @defer.inlineCallbacks
    def evaluate(self, values, xSSE=None):
        """
        This is where it all happens!

        "Returns" a C{Deferred} that fires with the evaluated SSE. If
        I{xSSE} is set and the evaluated SSE exceeds it, the
        "returned" SSE will be higher but beyond that its value is
        meaningless. It's a failed challenge that I{ade} will discard
        and we should never see it again anywhere, including in reports.
        """
        if values is None or not self.running:
            SSE = -1
        elif self.N_workers is None:
            # Can use an ErrorTabulator as SSE, for testing and
            # debugging purposes.
            if self.cfg.et_sse:
                SSE = yield self.ev.evaluate(values, xSSE=xSSE)
            else: SSE = yield self.ev.evaluateSSE(values, xSSE=xSSE)
        else:
            dList = []
            for ID in self.ev:
                dList.append(self.qWire.call('evaluate', values, ID, xSSE))
            SSEs = yield defer.gatherResults(dList)
            SSE = 0
            for SSEk in SSEs:
                if SSEk is None:
                    SSE = None
                    break
                if SSEk < 0:
                    SSE = SSEk
                    break
                SSE += SSEk
        defer.returnValue(SSE)

    def differential_evolution(self, **kw):
        """
        Runs asynchronous differential evolution to determine parameters
        for my configuration as defined in the class-level stuff
        above, and in your subclass.

        Returns a C{Deferred} that fires with a C{population} object
        containing the last generation's population. You can obtain
        the all-time best individual by calling the population
        object's C{best} method.

        @keyword genFunc: A callable that takes one argument (the
            generation number) to be called after each generation.
        """
        def autosave(kg):
            if self.savePicklePath:
                self.save(self.savePicklePath)
        
        kw['logHandle'] = self.logHandle
        kw['xSSE'] = self.cfg.xsse
        de = DifferentialEvolution(self.p, **kw)
        return de(autosave).addErrback(oops)

    @defer.inlineCallbacks
    def hoyle(self, **kw):
        """
        Idiotic creationist alternative to L{differential_evolution}. Use
        this if you don't believe in the power of random mutation and
        natural selection. Good luck.
        
        "The chance that higher life forms might have emerged in this
        way is comparable with the chance that a tornado sweeping
        through a junk-yard might assemble a Boeing 747 from the
        materials therein" (Hoyle on evolution, I{Nature}, Vol. 294,
        No. 5837, Nov. 12, 1981, p. 105).
        
        Yeah, well, just try it and see.
        """
        def evaluated(i):
            p.report(i)
            if i < p.best():
                p.push(i)
            dq.put(None)

        def doIteration(null):
            values = np.random.uniform(size=p.Nd)
            i = p.spawn(values, fromUnity=True)
            if p.pm.passesConstraints(i.values):
                i.evaluate().addCallback(evaluated)

        p = self.p
        dq = defer.DeferredQueue()
        for k in range(self.ev.N_cores):
            dq.put(None)
        while p.counter < 1000000:
            dList = []
            for k in range(1000):
                dList.append(dq.get().addCallback(doIteration))
            yield defer.DeferredList(dList)
            msg(-1, "{:d} tornadoes", p.counter, '-')
        defer.returnValue(population)
        
    @defer.inlineCallbacks
    def __call__(self, **kw):
        """
        Call your instance of me to get the final population after I have
        performed all heuristic functions defined in my I{funcList} in
        succession.

        Each function starts with the final population of the previous.
        The first one initiates its own starting population.
        """
        for k, func in enumerate(self.funcList):
            yield func(**kw)
        yield self.shutdown()
        defer.returnValue(self.p)
            
