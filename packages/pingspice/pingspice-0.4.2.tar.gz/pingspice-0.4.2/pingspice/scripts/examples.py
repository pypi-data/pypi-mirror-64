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
Extraction of example files into C{~/pingspice-examples}.
"""

import re, os, os.path, shutil, pkg_resources

from ade.util import msg


PKG_DIR = ('pingspice', 'examples')


def extract():
    """
    Call via the I{pingspice-examples} entry point to extract example
    files to a subdirectory I{pingspice-examples} of your home
    directory, creating the subdirectory if necessary.

    It will not overwrite existing files, so feel free to modify the
    examples. Delete a modified example file (or the whole
    subdirectory) and run this again to restore the default file.
    """
    msg(True)
    sDir = pkg_resources.resource_filename(*PKG_DIR)
    eDir = os.path.expanduser(
        os.path.join("~", "-".join(PKG_DIR)))
    msg("Extracting {} to\n{}\n{}", " ".join(PKG_DIR), eDir, "-"*79)
    if os.path.exists(eDir):
        msg("Subdirectory already exists")
    else:
        os.mkdir(eDir)
        msg("Subdirectory created")
    reFile = re.compile(r'[a-z].+\.(py|c|txt|cir)$')
    for fileName in pkg_resources.resource_listdir(*PKG_DIR):
        if not reFile.match(fileName):
            continue
        ePath = os.path.join(eDir, fileName)
        if os.path.exists(ePath):
            msg("{} already exists", ePath)
        else:
            sPath = os.path.join(sDir, fileName)
            if os.path.isfile(sPath):
                shutil.copy(sPath, ePath)
                msg("{} created", ePath)
