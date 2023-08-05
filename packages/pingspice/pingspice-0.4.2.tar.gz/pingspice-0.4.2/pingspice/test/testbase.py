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
A base module for all L{pingspice} unit tests.
"""

import os.path, inspect, re, atexit, pickle, time
from contextlib import contextmanager

import numpy as np

from twisted.internet import reactor, defer, task
from twisted.trial import unittest

from ade import abort

from pingspice.circuit.av import AV, AV_Manager, AV_Maker
from pingspice.circuit.netlist import Netlist
from pingspice.util import sub, msg, oops, deferToThread, Config


VERBOSE = False


ST75NF20 = {
    # Finder = pingspice.lib.mosfets.ST75NF20_Finder
    # SSE = 4204.5 after 5904 evaluations
    # Commit following #a3565d1c, 2020-02-26
    'T_chl': -5.96276,
    'T_chm': 1.14928,
    'T_chv': 0.00628177,
    'T_drm': 1.35649,
    'T_drv': 0.0023024,
    'd_cjo': 1.04679e-08,
    'd_ikr': -99,
    'd_is': -11.2447,
    'd_m': 0.855679,
    'd_n': -4.00737e-05,
    'd_rs': -2.60605,
    'd_tt': -6.60918,
    'd_vj': 0.382868,
    'if_hca': -7.47928,
    'if_hcb': -8.28741,
    'ld': 1.70798e-09,
    'lgs_vs_ld': 1.21723,
    'm_Bt': -99,
    'm_L': -6.82094,
    'm_L2W': 6.28052,
    'm_L2xj': -1.0279,
    'm_NA': 19.2286,
    'm_Rp': 18.7899,
    'm_aK': -1.17367,
    'm_aR': 0.0281293,
    'm_aV': 5.7473,
    'm_dB': 0.861728,
    'm_dI': 218.099,
    'm_dL': -11.5932,
    'm_dR': -0.599271,
    'm_dV': -0.155393,
    'm_eta': -99,
    'm_kappa': 0,
    'm_nfs': 12.606,
    'm_tox': -8.29778,
    'm_vsa': 1,
    'mt_cbd': 1.48171,
    'mt_cgdo': 7.35398e-11,
    'mt_cgso': 0.815395,
    'mt_crss': 4.54434e-09,
    'mt_m': 0.883096,
    'mt_vj': 0.193175,
    'rd': 0.00291177,
    'rg': 3.04812,
    'rs': 0.000737872,
    'tca0': 10,
    'vf_lca': -2.77789,
}


class Bogus:
    pass


def deleteIfExists(fileNameOrPath):
    def tryDelete(fp):
        if os.path.exists(fp):
            os.remove(fp)
            return True
        return False
    if not tryDelete(fileNameOrPath):
        tryDelete(fileInModuleDir(fileNameOrPath))

def tempFiles(*args):
    for fileName in args:
        atexit.register(deleteIfExists, fileName)
    return args

def moduleDir(absolute=False, klass=None):
    if klass is None:
        klass = Bogus
    modulePath = inspect.getfile(klass)
    if absolute:
        modulePath = os.path.abspath(modulePath)
    return os.path.dirname(modulePath)

def fileInModuleDir(fileNameOrPath, absolute=False, isTemp=False, klass=None):
    filePath = os.path.normpath(
        os.path.join(moduleDir(absolute, klass), fileNameOrPath))
    if isTemp:
        tempFiles(filePath)
    return filePath


class RC_Mixin:
    _time = 0.01

    def fudge(self, R, C):
         # Due to R2, L2
        scale = 1.0 if R >= 1.0 else 0.95
        if C == 47000E-6:
            scale *= 1.06
        else:
            scale *= 0.97
        return scale

    def makeNetlist(self):
        filePath = fileInModuleDir('rc.cir', absolute=True)
        with open(filePath) as fh:
            self.netlist = fh.read()

    def makeAV(self, ID=None):
        if ID is None: ID = getattr(self, 'ID', -1)
        self.ID = ID + 1
        if not hasattr(self, 'avm'):
            from pingspice.circuit.av import AV_Manager, AV_Maker
            self.avm = AV_Manager()
            self.avList = self.avm.avList
            self.f = AV_Maker(self.avm)
        self.avm.setSetupID(self.ID)
        av = self.f.av('res', 5, 20)
        av.dev = 'R1'
        return self.ID

    @defer.inlineCallbacks
    def addSetup(self, tStep, tStop, mr=None, timeout=None, uic=False):
        self.makeAV()
        if mr is None:
            if not hasattr(self, 'mr'):
                self.mr = self.MultiRunner(Config(), self.avList, self.N_cores)
            mr = self.mr
        from pingspice.analysis.sim import TRAN
        analyzerDef = [TRAN, tStep, tStop]
        if uic: analyzerDef.append('uic')
        result = yield mr.addSetup(
            self.ID,
            ['time', 'V(2)'], analyzerDef, self.netlist).addErrback(oops)
        if timeout:
            aList = []
            dq = mr.setups[self.ID].dq
            for k in range(mr.N_cores):
                analyzer = yield dq.get()
                analyzer.r.waiter.setDelay('timeout', timeout)
                aList.append(analyzer)
            for analyzer in aList:
                dq.put(analyzer)
        defer.returnValue(self.ID)
    
    def mrSetup(self, tStep, tStop, mr=None, timeout=None):
        self.makeNetlist()
        return self.addSetup(tStep, tStop, mr=mr, timeout=timeout)
    
    def _voltage(self, t, R, C):
        return self.fudge(R, C) * 12.0 * (1.0 - np.exp(-t / (R * C)))
    
    def checkRiseTime(self, V, R, C=47000E-6):
        self.assertGreater(len(V.time), 50)
        k = np.searchsorted(V.time, self._time)
        t = V.time[k]
        v = V.v2[k]
        ratio = v / self._voltage(t, R, C)
        self.msg(
            "Capacitor reached {:f}V after {:f} sec (k={:d}/{:d})",
            v, t, k, len(V.time))
        self.msg(
            "Simulated vs expected (with {:f} fudge factor): {:f}",
            self.fudge(R, C), ratio)
        self.assertAlmostEqual(ratio, 1.0, 1)


class MsgBase(object):
    """
    A mixin for providing a convenient message method.
    """
    def isVerbose(self):
        if hasattr(self, 'verbose'):
            return self.verbose
        if 'VERBOSE' in globals():
            return VERBOSE
        return False
    
    def verboserator(self):
        if self.isVerbose():
            yield None

    def msg(self, proto, *args):
        for null in self.verboserator():
            if not hasattr(self, 'msgAlready'):
                proto = "\n" + proto
                self.msgAlready = True
            if args and args[-1] == "-":
                args = args[:-1]
                proto += "\n{}".format("-"*40)
            if args:
                print(proto.format(*args))
            else: print(proto)


class MockElements(object):
    """
    Mock-up for L{pingspice.circuit.elements.Elements}.
    """
    def __init__(self, n, realAV=False):
        self.n = n
        if realAV:
            self.avm = AV_Manager()
            self.real_f = AV_Maker(self.avm)
        else: self.real_f = None
        self.calls = []
        self.alterables = []
        self.name = None
        self.refNums = {}

    def get(self, obj, name, *args):
        """
        See C{Elements.get}.
        """
        return self.n.pso.get(obj, name, *args)
        
    def __getattr__(self, name):
        self.name = name
        return self

    def otherSets(self, ID):
        return []
    
    def observe(self, ID=None, nest=False):
        if ID is None:
            return 1
        if ID == 1:
            nodes = set()
            for call in self.calls:
                args = call[1]
                nodes.add(args[0])
                nodes.add(args[1])
            return nodes

    def __call__(self, *args, **kw):
        args = list(args)
        refDes = args.pop(0) if self.name is None else self.name
        self.calls.append([refDes, args, kw])
        self.name = None
        if len(refDes) > 1:
            return refDes
        refNumber = self.refNums.setdefault(refDes, 0)
        self.refNums[refDes] += 1
        return sub("{}{:d}", refDes, refNumber)
    
    def iNode(self, node=None, N=1):
        return "n_01"
        
    def av(self, *args):
        av = self.real_f.av(*args) if self.real_f else args
        self.alterables.append(av)
        return av
    
    def vav(self, name, *args):
        if isinstance(args[0], AV):
            av = args[0]
        else: av = self.av(name, *args)
        self.calls.append(['vav', name, av])

    @contextmanager
    def dashBlock(self, proto, *args):
        yield


class MockNetlist(object):
    """
    Mock-up for L{pingspice.circuit.netlist.Netlist}.
    """
    circuitName = "pingspice-circuit"
    avm = None
    
    def __init__(self, *args, **options):
        self.knowns = {}
        self.calls = 0
        if args and isinstance(args[0], str):
            filePath = args[0]
            self.circuitName = os.path.splitext(os.path.split(filePath)[-1])[0]
            self.fh = open(filePath, 'w')
            args = args[1:]
        elif len(args) > 1:
            self.fh, self.circuitName = args[:2]
            args = args[2:]
        if args:
            # NO TYPE CHECKING IN MOCK VERSION
            self.avm = args[0]
        # As-needed import
        from pingspice.circuit.options import PS_Options
        self.pso = PS_Options(options)
        self.options = options
    
    @contextmanager
    def __call__(self, *args, **params):
        if self.calls == 0 and args:
            self.circuitName = args[0]
        self.calls += 1
        self.f = MockElements(self)
        yield self.f


class MockWaiter(object):
    """
    For unit testing L{ngspice.stdio.NgspiceProtocol}.
    """
    def __init__(self):
        self.dExited = defer.Deferred()
    
    def setEvent(self, name):
        if name == 'exited' and not self.dExited.called:
            self.dExited.callback(None)
    
    def waitForEvent(self, *args, **kw):
        return defer.succeed(None)

    def delay(self, *args):
        return defer.succeed(None)
        
        
class MockNgspiceProtocol(object):
    """
    For unit testing L{ngspice.cmd.Commander}.
    """
    def __init__(self, cfg=None, waiter=None):
        self.cfg = cfg
        if waiter is None: waiter = MockWaiter()
        self.waiter = waiter
        self.lines = []
        self.watchers = {'out':set(), 'err':set()}
        self.running = True
        self.dError = None
        self._lastCmd = None, None
        self._lastAnalysis = None

    def _filerator(self, *args, **kw):
        fileName = sub("rc-{}.txt", "-".join(args))
        with open(fileInModuleDir(fileName), 'r') as fh:
            startedYielding = False
            for line in fh:
                # Initial mock STDOUT lines starting with '#' are
                # ignored and provide some description about the file
                if not startedYielding and line.startswith('#'):
                    continue
                startedYielding = True
                if 'k' in kw:
                    parts = line.split()
                    if not parts[0].isdigit(): continue
                    k = int(parts[0])
                    if k != kw['k']: continue
                    textValue = "".join(parts[1:])
                    yield sub("{}[{:d}] = {}", args[0], k, textValue)
                    break
                if 'k0' in kw and 'k1' in kw:
                    parts = line.split()
                    if not parts[0].isdigit(): continue
                    k = int(parts[0])
                    if k < kw['k0'] or k > kw['k1']:
                        continue
                line = line.rstrip('\n')
                yield line
    
    def shutdown(self):
        pass

    def cmd(self, *args, **kw):
        def doneWaiting(null):
            self.dError = None
        
        self._lastCmd = (args, kw)
        # Errors
        stderr = None
        if args[0] == 'tran' and args[1:] == (1, 2, 3):
            stderr = [
                "Warning: TSTART is invalid, must be less than TSTOP.",
                "",
                "tran simulation(s) aborted"]
        elif args[0] == 'bogus':
            stderr = ["bogus: no such command available in ngspice"]
        # Possible errors
        elif args[0] == 'alter':
            if args[1] != 'r1':
                stderr = [sub(
                    "Error: no such device or model name {}", args[1])]
        if stderr:
            self.dError = defer.succeed(None).addCallback(doneWaiting)
            for f in self.watchers['err']:
                for line in stderr:
                    f(line)
            return ""
        return sub("MOCK CMD: {}, {}", args, kw)
    
    def registerWatcher(self, out=None, err=None):
        """
        Copied from L{NgspiceProtocol}, #93c5595
        """
        for name, f in (('out', out), ('err', err)):
            if f is None: continue
            if not callable(f):
                raise ValueError(sub("'{}' is not callable!", f))
            self.watchers[name].add(f)

    def unregisterWatchers(self, *args):
        """
        Copied from L{NgspiceProtocol}, #93c5595
        """
        for f in args:
            for watchers in self.watchers.values():
                watchers.discard(f)

    def response(self, N=None, func=None):
        parts = None
        responseLines = []
        args, kw = self._lastCmd
        if args == ('set',):
            parts = ['set']
        elif args[0] in ('tran', 'ac', 'dc'):
            parts = [args[0]]
            self._lastAnalysis = args[0]
        elif args[0] == 'display':
            parts = ['display', self._lastAnalysis]
        elif args[0] == 'print':
            vectorName = args[1].replace('(', '').replace(')', '').lower()
            parts = [vectorName, self._lastAnalysis]
        elif args[0] in ("show", "showmod"):
            if args[1] not in ('r1', 'c1', 'l2', 'a1', 'v1'):
                # Stupidly, this does not go to STDERR
                responseLines.append("No matching instances or models")
            else:
                parts = list(args)
                while ":" in parts:
                    parts.remove(":")
        elif args[0] == 'echo':
            responseLines.append(args[1])
        if parts:
            for line in self._filerator(*parts):
                if func:
                    output = func(line)
                    if output is not None: line = output
                responseLines.append(line)
        if self.cfg.hardcore:
            print "\nRESPONSE", args, kw, responseLines
        return defer.succeed(responseLines)


class MockCommander(object):
    """
    For unit testing  L{ngspice.sourcery.Sourcer}.
    """
    def __call__(self, *args, **kw):
        if args[0] == 'source':
            if args[1].count('\n') > 2 or os.path.exists(args[1]):
                from pingspice.ngspice.cmd import Result
                result = Result()
                result.stdout = \
                    "Circuit: circuit 'boost-03' generated by pingspice"
                return defer.succeed(result)
            raise Exception("Oops, bad source")


class MockSourcer(object):
    """
    For unit testing L{analysis.sim.Analyzer}.
    """
    def __init__(self, *args, **kw):
        self.called = []

    def __str__(self):
        with open(fileInModuleDir("rc.cir", absolute=True), 'r') as fh:
            result = fh.read()
        return result
        
    def write(self, *args, **kw):
        self.called.append(('write', args, kw))


class MockResult(object):
    def __init__(self):
        self.cmd = ""
        self.stdout = []
        self.stderr = []
        self.error = ""

    def __repr__(self):
        if self.error:
            return "ERROR: " + self.error
        return "MockResult " + self.cmd
        
    def __nonzero__(self):
        return not self.error
    def __contains__(self, line):
        return line in self.stdout
    def __getitem__(self, k):
        return self.stdout[k]
    def __iter__(self):
        for line in self.stdout:
            yield line
    def __len__(self):
        return len(self.stdout)

    
class MockNgspiceRunner(object):
    _N = 100
    #          0       1       2      3             4
    _names = ['time', 'V(1)', 'neg', 'vcs#branch', 'V(2)']

    def __init__(self, *args, **kw):
        self.cfg = args[0] if args else Config()
        self.timeout = kw.get('timeout', 60)
        self.gotten = []
        self.calls = {}
        self.memUsed = 360000
        self.employedByAnalyzer = False
        self.s = MockSourcer()
        self.np = MockNgspiceProtocol()
        self.cmd = MockCommander()
        self.waiter = MockWaiter()
        self.running = True

    def shutdown(self):
        self.running = False
        return defer.succeed(None)
    
    def cancel(self):
        return defer.succeed(None)

    def call(self, *args, **kw):
        parts = None
        vectorName = None
        result = MockResult()
        result.cmd = " ".join([str(x) for x in args])
        self.calls.setdefault(args[0], []).append(args[1:])
        if not self.running:
            result.error = "DEAD"
        elif args[0] in ('tran', 'ac', 'dc'):
            self.analysis = args[0]
            parts = [args[0]]
        elif args[0] == 'display':
            parts = ['display', self.analysis]
        elif args[0].startswith('print'):
            mIndex = re.search(r'\[([0-9]+)\]', args[1])
            if mIndex:
                vectorName = args[1][:mIndex.start(0)]
                kw['k'] = int(mIndex.group(1))
            else:
                mIndices = re.search(r'\[([0-9]*)\:([0-9]*)\]', args[1])
                if mIndices:
                    vectorName = args[1][:mIndices.start(0)]
                    for k, text in enumerate(mIndices.groups()):
                        kw[sub("k{:d}", k)] = int(text) if text else None
                else:
                    vectorName = args[1]
            vectorName = vectorName.replace('(', '').replace(')', '').lower()
            parts = [vectorName, self.analysis]
        # Possibly use file mock STDOUT
        if parts:
            bogus = True
            for line in self.np._filerator(*parts, **kw):
                output = kw['cmd_func'](line) if 'cmd_func' in kw else None
                if output is not None: line = output
                result.stdout.append(line)
                bogus = False
        else: bogus = False
        if bogus and vectorName:
            result.error = sub("Error: no such vector {}", vectorName)
        return defer.succeed(result)
    
    def cnr(self, *args, **kw):
        kw['cmd_N'] = 0
        return self.call(*args, **kw)

    def sync(self, *args):
        return defer.succeed([])
    
    def source(self, netlistFileOrText, **kw):
        filePath = fileInModuleDir("rc.cir")
        result = MockResult()
        result.cmd = "source " + filePath
        if netlistFileOrText == "rc.cir":
            self.filePath = filePath
        elif netlistFileOrText.count('\n') < 2:
            result.stderr = ["Bogus netlist"]
            result.error = "Bogus netlist"
        return defer.succeed(result)
    
    def delayForResponse(self):
        return defer.succeed(None)
    
    def memUsage(self):
        return defer.succeed(self.memUsed)
    
    def clearData(self):
        return self.cnr('destroy', 'all')

    def setting(self, name, value):
        if value is True:
            return self.cnr('set', name)
        return self.cnr('set', name, '=', value)

    def setSavedVectors(self, *args, **kw):
        return self.cnr('save', *args)

    def waitForAlterations(self, *args):
        return defer.succeed(None)
    
    def alter(self, *args):
        return self.call('alter', *args)

    def altermod(self, *args):
        return self.call('altermod', *args)
    
    def get(self, *names):
        result = []
        for name in names:
            if name not in self._names:
                result = []
                break
            self.gotten.append(name)
            result.append(self._names.index(name)*np.ones(self._N))
        if not result:
            result = MockResult()
            result.error = sub("Error getting '{}'", name)
        elif len(result) == 1:
            result = result[0]
        return defer.succeed(result)

    def tran(self, *args):
        d = self.call('tran', *args)
        if len(args) > 2:
            d.addCallback(
                lambda result: task.deferLater(reactor, 1.0, lambda : result))
        return d


class MockVector(object):
    def __init__(self, r, names):
        self.names = names
        self.values = {}
        self.independents = []

    def __contains__(self, name):
        return name in self.names
        
    def __getitem__(self, name):
        return self.values[name]

    def __getattr__(self, name):
        if name in ('_notRunning', '_error'):
            return False
        return self[name]

    def error(self, *args):
        if args: self._error = str(args[0])
        return self._error
    
    def addName(self, name, independent=False):
        if independent and name not in self.independents:
            self.independents.append(name)
        if name not in self.names:
            self.names.append(name)
        return name

    def addVector(self, name, X, independent=False):
        self.addName(name, independent)
        self.values[name] = X

    def copy(self):
        V2 = MockVector(None, self.names)
        V2.values.update(self.values)
        V2.independents = self.independents
        errMsg = self.error()
        if errMsg: V2.error(errMsg)
        return V2
        

class MockAV_Maker(object):
    def __init__(self, avManager=None, knowns={}):
        if avManager is None:
            from pingspice.circuit.av import AV_Manager
            avManager = AV_Manager(knowns)
        self.avm = avManager

    def av(self, name, *args):
        from pingspice.circuit.av import AV
        thisAV = AV(name, *args)
        self.avm.setRelationships(thisAV)
        self.avm.add(thisAV)
        return thisAV
        

class MockIV_Manager(object):
    """
    See C{analysis.evaluate.IV_Manager}.

    I have four test configurations, settable with an integer written
    to my I{_cfg} attribute:

        1. [CI, D]

        2. [CI, EI, D], where EI is an enumerable indep with values=1.0.

        3. [CI*, D], where CI* is CI reversed and thus not intepolatable.

        4. [D]
    
    Default is no enumerable independent vectors. If I{_noNumerables}
    is made C{False}, I will pretend to have an enumerable vector at
    kCol=1, and the dependent vector at kCol=2.
    """
    def __init__(self, indieFlags):
        self.indieFlags = indieFlags
        self.kInterp = 0
        self.calls = {}
        self._cfg = 1
        
    def _addCall(self, name, *args, **kw):
        self.calls.setdefault(name, []).append((args, kw))

    def __nonzero__(self):
        return bool(self.indieFlags)
        
    def __iter__(self):
        self._addCall('__iter__')
        for k, isIndep in enumerate(self.indieFlags):
            if isIndep:
                yield k
    
    def dependerator(self):
        self._addCall('dependerator')
        yield 1 if self._cfg in (1, 3) else 2 if self._cfg == 2 else 0

    def enumerableator(self):
        if self._cfg == 2:
            yield 1

    def clear(self):
        pass
            
    def noEnumerables(self):
        return self._cfg != 2

    def setup(self, X):
        pass

    def subseterator(self, kCol, *args):
        def pairs():
            for k in range(len(args)/2):
                yield args[2*k:2*k+2]

        if self._cfg == 2:
            if kCol != 1:
                raise ValueError("Not an enumerable vector column!")
            yield [np.flatnonzero(np.equal(X[:,kCol], 1)) for kCol, X in args]
                
    
class MockEvalSpec(object):
    """
    See C{analysis.evaluate.EvalSpec}.
    """
    def __init__(self, ID, nameList, indieFlags=[True, False], logValues=set()):
        self.ID = ID
        self.nameList = nameList
        self.indieFlags = indieFlags
        self.logValues = logValues
        self.q = None
        self.ivm = MockIV_Manager(indieFlags)
    
    def canInterpolate(self):
        return self.ivm.kInterp is not None

    def setupX(self, X, q=None):
        """
        See: L{EvalSpec.setupX}.
        """
        if X is None:
            self.N = 1
        elif callable(X):
            self.N = 1
            if not getattr(X, 'dr', False):
                self.q = q
        else:
            Nc = X.shape[1]
            self.N = X.shape[0]
            self.ivm.setup(X)
        self.X = X


class MockSpecs(object):
    """
    I load attributes from specs-NMOS.dat (N-channel) or
    specs-PMOS.dat (P-channel). These test files ship with the
    pingspice package and can be updated by uncommenting
    L{analysis.param.PICKLE_PATH}.
    """
    def __init__(self, P_channel=False):
        filePath = fileInModuleDir(
            'specs-PMOS.dat' if P_channel else 'specs-NMOS.dat')
        with open(filePath, 'rb') as fh:
            self._specs = pickle.load(fh)
    
    def __getattr__(self, name):
        return getattr(self._specs, name)

        
class MockIndividual(object):
    def __init__(self, p, values=None):
        self.p = p
        if values is None:
            self.values = np.empty(p.Nd)
        elif len(values) != p.Nd:
            raise ValueError("Expected {:d} values".format(self.p.Nd))
        self.values = values
        self.SSE = None
        self.partial_SSE = False

    def __repr__(self):
        print self.SSE, self.values
        
    def spawn(self, values):
        return MockIndividual(self.p, values)

    def __sub__(self, other):
        return MockIndividual(self.values - other.values)

    def __add__(self, other):
        return MockIndividual(self.values + other.values)

    def __nonzero__(self):
        return bool(self.SSE)
    
    def __eq__(self, other):
        return self.SSE == other.SSE
    
    def equals(self, other):
        if hasattr(other, 'values'):
            other = other.values
        if not hasattr(other, 'shape'):
            other = np.array(other)
        return np.all(self.values == other)

    def __lt__(self, other):
        return self.SSE is not None and self.SSE < other.SSE

    def __gt__(self, other):
        return self.SSE is None or self.SSE > other.SSE
    
    def __getitem__(self, k):
        return self.values[k]

    def __setitem__(self, k, value):
        self.values[k] = value
            
    def __iter__(self):
        for value in self.values:
            yield value

    def __len__(self):
        return len(self.values)

    def limit(self):
        np.clip(self.values, self.p.pm.mins, self.p.pm.maxs, self.values)
        return self
    
    def evaluate(self, xSSE=None):
        def done(SSE):
            self.SSE = SSE
            self.partial_SSE = xSSE is not None
            return self
        return self.p.evalFunc(self.values, xSSE).addCallback(done)


class MockParameterManager(object):
    def fromUnity(self, values):
        return -5 + 10*values
    
    def pv(self, values):
        return 1.0

    def lottery(self, values):
        return np.all(np.abs(values < 5))

    def prettyValues(self, values, *args):
        """
        Returns an easily readable string representation of the supplied
        I{values} with their parameter names, sorted.

        You can provide as an additional argument a prelude string, or
        a string proto with additional args, and the string will
        precede the values.
        """
        lineParts = []
        if args:
            lineParts.append(args[0].format(*args[1:]))
        for k, name, value in self.sortedNamerator(values):
            lineParts.append("{}={:g}".format(name, value))
        text = " ".join(lineParts)
        return self.fill(text)


class MockPopulation(object):
    def __init__(self, func, bounds, names, constraints=[], popsize=10):
        def evalFunc(values, xSSE):
            return defer.maybeDeferred(func, values, xSSE)

        self.Nd = len(bounds)
        self.Np = self.Nd * popsize
        self.pm = MockParameterManager()
        if not callable(func):
            raise ValueError(sub("Object '{}' is not callable", func))
        self.evalFunc = evalFunc
        self.counter = 0

    @property
    def kBest(self):
        return np.argmin([i.SSE for i in self.iList])
    
    def __getitem__(self, k):
        return self.iList[k]
        
    def __setitem__(self, k, i):
        self.iList[k] = i

    def spawn(self, values):
        return MockIndividual(self, values)
        
    @defer.inlineCallbacks
    def setup(self, uniform=False):
        XY = np.random.rand(self.Np, self.Nd) + 1E-2
        i = MockIndividual(self, np.array([2.0, 2.0]))
        yield i.evaluate()
        self.iList = [i]
        for xy in XY:
            i = MockIndividual(self, xy)
            yield i.evaluate()
            self.iList.append(i)

    def replacement(self, *args, **kw):
        return True
            
    def push(self, i):
        self.iList.append(i)
        self.iList.pop(0)

    def best(self):
        return self.iList[self.kBest]


class AlterationChecker(MsgBase):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.calls = {}
        self.expected = {}
        self.aa = (self.fDev, self.fModel, self.fAV)

    @property
    def alter(self):
        return len(self.calls.get('alter', []))

    @property
    def altermod(self):
        return len(self.calls.get('altermod', []))

    @property
    def av(self):
        return len(self.calls.get('av', []))
    
    def fDev(self, *args):
        self.calls.setdefault('alter', []).append(args)

    def fModel(self, *args):
        self.calls.setdefault('altermod', []).append(args)

    def fAV(self, *args):
        self.calls.setdefault('av', []).append(args)

    def ea(self, *args):
        """
        Adds an expected 'alter' call.
        """
        self.expected.setdefault('alter', []).append(args)

    def eam(self, *args):
        """
        Adds an expected 'altermod' call.
        """
        self.expected.setdefault('altermod', []).append(args)

    def eav(self, *args):
        """
        Adds an expected call to L{fAV}, with (1) a regexp pattern for the
        AV object's string representation and (2) possibly also its
        value.
        """
        self.expected.setdefault('av', []).append(args)
        
    def check(self, Ne=0):
        """
        Returns the first expected call that was not made, or a string
        reporting an unexpected call, or C{None} if all expected calls
        were made.

        @keyword Ne: The number, if any, of AV calls expected beyond
            those accounted for with 'alter' and 'altermod' calls, and
            expected 'av' calls.
        """
        def info(callType):
            for k, call in enumerate(calls):
                self.msg("{:02d} {}", k+1, call)
        
        def checkNoExcess(callType, Ne=None):
            Nc = len(calls)
            if Ne is None: Ne = len(callsExpected)
            if Nc > Ne:
                info(callType)
                return sub(
                    "Got {:d} more '{}' calls than expected",
                    Nc-Ne, callType)

        def failed(callType):
            info(callType)
            return [callType] + list(callExpected)

        N_av_expected = 0
        callTypes = 'alter', 'altermod'
        for callType in callTypes:
            calls = self.calls.get(callType, [])
            callsExpected = self.expected.get(callType, [])
            N_av_expected += len(callsExpected)
            oops = checkNoExcess(callType)
            if oops: return oops
            kFound = set()
            for callExpected in callsExpected:
                OK = False
                N = len(callExpected)
                for k, call in enumerate(calls):
                    if k not in kFound and call[:N] == callExpected:
                        OK = True
                        kFound.add(k)
                        break
                if not OK: return failed(callType)
        calls = self.calls.get('av', [])
        callsExpected = self.expected.get('av', [])
        oops = checkNoExcess('av', N_av_expected+Ne)
        if oops: return oops
        kFound = set()
        for callExpected in callsExpected:
            pattern = callExpected[0]
            OK = False
            for k, call in enumerate(calls):
                if k in kFound: continue
                if re.search(pattern, repr(call[0])):
                    if len(callExpected) > 1 and callExpected[1] != call[1]:
                        continue
                    OK = True
                    kFound.add(k)
                    break
            if not OK: return failed('av')


class TestCase(MsgBase, unittest.TestCase):
    """
    Slightly improved TestCase.

    @ivar shutdownables: Append an object with a I{shutdown} method to
        this list to have that method called during L{tearDown}.
    """
    # Nothing should take longer than 10 seconds, and often problems
    # aren't apparent until the timeout stops the test.
    timeout = 10

    def __init__(self, *args, **kw):
        if getattr(self, 'verbose', False) or globals().get('VERBOSE', False):
            msg(True)
        self.pendingCalls = {}
        self.shutdownables = []
        super(TestCase, self).__init__(*args, **kw)

    def tearDown(self):
        msg(None)
        while self.pendingCalls:
            call = self.pendingCalls.keys()[0]
            if call.active():
                self.pendingCalls[call].callback(None)
                call.cancel()
        msg(None)
        if self.shutdownables:
            dList = [getattr(x, 'shutdown')() for x in self.shutdownables]
            return defer.DeferredList(dList)
    
    def st(self, *args, **kw):
        if not kw.get('always', False) and self.isVerbose(): return
        text = sub(*args) if args else ""
        raise unittest.SkipTest(text)
                
    def oops(self, failureObj):
        print "\nFAIL!!!!!!!\n{}\n{}".format('-'*40, failureObj.value)
        import pdb; pdb.set_trace()

    def deferToDelay(self, x=None):
        def delayOver(null):
            self.pendingCalls.pop(call, None)
            
        if x is None:
            x = self.unknownResponseWaitTime
        d = defer.Deferred().addCallbacks(delayOver, self.oops)
        call = reactor.callLater(x, d.callback, None)
        self.pendingCalls[call] = d
        return d
        
    def doCleanups(self):
        if hasattr(self, 'msgAlready'):
            del self.msgAlready
        return super(TestCase, self).doCleanups()

    def getV_at_t(self, V, name, t):
        """
        Returns the value of vector I{name} in the supplied instance I{V}
        of a subclass of I{VectorsBase} that is closest to the
        specified time I{t}.
        """
        time = V.time
        k = np.argmin(abs(time-t))
        return V[name][k]
        
    def plot(self, ph):
        from matplotlib import pyplot
        X = [i.values[0] for i in ph.p]
        Y = [i.values[1] for i in ph.p]
        pyplot.plot(X, Y, '-o')
        pyplot.plot(X[-1], Y[-1], 'xr')
        pyplot.show()

    def multiplerator(self, N, expected):
        def check(null):
            self.assertEqual(resultList, expected)
            del self.d
        
        dList = []
        resultList = []
        for k in xrange(N):
            yield k
            self.d.addCallback(resultList.append)
            dList.append(self.d)
        self.dm = defer.DeferredList(dList).addCallback(check)
            
    def checkOccurrences(self, pattern, text, number):
        occurrences = len(re.findall(pattern, text))
        if occurrences != number:
            info = \
                u"Expected {:d} occurrences, not {:d}, " +\
                u"of '{}' in\n-----\n{}\n-----\n"
            info = info.format(number, occurrences, pattern, text)
            self.assertEqual(occurrences, number, info)
    
    def checkBegins(self, pattern, text):
        pattern = r"^\s*%s" % (pattern,)
        self.assertTrue(bool(re.match(pattern, text)))

    def checkProducesFile(self, fileName, executable, *args, **kw):
        producedFile = fileInModuleDir(fileName)
        if os.path.exists(producedFile):
            os.remove(producedFile)
        result = executable(*args, **kw)
        self.assertTrue(
            os.path.exists(producedFile),
            "No file '{}' was produced.".format(
                producedFile))
        os.remove(producedFile)
        return result

    def runerator(self, executable, *args, **kw):
        return Runerator(self, executable, *args, **kw)

    def assertPattern(self, pattern, text):
        proto = "Pattern '{}' not in '{}'"
        if '\n' not in pattern:
            text = re.sub(r'\s*\n\s*', '', text)
        if isinstance(text, unicode):
            # What a pain unicode is...
            proto = unicode(proto)
        self.assertTrue(
            bool(re.search(pattern, text)),
            proto.format(pattern, text))

    def assertStringsEqual(self, a, b, msg=""):
        N_seg = 20
        def segment(x):
            k0 = max([0, k-N_seg])
            k1 = min([k+N_seg, len(x)])
            return "{}-!{}!-{}".format(x[k0:k], x[k], x[k+1:k1])
        
        for k, char in enumerate(a):
            if char != b[k]:
                s1 = segment(a)
                s2 = segment(b)
                msg += "\nFrom #1: '{}'\nFrom #2: '{}'".format(s1, s2)
                self.fail(msg)

    def assertNone(self, a):
        self.assertTrue(a is None, sub("{} is not None", a))
                
    def assertItemsAlmostEqual(self, a, b, tol=6):
        for ak, bk in zip(a, b):
            self.assertAlmostEqual(ak, bk, tol)
    
    def assertWithinOnePercent(self, x, xExpected):
        ratio = x / xExpected if xExpected else x+1
        msg = sub("{} not within 1% of {}", x, xExpected)
        self.assertLess(abs(ratio-1), 0.01, msg)

    def assertWithinFivePercent(self, x, xExpected):
        ratio = x / xExpected if xExpected else x+1
        msg = sub("{} not within 5% of {}", x, xExpected)
        self.assertLess(abs(ratio-1), 0.05, msg)

    def assertWithinTenPercent(self, x, xExpected):
        ratio = x / xExpected if xExpected else x+1
        msg = sub("{} not within 10% of {}", x, xExpected)
        self.assertLess(abs(ratio-1), 0.10, msg)
        
    def assertBetween(self, x, xMin, xMax):
        self.assertGreaterEqual(x, xMin)
        self.assertLessEqual(x, xMax)

    def assertInItem(self, thingIn, seq):
        for thing in seq:
            if thingIn in thing:
                return
        self.fail(sub("'{}' not in {}", thingIn, seq))

    def assertNotInItem(self, thingIn, seq):
        for thing in seq:
            if thingIn in thing:
                self.fail(sub("'{}' in {}", thingIn, seq))

    def assertNone(self, x):
        self.assertIs(x, None)


class FinderBase(TestCase):
    """
    Methods used by L{test.lib.test_mosfets.FinderBase} and
    L{test.lib.test_diodes.FinderBase}. Your subclass must have the
    attributes listed.

    @cvar PARAMS: A dict or string with parameter names and values, if
        L{getV} will be called with I{text} not set.

    @cvar Finder: A subclass of L{analysis.param.ParameterFinder} for
        the device whose model is being tested.
    
    @ivar cfg: An instance of L{Config}.
    @ivar mf: An instance of a subclass of L{analysis.param.ParameterFinder}.
    @ivar logValues: A set of cnames that are evaluated in log space.
    """
    def setUp(self):
        abort.restart()
        self.tList = []
        quiet = not self.isVerbose() \
                and not self.chatty and not self.spew and not self.hardcore
        self.cfg = Config(
            quiet=quiet,
            verbose=self.isVerbose(),
            chatty=self.chatty, spew=self.spew,
            hardcore=self.hardcore, nodes=self.nodes, study=self.study_err)
        self.plotFile = fileInModuleDir(
            "pfinder.png", isTemp=not self.keepPlotFile)
        self.mf = self.Finder(self.cfg, plotFile=self.plotFile)

    @defer.inlineCallbacks
    def tearDown(self):
        # As-needed import
        # -------------------------------------------------
        from ade import abort
        # -------------------------------------------------
        abort.abortNow()
        abort.shutdown()
        if hasattr(self, 'r'):
            yield self.r.shutdown()
        if hasattr(self, 'q'):
            yield self.q.shutdown()
        yield TestCase.tearDown(self)
        
    def setSetup(self, ID, *names):
        self.ID = ID
        self.addLater = names
        if self.cfg.chatty:
            self.mf.showNetlists = [ID]
        # The order of the next two lines does matter. Finalize
        # AV_Manager after creating netlist
        OK = self.mf.analyzerPrep(ID)
        self.mf.avm.finalize()
        self.assertTrue(OK)
        self.netlist = self.mf.netlists[ID]

    def aa(self, ID):
        """
        Returns the arguments of L{testbase.FinderBase.DC}
        L{testbase.FinderBase.TRAN} to get an analyzer for setup
        I{ID}.
        """
        analyzers = self.mf.s.analyzers
        aco = analyzers[ID]
        return aco[1:]

    def CapacitanceAnalyzer(self):
        a = self.mf.analyzers[111][0]
        return a.setup(
            111, self.mf.nameLists[111], self.mf.avm.avList, 0, 50, 0.1)
        
    def DC(self, *args):
        from pingspice.ngspice import NgspiceRunner
        # As-needed imports
        # -------------------------------------------------
        from pingspice.ngspice import NgspiceRunner
        from pingspice.analysis.sim import DC
        # -------------------------------------------------
        self.r = NgspiceRunner(self.cfg)
        a = DC(
            self.r, self.ID,
            self.mf.nameLists[self.ID],
            self.mf.avm.avList, *args)
        return a.setup(self.netlist)

    def TRAN(self, *args):
        if hasattr(args[0], '__iter__'):
            nameList = args[0]
            args = args[1:]
        else: nameList = self.mf.nameLists[self.ID]
        # As-needed imports
        # -------------------------------------------------
        from pingspice.ngspice import NgspiceRunner
        from pingspice.analysis.sim import TRAN
        # -------------------------------------------------
        self.r = NgspiceRunner(self.cfg)
        a = TRAN(self.r, self.ID, nameList, self.mf.avm.avList, *args)
        return a.setup(self.netlist)
        
    def ploterator(self, ID, SSE, N, V, *names):
        # As-needed import
        # -------------------------------------------------
        from yampex.plot import Plotter
        # -------------------------------------------------
        p = Plotter(1, N)
        p.add_marker('.')
        p.use_legend(); p.use_grid()
        p.set_title("SSE = {:f}", SSE)
        with p as sp:
            Ii = []
            Id = []
            independents = self.mf.independents.get(ID, [])
            for k, name in enumerate(names):
                if name in independents:
                    Ii.append(k)
                else: Id.append(k)
            namesToPlot = [names[k] for k in Ii]
            namesToPlot.extend([names[k] for k in Id])
            ax = sp(V, *namesToPlot)
            X = self.mf.Xs[ID]
            if not callable(X):
                Xi = X[:,Ii[0]]
                for k in Id:
                    if names[k] is None: continue
                    name = namesToPlot[k]
                    if k < X.shape[1]:
                        Xd = X[:,k]
                        if name.lstrip('+') in self.logValues:
                            Xd = np.power(10.0, Xd)
                        ax.plot(Xi, Xd, 'x', legend=sub("{} (goal)", name))
            for k in range(N-1):
                yield sp
        sp.show()
        
    def evaluate(self, V, N=1, noPlot=False, skipNames=[]):
        def done(null):
            SSE = et.total()
            if self.cfg.verbose:
                print sub("\nSSE: {:5g}\n", SSE)
                if noPlot:
                    return SSE
                names1 = independents[:1] if independents else nameList[:1]
                for name in nameList:
                    if name.lstrip('+') == names1[0]:
                        continue
                    names1.append(name)
                names = [names1[0]]
                for name in names1[1:]:
                    if name.lstrip('+') in skipNames:
                        name = None
                    names.append(name)
                if not names or names[0] not in V:
                    pi = [] if N>1 else None
                elif N > 1:
                    pi = self.ploterator(ID, SSE, N, V, *names)
                else:
                    pi = None
                    list(self.ploterator(ID, SSE, 1, V, *names))
            else: pi = [] if N>1 else None
            if pi is None:
                return SSE
            return SSE, pi
        
        # As-needed imports
        # -------------------------------------------------
        import asynqueue 
        from pingspice.analysis.evaluate import EvalSpec
        from pingspice.analysis.sse import ErrorTabulator
        # -------------------------------------------------
        ID = self.ID
        nameList = self.mf.nameLists[ID]
        independents = self.mf.independents.get(ID, [])
        indieFlags = [(x.lstrip('+') in independents) for x in nameList]
        evalSpec = EvalSpec(ID, nameList, indieFlags, self.logValues)
        if not hasattr(self, 'q'):
            self.q = asynqueue.ThreadQueue(raw=True)
        evalSpec.setupX(self.mf.Xs[ID], self.q)
        evalSpec.setWeights(self.mf.weights)
        evalSpec.logValues = self.mf.logValues
        et = ErrorTabulator(transforms=self.mf.transforms)
        return et.add(ID, V, evalSpec).addCallback(done)

    def time(self):
        self.tList.append(time.time())
        lines = ["\nCall durations", "-"*79]
        for k, t in enumerate(self.tList[:-1]):
            lines.append(sub(
                "Call #{:d}: {:f} seconds",
                k+1, self.tList[k+1] - self.tList[k]))
        return "\n".join(lines)
    
    def _paramerator(self):
        names = set()
        for av in self.mf.avm:
            if not av.isParam(): continue
            name = av.name
            if name in names: continue
            names.add(name)
            yield name
    
    def getValues(self, textOrDict=None):
        if textOrDict is None:
            textOrDict = self.PARAMS
        values = []
        for name in self._paramerator():
            if isinstance(textOrDict, dict):
                values.append(textOrDict[name])
            else:
                match = re.search(sub("(^|\s){}=([0-9\.e\-\+]+)", name), textOrDict)
                if match is None:
                    raise KeyError(sub("No value defined for '{}'", name))
                values.append(float(match.group(2)))
        return values

    def alterValue(self, values, name, value):
        for k, thisName in enumerate(self._paramerator()):
            if thisName == name:
                values[k] = value
                return
    
    @defer.inlineCallbacks
    def getV(self, a, textOrDict=None, study=False, values=None):
        study = True if study else self.study
        if values is None:
            values = self.getValues(textOrDict)
        for name in getattr(self, 'addLater', []):
            yield a.addName(name)
        V = yield a(values)
        if V.error() or study:
            if hasattr(a, 'study'):
                yield a.study(values)
        if V.error():
            import pdb; pdb.set_trace()
        defer.returnValue(V.copy())

    @defer.inlineCallbacks
    def checkSSE_DC(self, ID, SSE_expected, *skippedNames, **kw):
        """
        Asserts that SSE is within 5% of I{SSE_expected}, after a DC
        analysis of the specified setup I{ID}, perhaps with one or
        more I{skippedNames} omitted from the call to L{evaluate}.

        @keyword include: Specify a vector name to include in the call
            to I{setSetup}.
        
        @keyword remove: Specify a vector name to remove from this
            setup's nameList before setup, analyzer construction, and
            V acquisition, and then append back to it afterwards.

        @keyword textOrDict: Supply as a keyword in the call to
            L{getV}.
        """
        remove = kw.get('remove', None)
        if remove: self.mf.nameLists[ID].remove(remove)
        args = [ID]
        include = kw.get('include', None)
        if include: args.append(include)
        self.setSetup(*args)
        a = yield self.DC(*self.aa(ID))
        V = yield self.getV(a, textOrDict=kw.get('textOrDict', None))
        if remove: self.mf.nameLists[ID].append(remove)
        SSE = yield self.evaluate(V, skipNames=skippedNames)
        self.assertWithinFivePercent(SSE, SSE_expected)

    @defer.inlineCallbacks
    def checkSSE_TRAN(
            self, ID, SSE_expected,
            include=None, remove=None, textOrDict=None):
        """
        Asserts that SSE is within 5% of I{SSE_expected}, after a TRAN
        analysis of the specified setup I{ID}.

        @keyword include: Specify a vector name to include in the call
            to I{setSetup}.

        @keyword remove: Specify a vector name to remove from this
            setup's nameList before setup, analyzer construction, and
            V acquisition, and then append back to it afterwards.

        @keyword textOrDict: Supply as a keyword in the call to
            L{getV}.
        """
        if remove: self.mf.nameLists[ID].remove(remove)
        args = [ID]
        if include: args.append(include)
        self.setSetup(*args)
        a = yield self.TRAN(*self.aa(ID))
        V = yield self.getV(a, textOrDict=textOrDict)
        if remove: self.mf.nameLists[ID].append(remove)
        SSE = yield self.evaluate(V)
        self.assertWithinFivePercent(SSE, SSE_expected)


class CapacitorTestBase(TestCase):
    """
    @cvar CapacitorCircuit: A subclass, or reference to one, of
        C{Include}, constructed with node 'out' and possibly also 'v0'.
    """
    def setUp(self):
        self.avm = AV_Manager()
        self.n = Netlist(None, self.avm, ts=self.ts)

    def makeCircuit(self, *args, **kw):
        """
        Special test-only keyword I{N}: The number of times to repeat
        L{SillyCircuit}, in parallel.
        """
        nodes = ['out']
        with self.n() as f:
            if args:
                f.vav('v0', args[0])
                nodes.append('v0')
            N = kw.pop('N', 1)
            for k in range(N):
                self.sc = self.CapacitorCircuit(f, *nodes, **kw)
        self.lines = str(self.n).split('\n')
        if self.isVerbose():
            print
            for line in self.lines:
                print line
        return self.sc
    
    def av(self, *args, **kw):
        avMaker = AV_Maker(self.avm)
        av = avMaker.av(*args)
        for name in kw:
            setattr(av, name, kw[name])
        return av
    
    def tokenerator(self, pattern=None):
        continuations = []
        lines = list(self.lines[1:])
        while lines:
            line = lines.pop(0).strip()
            if not line or line.startswith('*') or line == '.END':
                continue
            tokens = line.split()
            while lines:
                if lines[0].startswith('+'):
                    tokens.extend(lines.pop(0)[1:].split())
                else: break
            if pattern:
                if not re.match(pattern, tokens[0]):
                    continue
            yield tokens

    def checkComponents(self, *refDes):
        """
        Checks that all the components whose reference designators are
        listed as arguments appear, and only those components, in no
        particular order.
        """
        rds = set([tokens[0].upper() for tokens in self.tokenerator()])
        if '.END' in rds: rds.remove('.END')
        print("First list is all the unique reference designators found:")
        self.assertEqual(sorted(rds), sorted(refDes))

    def checkTokens(self, *args):
        """
        Checks the component entry for the refDes specified as a first
        argument. Each token after the refDes must match each pattern
        that appears as additional arguments, in order.
        """
        entryList =  list(self.tokenerator(args[0]))
        self.assertEqual(len(entryList), 1)
        tokens = entryList[0]
        self.assertEqual(len(tokens), len(args))
        for k, token in enumerate(tokens):
            self.assertPattern(str(args[k]), str(token))

    def checkError(self, *nodes, **kw):
        with self.n() as f:
            self.assertRaises(
                capacitance.CapacitanceConfigError,
                SillyCircuit, f, *nodes, **kw)
