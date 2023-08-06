#Title:          BuildMGF.py
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
BuildMGF.py
This is a part of the PTMAnalysis pipeline.  It creates an
.mgf file of all the consensus spectra created by ComputePTMFeatures.py
"""

import os
import sys
import string
import getopt
import MSSpectrum
from Utils import *
Initialize()
from TrainPTMFeatures import FormatBits

class PeptideFeatureBag:
    pass

class MGFBuilder:
    def __init__(self):
        self.ConsensusSpectrumDir = "ptmscore\\LensLTQ-99-5\\spectra"
        self.PeptideFeatureFileName = "PTMScore\\LensLTQ-99-5.txt"
        self.MGFPath = "PTMScore\\LensLTQ-99-5.mgf"
        self.ModifiedPeptides = []
    def ParsePeptideFeatureFile(self):
        """
        Parse the contents of the peptide feature-file.  We need to know the
        path to the consensus spectrum file, the consensus annotation MQScore,
        and the index.
        """
        File = open(self.PeptideFeatureFileName, "rb")
        LineNumber = 0
        for FileLine in File.xreadlines():
            LineNumber +=1
            if FileLine[0] == "#":
                continue
            Bits = list(FileLine.replace("\r", "").replace("\n", "").split("\t"))
            try:
                ConsensusMQScore = float(Bits[FormatBits.ConsensusMQScore])
            except:
                print "** Error: Can't parse consensus MQScore from line %s!"%LineNumber
                print Bits
                continue
            PeptideFeatures = PeptideFeatureBag()
            PeptideFeatures.Bits = Bits
            PeptideFeatures.ConsensusMQScore = ConsensusMQScore
            NiceAnnotation = Bits[FormatBits.Peptide].replace("*", "-")
            PeptideFeatures.Bits[FormatBits.Peptide] = NiceAnnotation
            FirstResidue = NiceAnnotation[2]
            Charge = Bits[FormatBits.Charge]
            PeptideFeatures.SpectrumPath = os.path.join(self.ConsensusSpectrumDir, FirstResidue, "%s.%s.dta"%(NiceAnnotation, Charge))
            self.ModifiedPeptides.append(PeptideFeatures)
        File.close()
        print "Parsed %s modified peptides from %s file lines."%(len(self.ModifiedPeptides), LineNumber)
    def PrepareSearchMGF(self):
        """
        Concatenate our consensus spectra into an MGF file, for searching.
        """
        MGFFile = open(self.MGFPath, "wb")
        ScanNumber = 1
        for PeptideIndex in range(len(self.ModifiedPeptides)):
            if PeptideIndex % 100 == 0:
                print "Peptide species %s/%s..."%(PeptideIndex, len(self.ModifiedPeptides))
            PeptideFeatures = self.ModifiedPeptides[PeptideIndex]
            Spectrum = MSSpectrum.SpectrumClass()
            Spectrum.ReadPeaks(PeptideFeatures.SpectrumPath)
            Spectrum.WriteMGFPeaks(MGFFile, PeptideFeatures.Bits[FormatBits.Peptide], ScanNumber)
            ScanNumber += 1
        MGFFile.close()
    def Main(self):
        self.ParsePeptideFeatureFile()
        self.PrepareSearchMGF()
    def ParseCommandLine(self, Arguments):
        (Options, Args) = getopt.getopt(Arguments, "d:m:")
        OptionsSeen = {}
        for (Option, Value) in Options:
            OptionsSeen[Option] = 1
            if Option == "-d":
                self.PeptideFeatureDir = Value
            elif Option == "-m":
                self.MGFPath = Value
        self.ConsensusSpectrumDir = os.path.join(self.PeptideFeatureDir, "Spectra")
        self.PeptideFeatureFileName = os.path.join(self.PeptideFeatureDir, "PTMFeatures.txt")

UsageInfo = """
BuildMGF arguments:
  -d [DIR]: Peptide feature directory
  -m [FILE]: Output .mgf file name
"""
  
if __name__ == "__main__":
    Builder = MGFBuilder()
    Builder.ParseCommandLine(sys.argv[1:])
    Builder.Main()
