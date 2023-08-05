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
C{ps2sc}: Convert a pingspice L{Subcircuit} subclass into a
Ngspice-compatible subcircuit file.
"""

from twisted.python import reflect

from pingspice.circuit import netlist
from pingspice.circuit.netlist import Subcircuit

from pingspice.util import *


args = Args(
    """
    Pingspice Subcircuit to Ngspice subcircuit file converter.

    The first (and possibly only) positional argument is the fully
    qualified name (package.module.class) of a subclass of Subcircuit
    (found in the pingspice.circuit.netlist module). Pingspice comes
    with tons of such subclasses that attempt to model various
    electronic components. You can also define your own.

    The second argument is the name of a file (typically having a
    C{.cir} extension) that will be written with the subcircuit as an
    Ngspice-compatible netlist. If the argument is omitted, the
    netlist will be printed to STDOUT.
    """
)
# Output
args('-t', '--ts', 1e-9,
     "TRAN timestep to assume for simulation-friendly inductors")
# Positional argument
args("<Subcircuit subclass> [<netlist output file>]")


def is_subcircuit(x):
    """
    Returns C{True} if I{x} is a subclass of L{Subcircuit}.
    """
    try:
        OK = issubclass(x, Subcircuit)
    except: OK = False
    return OK

def find_subcircuit(fqn):
    """
    Returns a subclass of L{Subcircuit} in the module for the class
    specified by I{fqn}, with the class name case-insensitive,
    if it exists. Otherwise, returns C{None}.
    """
    parts = fqn.split('.')
    try:
        module = reflect.namedObject('.'.join(parts[:-1]))
        className = parts[-1].upper()
        for name in dir(module):
            if name.upper() == className:
                SubClass = getattr(module, className)
                if is_subcircuit(SubClass):
                    return SubClass
    except: pass
        
def tryGetClass(name):
    try:
        SubClass = reflect.namedObject(name)
        if not is_subcircuit(SubClass):
            raise AttributeError
    except ImportError:
        if not name.startswith('pingspice.'):
            return tryGetClass('pingspice.' + name)
    except AttributeError:
        SubClass = find_subcircuit(name)
        if SubClass is None:
            raise RuntimeError(sub(
                "Couldn't import any Subcircuit subclass '{}'", name))
    return SubClass
                          
def main():
    if not args:
        raise RuntimeError(
            "You must specify the FQN of a subclass of "+\
            "pingspice.circuit.netlist.Subcircuit")
    SubcircuitSubclass = tryGetClass(args[0])
    SubcircuitSubclass.export(*args[1:], ts=args.t)


if __name__ == '__main__' and not args.h:
    main()
