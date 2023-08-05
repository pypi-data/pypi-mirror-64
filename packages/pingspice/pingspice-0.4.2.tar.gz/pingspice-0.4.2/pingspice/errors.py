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
Exceptions of universal interest.

This is imported by C{util}, so it can't import anything.
"""


def sub(proto, *args):
    """
    This really should be a built-in function.
    """
    if not args: return str(proto)
    return proto.format(*args)


class Error(Exception):
    """
    Subclass this to make your exception treat its constructor like a
    sub with proto/args text expansion.
    """
    def __init__(self, proto, *args):
        Exception.__init__(self, sub(proto, *args))

    
class NetlistError(Error):
    """
    There was a problem involving construction of a netlist.
    """


class ModelError(Error):
    """
    There was a problem involving an Ngspice model.
    """


class SubcircuitError(Error):
    """
    There was a problem involving a subcircuit.
    """

class CapacitanceConfigError(Error):
    """
    There was a problem with the special pingspice Capacitance.
    """
    

class ArgumentError(Exception):
    """
    You supplied improper arguments.
    """
    def __init__(self, args, N=None, text=None):
        if text is None:
            if N is None:
                text = sub("Improper arguments '{}'", args)
            else:
                text = sub("Expected {:d} arguments, got {:d}", N, len(args))
        Exception.__init__(self, text)

