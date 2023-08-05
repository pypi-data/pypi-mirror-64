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
Evaluation over the wire.
"""

from twisted.internet import reactor, defer

from asynqueue.wire import p2o, WireWorkerUniverse

from pingspice.analysis.evaluate import Evaluator
from pingspice.util import msg


class WireEvaluator(WireWorkerUniverse):
    """
    I am a universe for a WireWorker that sets up its own remote
    Evaluator and computes the SSE of parameter values.

    Once L{setup} is done, the communication over the wire is very
    efficient, with just a sequence of values going one way and a
    single float value returning the other.
    """
    def setup(self, cfg, N_cores=1, skipIDs=[]):
        """
        After sending an L{analysis.param.Setups} object via pickle
        chunks, call this once via a C{WireWorker.update} to setup my
        L{Evaluator} object I{ev}.

        Returns a C{Deferred} that fires when I{ev} has been setup.

        @see: L{Solver.setup}.
        """
        setups = p2o(self.pickleString)
        del self.pickleString
        self.ev = Evaluator(
            cfg,
            setups.avList,
            setups.transforms, setups.logValues, N_cores=N_cores)
        return self.ev.setup(
            setups.nameLists,
            setups.analyzers,
            setups.Xs,
            setups.netlists,
            setups.independents,
            setups.weights,
            skipIDs
        )

    def send_chunk(self, chunk):
        """
        Call this as many times as needed with chunks of a pickled
        L{analysis.param.Setups} object to build up my
        I{pickleString}, in preparation for a call to L{setup}.

        @see: L{Solver.setup}.
        """
        if not hasattr(self, 'pickleString'):
            self.pickleString = ""
        self.pickleString += chunk
            
    def shutdown(self):
        """
        Call this to shut down my L{Evaluator} and then stop my
        C{WireServer}.

        @see: L{Solver.shutdown}.
        """
        def done(null):
            reactor.callLater(0.1, self.ws.stop)
        if hasattr(self, 'ev'):
            return self.ev.shutdown().addCallback(done)
        return defer.succeed(None)
    
    def evaluate(self, values, ID, xSSE):
        """
        Call this with a sequence of alterable I{values}, a setup I{ID},
        and a target SSE I{xSSE} to obtain the SSE of that setup for
        those values.

        If I{xSSE} is not C{None}, an SSE greater than I{xSSE} will
        only be accurate to the extent that it exceeds I{xSSE} and
        thus a challenge based on the evaluation would fail.
        """
        return self.ev.evaluateSSE(values, ID, xSSE)
