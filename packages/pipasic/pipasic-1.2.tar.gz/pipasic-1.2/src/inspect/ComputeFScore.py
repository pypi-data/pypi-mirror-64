#Title:          PValue.py
#Author:         Stephen Tanner, Samuel Payne, Natalie Castellana, Pavel Pevzner, Vineet Bafna
#Created:        2010
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
This script, based on PeptideProphet, computes an F-Score.  The F-Score
for a match is a weighted sum of the length-corrected MQScore and the delta score.

Also, there is no length constraint on peptides.  An FScore is computed for all peptides.
The FScore column of each peptide-spectrum match (PSM) is updated, but no p-value or FDR is caluclated.

"""
import os
import sys
import random
import math
import getopt
import traceback
import struct
import ResultsParser
import SelectProteins
import Learning
from Utils import *
Initialize()

class Defaults:
    MQScoreWeight = 0.3
    DeltaScoreWeight = 1.5
    ###########################
    BlindMQScoreWeight = 0.3
    BlindDeltaScoreWeight = 1.5
    
    ###########################
    

BLIND_MOD_PENALTY = 1.0
MIN_MQSCORE = -10.0

# Parse the scores from at most this many output files.  
MAX_RESULTS_FILES_TO_PARSE = 100

BIN_MULTIPLIER = 10.0
SQRT2PI = math.sqrt(2 * math.pi)

Cof = [76.18009172947146, -86.50532032941677,
    24.01409824083091, -1.231739572450155, 
    0.1208650973866179e-2, -0.5395239384952e-5]

class Bag:
    pass

class FScoreParser(ResultsParser.ResultsParser):
    def __init__(self):
        
        self.VerboseFlag = 0
        self.MQScoreWeight = Defaults.MQScoreWeight
        self.DeltaScoreWeight = Defaults.DeltaScoreWeight
        self.BlindFlag = 0
        self.MaxDeltaScoreGap = -3.5
        self.SplitByCharge = 0
        self.Columns = ResultsParser.Columns()
        ResultsParser.ResultsParser.__init__(self)

    def ReadDeltaScoreDistribution(self, FilePath):
        """
        Read delta-scores from a file, to compute the average delta-score.
        If passed a directory, iterate over all results files in the directory.
        """
        #
        self.AllSpectrumCount2 = 0
        self.AllSpectrumCount3 = 0
        self.MeanDeltaScore2 = 0
        self.MeanDeltaScore3 = 0
        self.ProcessResultsFiles(FilePath, self.ReadDeltaScoreDistributionFromFile, MAX_RESULTS_FILES_TO_PARSE)
        
        if self.SplitByCharge == 1:
            self.MeanDeltaScore2 /= max(1, self.AllSpectrumCount2)
            self.MeanDeltaScore3 /= max(1, self.AllSpectrumCount3)
            if self.VerboseFlag:
                print "Mean delta score ch1..2: %s over %s spectra"%(self.MeanDeltaScore2, self.AllSpectrumCount2)
                print "Mean delta score ch3: %s over %s spectra"%(self.MeanDeltaScore3, self.AllSpectrumCount3)
            if not self.MeanDeltaScore2:
                self.MeanDeltaScore2 = 0.001
            if not self.MeanDeltaScore3:
                self.MeanDeltaScore3 = 0.001
        else:
            self.MeanDeltaScore = (self.MeanDeltaScore2 + self.MeanDeltaScore3)/(max(1,self.AllSpectrumCount2+self.AllSpectrumCount3))
            if self.VerboseFlag:
                print "Mean delta score: %s over %s spectra"%(self.MeanDeltaScore, self.AllSpectrumCount2+self.AllSpectrumCount3)

    def ReadDeltaScoreDistributionFromFile(self, FilePath):
        "Read delta-scores from a single file, to compute the average delta-score."
        print "Read delta-score distribution from %s..."%FilePath
        try:
            File = open(FilePath, "rb")
        except:
            traceback.print_exc()
            return
        OldSpectrum = None
        for FileLine in File.xreadlines():
            # Skip header lines and blank lines
            if FileLine[0] == "#":
                self.Columns.initializeHeaders(FileLine)
                continue
            if not FileLine.strip():
                continue
            Bits = list(FileLine.split("\t"))
            if len(Bits) <= self.Columns.getIndex("DeltaScore"):
                continue
            try:
                Charge = int(Bits[self.Columns.getIndex("Charge")])
                MQScore = float(Bits[self.Columns.getIndex("MQScore")])
                DeltaScore = float(Bits[self.Columns.getIndex("DeltaScore")])
                Peptide = GetPeptideFromModdedName(Bits[self.Columns.getIndex("Annotation")])
                Spectrum = (os.path.basename(Bits[self.Columns.getIndex("SpectrumFile")]), Bits[self.Columns.getIndex("Scan#")])
            except:
                traceback.print_exc()
                print Bits
                continue # header line
            if Spectrum == OldSpectrum:
                continue
            
            OldSpectrum = Spectrum
            
            if DeltaScore < 0:
                print "## Warning: DeltaScore < 0!", Spectrum, FilePath
                print DeltaScore
                print MQScore
                print Bits
                raw_input()
                continue
            if Charge < 3:
                self.AllSpectrumCount2 += 1
                self.MeanDeltaScore2 += DeltaScore
                
            else:
                self.AllSpectrumCount3 += 1
                self.MeanDeltaScore3 += DeltaScore
        File.close()            
    def WriteMatchesForSpectrum(self, MatchesForSpectrum, OutFile):
        
        for Match in MatchesForSpectrum:
            # Skip short matches:
            Length = len(Match.Peptide.Aminos)
            
            if self.SplitByCharge:
                if Match.Charge < 3:
                    CurrMeanDeltaScore = self.MeanDeltaScore2
                else:
                    CurrMeanDeltaScore = self.MeanDeltaScore3

            else:
                CurrMeanDeltaScore = self.MeanDeltaScore

            WeightedScore = self.MQScoreWeight * Match.MQScore + self.DeltaScoreWeight * (Match.DeltaScore / CurrMeanDeltaScore)
            ScoreBin = int(round(WeightedScore * BIN_MULTIPLIER))
            
            Match.Bits[self.Columns.getIndex("F-Score")] = "%s"%WeightedScore
    
            OutFile.write(string.join(Match.Bits, "\t"))
            OutFile.write("\n")

    def WriteFixedScores(self, OutputPath):
       
        self.WriteScoresPath = OutputPath
        # Make the output directory, if it doesn't exist already.
        # Assume: OutputPath is a directory if ReadScoresPath is a directory,
        # and OutputPath is a file if ReadScoresPath is a file.
        if os.path.isdir(self.ReadScoresPath):
            DirName = OutputPath
        else:
            DirName = os.path.split(OutputPath)[0]
        try:
            os.makedirs(DirName)
        except:
            pass
        self.ProcessResultsFiles(self.ReadScoresPath, self.WriteFixedScoresFile)
        

    def WriteFixedScoresFile(self, Path):
        if os.path.isdir(self.ReadScoresPath):
            OutputPath = os.path.join(self.WriteScoresPath, os.path.split(Path)[1])
        else:
            OutputPath = self.WriteScoresPath
        
        try:
            InFile = open(Path, "rb")
            OutFile = open(OutputPath, "wb")
            LineCount = 0
            
            OldSpectrum = None
            MatchesForSpectrum = []
            for FileLine in InFile:
                # Lines starting with # are comments (e.g. header line), and are written out as-is:
                if FileLine[0] == "#":
                    self.Columns.initializeHeaders(FileLine)
                    OutFile.write(FileLine)
                    continue
                Bits = list(FileLine.strip().split("\t"))
                Match = Bag()
                try:
                    Match.Bits = Bits
                    Match.Charge = int(Bits[self.Columns.getIndex("Charge")])
                    Match.MQScore = float(Bits[self.Columns.getIndex("MQScore")])
                    Match.DeltaScore = float(Bits[self.Columns.getIndex("DeltaScore")])
                    Match.Peptide = GetPeptideFromModdedName(Bits[self.Columns.getIndex("Annotation")])
                    Match.ProteinName = Bits[self.Columns.getIndex("Protein")]
                except:
                    continue
                LineCount += 1
                Spectrum = (Bits[0], Bits[1])
                if Spectrum != OldSpectrum:
                    self.WriteMatchesForSpectrum(MatchesForSpectrum, OutFile)
                    MatchesForSpectrum = []
                OldSpectrum = Spectrum
                MatchesForSpectrum.append(Match)
            # Finish the last spectrum:
            self.WriteMatchesForSpectrum(MatchesForSpectrum, OutFile)
            InFile.close()
            OutFile.close()
            
            
        except:
            traceback.print_exc()
            print "* Error filtering annotations from '%s' to '%s'"%(Path, OutputPath)

    def Run(self):
        self.ReadDeltaScoreDistribution(self.ReadScoresPath)
        self.WriteFixedScores(self.WriteScoresPath)

    def ParseCommandLine(self, Arguments):
        (Options, Args) = getopt.getopt(Arguments, "r:w:cvb")
        OptionsSeen = {}

        for (Option, Value) in Options:
            OptionsSeen[Option] = 1
            if Option == "-b":
                self.BlindFlag = 1
                self.MQScoreWeight = Defaults.BlindMQScoreWeight
                self.DeltaScoreWeight = Defaults.BlindDeltaScoreWeight
                
            elif Option == "-r":
                self.ReadScoresPath  = Value
            elif Option == "-w":
                self.WriteScoresPath = Value
            elif Option == "-c":
                self.SplitByCharge = 1
            elif Option == "-v":
                self.VerboseFlag = 1
            else:
                print "** Unknown option:", Option, Value
        # Check validity of options:
        if not OptionsSeen.has_key("-r") or not OptionsSeen.has_key("-w"):
            print "* Error: Missing Arguments"
            return 0
        # No major problems - return TRUE for success.
        return 1

UsageInfo = """
ComputeFScore.py - Compute FScore based on match quality score (MQScore) and delta score.  
Write out an updated results file.

Required Parameters:
 -r [FILENAME] Read results from filename (and fit the probability mixture
    model to these results).  If the option value is a directory, we'll read
    all the results-files from the directory.
 -w [FILENAME] Write re-scored results to a file.
 
Optional Parameters:
 -c Split by charge (compute the FScore separately for charge 1 and 2, and for charge 3.
 -b Results are from a blind search (not recommended)

Internal use only:
 -v Verbose output (for debugging)

    
Example:
  ComputeFScore.py -r ShewanellaResults -w ShewanellaFiltered -c
"""

def Main(Parser = None):
    global MAX_RESULTS_FILES_TO_PARSE
    
    if not Parser:
        Parser = FScoreParser()
        Result = Parser.ParseCommandLine(sys.argv[1:])
        if not Result:
            print UsageInfo
            return
        Parser.Run()
    
if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except:
        print "psyco not found - running without optimization"
    #TestMain()
    Main()
