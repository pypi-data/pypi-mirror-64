#Title:          ReleasePyInspect.py
#Author:         Stephen Tanner, Samuel Payne, Natalie Castellana, Pavel Pevzner, Vineet Bafna
#Created:        2005
# Copyright 2007,2008,2009 The Regents of the University of California
# All Rights Reserved
#
# Permission to use, copy, modify and distribute any part of this
# program for educational, research and non-profit purposes, by non-profit
# institutions only, without fee, and without a written agreement is hereby
# granted, provided that the above copyright notice, this paragraph and
# the following three paragraphs appear in all copies.
#
# Those desiring to incorporate this work into commercial
# products or use for commercial purposes should contact the Technology
# Transfer & Intellectual Property Services, University of California,
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910,
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES,
# INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.
#
# THE SOFTWARE PROVIDED HEREIN IS ON AN "AS IS" BASIS, AND THE UNIVERSITY
# OF CALIFORNIA HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.  THE UNIVERSITY OF CALIFORNIA MAKES NO
# REPRESENTATIONS AND EXTENDS NO WARRANTIES OF ANY KIND, EITHER IMPLIED OR
# EXPRESS, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR THAT THE USE OF
# THE SOFTWARE WILL NOT INFRINGE ANY PATENT, TRADEMARK OR OTHER RIGHTS.

"""
Script to build PyInspect
"""
import sys
import os

import distutils.core

PyInspectFileNames = [
    "PyInspect/PyInspect.c", "PyInspect/PySpectrum.c", "PyInspect/PyUtils.c",
    "base64.c", "BN.c", "BuildMS2DB.c", "ChargeState.c", "CMemLeak.c",
    "Errors.c", "ExonGraphAlign.c", "FreeMod.c", "IonScoring.c", "LDA.c",
    "Mods.c", "MS2DB.c", "ParentMass.c", "ParseInput.c", "ParseXML.c", "PValue.c",
    "Run.c", "Score.c", "Scorpion.c", "SNP.c",
    "Spectrum.c", "Spliced.c", "SpliceDB.c",
    "SpliceScan.c", "SVM.c", "Tagger.c", "Trie.c", "Utils.c","TagFile.c"]

def Main(Arguments):
    print "Prepping PyInspect..."
    if sys.platform == "win32":
        LibraryList = ["libexpat"]
    else:
        LibraryList = ["expat"]
        
    PyInspectExtension = distutils.core.Extension('PyInspect',
        sources = PyInspectFileNames,
        include_dirs = [".", "expat/lib"],
        library_dirs = ["expat/lib/release","pdk_wrapper"], 
        libraries = LibraryList)

    distutils.core.setup(name = 'PyInspect', version = '1.0', ext_modules=[PyInspectExtension],
        script_args = Arguments)

if __name__ == "__main__":
    Main(sys.argv[1:])
