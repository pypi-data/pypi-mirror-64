#!/usr/bin/env python
#
# Tutorial for pingspice:
# Object-oriented circuit construction and efficient asynchronous
# simulation with Ngspice and Twisted.

"""
Example: Exploring properties of a JFET as current limiter
"""

import numpy as np
from twisted.internet import reactor, defer

from yampex.plot import Plotter

from pingspice.circuit.netlist import Include, Netlist
from pingspice.analysis.msim import MultiRunner
from pingspice.util import sub, oops, msg, Config


class CurrentLimiter(Include):
    """
    I represent a simple current limiter using a JFET and a tiny
    shunt resistance Rs.

    Per Siliconix App Note AN103 (1997-03-10), the value of Rs to
    limit current to Imax is approximately
    M{-VTO/Imax*(1-sqrt(Imax/Idss))}. Idss is I(Vgs=0), which is 2-4
    times BETA when there is any significant current limiting
    happening. "For best regulation, [Imax] must be considerably less
    than Idss."

    So, if M{Idss=2*Imax} and M{BETA=Idss/2}, set BETA=Imax. But I set
    it a bit higher than that, M{2*Imax}.

    I introduce the following alterable values into the circuit in
    which I am included:

        - B{slope}: A channel-length modulation parameter for the JFET
          that reduces how drastic the current limiting eventually
          gets. Basically, a slope limiter for the voltage vs. current
          curve after limiting starts.

        - B{shunt}: The shunt resistance.

    @ivar Imax: Maximum current, the point where I really start
        dissipating power to limit amperage.
    """
    def setup(self, f, pos, neg):
        """
        Conventional current flow is from my I{pos} (more positive)
        terminal into me and then out my I{neg} (more negative)
        terminal.
        """
        Im = self.Imax
        limiter = f.MODEL(
            'limiter', 'njf',
            BETA=Im*2, VTO=f.av('vto', -1.2, -1.0),
            LAMBDA=f.av('slope', -2, -1, 'log'))
        f.J(pos, neg, 110, limiter)
        f.R(110, neg, 0.4/Im)


class CircuitAnalyzer(object):
    """
    I construct a simple test circuit using the L{CurrentLimiter} and
    a DC Analyzer to analyzer it.

    Call my L{setup} to get me setup for trying out different values
    of I{gain}, I{limit}, and I{transition}.

    @ivar verbose: Set C{True} to log/print details about Ngspice's
        operations.
    """
    nodes = ['V(10)', 'V(20)']
    
    def __init__(self, verbose=False, study=False):
        cfg = Config(hardcore=verbose, devel=study)
        self.mr = MultiRunner(cfg)

    def setup(self, Imax):
        """
        Sets me up with a current limiter set to the maximum current
        I{Imax}.

        Returns a Deferred that fires when my instance is ready to
        call with I{gain}, I{limit}, and I{transition} values, with an
        C{OrderedDict} of min,default,max for those values.
        """
        def func(f):
            CurrentLimiter(f, 10, 20, Imax=Imax)
            f.R(10, 20, 1E3)
            f.Isrc(0, 10, DC=1)
            f.R(20, 0, 1.0)

        def done(ID):
            self.ID = ID
            return self.mr.params(ID)

        args = ['Isrc', 0.7*Imax, 1.4*Imax, 1]
        d = self.mr.newSetup(func, self.nodes, 'DC', *args)
        d.addCallback(done)
        return d

    def __call__(self, *values):
        """
        Call with values for I{gain}, I{limit}, and I{transition}.

        Returns a C{Deferred} that fires with (1) swept input current
        from 0 to 20% greater than my current limiter's maximum, and
        (2) the current limiter's effective resistance over the swept
        current range.

        You B{can} call this concurrently. In fact, the L{MultiRunner}
        is intended for that very purpose! If there are more pending
        requests for simulation output than the number of Ngspice
        simulators running, the request will be queued up and serviced
        in turn.
        """
        def gotV(V):
            Vin = V['V(10)']
            Vout = V['V(20)']
            return Vout, (Vin-Vout)/Vout
        return self.mr.run(self.ID, values).addCallback(gotV)
    

class Runner(object):
    """
    @cvar details: Set C{True} to see what happens on STDIO between
        Python and Ngspice.
    """
    details = False
    Imax = 100.0

    def __init__(self):
        msg(True)
        self.ca = CircuitAnalyzer(self.details)

    @defer.inlineCallbacks
    def _run(self):
        defaults = yield self.ca.setup(self.Imax)
        p = Plotter(len(defaults))
        p.use_grid()
        p.set_ylabel("mOhms")
        p.set_xlabel("Amps")
        with p as sp:
            for k, name in enumerate(defaults):
                dList = []
                sp.set_title("Effect of Parameter '{}'", name)
                sp.add_axvline(float(self.Imax))
                for otherName in defaults:
                    if otherName != name:
                        sp.add_textBox(
                            "NW", "{} = {:.3f}",
                            otherName, defaults[otherName][1])
                values = [defaults[x][1] for x in defaults]
                low, default, high = defaults[name]
                for kk, value in enumerate(np.linspace(low, high, 5)):
                    values[k] = value
                    dList.append(self.ca(*values))
                    sp.add_legend("{:.3f}", value)
                IRs = yield defer.gatherResults(dList)
                sp(IRs[0][0], *[1000*x[1] for x in IRs])
        p.show()
        reactor.stop()

    def run(self):
        """
        Runs ... in a non-blocking asynchronous manner and using several
        separate Ngspice processes running in parallel.

        Does a subplot of each result and exits when the plot is
        closed.

        This is all accomplished by calling my L{_run} method, with an
        error callback added to the resulting C{Deferred} object. This
        is good Twisted programming practice to deal with the
        inevitable errors that occurr during program development.
        """
        return self._run().addErrback(oops)


# Set up things to run under control of Twisted's reactor
reactor.callWhenRunning(Runner().run)
# Start Twisted's reactor and everything goes from there
reactor.run()

        



