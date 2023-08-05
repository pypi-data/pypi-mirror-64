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

from collections import OrderedDict
from contextlib import contextmanager

import numpy as np
from twisted.internet import reactor, defer

from ade import abort

from pingspice.circuit.av import AV_Manager
from pingspice.circuit.netlist import Netlist
from pingspice.ngspice import NgspiceRunner
from pingspice.analysis.names import ParameterNamer
from pingspice.analysis import sim
from pingspice.util import *


class Setup(object):
    """
    I maintain a C{DeferredQueue} of one or more analyzers.

    There are two different kinds of setup, for Ngspice simulations
    and for Python-only simulations.
    
    I am constructing analyzers from a class provided in the first
    item of definition sequence (argument #4), I will construct an
    NgspiceRunner for each analyzer and then construct the analyzer
    with (1) a reference to the NgspiceRunner, (2) my setup ID, (3) my
    list of vector names, (4) my I{avList}, and any additional
    arguments that have been included in the definition sequence. Then
    I will call its C{setup} method with the circuit I{netlist}
    string.

    If I am just setting up an existing analyzer (which must be an
    instance of L{psim.Analyzer}, I will call its C{setup} method with
    (1) my setup ID, (2) my list of vector names, (3) my I{avList},
    and any additional arguments that have included in the definition
    sequence. In this case, whatever is in my I{netlist} attribute is
    ignored because Python-only Analyzers don't use circuit files.

    Construct me with:

    @param cfg: An instance of L{Config} containing Boolean runtime
        options.
    
    @param ID: My integer setup ID.

    @param avList: A reference to a shared list of AV objects.

    @param names: The names of the vectors that my analyzers will be
        providing.
    
    @param analyzer: The definition sequence for my analyzers,
        consisting of a subclass of L{sim.Analyzer} followed by args
        for its constructor, or an instance of L{psim.Analyzer},
        followed by args for its C{setup} method.

    @keyword netlist: Text of the SPICE circuit file for my analyzers,
        if an analyzer object is not being supplied.

    @keyword N_cores: The number of analyzers I spawn and handle.

    @cvar timeout: The number of seconds an analyzer will wait
        for a response to its commands.
    """
    timeout = 40
    
    def __init__(
            self, cfg, ID, avList, names, analyzer, netlist=None, N_cores=2):
        """
        C{Setup(self, cfg, ID, avList, names, analyzer,}
        C{  netlist=None, N_cores=2)}
        """
        self.cfg = cfg
        self.avList = avList
        self.ID = ID
        self.names = names
        self.aco = analyzer[0]
        self.N = 0
        self.N_analyzers = 1 if self.isPythonAnalyzer() or cfg.debug \
            else N_cores
        self.args = analyzer[1:]
        self.netlist = netlist
        self.dq = defer.DeferredQueue(self.N_analyzers)
        self.running = True
        
    def __len__(self):
        return self.N

    def __repr__(self):
        return sub(
            "<Setup ID={:d} for [{}] at {}",
            self.ID, ", ".join(self.names), hex(id(self)))
    
    @defer.inlineCallbacks
    def shutdown(self):
        """
        Shuts down all my analyzers.

        Returns a C{Deferred} that fires when they're all shut
        down. Repeated calls are disregarded.
        """
        if self.running:
            self.running = False
            msg(4, "Shutting down {:d} analyzers of {}", self.N, self)
            for k in range(self.N):
                analyzer = yield self.dq.get()
                if analyzer:
                    # After timeouts, it might be a None object, weirdly
                    yield analyzer.shutdown()
                msg(6, "#{:d} is shut down", k+1)
            self.N = 0

    def isPythonAnalyzer(self):
        """
        Returns C{True} if my analyzer(s) are Python-only, rather than
        Ngspice-based.
        """
        if isinstance(self.aco, type):
            return False
        return hasattr(self.aco, 'avDefine')
            
    def fireAnalyzer(self, analyzer):
        """
        Shut down and dismiss the specified I{analyzer}.
        """
        self.N -= 1
        return analyzer.shutdown()
            
    @defer.inlineCallbacks
    def addAnalyzer(self, noPut=False):
        """
        Sets up an analyzer and adds it to my C{DeferredQueue}.

        Declines to add an analyzer if I already have the number I{N}
        that I was configured with, or if I'm not running anymore.
        
        Returns a C{Deferred} that fires with a reference to the
        analyzer, or C{None} if no analyzer was added.

        @keyword noPut: Set C{True} and I won't put the new analyzer
            into my queue. Then you must do it instead.
        """
        analyzer = None
        if not self.running:
            msg("WARNING: {} is not running, so declining to add {}",
                repr(self), repr(self.aco))
        elif self.N >= self.N_analyzers:
            msg("WARNING: {} already has {:d} analyzers, "+\
                "declining to add {}", repr(self), self.N, repr(self.aco))
        else:
            if self.isPythonAnalyzer():
                analyzer = yield self.aco.setup(
                    self.ID, self.names, self.avList, *self.args)
                # Set the analyzer's timeout, unless a console will be
                # opened upon failure
                if analyzer is not None and not self.cfg.console:
                    analyzer.timeout = self.timeout
            else:
                # The NgspiceRunner takes care of the timeout
                r = NgspiceRunner(self.cfg, timeout=self.timeout)
                analyzer = self.aco(
                    r, self.ID, self.names, self.avList, *self.args)
                analyzer = yield analyzer.setup(self.netlist)
                if analyzer:
                    analyzer.initialMemUsage = yield analyzer.r.memUsage()
            if analyzer is None:
                msg("WARNING: {} had a problem setting up an analyzer "+\
                    "for ID {:d}", repr(self), self.ID)
            else:
                if not noPut:
                    self.dq.put(analyzer)
                self.N += 1
        defer.returnValue(analyzer)
            
    def populate(self):
        """
        Populates my DeferredQueue I{dq} with I{N_analyzers}, returning a
        C{Deferred} that fires with my setup I{ID} when all the
        analyzers have been set up, or with C{None} if there was a problem.
        """
        def failed(failureObj):
            msg("\nERROR adding analyzers for setup {:d}:", self.ID)
            oops(failureObj, keepGoing=True)

        def done(analyzers):
            return None if None in analyzers else self.ID
        
        dList = []
        for k in range(self.N_analyzers):
            dList.append(self.addAnalyzer().addErrback(failed))
        return defer.gatherResults(dList).addCallbacks(done)

    def isBloated(self, analyzer):
        """
        Returns C{True} if the Ngspice process for the specified
        I{analyzer} is using too much RAM.

        "Too much" is defined as at least 300K and twice what it was
        using when it first launched.
        """
        def done(memUsage):
            if memUsage < 300000:
                return False
            return memUsage >= 2*analyzer.initialMemUsage
        if hasattr(analyzer, 'r'):
            return analyzer.r.memUsage().addCallback(done)
        return defer.succeed(False)

    
class MultiRunner(object):
    """
    I run parallel simulations of one or more simulation setups via a
    pool of Ngspice processes.

    Construct me with a L{Config} object I{cfg} and, unless you want
    to use me for setting up a circuit with a call to L{newSetup}, a
    list I{avList} of L{AV} objects.

    @cvar retry: Set C{True} to have me retry (once) an analysis that
        resulted in an Ngspice error. If it succeeds the second time,
        that result is what the C{Deferred} returned from L{run} will
        fire with. This is C{False} by default because it doesn't seem
        to accomplish anything.
    """
    retry = False
    
    def __init__(self, cfg, avList=None, N_cores=1):
        """C{Multi-Runner(cfg, avList=None, N_cores=1)}"""
        self.cfg = cfg
        self.setups = {}
        self.N_cores = N_cores
        self.ignoreErrors = False
        self.running = True
        self.avList = avList
        self.running = True
        self._paramNames = None
        self.avm = None

    @property
    def paramNames(self):
        if self._paramNames is None:
            self._paramNames = [av.name for av in self.avList if av.isParam()]
        return self._paramNames
    @paramNames.deleter
    def paramNames(self):
        self._paramNames = None

    def params(self, ID):
        """
        Returns an C{OrderedDict} with 3-tuples containing the minimum,
        default, and maximum values for each parameter of the
        specified setup I{ID}.
        """
        result = OrderedDict()
        for av in self.avm.IDerator(ID):
            if av.isParam():
                seq = list(av.minMax)
                seq.insert(1, av.default)
                result[av.name] = seq
        return result
        
    def newSetup(self, func, nameList, analyzerClass, *args, **kw):
        """
        Sets up a circuit using a supplied circuit generation function
        I{func} and an analyzer with the supplied I{nameList} and
        an I{analyzerClass} with its constructor I{args}.

        You can supply Ngspice and pingspice-only simulation options
        as keywords. The only other keyword accepted is I{ID},
        described below.

        Your circuit generation function I{func} must accept as its
        sole argument an instance of a circuit generation tool
        (commonly referenced as I{f}). No circuitry will be produced
        other than what that function generates.

        An arbitrary ID of 100 will be used for this setup unless you
        specify a different one with the I{ID} keyword.

        Calls L{addSetup} with the new setup. Returns a C{Deferred}
        that fires with the setup ID when I have added a full set of
        analyzers all set up for this circuit.
        """
        ID = kw.pop('ID', 100)
        if self.avm is None:
            self.avm = AV_Manager(verbose=self.cfg.chatty)
            self.avList = self.avm.avList
        self.avm.setSetupID(ID)
        n = Netlist(self.avm, **kw)
        with n() as f:
            func(f)
        del self.paramNames     # Forces rebuilding my parameter list
        if isinstance(analyzerClass, str):
            analyzerClass = getattr(sim, analyzerClass)
        args = list(args)
        args.insert(0, analyzerClass)
        return self.addSetup(
            ID, nameList, args, str(n)).addCallback(lambda _: ID)
        
    def addSetup(self, ID, names, aseq, netlist=None):
        """
        Sets me up for a new analysis.

        The new analysis will be done under the specified integer
        setup I{ID} using the supplied list of I{names} of vectors to
        be retrieved after each analysis and I{aseq} definition
        sequence. For an Ngspice analyzer, the I{netlist} is also
        included.

        The definition sequence consists of a subclass of
        L{sim.Analyzer} followed by args for its constructor, or an
        instance of L{psim.Analyzer}, followed by args for its
        C{setup} method.
        
        Returns a C{Deferred} that fires when I have added full set of
        analyzers all set up for the new analysis.
        """
        if ID in self.setups:
            raise ValueError(sub(
                "Attempted to overwrite an existing setup {:03d}!", ID))
        s = Setup(
            self.cfg, ID, self.avList, names, aseq, netlist, self.N_cores)
        self.setups[ID] = s
        return s.populate().addErrback(oops)
    
    @defer.inlineCallbacks
    def shutdown(self):
        """
        Shuts everybody down.

        Do not try to run anything after calling this unless you wait
        for the returned C{Deferred} and then generate all new setups.
        """
        if self.running:
            self.running = False
            self.ignoreErrors = True
            msg(2, "Shutting down {:d} setups ...", len(self.setups))
            for s in self.setups.values():
                yield s.shutdown()

    def _checkValues(self, alterableValues):
        """
        Called by L{run} to make sure values list is legit.
        """
        if not hasattr(alterableValues, '__iter__'):
            alterableValues = [alterableValues]
        N_av = len(alterableValues)
        N_pn = len(self.paramNames)
        if N_av != N_pn:
            text =  sub("You provided {:d} alterable values ", N_av)
            text += sub(
                "with an AV list containing {:d} parameter objects:\n", N_pn)
            lines = [text, "-"*79]
            for k, av in enumerate(self.avList):
                lines.append(sub("{:>2d} {}", k, av))
            raise ValueError("\n".join(lines))
        return alterableValues

    @defer.inlineCallbacks
    def run(self, ID, alterableValues, study=False, noRerun=False):
        """
        Runs one of my analyzers for the setup specified by integer I{ID}
        with the supplied list of I{alterableValues}.

        The list contains alterable device, device parameter, and/or
        model parameter values in the order of my I{paramNames} list.

        Unless operations are being aborted, "returns" a C{Deferred}
        that fires with a L{sim.Vectors} object, or L{psim.Vectors} if
        the specified ID is served by a Python-only simulator,
        populated with result vectors. To see if there are errors,
        call the object's C{error} status checker.

        If some analyzer (not necessarily one of mine) has initiated a
        class-wide abort with a call to L{AnalyzerBase.abortAll}, the
        C{Deferred} will fire with C{None}.

        If the global 'study' configuration option is set, an error
        will cause the analyzer to create a new netlist file in your
        home directory with 'alter' and 'altermod' commands included
        in its '.options' section. The file will have a name of the
        form "pingspice-setup-XX.cir" where "XX" is the integer setup
        ID.
        
        If the global 'devel' configuration option is set, the
        analyzer will create the new netlist file after every
        analysis, not just a failing one, and will wait for the file
        to be moved or removed before proceeding. This can be useful
        for development purposes but is obviously impractical for
        regular operation.

        Returns a C{Deferred} that fires with a populated
        L{sim.Vectors} object for the specified setup, or C{None} if
        there was a fatal error.

        @keyword study: Set C{True} to have netlists of each setup
            written for study, even without an error and even if it
            means overwriting an existing netlist file.

        @keyword noRerun: Only gets set C{True} by a recursive
            repeated call, if there was an error and my I{retry}
            attribute is set C{True}.
        
        @see: L{sim.Analyzer.__call__} and L{sim.Analyzer.study}.
        """
        def replace(analyzer):
            d = s.fireAnalyzer(analyzer)
            d.addCallback(lambda _: s.addAnalyzer(noPut=True))
            return d

        def processError():
            if not self.ignoreErrors:
                if self.cfg.verbose:
                    msg("")
                    pn = ParameterNamer(self.paramNames)
                    prelude = sub("FAILED, setup {} with", ID)
                    msg(-1, pn.prettyValues(alterableValues, prelude), -1)
            if self.cfg.stop or analyzer.aborted:
                return defer.succeed(None)
            # Replace this loser with a new analyzer
            return replace(analyzer)
        
        alterableValues = self._checkValues(alterableValues)
        s = self.setups[ID]
        analyzer = yield s.dq.get()
        if not self.running:
            analyzer = None
        elif analyzer and analyzer.aborted:
            abort.abortNow()
            analyzer = None
        if analyzer is None:
            s.dq.put(None)
        else:
            # Get a copy of the analyzer's V object with results for
            # alterableValues
            d = analyzer(
                alterableValues,
                study=study or self.cfg.devel,
                stop=self.cfg.study_stop, overwrite=study)
            # An errback, strictly for coding bugs and maybe abort weirdness
            d.addErrback(oops, keepGoing=True)
            V = yield d
            if V is None:
                s.dq.put(None)
            else:
                if V.error():
                    analyzer = yield processError()
                    rerun = self.retry and not noRerun
                else:
                    rerun = False
                    # No error, is the analyzer bloated?
                    bloated = yield s.isBloated(analyzer)
                    if bloated:
                        # Replace this fatso with a new analyzer
                        analyzer = yield replace(analyzer)
                # The former or replacement analyzer is ready for
                # another call
                s.dq.put(analyzer)
                # Need to re-run?
                if rerun:
                    if self.cfg.verbose:
                        msg(-1, "RETRYING failed analysis...", ID, -1)
                    V = yield self.run(ID, alterableValues, study, True)
                    if self.cfg.verbose and V.error():
                        msg(-1, "RETRY FAILED!!!", -1)
                # The "return" value is the Vectors object
                defer.returnValue(V)

    def runAllSetups(self, alterableValues):
        """
        Calls L{run} for each setup with the alterable values in the
        supplied list.

        Returns a C{Deferred} that fires with a list of populated
        L{sim.Vectors} objects, one for each setup.
        """
        dList = [self.run(ID, alterableValues) for ID in self.setups]
        return defer.gatherResults(dList)
