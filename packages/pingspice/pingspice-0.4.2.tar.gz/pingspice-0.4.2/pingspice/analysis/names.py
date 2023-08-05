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
Parameter names.
"""

from pingspice.util import MAX_LINE_LENGTH, fill


class ParameterNamer(object):
    """
    I associate parameter values with names in a visually pleasing
    way.
    
    @ivar dashes: A text consisting of a dashed line as long as the
        fill width.
    """
    def __init__(self, names):
        """Constructor"""
        self.names = names
        self.sortedNameIndices = [
            self.names.index(name) for name in sorted(self.names)]
        self.dashes = "-"*MAX_LINE_LENGTH
        
    def sortedNamerator(self, values=None):
        """
        Generates tuples of sorted names with (1) the index in a
        I{values} list of parameters where each named parameter
        appears, and (2) the name itself.

        If such a list of I{values} is supplied, each tuple also
        includes (3) the value for that name.
        """
        if values is None:
            for k in self.sortedNameIndices:
                yield k, self.names[k]
        else:
            for k in self.sortedNameIndices:
                yield k, self.names[k], values[k]

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
        return fill(text)
