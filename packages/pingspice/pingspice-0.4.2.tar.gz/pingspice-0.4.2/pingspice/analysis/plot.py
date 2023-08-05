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
Plotting simulated vs. expected device curves.
"""

import os, os.path, sys, math
from cStringIO import StringIO

import numpy as np
from yampex import plot

from pingspice.util import *


class Stylist(object):
    """
    L{Plotter} uses an instance of me to color simulation lines (or
    dots) and goal points for one subplot.

    @keyword linePlot: Set C{True} if the plot has lines instead of
        dots.
    
    @cvar colors: A sequence of 2-tuples, each with a simulation color
        and goal point ("x") color.
    """
    colors = (
        ('b', 'g'),
        ('r', 'c'),
        ('m', 'y'),
        ('darkgoldenrod', '#ff7f0e'))

    __slots__ = ['linePlot', 'kList']
    
    def __init__(self, linePlot=False):
        """
        C{Stylist(linePlot=False)}
        """
        self.linePlot = linePlot
        self.kList = [-1, -1]

    def _kNext(self, kWhich):
        """
        Returns the index of the next simulation line or dots
        (I{kWhich}=0) or of the next goal points (I{kWhich}=1).
        """
        k = self.kList[kWhich] = (self.kList[kWhich] + 1) % len(self.colors)
        return k
    
    def sc(self):
        """
        Returns the next simulation color.
        """
        return self.colors[self._kNext(0)][0]

    def xc(self):
        """
        Returns the next goal point color.
        """
        return self.colors[self._kNext(1)][1]

    def doSettings(self, dots=False, bigger=False):
        """
        Returns a dict with kw settings for the next simulation plot and
        another dict for its goal points.

        @keyword dots: Set C{True} to draw dots. Implied if my
            I{linePlot} attribute is not set.

        @keyword bigger: Set C{True} for bigger markers.
        """
        kws = {'color': self.sc()}
        kwx = {
            'marker': 'x',
            'markersize': 4.0 if bigger else 3.0,
            'linestyle': '',
            'color': self.xc()
        }
        if self.linePlot:
            if dots:
                # Lines with small dots
                kws['marker'] = '.'
                kws['markersize'] = 2.0 if bigger else 1.5
        else:
            # Dots only (except faint connecting lines)
            kws['marker'] = '.'
            kws['linestyle'] = 'dotted'
            kws['linewidth'] = 0.5
            kws['markersize'] = 4.0 if bigger else 3.0
        return kws, kwx
    

class Data(object):
    """
    I offer ways of getting goal and simulated data from L{Run}
    objects.

    Construct me with a set (perhaps empty) of canonical names of
    vectors with log values. I'll convert those to linear space
    whenever you access them with a call to L{getValue}.
    """
    noLimits = False
    fracExtra = 0.05

    def __init__(self, logValues):
        """
        C{Data(logValues)}
        """
        self.logValues = logValues

    def setup(self, run):
        """
        Sets up my instance with data from a new L{Run} object I{run}.

        Returns the length of the column vectors in my I{X} goals
        array. (Not the number of columns.)
        """
        self.X = run.X
        self.V = run.V
        self.nameList = run.nameList
        return run.X.shape[0]
    
    def getValue(self, container, name, k=None):
        """
        With a C{analysis.sim.Vectors} instance and a vector I{name},
        returns the simulation vector, log-transformed if the name
        is in my L{Plotter} object's I{logValues} set.

        With a 2-D goal points array, a vector I{name}, and a
        column index I{k}, returns a 1-D array of goal points for
        that vector. No log transformation is done because
        C{analysis.param.Setups} does that at the outset when
        preparing its I{X} array.

        @keyword k: Set to the index of a column of the I{container}
            (only for an array) to select just a single column vector.
        """
        if k is None:
            value = container[name]
            if name in self.logValues:
                value = np.log10(value)
        else: value = container[:,k]
        return value

    def getLimits(self, X, Xmin, Xmax):
        """
        Returns a 1-D Numpy array of indices for items in the supplied
        vector I{X} that are inside or just a little bit outside the
        limits specified with I{Xmin} and I{Xmax}.
        """
        Xd = Xmax - Xmin
        Xmin -= self.fracExtra*Xd
        Xmax += self.fracExtra*Xd
        return np.flatnonzero(np.logical_and(X >= Xmin, X <= Xmax))
    
    def maybeNegative(self, name):
        """
        Returns the sign of I{name} with its sign character "-" (if any)
        stripped off.
        """
        if name.startswith('-'):
            return -1, name[1:]
        return +1, name

    def vector(self, name, K=None):
        """
        Returns a subset of items of the simulation vector with the
        specified I{name}.

        If an index array I{K} is supplied, selects the subset of the
        vector with those indices.

        If I{name} is preceded by a "-" character, the values will be
        inverted, i.e., negated.
        """
        sign, name = self.maybeNegative(name)
        Z = sign * self.getValue(self.V, name)
        if K is not None: Z = Z[K]
        return Z
    
    def goal(self, name, K=None):
        """
        Returns a subset of items of the column vector in my goal array
        I{X} for the current run corresponding to the specified
        I{name}, with items (optionally) selected by index array I{K}.

        The I{name} is looked up in my I{nameList} for the current run
        and the position where the name appears is used as the column
        index.
        """
        sign, name = self.maybeNegative(name)
        if name not in self.nameList:
            raise ValueError(
                sub("Trying to plot unknown vector '{}'", name))
        k = self.nameList.index(name)
        shape = self.X.shape
        if len(shape) > 1 and k < shape[1]:
            Z = sign * self.getValue(self.X, name, k)
            return Z if K is None else Z[K]
        import pdb; pdb.set_trace() 
        raise IndexError("WTF?")


class Subplotter(object):
    """
    Call an instance of me for each setup subplot.
    """
    Nmax_for_dots = 25
    Nmax_goals_for_bigger = 120
    reBranch = re.compile(r'([^\#]+)\#branch')

    def __init__(self, sp, logValues):
        self.sp = sp
        self.data = Data(logValues)

    def psVectorName(self, text):
        """
        Returns a prettified and standardized version of any Ngspice
        vector names in the supplied text.
        """
        newParts = []
        for part in text.split():
            match = self.reBranch.match(part)
            if match:
                part = "I({})".format(match.group(1))
            else: part = re.sub(r'^v\(', 'V(', part)
            newParts.append(part)
        return " ".join(newParts)
        
    def set_xAxis(self, xName):
        name = xName.lstrip('+')
        if name in ('time', 'ttrig'):
            self.sp.use_timex()
        elif name == 'charge':
            self.sp.opts['xscale'] = 1E9
            self.sp.opts['xlabel'] = "nC"

    def useBigger(self, Xg):
        """
        Returns C{True} if there are few enough goal points in the x-axis
        vector of goal points I{Xg} on a big enough subplot that
        bigger markers should be used.
        """
        # TODO: Account for tightest point spacing
        N = len(Xg)
        return N < self.Nmax_goals_for_bigger / self.sp.Nc

    def subseterator(self, xName):
        """
        Yields indices of each monotonically increasing portion of the
        independent vector I{xName} of my I{data}.

        @see: L{IV_Manager.subseterator} for a cousin of this method
            used for enumerable non-callable goals.
        """
        data = self.data
        X = self.data.vector(xName)
        Kr = np.concatenate([np.flatnonzero(np.diff(X) < 0)+1, [len(X)]])
        k0 = 0
        for k1 in Kr:
            yield np.arange(k0, k1)
            k0 = k1
    
    def plot(self, ax, xName, yNames, Ksim, Kg, lines=False, dots=False):
        """
        Plots x-axis and y-axis values of simulation output and goal
        points from the I{data} identified by I{xName} and
        I{yNames}.

        The I{xName} identifies the vector in goal array I{X} and
        L{Vector} object I{V} of I{data} to use for the x-axis. The
        I{yNames} is a sequence identifying the vector(s) in I{X} and
        I{V} to use for the y-axis.

        I{Ksim} is a 1-D array of indices of selected simulated values
        to plot.

        I{Kg} is a 1-D array of indices of selected goal values
        to plot, or C{None} if no goal values are to be plotted.
        """
        data = self.data
        Xsim = data.vector(xName, Ksim)
        have_Kg = Kg is not None and len(Kg)
        if have_Kg:
            Xg = data.goal(xName, Kg)
            K = data.getLimits(Xsim, Xg.min(), Xg.max())
            Xsim = Xsim[K]
            useBigger = self.useBigger(data.goal(xName))
        else: useBigger = False
        st = Stylist(lines)
        for k, yName in enumerate(yNames):
            Ysim = data.vector(yName, Ksim)
            if have_Kg:
                Ysim = Ysim[K]
                Yg = data.goal(yName, Kg)
            kws, kwx = st.doSettings(dots=dots, bigger=useBigger)
            ax.plot(Xsim, Ysim, **kws)
            if have_Kg:
                ax.plot(Xg, Yg, **kwx)
            
    def __call__(self, ID, run, *args):
        """
        Call my instance with a setup I{ID} and a L{Run} instance I{run}
        from a simulation for that setup to plot simulated vs
        expected, unless there's no plotSpec for this setup.

        B{Note:} Not concurrency-safe, because my I{data} object gets
        setup for one I{run} at a time. That's not a problem, because
        this method doesn't yield, and you shouldn't be haphazardly
        using threads with Twisted.
        """
        text = sub("SSE={:.2f}", float(run.SSE))
        args = list(args)
        if args:
            title = sub("{:d}: {}, {}", ID, args.pop(0), text)
        else: title = sub("{:d}, {}", ID, text)
        self.sp.set_title(self.psVectorName(title))
        if not args:
            text = sub("{:d}: {}", ID, text)
            ax = self.sp()
            ax.text(
                0.5, 0.5, text,
                horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes)
            return
        xName = args.pop(0)
        self.set_xAxis(xName)
        Ng = self.data.setup(run)
        yNames = list(args)
        for yName in yNames:
            self.sp.add_legend("{} (sim)", yName)
            if Ng: self.sp.add_legend("{} (goal)", yName)
        ax = self.sp()
        ivm = run.evalSpec.ivm
        Ysim = self.data.V.array()
        if Ysim is None:
            # Shouldn't happen!
            import pdb; pdb.set_trace()
        Nsim = Ysim.shape[0]
        lines = Nsim > self.Nmax_for_dots
        dots = Nsim < 2*self.Nmax_for_dots
        if ivm.noEnumerables() or ivm.kInterp is None:
            Kg = np.arange(Ng)
            # X-axis vector may retrace, with multiple curves. Plot
            # one curve (or the only curve) at a time. Because goal
            # points don't have lines, they can all be plotted with
            # the first curve.
            for Ksim in self.subseterator(xName):
                self.plot(ax, xName, yNames, Ksim, Kg, lines, dots)
                # No more goal point plotting
                Kg = None
            return
        for kCol in ivm.enumerableator():
            for Kg, Ksim in ivm.subseterator(kCol, kCol, run.X, kCol, Ysim):
                self.plot(ax, xName, yNames, Ksim, Kg, lines, dots)


class Plotter(object):
    """
    I plot simulation curves vs goal points.

    @keyword sp: Supply a C{yampex.Plotter} object in subplot context
        instead of having me construct a Plotter and create that
        context. For unit testing only.
    """
    defaultFilePlotDims = (1900, 1200)

    sizes = ('medium', 'small', 'x-small', 'xx-small')
    fontsizes = (
        ('title', 0), ('xlabel', 0), ('legend', 1), ('annotation', 1))

    def __init__(
            self, plotSpecs, logValues, plotFile=None, dims=None, sp=None):
        """
        C{Plotter(plotSpecs, logValues, plotFile=None, dims=None, sp=None)}
        """
        self.plotSpecs = plotSpecs
        self.logValues = logValues
        N = len([ID for ID in plotSpecs.keys() if plotSpecs[ID]])
        if plotFile and dims is None:
            dims = self.defaultFilePlotDims
        self.sp = sp
        if sp is None:
            self.pt = plot.Plotter(N, filePath=plotFile, figSize=dims)
            self.pt.add_line('-', 1)
            self.pt.set_zeroLine()
            Nr = self.pt.Nr
            kMax = len(self.sizes) - 1
            k0 = 0 if Nr < 3 else 1 if Nr < 5 else 2
            if dims and dims[0]*dims[1] < 1E6: k0 += 1
            for name, k in self.fontsizes:
                k += k0
                if k > kMax: k = kMax
                self.pt.set_fontsize(name, self.sizes[k])
        else: self.pt = None

    def _plot(self, sp, result):
        subplotter = Subplotter(sp, self.logValues)
        for ID, run in result:
            if ID in self.plotSpecs:
                plotSpec = self.plotSpecs[ID]
                if plotSpec:
                    subplotter(ID, run, *plotSpec)
        
    def __call__(self, result):
        """
        Call with an instance of L{sse.Result} to plot the results vs goal
        points.
        """
        if self.sp is None:
            if hasattr(result, 'description'):
                self.pt.set_title(result.description)
            with self.pt as sp:
                self._plot(sp, result)
            # Done with all vectors for all subplots
            self.pt.show()
        else: self._plot(self.sp, result)


        
