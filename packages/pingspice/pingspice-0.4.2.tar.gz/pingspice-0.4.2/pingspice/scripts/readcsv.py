#!/usr/bin/python

import sys, os.path

import numpy as np
from scipy import signal, interpolate, stats

from yampex.plot import Plotter

from pingspice.util import *

"""
Reads CSV files from a dual-channel BK oscilloscope.

(You'll never guess what kind of oscilloscope I use...)
"""

class Filter(object):
    N = 31
    _dither = None
    
    def __init__(self, fc, dither):
        if fc < 1.0:
            self._dither = dither
            self.b = signal.firwin(self.N, fc)
            self.bd = signal.firwin(self.N, fc, pass_zero=False)
            self.x = None
            self.xd = self.xDither(self.N)

    def xDither(self, N=1):
        return self._dither*np.random.randn(N)

    def settle(self, x):
        self.x = x * np.ones(self.N)
    
    def __call__(self, x):
        if self._dither is None:
            return x
        # HPF the dither and get a new sample
        self.xd[0:-1] = self.xd[1:]
        self.xd[-1] = self.xDither()
        xd = np.inner(self.bd, self.xd)
        # LPF the dithered signal and return
        if self.x is None:
            self.settle(x)
            return x
        self.x[0:-1] = self.x[1:]
        self.x[-1] = x + xd
        return np.inner(self.b, self.x)


class MinValues(object):
    def __init__(self, kStart, kEnd):
        self.kStart = kStart
        self.kEnd = kEnd
        self.k = 0
        self.x = []

    def push(self, x):
        if self.k >= self.kStart and self.k < self.kEnd:
            self.x.append(x)
        self.k += 1

    def get(self):
        return np.mean(self.x)
    

class Reader(object):
    """
    @ivar k0: In I{trig} mode, the sample index where CH1 transitioned
        to halfway between its minimum and maximum values.

    @ivar t0: In I{trig} mode, the time when CH1 transitioned to
        halfway between its minimum and maximum values.
    """
    N_bits = 8
    t0 = None
    xPrev = None
    kCountdown = None
    x_offset = 0.0
    y_offset = 0.0
    xm = ym = None
    
    def __init__(
            self, kI, kE, M, invert, zIndices, x_offset, y_offset,
            trig=False, mono=False):
        if x_offset != 0.0:
            self.x_offset = x_offset
        if y_offset != 0.0:
            self.y_offset = y_offset
        elif zIndices:
            self.xm = MinValues(*zIndices)
            self.ym = MinValues(*zIndices)
        self.M = M
        self.k = -1
        self.ktxy = []
        fc = 1.0 / M
        self.kStart, self.kEnd = kI
        if self.kStart is None:
            self.kStart = Filter.N
        self.kE = kE
        self.invert = invert
        self.trig = trig
        self.xPrevs = [] if mono else None

    def isOutlier(self, x):
        if self.xPrevs is None:
            return
        if isinstance(self.xPrevs, list):
            self.xPrevs.append(x)
            if len(self.xPrevs) > 8:
                self.xPrevs = np.array(self.xPrevs)
            return
        self.xPrevs[0:-1] = self.xPrevs[1:]
        self.xPrevs[-1] = x
        if stats.skewtest(self.xPrevs)[1] < 0.1:
            return True
        
    def acquire(self, t, x, y):
        if self.t0 is None:
            self.t0 = t
            self.k0 = self.k
        if self.trig:
            if self.kCountdown is None:
                if self.xPrev is not None:
                    xp = self.xPrev
                    xm = self.xMidway
                    if (xp < xm and x > xm) or (xp > xm and x < xm):
                        if self.M == 1:
                            self.t0 = t
                            self.k0 = self.k
                            self.kCountdown = 0
                        else: self.kCountdown = self.fx.N / 2 
                self.xPrev = x
            elif self.kCountdown:
                self.kCountdown -= 1
            else:
                self.t0 = t
                self.k0 = self.k
                self.trig = False
        if self.kE and self.k == self.kE[1]:
            self.fx.settle(x)
            self.fy.settle(y)
        else:
            x = self.fx(x)
            y = self.fy(y)
        if self.k % self.M:
            # Decimation, only keep every M samples
            return
        if self.isOutlier(x):
            return
        self.ktxy.append([self.k, t, x, y])

    def txyerator(self, fh):
        self.k = 0
        for line in fh:
            parts = line.split(',')[-3:]
            try:
                txy = [float(x.strip()) for x in parts]
            except:
                continue
            self.k += 1
            if self.k < self.kStart:
                continue
            if self.kE:
                if self.k >= self.kE[0] and self.k < self.kE[1]:
                    continue
            if self.kEnd and self.k >= self.kEnd:
                break
            if self.invert:
                txy[1] = -txy[1]
                txy[2] = -txy[2]
            yield txy

    def firstPass(self, fh):
        mins = [np.inf]*2
        maxs = [-np.inf]*2
        for txy in self.txyerator(fh):
            if self.xm:
                self.xm.push(txy[1])
                self.ym.push(txy[2])
            for k in (0, 1):
                x_or_y = txy[k+1]
                if x_or_y < mins[k]:
                    mins[k] = x_or_y
                if x_or_y > maxs[k]:
                    maxs[k] = x_or_y
        self.xMidway = 0.5*(mins[0] + maxs[0])
        dithers = [(maxs[k] - mins[k]) / 2**self.N_bits for k in (0, 1)]
        return dithers
            
    def load(self, fh):
        fc = 1.0 / self.M
        self.fx, self.fy = [
            Filter(fc, dither) for dither in self.firstPass(fh)]
        fh.seek(0)
        for txy in self.txyerator(fh):
            self.acquire(*txy)

    def makeVectors(self):
        KTXY = np.array(self.ktxy)
        for k, nameChar in enumerate("KTXY"):
            setattr(self, nameChar, KTXY[:,k])
        self.T -= self.t0
        if self.xm:
            self.x_offset = self.xm.get()
            self.y_offset = self.ym.get()
        self.X -= self.x_offset
        self.Y -= self.y_offset


class Readers(object):
    """
    Uses an item in I{offsets} for each filenname in I{csvFiles}. If
    there are fewer offsets than csvFiles, uses the offsets until
    they run out, then sticks with the last one found. If I{offsets}
    is empty, a y_offset of 0.0 will be used for all.
    """
    def __init__(
            self, csvFiles, kI, kE, M, invert, zIndices, offsets,
            trig, use_ch1, mono):
        self.rList = []
        self.trig = trig
        self.use_ch1 = use_ch1
        for x_offset, y_offset, csvFile in self._filerator(offsets, csvFiles):
            r = Reader(
                kI, kE, M, invert, zIndices, x_offset, y_offset, trig, mono)
            with open(csvFile) as fh:
                r.load(fh)
            self.rList.append(r)

    def _filerator(self, offsets, csvFiles):
        def getOffset(k):
            if k < len(offsets):
                return offsets[k]
            if offsets:
                return offsets[-1]
            return 0
        
        for k, csvFile in enumerate(csvFiles):
            if self.trig:
                if self.use_ch1:
                    yield getOffset(0), getOffset(k+1), csvFile
                    continue
                yield 0, getOffset(k), csvFile
                continue
            yield getOffset(0), getOffset(k+1), csvFile
    
    def __len__(self):
        N = len(self.rList)
        if self.use_ch1: N += 1
        return N

    def readerator(self):
        for k, r in enumerate(self.rList):
            if k == 0 and self.trig and self.use_ch1:
                yield r
            yield r
    
    def get(self, vectorName, k=None):
        if k is None:
            return [self.get(vectorName, kk) for kk in range(len(self))]
        if self.use_ch1:
            if k > 0:
                k -= 1
            elif vectorName == 'Y':
                vectorName = 'X'
        return getattr(self.rList[k], vectorName)
    
    def align(self, t0_offset):
        k0 = int(np.round(np.mean([r.k0 for r in self.rList])))
        for r in self.rList:
            r.t0 -= t0_offset
            if r.k0 < k0:
                r.ktxy = r.ktxy[:r.k0-k0]
            else:
                r.ktxy = r.ktxy[r.k0-k0:]

    def makeVectors(self):
        for r in self.rList:
            r.makeVectors()
    
    def max(self, vectorName):
        return max([max(x) for x in self.get(vectorName)])

    def offset(self, k):
        if self.use_ch1:
            if k == 0:
                return self.rList[0].x_offset
            return self.rList[k-1].y_offset
        return self.rList[k].y_offset

    
class Writer(object):
    """
    I write rows containing each value of my independent vector I{X}
    with something else related to each value.
    """
    fieldSpecs = [
        ('f', 12),
        ('f', 8),
        ('f', 8),
    ]
    spaces = "  "
    dashes = "-"*79
    
    def __init__(self, X):
        self.X = X
        self.comment = False
        msg(True)

    def setup(self, *I):
        protoParts = []
        protoPartsHeader = []
        for k in I:
            code, width = self.fieldSpecs[k]
            pp =  "{:" + str(width)
            if code == 'g':
                pp += "." + str(width-5)
            elif code == 'f':
                pp += "." + str(width-3)
            pp += code + "}"
            protoParts.append(pp)
            if self.comment and not protoPartsHeader:
                width -= 2
            pp = "{:" + str(width) + "s}"
            protoPartsHeader.append(pp)
        self.proto = self.spaces.join(protoParts)
        self.protoHeader = self.spaces.join(protoPartsHeader)

    def write(self, *args):
        if self.comment:
            args = list(args)
            args[0] = "# " + args[0]
        msg(*args)

    def writeHeader(self, *names):
        self.write(self.protoHeader, *names)
        self.write(self.dashes)
        
    def writeXY(self, Y, xName, yName):
        """
        Writes each of my X values with the corresponding Y value.
        """
        self.setup(1, 2)
        self.writeHeader(xName, yName)
        for x, y in zip(self.X, Y):
            self.write(self.proto, x, y)

    def writeXYs(self, Ys, xName, yNames):
        """
        Writes each of my X values with the corresponding row of all Y
        values accumulated in the list I{Ys}.
        """
        Z = np.column_stack(Ys)
        self.setup(
            0 if xName == 'time' else 1,
            *[2]*len(yNames)
        )
        self.writeHeader(xName, *yNames)
        for k, x in enumerate(self.X):
            self.write(self.proto, x, *Z[k,:])
    
    def writeTXY(self, X, Y, xName, yName):
        """
        Writes each of my X values as a time and followed by the
        corresponding I{X} and I{Y} values.
        """
        self.setup(0, 2, 2)
        self.writeHeader('time', xName, yName)
        for t, x, y in zip(self.X, X, Y):
            self.write(self.proto, t, x, y)

    def writePWL(self, X, xName):
        """
        Writes each of my X values as a time followed by the corresponding
        I{X} value, with a comment header, suitable for use as an
        XSPICE filesource.
        """
        self.comment = True
        self.setup(0, 2)
        self.write(
            "PWL waveform data for XSPICE filesource providing node '{}'\n",
            xName)
        self.writeHeader('time', 'voltage')
        self.comment = False
        for t, x in zip(self.X, X):
            self.write(self.proto, t, x)


class ArgsFromSpec(object):
    reOptBool = re.compile(r'([a-zA-Z])$')
    reOpt = re.compile(r'([a-zA-Z])\s+(.+)$')

    def __init__(self, fh, args):
        self.opts = set()
        self.values = {}
        for name, value in args._get_kwargs():
            self.opts.add(name)
            self.values[name] = value
        self.pargs = []
        positional = False
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('--'):
                positional = True
                continue
            if positional:
                self.parsePositionals(line)
            else: self.parseOpt(line)
        self.values['pargs'] = self.pargs
        del self.pargs

    def parseOpt(self, line):
        match = self.reOptBool.match(line)
        if match:
            name = match.group(1)
            if name not in self.opts:
                raise ValueError(sub("Unexpected bool option '{}'", name))
            self.values[name] = True
            return
        match = self.reOpt.match(line)
        if match:
            name = match.group(1)
            if name not in self.opts:
                raise ValueError(sub("Unexpected value option '{}'", name))
            self.values[name] = type(self.values[name])(match.group(2))
            return

    def parsePositionals(self, line):
        self.pargs.extend([
            x.strip() for x in line.split()])

    def __iter__(self):
        for name in self.values:
            yield name
        
    def __getattr__(self, name):
        return self.values[name]


class Helpers(object):
    def checkFile(self, filePath):
        if not os.path.exists(filePath):
            raise RuntimeError(sub("No file '{}' found", filePath))

    def str2list(self, text, what=str, sep=','):
        result = []
        parts = text.strip().split(sep)
        if len(parts) > 1 and parts[0] == '':
            result.append(what("0"))
        for part in parts:
            part = part.strip()
            if part:
                result.append(what(part))
        return result

    def parsePositionals(self, pargs):
        def isCSV(arg):
            parts = arg.split('.')
            if len(parts) == 1:
                return False
            if parts[-1].lower() == 'csv':
                return True
            return False

        k = 0
        names, csvFiles = [], []
        names.append("CH1" if isCSV(pargs[0]) else pargs.pop(0))
        while pargs:
            k += 1
            arg = pargs.pop(0)
            if not isCSV(arg):
                raise ValueError("Expected CSV file name")
            csvFiles.append(arg)
            if not pargs or isCSV(pargs[0]):
                name = "CH2"
                if k > 1: name += "-" + str(k)
                names.append(name)
                continue
            names.append(pargs.pop(0))
        return names, csvFiles


class _FakePlotter(object):
    def __enter__(self):
        return None
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def show(self, null):
        pass

    
class Runner(Helpers):
    p = None
    X = None
    smoothingScale = 1E-5

    def __init__(self, args):
        if not len(args):
            raise RuntimeError(
                "You must specify at least a spec file or one CSV file")
        possibleSpecfilePath = args[-1]
        if possibleSpecfilePath.endswith('.spec'):
            # Spec file
            self.checkFile(possibleSpecfilePath)
            with open(possibleSpecfilePath) as fh:
                args = ArgsFromSpec(fh, args)
        self.trig = args.r
        self.use_ch1 = args.c
        self.univariate = args.u
        if self.univariate:
            self.use_ch1 = True
        self.names, csvFiles = self.parsePositionals(list(args))
        self.windowTitle = ", ".join(
            [os.path.splitext(os.path.split(x)[-1])[0] for x in csvFiles])
        self.Ny = len(self.names)
        if self.trig and not self.use_ch1:
            self.Ny -= 1
        elif not args.t:
            self.Ny -= 1
        indices = self.str2list(args.k) if args.k else [0]
        if len(indices) == 1:
            kI = [int(indices[0]), None]
        else: kI = [int(x) for x in indices]
        indices = self.str2list(args.K) if args.K else None
        kE = [] if indices is None else [int(x) for x in indices]
        if args.f:
            self.checkFile(args.f)
            rz = Reader([0, None], [], 128, args.i, False, 0, 0, args.m)
            with open(args.f) as fh:
                rz.load(fh)
                rz.makeVectors()
            offsets = [rz.Y.mean()] * self.Ny
        else:
            offsets = self.str2list(args.o, float)
        self.rs = Readers(
            csvFiles, kI, kE,
            args.M, args.i, self.str2list(args.z, int),
            offsets, self.trig, self.use_ch1, args.m)
        if self.trig:
            self.rs.align(args.R)
        self.rs.makeVectors()
        if args.p or args.l or args.g or not args.w:
            self.plotSetup(args.t, args.g, args.l)
        else:
            self.xy = True
            self.p = _FakePlotter()
        if args.w:
            sweep = self.str2list(args.w, float)
            step = sweep[0]
            xMax = self.rs.max('X') if self.xy else self.rs.max('T')
            stop = min([sweep[1], xMax]) if len(sweep) > 1 else xMax
            start = float(sweep[2]) if len(sweep) > 2 else 0
            X = []
            x = start
            while True:
                X.append(x)
                x += step
                if x > stop:
                    break
            self.X = np.array(X)
            self.w = Writer(self.X)
        N = min([len(x) for x in self.rs.get('T')]) / args.M
        self.smoothingFactor = self.smoothingScale * args.s**2

    def plotSetup(self, vt, semilog, lines):
        N_names = len(self.names)
        if vt or self.univariate:
            Nx = 1
            Ny = 1 if self.univariate else self.Ny
            Nxy = 0
        elif self.trig:
            if N_names == 2:
                # With triggered and just 1 CSV file, VT is forced
                Nx = 1
                Ny = 2
                Nxy = 0
            else:
                # Transition XY mode: CH2 of first CSV vs CH2 of each
                # additional CSV, with t0 determined for each CH2 from
                # its file's CH1
                Nxy = self.Ny
        else:
            Nxy = self.Ny
        # Define subplot structure
        if Nxy:
            self.xy = True
            # One column if just a single XY plot, otherwise two columns
            Nx = 1 if Nxy == 1 else 2
            # Rows as needed
            Ny = int(np.ceil(Nxy // Nx))
        else: self.xy = False
        self.p = Plotter(Nx, Ny)
        self.p.set_grid()
        if semilog:
            self.p.set_semilogy()
        if not lines:
            self.p.add_marker('.')
    
    def spline(self, r, xName, Y_or_name, k):
        X = getattr(r, xName)
        Y = getattr(r, Y_or_name) if isinstance(Y_or_name, str) else Y_or_name
        if self.X is None:
            I = range(len(X))
            bbox = [X[0], X[-1]]
        else:
            I = np.flatnonzero(np.logical_and(X >= self.X[0], X <= self.X[-1]))
            if not len(I):
                return
            bbox = [self.X[0], self.X[-1]]
        smoothingFactor = np.square(
            Y.max() - Y.min()) * len(I) * self.smoothingFactor
        return interpolate.UnivariateSpline(
            X[I], Y[I], bbox=bbox, s=smoothingFactor, ext='const', k=k)

    def zeroLines(self, ax):
        for lineFunc, limFunc in (
                (ax.axhline, ax.get_xlim), (ax.axvline, ax.get_ylim)):
            axMin, axMax = limFunc()
            if axMin < 0 and axMax > 0:
                lineFunc(0, linestyle='-', linewidth=2, color='black', zorder=2)

    def plot(self, X, Y, p, r, s, xName, yName, offset=None):
        if not p: return
        p.clear_annotations()
        if s is None or self.univariate:
            N = len(r.K)
            for k in (0, N/4, N/2, 3*N/4, N-1):
                p.add_annotation(k, str(int(r.K[k])))
        for k in (np.argmin(X), np.argmax(X)):
            p.add_annotation(
                k, sub("({:.3g}, {:.3g})", X[k], Y[k]))
        if offset is not None:
            k = np.argmin(np.abs(Y))
            p.add_annotation(k, sub("offset = {:6.4f}", offset))
        if xName is None:
            p.set_timex()
        else: p.set_xlabel(xName)
        p.set_ylabel(yName)
        if s is not None:
            for x in (self.X[0], self.X[-1]):
                p.add_annotation(
                    np.searchsorted(X, x),
                    sub("({:.2g}, {:.3g})", x, float(s(x))))
        ax = p(X, Y)
        self.zeroLines(ax)
        if s is not None:
            ax.plot(self.X, s(self.X), 'o', color='red')
            Xs = np.linspace(X.min(), X.max(), 2000)
            ax.plot(Xs, s(Xs), '-', color='white', alpha=0.3, linewidth=3)
            ax.plot(Xs, s(Xs), '-', color='white', alpha=0.6, linewidth=2)
            ax.plot(Xs, s(Xs), '-', color='black', linewidth=1)
                
    def __call__(self):
        def doXY(r, xName, yName):
            s = None
            I = np.argsort(r.X)
            r.X = r.X[I]; r.Y = r.Y[I]
            if self.X is not None:
                s = self.spline(r, 'X', 'Y', 3)
            if s is not None:
                Y = s(self.X)
                Ys.append(Y)
                yNames.append(yName)
            self.plot(r.X, r.Y, p, r, s, xName, yName, offset=r.y_offset)

        def doVT_X(r, xName):
            sx = self.spline(r, 'T', 'X', 1)
            if sx is not None:
                if self.X is None:
                    self.X = sx.get_knots()
                    self.w = Writer(self.X)
                self.w.writePWL(sx(self.X), xName)
            self.plot(r.T, r.X, p, r, sx, None, xName, offset=r.x_offset)
            
        def doVT_XandY(r, xName, yName):
            sx = sy = None
            if self.X is not None:
                sx = self.spline(r, 'T', 'X', 3)
                if sx is not None:
                    sy = self.spline(r, 'T', 'Y', 3)
                    if sy is not None:
                        self.w.writeTXY(sx(self.X), sy(self.X), xName, yName)
            self.plot(r.T, r.X, p, r, sx, None, xName, offset=r.x_offset)
            self.plot(r.T, r.Y, p, r, sy, None, yName, offset=r.y_offset)

        def doVT_Y(r, Y, yName, offset):
            sy = None
            if self.X is not None:
                sy = self.spline(r, 'T', Y, 3)
                if sy is not None:
                    Ys.append(sy(self.X))
                    yNames.append(yName)
            self.plot(r.T, Y, p, r, sy, None, yName, offset=offset)

        Ys = []; yNames = []
        with self.p as p:
            if self.xy:
                xName = self.names.pop(0)
                for k, r in enumerate(self.rs.rList):
                    doXY(r, xName, self.names[k])
            elif self.univariate:
                doVT_X(self.rs.rList[0], self.names[0])
            elif not self.trig and not self.use_ch1:
                doVT_XandY(self.rs.rList[0], *self.names[:2])
            else:
                xName = 'time'
                for k, r in enumerate(self.rs.readerator()):
                    Y = self.rs.get('Y', k)
                    offset = self.rs.offset(k)
                    doVT_Y(r, Y, self.names[k+1-int(self.use_ch1)], offset)
        if Ys:
            self.w.writeXYs(Ys, xName, yNames)
        self.p.show(self.windowTitle)


args = Args("BK Scope CSV File Reader")
args('-o', '--offset', "", "Manual offset for <CH2>|<CH1,CH2> values")
args('-f', '--offset-file', "", "CSV file with zero-V CH2 values")
args('-z', '--zero', "",
     "Offset CH2 values (using <first,last> samples) so minimum ~= 0.0")
args('-k', '--indices', "", "Index of first[,last] sample(s) to acquire")
args('-K', '--omit-indices', "", "Index of first[,last] sample(s) to omit")
args('-M', '--M', 16, "Decimation rate, CSV entries to filtered data points")
args('-s', '--smoothing', 0.5, "Spline smoothing factor")
args('-t', '--time', "Make time the X vector with two Y vectors")
args('-p', '--plot', "Plot the vectors before writing")
args('-u', '--univariate', "Linear (for PWL source) spline to CH1 only")
args('-i', '--invert', "Invert CH1 and CH2 values")
args('-l', '--lines', "Draw CSV datapoints with lines (implies -p)")
args('-r', '--triggered', "CH1 transition midway between min, max = t0")
args('-R', '--trigger-offset', 0.0, "Time (sec) to shift t0")
args('-c', '--keep-CH1',
     "Use CH1 as first Y vector even while triggering on it")
args('-w', '--sweep', "", "<X step>[,<Xstop>[,<Xstart>]]")
args('-g', '--semilog', "Plot with log-scale Y axis")
args('-m', '--mono', "Try to enforce montoncity of CH1 with outlier rejection")
args("<spec file> | "+\
     "[<CH1 name>] <CSV #1> [<CH2 name #1>] [[<CSV #2>] [<CH2 name #2>] ...]")


def main():
    if args.h:
        return
    import pdb, traceback, sys
    try:
        Runner(args)()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)


if __name__ == '__main__':
    main()
