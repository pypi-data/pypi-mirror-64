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
C{pf}: Parameter Finder for I{pingspice} subcircuits using
Differential Evolution.
"""

from twisted.python import reflect
from twisted.internet import reactor
from twisted.logger import globalLogPublisher
from twisted.logger._levels import LogLevel

from pingspice.analysis.param import ParameterFinder
from pingspice.util import *


class Darwin(object):
    def __init__(self, args, FinderSubclass=None):
        cfg = Config(
            et_sse=args.E, xsse=args.x, console=args.o, debug=args.B,
            verbose=args.v, chatty=args.V, spew=args.S, hardcore=args.H,
            study_best=args.c, study=args.e, devel=args.C, study_stop=args.C)
        wire = args.w or args.x
        if args.D: globalLogPublisher.addObserver(self._analyze)
        if args.q: cfg.enable('study', 'stop')
        N = args.N
        if N == 0: N = None
        logFile = None if args.s else args.l
        self.savePicklePath = args.P if len(args.P) > 1 else None
        if FinderSubclass is None:
            klassName = args[0]
            FinderSubclass = self.tryGetClass(klassName)
            if FinderSubclass is None and not klassName.startswith('pingspice.'):
                klassName = "pingspice." + klassName.lstrip('.')
                FinderSubclass = self.tryGetClass(klassName)
            if FinderSubclass is None:
                raise ValueError(sub(
                    "Couldn't import any ParameterFinder class like '{}'",
                    klassName))
        plotDims = None if args.g in ('0', '') else args.g
        if plotDims: plotDims = [int(x) for x in args.g.split('x')]
        IDs = [int(x) for x in args.I.split(',')] if args.I else []
        self.finder = FinderSubclass(
            cfg, N_cores=N, wire=wire, IDs=IDs, #tcp=args[1:],
            logFile=logFile, plotFile=args.f, plotDims=plotDims)
        self.args = args

    def _analyze(self, event):
        """
        Provides some limited info about unhandled Deferred failures. For
        development purposes only.
        """
        if event.get("log_level") == LogLevel.critical:
            print sub("\nERROR: {}\n", event)
        
    def tryGetClass(self, name):
        try: FinderSubclass = reflect.namedObject(name)
        except ImportError:
            FinderSubclass = None
        if FinderSubclass is not None and \
           issubclass(FinderSubclass, ParameterFinder):
            return FinderSubclass
        if not name.endswith("_Finder"):
            return self.tryGetClass(name+"_Finder")
        
    @staticmethod
    def profile(f, *args, **kw):
        def done(result):
            pr.disable()
            import pstats
            with open('pf-profile.out', 'wb') as fh:
                ps = pstats.Stats(pr, stream=fh).sort_stats('cumulative')
                ps.print_stats()
            return result
        
        def substituteFunction(*args, **kw):
            d = f(*args, **kw)
            d.addCallback(done)
            return d
    
        from cProfile import Profile
        pr = Profile(); pr.enable()
        substituteFunction.func_name = f.func_name
        return substituteFunction()

    def cleak(self, f, *args, **kw):
        """
        For debugging memory leaks. Calls the deferred-returning function
        f (with any args, kw), recording changes made to the heap
        during the call. Prints a warning-level message about the heap
        every call, and stops with the debugger after 'stopInterval'
        calls, if defined.

        Returns a deferred that fires with the call result, which
        should make this indistinguishable from the original call.
        """
        def done(result):
            k = self._checkLeakStuff[0]
            if not hasattr(self, 'msgInterval') or k % self.msgInterval == 0:
                hpd = self._checkLeakStuff[1].heap()
                msg(True)
                msg("Heap after {:d} intervals:\n{}", k, hpd)
                msg("Heap (byrcs):\n{}", hpd.byrcs)
                # Particular focus
                for kk in xrange(4):
                    msg(-1, "Heap (byrcs[{:d}].byvia):\n{}",
                        kk, hpd.byrcs[kk].byvia, '-')
            if not hasattr(self, 'stopInterval') or k >= self.stopInterval:
                import pdb
                pdb.set_trace()
            return result
        
        if not self._checkLeakStuff:
            from guppy import hpy
            self._checkLeakStuff.extend([0, hpy()])
            self._checkLeakStuff[1].setrelheap()
        self._checkLeakStuff[0] += 1
        return f(*args, **kw).addCallback(done)
     
    def _run(self):
        def done(result):
            """
            Saves the final population (also auto-saved after each generation
            when the finder uses L{Solver.differential_evolution}) and
            stops the reactor if it's running.
            """
            if result and self.savePicklePath:
                p = result[1]
                p.save(self.savePicklePath)
            if reactor.running: reactor.stop()
        
        a = self.args
        F = [float(x.strip()) for x in a.F.split(',')]
        if len(F) == 1: F = F[0]
        picklePath = a[1] if len(a) > 1 else None
        d = self.finder(
            maxiter=a.m, popsize=a.p,
            CR=a.R, F=F, bitterEnd=a.b,
            randomBase=a.r, adaptive=not a.n,
            dwellByGrave=a.d, uniform=a.u,
            picklePath=picklePath, savePicklePath=self.savePicklePath)
        return d.addCallbacks(done, oops)

    def run(self):
        if self.args.i:
            return self.profile(self._run)
        if self.args.L:
            self._checkLeakStuff = []
            return self.cleak(self._run)
        return self._run()


args = Args(
    """
    Pingspice Parameter Finder using Differential Evolution.

    *Overwrites any existing .cir files.

    **Doesn't overwrite any existing .cir files.
    
    The first (and possibly only) positional argument is the fully
    qualified name (package.module.class) of a subclass of
    ParameterFinder (found in the pingspice.analysis.param
    module). You need to define such a subclass for the electronic
    component whose simulation model parameters you wish to find.

    If you specify the path of a compressed pickle file (with the
    ".dat" extension) from a previous run, your new run will resume
    with that Population.

    The -x option speeds things up when some evaluation setups take
    far longer than others, but only with WireEvaluator. So setting -x
    implies also setting -w.

    For the -r option, you can supply a float between 0.0 and 1.0 to
    use a compromise between DE/best/1/bin and DE/rand/1/bin. The
    default is 0.0 for DE/best/1/bin. To use traditional
    DE/rand/1/bin, set -r to 1.0.

    Press the Enter key to quit at any time.

    """
)
# ADE options
args('-m', '--maxiter', 1000, "Maximum number of DE generations to run")
args('-p', '--popsize', 4, "Population: # individuals per unknown parameter")
args('-R', '--CR', 0.7, "DE Crossover rate CR")
args('-F', '--F', "0.5,1.0", "DE mutation scaling F: two values for range")
args('-b', '--bitter-end', "Keep working to the end even with little progress")
args('-d', '--dwell', 5, "Extra generations before no-progress stopping")
args('-r', '--random-base', 0.0, "0.0 = DE/best/1, 1.0 = DE/rand/1")
args('-n', '--not-adaptive', "Don't use automatic F adaptation")
args('-u', '--uniform', "Initialize population uniformly instead of with LHS")
# Runtime options
args('-N', '--N-cores', 0, "Limit the number of CPU cores")
args('-w', '--wire', "Use WireEvaluator to split up Python processing load")
args('-x', '--xSSE',
     "Abort evaluation if challenger's SSE exceeds target's (implies -w)")
# Error handling
args('-W', '--warn-is-error', "Consider warnings to be errors (devel only)")
args('-o', '--console', "Start an interactive Ngspice console on failure")
args('-q', '--quit', "Quit if there's an Ngspice error")
# Netlist study files
args('-c', '--cir', "Write Ngspice .cir files for best individual*")
args('-e', '--cir-on-error', "Write Ngspice .cir files of failed analyses**")
args('-C', '--cir-all',
     "Write Ngspice .cir file of all analyses and exit**")
# Output
args('-l', '--logfile', "pfinder.log", "Logfile to (over)write with results")
args('-s', '--stdout', "Write to STDOUT instead of logfile")
args('-f', '--plotfile', "~/pfinder.png",
     "PNG file for simulation vs goal plots")
args('-g', '--plot-geometry', "1900x1400",
     "Plot geometry (<pixels w>x<pixels h>), '0' for fullscreen")
args('-P', '--pickle', "~/pfinder.dat",
     "Pickle dump file for finalized ade.Population object ('-' for none)")
# Verbosity
args('-v', '--verbose',
     "Verbose output, with some Ngspice warnings and failures")
args('-V', '--chatty',
     "Chatty verbose output, with all Ngspice warnings and failures")
args('-H', '--hardcore',
     "Hardcore verbosity, insane details about STDIO communication with Ngspice")
args('-S', '--spew', "Extremely verbose, with stdio CMD and RESPONSE")
# Devel options
args('-B', '--debug',
     "Run in debug mode: single core, wire mode disabled, STDIO logs")
args('-i', '--profile', "Run with the Python profiler (slower)")
args('-D', '--deferred-info',
     "Add a log observer for unhandled Deferred failures (devel only)")
args('-L', '--leak', "Run with memory leak analysis (slower)")
args('-E', '--ErrorTabulator',
     "Use ErrorTabulator instances as SSE (a bit slower, but can be useful)")
args('-I', '--setup-IDs', "",
     "Use only the specified setup IDs (comma-separated list, no spaces")
# Positional argument
args("<ParameterFinder subclass> [<pickle file>]")


def main(FinderSubclass=None):
    darwin = Darwin(args, FinderSubclass)
    reactor.callWhenRunning(darwin.run)
    reactor.run()

if __name__ == '__main__' and not args.h:
    main()
