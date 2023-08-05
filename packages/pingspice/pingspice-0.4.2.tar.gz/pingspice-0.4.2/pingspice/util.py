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
Generally useful stuff that's referenced by most modules of
L{pingspice}. Highlights:

    - The L{sub} function really should be a built-in function. Once
      you start using it, you'll never go back to C{format}.

    - The L{Config} object holds global Boolean configuration
      options. There are actually quite a few of them, and you'll
      probably refer to this a lot.

    - The C{msg} instance of the U{ade<http://edsuom.com/ade.html>}
      package's
      U{Messenger<http://edsuom.com/ade/ade.util.Messenger.html>}
      object provides a very convenient and flexible way to put
      messages onto a log file, file-like object, or STDOUT.

    - The L{oops} function is a handy universal errback to tack onto a
      C{Deferred}.

    - The L{tempfile} function creates the directory for or removes a
      temporary file using a module-level instance of
      L{TempfileManager}, which tries to delete all its files when
      Python shuts down.

    - Construct a L{Formatter} instance for a few methods that ensure
      your node names conform with Ngspice canonical format and your
      values are all strings with Booleans converted to "1" or "0".
"""

import time, re, sys, os.path, shutil
from tempfile import mkdtemp

import numpy as np
from twisted.python import failure
from twisted.internet import threads

from errors import *

MAX_LINE_LENGTH = 120

# Netlist aesthetics
DASHES_MAIN = 79
DASHES_SUBCKT = 76
DASHES_INCLUDE = 74


from ade.util import Messenger, Args
msg = Messenger()

from textwrap import TextWrapper
fill = TextWrapper(width=MAX_LINE_LENGTH, break_on_hyphens=False).fill

# Use this in place of 0 for a short-circuit resistance, because
# Ngspice makes 0 into 1e-3
RMIN = 1e-22


def brace(proto, *args):
    """
    Does a sub of I{proto} and I{args} and returns the result wrapped
    in braces ("{x}").
    """
    text = sub(proto, *args)
    return sub("{{{}}}", text)

def npr(x, y, *args, **kw):
    """
    Returns the args, except with the first two reversed if keyword
    I{reverse} is set C{True}.
    """
    newArgs = [x, y] + list(args)
    if kw.get('reverse', False):
        x = newArgs[0]
        newArgs[0] = newArgs[1]
        newArgs[1] = x
    return newArgs

def notseq(x):
    """
    Returns C{True} if I{x} is not a sequence.
    """
    return not hasattr(x, '__iter__')

def plural(word, obj):
    if hasattr(obj, '__iter__'):
        obj = len(obj)
    if obj > 1:
        word += "s" 
    return word

def tryCall(f, *args, **kw):
    """
    Tries running C{f(*args, **kw}), returning the result. Drops to
    the debugger if the call results in an error.
    """
    try:
        return f(*args, **kw)
    except:
        import sys, traceback, pdb
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(
            exc_type, exc_value, exc_traceback, file=sys.stdout)
        pdb.post_mortem(exc_traceback)

def oops(failureObj, log=None, keepGoing=False):
    """
    A handy universal errback.

    Prints or logs the failure's error message and then, unless
    I{keepGoing} is set C{True}, stops everything so you can figure
    out what went wrong.
    """
    def text():
        if isinstance(failureObj, failure.Failure):
            info = failureObj.getTraceback()
        else: info = str(failureObj)
        return sub("Failure:\n{}\n{}", '-'*40, info)
    
    if log is None:
        print(text())
    elif isinstance(failureObj, failure.Failure):
        log.failure(sub("Failure:\n{}\n", '-'*40), failureObj)
    else: log.failure(text())
    if keepGoing: return
    #import pdb, traceback, sys
    #type, value, tb = sys.exc_info()
    #pdb.post_mortem(tb)
    from twisted.internet import reactor
    if reactor.running:
        # I know, I know...
        reactor.crash()

def deferToThread(f, *args, **kw):
    """
    Call this with a callable I{f} and any I{args} or I{kw} it takes
    to have it run in a dedicated worker thread. Returns a C{Deferred}
    that fires with the eventual result.
    """
    return threads.deferToThread(f, *args, **kw)


class Formatter(object):
    """
    I provide a few methods that ensure your node names conform with
    Ngspice canonical format and your values are all strings with
    Booleans converted to "1" or "0".

    You can specify a numbered node with "v" (or "V") followed
    immediately by the number and that will be converted to
    V(<number>). For example,::

        v5 -> V(5)

    That is especially useful for specifying numbered nodes in
    keywords or attribute names, since you can't use numbers or
    parentheses in those cases.

    Since a number as a node name cannot be anything but equivalent to
    'V(xxx)' where 'xxx' is the number, you might think that supplying
    just a number will convert to that. But, due to the way Ngspice
    parses the name, that doesn't work. It wouldn't be a good practice
    to just use the integer digits, anyhow, as that couldn't work
    for specifying a numbered nodes in keywords or attribute names.

    Vector or node names are converted to lowercase, except for the
    "V" in those specified in (or converted to) "V(<name>)" format.
    """
    reNumberedNode = re.compile(r'[vV]([0-9]+)$')
    fill = TextWrapper(
        width=79, subsequent_indent="+ ",
        break_on_hyphens=False, break_long_words=False).fill

    def sanitize(self, value):
        """
        Ultimately, all space-delimited tokens, array values, and wrapped
        arguments and keywords get run through this function.
        """
        if isinstance(value, (list, tuple)):
            return "[ " + " ".join([self.sanitize(x) for x in value]) + " ]"
        if isinstance(value, bool):
            return "1" if value else "0"
        return str(value)

    def toTokens(self, *args):
        """
        Returns a list of string tokens from the supplied arguments. Blank
        strings and C{None} objects are ignored and L{Wrapper} objects are
        parsed into strings.
        """
        tokens = []
        for arg in args:
    	    if arg is None or arg == '':
    	        continue
            arg = arg() if callable(arg) else self.sanitize(arg)
    	    tokens.append(arg)
        return tokens

    def toCanonical(self, name):
        """
        Ensures that the supplied vector or node I{name} is in
        Ngspice-canonical format.
        """
        def matchSub(proto):
            return proto.format(match.group(1).lower())

        name = name.lstrip('+')
        match = self.reNumberedNode.match(name)
        if match:
            return matchSub("V({})")
        if name.startswith('V('):
            return "V(" + name[2:].lower()
        return name.lower()

    def prettify(self, text):
        """
        For removing ugly superfluous junk from a netlist line and
        wrapping with continuation lines if necessary.
        """
        text = re.sub(r'([^\-])--([^\-])', r'\1+\2', text)
        return self.fill(text)


class Bag(object):
    """
    Use an instance of me to let functions within methods have easy
    access to stuff defined in the main method body.
    """
    # TODO: Why was this commented out? A single slot would make sense here!
    #__slots__ = ['x']
    
    def __init__(self, initialValue=None):
        self.x = initialValue

    def __nonzero__(self):
        return bool(self.x)

    def pop(self):
        """
        Reverts my I{x} to its default C{None} starting value and returns
        the value it had.
        """
        x = self.x
        self.x = None
        return x

    def increment(self):
        """
        If my I{x} attribute is an int or float, adds one to its value and
        returns the new value.

        If I{x} cannot be incremented, an exception is raised.
        """
        self.x += 1
        return self.x
    
    def __call__(self, *args):
        """
        Call this with the new value of I{x} as the first (possibly only)
        argument. If there are no arguments, I{x} remains
        unchanged. In either case, the ending value is returned.
        """
        if args:
            self.x = args[0]
        return self.x


class TempfileManager(object):
    """
    I manage temporary files in my temporary file subdirectory,
    attempting to remove all the ones I've created when Python shuts
    down.

    @cvar prefix: The prefix for all temp files.
    @type prefix: str
    
    @ivar tempDir: The subdirectory where I keep all of my temporary
        files, creating it if necessary.
    @type tempDir: str

    @ivar filePaths: Full paths of temp files registered for deletion
        when Python shuts down.
    @type filePaths: set
    """
    prefix = "pingspice-"
    
    def __init__(self):
        """
        C{TempfileManager()}
        """
        # Make the new temp directory
        self.tempDir = mkdtemp(prefix=self.prefix)
        # Create an empty set of temp file paths
        self.filePaths = set()

    def __del__(self):
        """
        Removes my temp directory and all files in it when my instance
        gets deleted.
        
        This should work consistently, so long as you never construct
        your own instance of me. Do everything through the L{tempfile}
        function.
        """
        self.rm()

    def new(self, ext, keep=False):
        """
        Generates and returns a new, unique temporary file path, given the
        supplied extension (a string beginning with or lacking a dot).
        
        The file path will be in my temp directory, which I create if
        necessary. Creating the actual temp file is up to you, though
        I will delete it when Python shuts down or if you call L{rm}
        with the file path. (Set the I{keep} keyword True to prevent
        that deletion from happening.)
        """
        k = 1
        while True:
            fileName = sub("pingspice-{:04d}.{}", k, ext.lstrip('.'))
            filePath = os.path.join(self.tempDir, fileName)
            if os.path.exists(filePath):
                k += 1
                continue
            if not keep: self.filePaths.add(filePath)
            return filePath
        
    def rm(self, filePath=None, register=False):
        """
        Call with a I{filePath} to delete a single specified file,
        immediately unless I{register} is set C{True}. In that case,
        registers the file path for deletion when Python shuts down.
        
        Call with nothing to immediately delete all registered files.
        """
        if filePath is None:
            while self.filePaths:
                os.remove(self.filePaths.pop())
            if os.path.exists(self.tempDir):
                shutil.rmtree(self.tempDir, True)
            return
        if register:
            self.filePaths.add(filePath)
        elif filePath in self.filePaths:
            self.filePaths.remove(filePath)
            if os.path.exists(filePath):
                os.remove(filePath)
_tfm = TempfileManager()

def tempfile(text, register=False, keep=False):
    """
    Creates the directory for or removes a temporary file using a
    module-level instance of L{TempfileManager}, which tries to delete
    all its files when Python shuts down.
    
    Call with the full path of a temporary file generated during this
    Python session and it gets deleted, unless the I{register} keyword
    is set C{True}. In that case, the full path gets registered for
    deletion when Python shuts down.

    Call with an extension (a string beginning with or lacking a dot)
    and a unique temp file path is returned with that extension, in
    the temp directory (newly created if necessary). Unless the
    I{keep} keyword is set C{True}, any file created at that path will
    be deleted when Python shuts down.
    """
    if '_tfm' not in globals(): return
    if '.' not in text.lstrip('.'):
        return _tfm.new(text, keep)
    _tfm.rm(text, register)
    

class SlotPickleMixin(object):
    """
    Copied from
    http://code.activestate.com/recipes/
    578433-mixin-for-pickling-objects-with-__slots__/
    """
    def __getstate__(self):
        return dict(
            (slot, getattr(self, slot))
            for slot in self.__slots__
            if hasattr(self, slot)
        )

    def __setstate__(self, state):
        for slot, value in state.items():
            setattr(self, slot, value)


class _Debug(object):
    debugMode = False
    @classmethod
    def _msg(cls, *args):
        if not args:
            return cls.debugMode
        if len(args) == 1:
            if isinstance(args[0], bool):
                cls.debugMode = args[0]
                return
        if cls.debugMode:
            msg(*args)
MSG = _Debug()._msg


class Config(object):
    """
    I hold a set of Boolean configuration options for an entire
    pingspice run. Request an option as an attribute. The value will
    be C{False} if not set.

    @ivar quiet: Prevents logging or printing anything. Overrides
        I{verbose}, I{chatty}, I{spew}, and I{hardcore}.
    
    @ivar verbose: Prints a small amount of Ngspice status output.

    @ivar chatty: Prints a bit more status output than normal.

    @ivar spew: Include details about STDIO communiction with Ngspice
        (for pingspice debugging.)

    @ivar hardcore: Include an insane amount of details about STDIO
        communiction with Ngspice (for increasingly rare in-depth
        pingspice debugging.)

    @ivar nodes: Log info about the nodes connected for each
        L{Include} and L{Subcircuit} constructed for analysis. Default
        is C{False}, because this can result in a lot of info clogging
        up your logs.
    
    @ivar console: Drop to a primitive console upon an Ngspice error,
        for netlist debugging.

    @ivar source: Prints the original source (without any
        alterations).
    
    @ivar study: If using an analyzer, have it create a netlist file
        for study upon an Ngspice error.

    @ivar study_stop: Exit after creating a netlist file
        for study.

    @ivar study_best: Have L{Solver} write a netlist file for each
        setup of the best parameter combination reported to it.
    
    @ivar devel: If using an analyzer, have it create a netlist for
        study after B{every} analysis, unless a netlist file is
        already there for that setup. This is intended for development
        purposes.

    @ivar keep: If using an analyzer, have it set the 'keep'
        pingspice-only simulation option to keep any files generated
        for the netlist. Implied by I{study} and I{study_best} and the
        options that imply those options, I{devel} and I{study_stop}.
    
    @ivar warn_err: Consider warnings to be errors (for development
        purposes).
    
    @ivar fail: Where a C{Deferred} is awaiting a result, run
        its errback upon an Ngspice error.

    @ivar stop: Stop everything upon an Ngspice error.

    @ivar waitmsg: Include a "WAITING..." message and follow-up
        "DONE..." when Ngspice is taking a while.

    @ivar full: Have Ngspice save a full suite of all its simulation
        vectors (can take up a I{lot} of RAM).

    @ivar et_sse: Have L{evaluate} return an instance of
        L{ErrorTabulator} as the SSE instead of a float. This works
        the same since it will evaluate as a float, and there's no
        performance penalty. (Speed is the same!) Allows you to see
        details about any significant inconsistency between SSE
        reported and the SSE that L{Solver} recomputes, which should
        never happen now that all the lock/release has finally been
        figured out.

    @ivar xsse: Set C{True} to abort an evaluation if the challenger's
        SSE exceeds the target SSE. Can speed things up if your
        paramfinder has very slow setups numbered higher than faster
        ones.

    @ivar debug: Force single-core, no-wire operation and write every
        line of STDIN, STDOUT, and STDERR to text files STDIN.log,
        STDOUT.log, and STDERR.log. Obviously, for debugging only.
    """
    optNames = {
        # Verbosity
        'quiet', 'verbose', 'chatty', 'spew', 'hardcore', 'nodes',
        # Actions to take on Ngspice error
        'console', 'study', 'study_stop', 'fail', 'stop', 'warn_err',
        # Simulation options
        'waitmsg', 'full', 'et_sse', 'xsse',
        # Study options
        'source', 'devel', 'study_best', 'keep', 'debug',
    }
    impliedBy = {
        # Not recursive: Everything that implies an option, even
        # indirectly, must be listed in that option's entry
        'verbose':      ('chatty', 'spew', 'hardcore', 'et_sse',),
        'chatty':       ('spew', 'hardcore',),
        'spew':         ('hardcore',),
        'study':        ('devel', 'study_stop',),
        'keep':         ('study', 'devel', 'study_stop', 'study_best',),
    }
    
    def __init__(self, *args, **kw):
        """
        C{Config(enabledSet)} or C{Config(**kw)}
        """
        if len(args) == 1 and isinstance(args[0], set):
            self.enabled = args[0].copy()
            return
        self.enabled = set()
        self.enable(*args)
        for name in kw:
            if kw[name]: self.enable(name)

    def __repr__(self):
        enabled = sorted([
            name for name in self.optNames if self.isEnabled(name)])
        namesEnabled = ", ".join(enabled) if enabled else "--"
        return sub("Config at {}: {}", hex(id(self)), namesEnabled)
            
    def __getstate__(self):
        return {'enabled': self.enabled}

    def __setstate__(self, state):
        self.enabled = state['enabled']

    def isEnabled(self, name):
        """
        Returns C{True} if the named option is enabled, directly or by
        implication.
        """
        self.check(name)
        yesno = name in self.enabled
        if yesno or name not in self.impliedBy:
            return yesno
        for implier in self.impliedBy[name]:
            if implier in self.enabled:
                return True
        return False

    def __getattr__(self, name):
        return self.isEnabled(name)

    def copy(self):
        """
        Returns a copy of me with the same options enabled as I currently
        have. If you change any of my options, it does not affect
        those of the copy, and vice-versa.
        """
        return Config(*self.enabled)
    
    def check(self, name):
        """
        Raises an exception if I{name} is not one of my options.
        """
        if name not in self.optNames:
            raise AttributeError(sub("Unknown config option '{}'", name))
    
    def any(self, *args):
        """
        Returns C{True} if any of the named options are enabled, directly
        or by implication.
        """
        for name in args:
            self.check(name)
            if self.isEnabled(name):
                return True
        return False

    def all(self, *args):
        """
        Returns C{True} if B{all} of the named options are enabled, directly
        or by implication.
        """
        for name in args:
            self.check(name)
        return set(args) <= self.enabled

    def none(self, *args):
        """
        Returns C{True} if B{none} of the named options are enabled, directly
        or by implication.
        """
        return not self.any(*args)
    
    def enable(self, *names):
        """
        Enables all of the options named as arguments, first checking that
        they are in fact the valid names of options.
        """
        for name in names:
            self.check(name)
            self.enabled.add(name)
        return self

    def disable(self, *names):
        """
        Disables all of the options named as arguments, first checking
        that they are in fact the valid names of options.
        """
        for name in names:
            self.check(name)
            self.enabled.discard(name)
        return self
