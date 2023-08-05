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
Simulation analysis with Ngspice.

Python-only analyses that don't even use Ngspice are also an option,
sometimes useful for quick fitness evaluations. See L{analysis.psim}
for those.
"""

import re, os.path

import numpy as np
from twisted.internet import defer, reactor

from asynqueue.iteration import Delay

from pingspice.circuit.av import AV, AV_Error, AV_ListHolder
from pingspice.ngspice.runner import NgspiceRunner
from pingspice.ngspice.misc import ShuttingDownToken, NgspiceError
from pingspice.analysis.vectors import Vectors_Ngspice
from pingspice.util import *


class AnalyzerBase(AV_ListHolder):
    """
    Base class for all analyzers.

    No constructor is used; your subclass is welcome to have one,
    e.g., L{Analyzer.__init__}. Make sure your subclass has an
    instance of a L{VectorsBase} subclass accessible as I{V} from the
    get-go.
    
    @ivar maxWait: The number of seconds an analyzer will wait for
        vectors from its Ngspice or Python-only simulation. This
        timeout should be greater than the timeout for an
        NgspiceRunner to await a response to its commands. The default
        C{None}, for no timeout at all.
    """
    maxWait = None
    aborted = False

    @classmethod
    def abortAll(cls):
        """
        Call this when all instances of me, present or future, should
        abort their operations.

        Setting and checking any kind of class-wide status often has
        unintended consequences. Only call this if you really want
        your I{pingspice} application to quit as soon as possible, no
        questions asked, without the possibility of restarting except
        as a new Python process.
        """
        cls.aborted = True
    
    @property
    def dLock(self):
        """
        Property: An instance of C{DeferredLock}, newly constructed and
        awaiting release if I didn't have one yet.
        """
        if not hasattr(self, '_dLock'):
            self._dLock = defer.DeferredLock()
            self._dLock.acquire()
        return self._dLock


class Analyzer(AnalyzerBase):
    """
    Base class for L{TRAN} and L{DC}, which run the transient and DC
    analysis, respectively, for one Ngspice process and handle the
    results.
    
    Construct me with an L{NgspiceRunner} instance I{r}, an integer
    setup I{ID}, a list of I{vectorNames}, a reference to a shared
    I{avList} of all AV objects defined for my setup, and the
    arguments specific to the type of analysis I'm doing.

    You can also construct an instance for a one-time run by
    supplying, after the L{NgspiceRunner} instance, just the
    I{vectorNames} list and any analysis-specific arguments.

    To reduce memory consumption (which can be considerable with
    simulations that take more than a few minutes on a modern PC), I
    tell Ngspice to discard vectors other than those in the
    I{vectorNames} list. You can disable this and save all vectors by
    setting the 'full' L{Config} option in I{r}.
    
    If you want to specify Ngspice options for my runs to override the
    defaults for all runs, supply them in the I{args} sequence as
    2-tuples. The first element of each tuple is a string with the
    name of the option and the second element is the value of the
    option in the same format as it would appear in the global
    C{OPTIONS} dict of L{pingspice.ngspice.sourcery}.

    @ivar maxWait: Defines how long I will wait for a result from my
        NgspiceRunner, which actually should time out before I do.

    @ivar absVals: Set to a sequence with the names of all vectors
        whose raw vector values are always treated as positive
        numbers. See L{VectorsBase}.

    @ivar setupHasRun: Gets set C{True} after my L{setup} has run.
    """
    setupHasRun = False
    
    def __init__(self, r, *args):
        """
        Constructor (two different forms):

        B{AV Mode:}
        C{Analyzer(r, ID, vectorNames, avList, *args)}

        B{One-time Mode:}
        C{Analyzer(r, vectorNames, *args)}
        """
        self.r = r
        self.cfg = r.cfg
        if self.aborted: return
        self.kw = {}
        self.cmdList = []
        newArgs = []
        for arg in args:
            if isinstance(arg, tuple) and len(arg) == 2:
                self.kw[arg[0]] = arg[1]
                continue
            newArgs.append(arg)
        args = newArgs
        # For alterables: ID, vectorNames, avList, *args
        # For one-time run: vectorNames, *args
        if r.employedByAnalyzer:
            raise RuntimeError(sub(
                "{} is already being used by an analyzer", r))
        r.employedByAnalyzer = True
        if isinstance(args[0], int):
            self.ID, vectorNames, self.avList = args[:3]
            self.args = list(args[3:])
        else:
            self.ID = None
            vectorNames = args[0]
            self.args = list(args[1:])
        self.V = Vectors_Ngspice(r, vectorNames)
        self.customize()

    @classmethod
    def onetime(cls, netlist, vectorNames, *args, **kw):
        """
        Makes an instance of me fully set up for one-time usage with its
        own L{NgspiceRunner} sourced with the supplied I{netlist},
        runs it, and shuts it down.

        After constructing and setting up the instance of me, I run it
        with the args following the L{vectorNames} second arg to
        obtain a L{Vectors_Ngspice} object.

        The I{netlist} first arg can be the path of a netlist file or
        actual netlist text. That first argument is followed by the
        I{vectorNames} and then arguments specific to the type of
        analysis being done.

        You can specify as keywords the keywords recognized by the
        L{NgspiceRunner} constructor. The I{study} and I{overwrite}
        keywords are recognized and used as for a call to my
        instance. You can also include keywords set C{True} for
        L{Config} options to have enabled.

        Returns a C{Deferred} that fires after setting up, running,
        vector fetching, and shutting down the instance, with the
        populated L{Vectors_Ngspice} object.
        """
        @defer.inlineCallbacks
        def everything():
            a = yield cls(r, vectorNames, *args).setup(netlist)
            if a is None:
                raise NgspiceError("Couldn't setup an NgspiceRunner!")
            V = yield a(study=study, overwrite=overwrite)
            yield V(*vectorNames)
            yield a.shutdown()
            defer.returnValue(V)

        timeout = kw.pop('timeout', None)
        waiting = kw.pop('waiting', None)
        study = kw.pop('study', False)
        overwrite = kw.pop('overwrite', False)
        r = NgspiceRunner(Config(**kw), timeout, waiting)
        return everything()
        
    def shutdown(self):
        """
        After L{setup} and any pending calls to my instance have finished,
        shuts down my L{NgspiceRunner} I{r}.

        Returns a C{Deferred} that fires when the Ngspice process
        underlying my L{NgspiceRunner} instance I{r} has exited.

        Calling this repeatedly will have no effect, since repeatedly
        calling L{NgspiceRunner.shutdown} doesn't have any. If Ngspice
        has already exited, the returned C{Deferred} fires
        immediately.
        """
        # The Deferred from lock acquisition and
        # NgspiceRunner.shutdown is not needed or returned. If lock
        # acquisition hangs on a second call, so be it.
        self.dLock.run(self.r.shutdown)
        # Instead, the Deferred from awaiting Ngspice process exit is
        # returned.
        return self.r.waiter.waitForEvent('exited')
        
    def __repr__(self):
        return sub("<Analyzer ID={}: {}>", self.ID, self.r)
    
    def customize(self):
        """
        L{TRAN}, L{AC}, and L{DC} override this to set parameters for
        their simulation commands. L{OP} has no need of it.
        """
        pass

    def _notAllVectors(self):
        """
        Returns C{True} if I do a TRAN analysis and will not be saving all
        vectors from it.
        """
        if self.cfg.full: return
        return getattr(self, 'fName', None) == 'tran'
    
    @defer.inlineCallbacks
    def setup(self, netlist):
        """
        Tells my NgspiceRunner to source a netlist and then sets it up
        with a number of standard options intended to make convergence
        more likely.

        Any options you supplied via 2-tuples in the I{args} to my
        constructor will override the standard options.

        Returns a C{Deferred} that fires when all that is done, with a
        reference to me if all went OK or C{None} if not. Does not
        fire any errback; rely on the result to determine success.
        
        If there was a problem and the C{cfg.study} option is set, a
        copy of the offending netlist will be written for study.
        """
        if self.aborted:
            result = None
        else: result = yield self.r.source(netlist, **self.kw)
        if result:
            self.netlistText = str(self.r.s)
            if self._notAllVectors():
                # Greatly reduces memory consumption for TRAN analysis
                result = yield self.r.setSavedVectors(*self.V.cnames)
                self.cmdList.append(result.cmd)
        if result:
            result = self
            self.setupHasRun = True
        elif not self.aborted:
            if self.cfg.verbose:
                try:
                    if len(netlist) > 30: netlist = netlist[:27] + "..."
                except: pass
                msg("FATAL ERROR: Couldn't source '{}':\n{}", netlist, result)
            if self.cfg.study:
                yield self.study(stop=True)
            result = None
        # Ready for business, or shutdown
        if not self.aborted and self.dLock.locked:
            self.dLock.release()
            defer.returnValue(result)

    def addName(self, name, k=None):
        """
        Call after L{setup} to add a vector with I{name} to my
        L{Vectors_Ngspice} object I{V}.

        The vector will be included in Ngspice's saved outputs, even
        if doing a TRAN analysis and the 'full' config option is not
        set.

        Returns a C{Deferred} that fires when I'm ready to run an
        analysis that includes this vector as well as those defined in
        my constructor.

        @keyword k: Set this to an integer to have the name inserted
            at a specific position in the names list of my
            L{Vectors_Ngspice} object's L{NameManager} rather than
            appended. The order isn't usually important, but does
            affect the result of a call to L{Vectors_Ngspice.array}.
        """
        if not self.setupHasRun:
            raise RuntimeError(
                "Call only after setup has run and sourced the netlist")
        cname = self.V.addName(name, k)
        if self._notAllVectors():
            return self.r.setSavedVectors(cname)
        return defer.succeed(None)
    
    def getAlterations(self, values):
        """
        Returns a C{Deferred} that fires with a list of lines to be placed
        into a netlist, doing alterations of component values and
        model parameters from their defaults.
        """
        def write(cmdName, args):
            lines.append(sub(
                "{} {}", cmdName, " ".join([str(x) for x in args])))
            
        def writeAlter(*args):
            write('alter', args)
            
        def writeAltermod(*args):
            write('altermod', args)
            
        def writeComment(av, value):
            if isinstance(value, float):
                value = sub("{:.5g}", value)
            text = sub("{} = {}", av, value)
            lines.append("* " + text)
            
        def done(N_alterations):
            if N_alterations:
                lines.insert(0, sub(
                    "\n* There {} {:d} {}",
                    "is" if N_alterations == 1 else "are",
                    N_alterations, plural("alteration", N_alterations)))
                lines.insert(1, sub("*{}", "-"*78))
            return lines
        
        lines = []
        d = self.alterations(
            values, writeAlter, writeAltermod, writeComment, ID=self.ID)
        d.addCallbacks(done, oops)
        return d

    def _doAlterations(self, values):
        """
        Has Ngspice do alterations on component values and model
        parameters in accordance with the supplied sequence of
        I{values}.

        Returns a C{Deferred} that fires when the alterations are
        done.

        Only one call to this method can be active at a time for a
        single instance of me. The L{__call__} method uses my L{dLock}
        to ensure that.
        """
        d = self.alterations(values, self.r.alter, self.r.altermod, ID=self.ID)
        d.addCallback(self.r.waitForAlterations)
        return d
    
    @defer.inlineCallbacks
    def __call__(self, *args, **kw):
        """
        Performs an analysis of my subclass type (L{TRAN}, L{AC}, or
        L{DC}), and updates my L{Vectors_Ngspice} object I{V} with the
        resulting simulation vectors.

        There are two different call patterns, depending on whether
        I'm operating in AV mode or one-time mode.

        "Returns" a C{Deferred} that fires with a reference to a fresh
        copy of my L{Vectors_Ngspice} instance. It will contain the
        Numpy vectors resulting from the analysis, unless the value is
        out of a defined range or produced a Numpy error or there was
        an Ngspice error.
        
        If there's an error and the 'stop' L{Config} option is set, or
        a netlist study occurs with the 'study_stop' option set, I
        will shut myself down and call L{abortAll} to abort all other
        analyzers. If there's already a class-wide abort condition, I
        won't bother running any analysis. In either of those cases,
        the C{Deferred} will fire with C{None}.

        AV Mode
        =======
            Call this (i.e., my instance) with a list of float values
            (or sub-lists of floats in the case of vector values). I
            will update the device values, device parameter values,
            and model parameter values whose names are defined in AV
            objects in my I{avList} before doing the analysis.
    
            The total number of items in the values list must equal the
            number of parent AV objects in my I{avList}. If no alterables
            have been defined, then an empty list is what's acceptable
            (the default if no arg is supplied).
    
            To get an analysis at the default values for everything,
            you may call this with nothing.

        One-time Mode
        =============
            In one-time mode, I have no setup I{ID} or I{avList}, and
            no alterations are done.

            If you supply the file path or text of a netlist as an
            argument, I will call my L{setup} with it. Otherwise, make
            sure that I've had my L{setup} method called with a
            netlist or that the L{NgspiceRunner} you constructed me
            with has had its L{NgspiceRunner.source} method called
            with one.

        @keyword study: Set C{True} to have a new netlist file written
            with 'alter' and 'altermod' commands included in its
            '.options' section, whether the analysis succeeds or
            not. B{Warning:} This can cause a lot of disk activity and
            should only be used for a single analysis or during
            debugging. You can also set it to the filePath of the
            netlist file you want generated.

        @keyword stop: Set C{True} to have Python shut down after a
            call to L{study} causes a netlist file to be written. Does
            not imply the I{study} keyword because L{study} might only
            get called on an error if that keyword is not set.

        @keyword overwrite: Set C{True} to have the netlist file
            overwrite any existing one. Ignored if I{study} is not
            set and there's no error.
        """
        @defer.inlineCallbacks
        def prepare_OTM():
            """
            Prepares for a one-time mode analysis, acquiring the lock after
            running my setup method.
            """
            if args:
                yield self.setup(args[0])
            elif not self.setupHasRun:
                raise RuntimeError("Must run setup first")
            # We'll need the lock before proceeding, even though we
            # aren't doing alterations
            yield self.dLock.acquire()

        @defer.inlineCallbacks
        def prepare_AV():
            """
            Prepares for an AV mode analysis, acquiring the lock before doing
            alterations.
            """
            # Need the lock before doing alterations
            yield self.dLock.acquire()
            # Clear data from previous run and thus keep Ngspice
            # processes from growing forever
            yield self.r.clearData()
            # Process the alterable values (if any) in the proper order
            self.checkValues(values, verbose=self.cfg.spew)
            yield self._doAlterations(values)

        def runAnalysis():
            """
            Runs the analysis with these alterable device, device parameter,
            and/or model parameter values.
            """
            def done(*args):
                if d.called: return
                # A proper callback firing, with result, or a timeout
                # with None
                d.callback(args[0] if args else None)
            
            d = defer.Deferred()
            dr = getattr(self.r, self.fName)(*self.args)
            dr.addCallback(done, d)
            d.addErrback(self.V.error)
            if self.maxWait:
                self.r.waiter.callAfter(dr, self.maxWait, done)
            return d

        def processResult(result):
            """
            Processes the analysis I{result}, returning a C{Deferred} that
            fires with a text version of the analysis command used, or
            SHUTDOWN if I'm shutting down.
            """
            if result:
                d = self.V()
                d.addCallback(lambda _: result.cmd)
                # Not sure this next line is necessary. Will calling
                # my V instance ever result in a Failure?
                d.addErrback(self.V.error)
                return d
            if result is None:
                # Timeout
                cmd = sub(
                    "{} {}", self.fName, " ".join([str(x) for x in self.args]))
                result = sub("TIMEOUT running '{}'", cmd)
            else: cmd = None
            self.V.error(str(result))
            return defer.succeed(cmd)

        if len(args) > 1:
            raise ValueError(sub(
                "Call a {} instance with zero or one arg", self))
        if not self.aborted:
            if self.ID is None:
                values = None
                yield prepare_OTM()
            else:
                values = args[0] if args else []
                yield prepare_AV()
            result = yield runAnalysis()
            cmd = yield processResult(result)
            if cmd and cmd not in self.cmdList: self.cmdList.append(cmd)
            study, stop, overwrite = [
                kw.get(x, False) for x in ('study', 'stop', 'overwrite')]
            if study:
                filePath = study if isinstance(study, str) else None
                yield self.study(
                    values,
                    filePath=filePath, stop=stop, overwrite=overwrite)
            errorCausedShutdown = False
            errMsg = self.V.error()
            if errMsg:
                if self.cfg.chatty:
                    msg(-1, "ERROR in {}:\n{}", repr(self), errMsg)
                if self.cfg.stop:
                    errorCausedShutdown = True
                elif self.cfg.study and not study:
                    yield self.study(
                        values, stop=stop,
                        overwrite=overwrite, info=errMsg)
            if errorCausedShutdown:
                msg(-1, "ERROR CAUSED SHUTDOWN...")
                self.abortAll()
                yield self.shutdown()
            else:
                # I make a copy of my V object as it stands now BEFORE
                # releasing the lock. Is the copy necessary? Yes,
                # because the next call will change my V
                # object. Potential memory leak?  Yes, that too! You
                # need to not keep gratuitous references to this copy
                # laying around.
                V = self.V.copy()
                self.dLock.release()
                defer.returnValue(V)
    
    def study(
            self, values=None, ID=None,
            filePath=None, stop=False, overwrite=False, info=None):
        """
        Creates a file with a copy of my netlist and commands to do
        alterations in accord with the supplied I{values}, for
        inspection and running in Ngspice.

        If you supply an integer I{ID}, it will be used as a suffix to
        the netlist filename before the extension. Otherwise, if I
        have an I{ID} (not running in one-time mode), that will be
        used. The file path will be C{~/pingspice-setup-XXX.cir},
        where XXX is the I{ID} With leading zeros. Alternatively, you
        can specify the entire I{filePath} yourself.

        "Returns" a C{Deferred} that fires when the temporary file has
        been written, unless I{stop} is set C{True}. In that case, the
        Python process is rudely and immediately shut down.

        If there's already a file at at the file path, it will not be
        overwritten, unless I{overwrite} is set C{True}. This is so
        that the first error encountered for a given setup is the only
        one that produces a netlist.
        """
        def getFilePath():
            if filePath is None:
                thisID = getattr(self, 'ID', 0) if ID is None else ID
                suffix = sub(
                    "-{:03d}", thisID) if isinstance(thisID, int) else ""
                fp = sub("~/pingspice-setup{}.cir", suffix)
            else: fp = filePath
            return os.path.expanduser(fp)

        def getLines():
            if values is None:
                return defer.succeed([])
            return self.getAlterations(values)

        def gotLines(lines):
            if self.cmdList:
                lines.append("* Setup and analysis command(s):")
                lines.extend(self.cmdList)
            if info:
                lines.extend(["*", "* Produced error:", "*"*79])
                for line in info.split('\n'):
                    lines.append("* "+line)
                lines.append("*"*79)
            if not os.path.isdir(os.path.dirname(fp)):
                raise ValueError(sub("No directory for filepath '{}'", fp))
            try: self.r.s.write(fp, lines)
            except:
                msg(-1, sub("WARNING: Couldn't write netlist to {}", fp))
            if stop: return self.shutdown()

        if self.aborted:
            return defer.succeed(None)
        fp = getFilePath()
        if not overwrite and os.path.exists(fp):
            if self.cfg.verbose:
                msg(-1, "Netlist {} already exists, not overwriting", fp)
            return defer.succeed(None)
        if stop:
            self.abortAll()
            msg(-1, "STOPPING to study netlist {}", fp)
        elif not overwrite or self.cfg.spew:
            msg(-1, "Wrote netlist {} for direct Ngspice study", fp)
        return getLines().addCallbacks(gotLines, oops)


class TRAN(Analyzer):
    """
    I initiate and handle the results of all Ngspice TRAN runs for one
    Ngspice process. Include the Ngspice arguments for a transient
    analysis as additional arguments.

    Some examples of constructor arguments::

        TRAN(r, ID, vectorNames, avList, tstep, tstop)
        TRAN(r, ID, vectorNames, avList, tstep, tstop, 'uic')
        TRAN(r, ID, vectorNames, avList, tstep, tstop, tstart)
        TRAN(r, ID, vectorNames, avList, tstep, tstop, tstart, tmax)
        TRAN(r, ID, vectorNames, avList, tstep, tstop, tstart, tmax)
        TRAN(r, vectorNames, tstep, tstop)
        TRAN(r, vectorNames, tstep, tstop, start, 'uic')

    The 'time' vector is automatically added to your I{vectorNames}.
    """
    fName = 'tran'
    
    def customize(self):
        """
        Sets parameters for transient analysis of all runs to follow.
        """
        self.V.addName('time')


class DC(Analyzer):
    """
    I initiate and handle the results of all Ngspice DC runs for one
    Ngspice process. Include the Ngspice arguments for a DC sweep as
    additional arguments.

    There are at least four: (1) a swept source name (voltage or
    current source, resistance, or temperature), and the (2) start,
    (3) stop, and (4) increment for sweeping it. Optionally, there can
    be an additional four arguments for sweeping another source.

    There are four possible constructor patterns::

        DC(r, ID, vectorNames, avList, src, vstart, vstop, vincr)
    
        DC(r, ID, vectorNames, avList,
           src, vstart, vstop, vincr, src2, vstart2, vstop2, vincr2)

        DC(r, vectorNames, src, vstart, vstop, vincr)
    
        DC(r, vectorNames,
           src, vstart, vstop, vincr, src2, vstart2, vstop2, vincr2)
    
    Swept voltages (or currents) will have their result vectors
    included in my L{Vectors_Ngspice} after each analysis, even though
    you could just compute them yourself.
    """
    fName = 'dc'

    def customize(self):
        """
        Sets parameters for DC analysis of all runs to follow.
        """
        N = len(self.args)
        if N not in (4, 8):
            argText = ", ".join(self.args)
            raise ValueError(sub(
                "Args {} do not specify one or two sweeps", argText))
        for k in (0, 4):
            if k >= N: break
            arg = self.args[k].lower()
            if self.args[k+3] < 0:
                raise ValueError("Please don't try to do a negative DC sweep")


class AC(Analyzer):
    """
    I initiate and handle the results of all Ngspice AC runs for one
    Ngspice process. Include the Ngspice arguments for an AC sweep as
    additional arguments.

    There are exactly four of them: (1) a string 'dec', 'oct', or
    'lin' specifying sweep type, (2) an int specifying the number of
    points per decade, per octave, or total, (3) the starting
    frequency in Hz, and (4) the end frequency in Hz. Here are the possible
    call patterns::

        AC(r, ID, vectorNames, avList, 'dec', Nd, fstart, fstop)
        AC(r, ID, vectorNames, avList, 'oct', No, fstart, fstop)
        AC(r, ID, vectorNames, avList, 'lin', Np, fstart, fstop)
        AC(r, vectorNames, 'dec', Nd, fstart, fstop)
        AC(r, vectorNames, 'oct', No, fstart, fstop)
        AC(r, vectorNames, 'lin', Np, fstart, fstop)

    You'll need to have set the AC value of one (and preferably just
    one) independent source to use me.
    """
    fName = 'ac'

    def customize(self):
        """
        Sets parameters for AC analysis of all runs to follow.
        """
        self.V.addName('frequency')
        N = len(self.args)
        if N != 4:
            argText = ", ".join(self.args)
            raise ValueError(sub(
                "Args {} do not specify an AC sweep", argText))
        if self.args[3] < self.args[2]:
            raise ValueError(
                "Please don't try to do a negative frequency sweep")


class OP(Analyzer):
    """
    I initiate and handle the results of all Ngspice OP runs for one
    Ngspice process. An operating point analysis (15.3.5) takes no
    arguments, so there are no additional constructor arguments. There
    are just two call patterns::

        OP(r, ID, vectorNames, avList)
        OP(r, vectorNames)

    """
    fName = 'op'
