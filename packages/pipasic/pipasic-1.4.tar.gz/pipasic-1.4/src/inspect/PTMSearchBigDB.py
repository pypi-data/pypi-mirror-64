#Title:          PTMSearchBigDB.py
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
Context:
  We've performed an unrestrictive search of many spectra against a small database.
  We've found a collection of modified peptides, after taking a p-value threshold at
  the spectrum level.  We want to better distinguish between VALID and INVALID annotations.

Plan:
  Let's take each modified peptide and search its consensus spectrum against
  a large database (Swiss-Prot).  The resulting delta-score should be an informative feature
  when in comes to distinguishing beween the VALID and INVALID annotations.  The delta-score
  will be zero (actually, slightly negative) if the consensus spectrum matches an unmodified
  peptide (e.g. an unanticipated contaminant).
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

class PTMSearcher:
    def __init__(self):
        self.HeaderLines = []
        self.ConsensusSpectrumDir = "ptmscore\\LensLTQ-99-5\\spectra"
        self.PeptideFeatureFileName = "PTMScore\\LensLTQ-99-5.txt"
        self.FixedFeatureFileName = None
        self.ModifiedPeptides = []
        self.InspectOut = None        
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
                self.HeaderLines.append(FileLine)
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
    def ComputeDeltaScoreFeatureFile(self, FileName):
        File = open(FileName, "rb")
        OldSpectrum = None
        for FileLine in File.xreadlines():
            if FileLine[0] == "#":
                continue
            Bits = FileLine.split("\t")
            Spectrum = (Bits[0], Bits[1])
            if Spectrum == OldSpectrum:
                continue
            OldSpectrum = Spectrum
            MQScore = float(Bits[5])
            ScanNumber = int(Bits[1])
            PeptideFeatures = self.ModifiedPeptides[ScanNumber]
            while len(PeptideFeatures.Bits) <= FormatBits.ConsensusDeltaBigDB:
                  PeptideFeatures.Bits.append("")
            PeptideFeatures.Bits[FormatBits.BigDBAnnotation] = Bits[2]
            PeptideFeatures.Bits[FormatBits.BigDBMQScore] = Bits[5]
            DeltaScore = float(PeptideFeatures.ConsensusMQScore - MQScore)
            PeptideFeatures.Bits[FormatBits.ConsensusDeltaBigDB] = str(DeltaScore)
        File.close()
    def ComputeDeltaScoreFeature(self):
        """
        Parse annotations from the inspect search.  Tweak the corresponding modified-peptides
        to know their modless-annotation and delta-score.
        """
        # Iterate over just one result file, or a directory full of results-files:
        if os.path.isdir(self.InspectOut):
            for FileName in os.listdir(self.InspectOut):
                Path = os.path.join(self.InspectOut, FileName)
                self.ComputeDeltaScoreFeatureFile(Path)
        else:
            self.ComputeDeltaScoreFeatureFile(self.InspectOut)
        # Write out the fixed feature-rows:
        File = open(self.FixedFeatureFileName, "wb")
        for HeaderLine in self.HeaderLines:
            File.write(HeaderLine)
        for Peptide in self.ModifiedPeptides:
            FileLine = string.join(Peptide.Bits, "\t")
            File.write(FileLine + "\n")
        File.close()
    def Main(self):
        self.ParsePeptideFeatureFile()
        self.ComputeDeltaScoreFeature()
    def ParseCommandLine(self, Arguments):
        (Options, Args) = getopt.getopt(Arguments, "d:w:r:")
        OptionsSeen = {}
        for (Option, Value) in Options:
            OptionsSeen[Option] = 1
            if Option == "-d":
                self.PeptideFeatureDir = Value
            elif Option == "-w":
                self.FixedFeatureFileName = Value
            elif Option == "-r":
                self.InspectOut = Value
        if not self.PeptideFeatureDir:
            print UsageInfo
            sys.exit(-1)
        self.PeptideFeatureFileName = os.path.join(self.PeptideFeatureDir, "PTMFeatures.txt")
        self.ConsensusSpectrumDir = os.path.join(self.PeptideFeatureDir, "Clusters")
        
UsageInfo = """
PTMSearchBigDB arguments:
  -d [DIR]: Peptide directory.  This directory should contain PTMFeatures.txt, as well
     as the consensus spectra and clusters.
  -w [FILE]: Output file, for peptides with delta-score included
  -r [FILE]: Inspect output filename
"""
  
if __name__ == "__main__":
    Searcher = PTMSearcher()
    Searcher.ParseCommandLine(sys.argv[1:])
    Searcher.Main()
