#Title:          BuildInspect.py
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
Python script to build Inspect.  An alternative to makefiles.
"""
import sys
import distutils
import distutils.command.build
import distutils.ccompiler

def BuildInspect(BuildNow = 0):
    InspectSourceFiles = [
        "base64.c", "BN.c", "BuildMS2DB.c", "ChargeState.c", "CMemLeak.c",
        "Errors.c", "ExonGraphAlign.c", 
        "FreeMod.c", "IonScoring.c", "LDA.c", "main.c", "Mods.c",
        "MS2DB.c", "ParentMass.c", "ParseInput.c", 
        "ParseXML.c", "PValue.c", 
        "Run.c", "Score.c", "Scorpion.c", "SNP.c", "Spectrum.c", "Spliced.c", 
        "SpliceDB.c", "SpliceScan.c", "SVM.c", "Tagger.c", "Trie.c", "Utils.c", "TagFile.c"
        ]
    ExtraIncludeDirectories = ["expat\\lib",]
    class MyBuildClass(distutils.command.build.build):
        def build_opt(self):
            CC = distutils.ccompiler.new_compiler()
            #if sys.platform != 'win32':
            #    CC.add_library('m')
            #import os.path
            print dir(CC)
            CC.library_dirs.append("expat/lib/release")
            if sys.platform == "win32":
                CC.add_library("libexpat")
            else:
                CC.add_library("expat") # not "libexpat", that won't work on Linux.
                CC.add_library("m")
            CC.set_include_dirs(ExtraIncludeDirectories)
            opt_obj = CC.compile(InspectSourceFiles)
            CC.link_executable(opt_obj, "inspect")
        def run(self):
            self.build_opt()
            distutils.command.build.build.run(self)
    if BuildNow:
        Dist = distutils.dist.Distribution()
        Dist.parse_config_files()
        Dist.cmdclass["build"] = MyBuildClass
        Dist.commands = ["build"]
        Dist.run_commands()
    else:
        distutils.core.setup(cmdclass = {"build":MyBuildClass,})

def BuildInspectOnConvey(BuildNow = 0):
    InspectSourceFiles = [
        "base64.c", "BN.c", "BuildMS2DB.c", "ChargeState.c", "CMemLeak.c",
        "Errors.c", "ExonGraphAlign.c", 
        "FreeMod.c", "IonScoring.c", "LDA.c", "main.c", "Mods.c",
        "MS2DB.c", "ParentMass.c", "ParseInput.c", 
        "ParseXML.c", "PValue.c", 
        "Run.c", "Score.c", "Scorpion.c", "SNP.c", "Spectrum.c", "Spliced.c", 
        "SpliceDB.c", "SpliceScan.c", "SVM.c", "Tagger.c", "Trie.c", "Utils.c", "TagFile.c",
        "cny_kernel_wrapper.c", "pdk_kernel.c", "kernel.c", "cny_util.c"]
    ExtraIncludeDirectories = ["expat\\lib",]
    class MyBuildClass(distutils.command.build.build):
        def build_opt(self):
            CC = distutils.ccompiler.new_compiler()
            #if sys.platform != 'win32':
            #    CC.add_library('m')
            #import os.path
            print dir(CC)
            CC.library_dirs.append("expat/lib/release")
            if sys.platform == "win32":
                CC.add_library("libexpat")
            else:
                CC.add_library("expat") # not "libexpat", that won't work on Linux.
                CC.add_library("m")
            CC.set_include_dirs(ExtraIncludeDirectories)
            opt_obj = CC.compile(InspectSourceFiles)
            CC.link_executable(opt_obj, "inspect")
        def run(self):
            self.build_opt()
            distutils.command.build.build.run(self)
    if BuildNow:
        Dist = distutils.dist.Distribution()
        Dist.parse_config_files()
        Dist.cmdclass["build"] = MyBuildClass
        Dist.commands = ["build"]
        Dist.run_commands()
    else:
        distutils.core.setup(cmdclass = {"build":MyBuildClass,})
    

if __name__ == "__main__":
    #sys.argv = ["", "build"]
    BuildInspect()
    
