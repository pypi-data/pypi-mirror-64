#Title:          PTMChooserLM.py
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
Low-memory-usage version of PTMChooser.
"""
import sys
import getopt
import struct
import types
import traceback
import os
import time
import Label
import MakeImage
import ExplainPTMs
from Utils import *
Initialize()
        
UsageInfo = """PTMChooser - Parse database search output, and select a parsimonious
  set of PTMs to explain the results.

Required parameters:
  -r [FileName]: Results file to parse.  If a directory is specified,
    then ALL files in the directory shall be parsed.
  -d [FileName]: Database .trie file searched

Optional parameters:  
  -s [Dir]: Summary directory to write findings to (default: PTMSummary)
  -v [value]: p-value cutoff.  Annotations with inferior p-values are
    discarded
  -l [count]: Maximum number of lines to read from the results file(s).
    Use this option to preview full results quickly.
  -p Generate PTM frequency matrix.  This option detects common,
    non-site-specific modifications such as oxidized methionine.  It is
    not well-suited to finding point mutations. 
  
Options for PTM site mode:
  -i Generate spectrum images for the representative spectra for
    each site
  -w [value]: p-value cutoff for selecting a site-specific PTM.
    Defaults to the value of -v; cannot be larger.
  -c Size of the protecting group on cysteine residues (defaults to 57).
  -t Maximum sites to report (defaults to 1000)
  -m Minimum size of mass delta (defaults to 3).  Mass differences of
    less than three daltons on ion trap spectra are most likely due
    to incorrect parent mass reporting, and so are filtered.
  -k [file]: File enumerating known PTMs, such as M+16.  Used to override
    name reporting.
"""

MaxLineCount = None # by default, read the entire results file.  Override with -l option.

class SiteClass:
    "For a putative PTM."
    def __init__(self):
        self.Residue = "" # M1, Q155, that sort of thing
        self.DBPos = None
        self.Mass = None
        self.BestPeptides = [] # sorted list (pvalue, -score, peptide) for the best 10 hits
        self.BestModlessPeptides = [] # sorted list (pvalue, -score, peptide) for the best 10 hits
        self.BestOtherModPeptides = [] # sorted list (pvalue, -score, peptide) for the best 10 hits
        self.ModdedSpecies = {}
        self.AnnotationCount = 0
        self.ModlessAnnotationCount = 0
        self.OtherModAnnotationCount = 0
        self.AA = "X"
        # Count how many annotations use N-terminus, middle, C-terminus.
        self.TerminalCount = [0, 0, 0]

class PTMClass:
    "For known PTMs"
    def __init__(self, Mass):
        self.Mass = Mass
        self.AA = {}
        self.Terminus = ""
        self.Name = str(Mass)
    def GetNameWithLink(self):
        return self.Name
    def BuildPTModClass(self):
        self.PTMod = PTModClass("%+d"%self.Mass)
        self.PTMod.Mass = self.Mass
        self.PTMod.Bases = self.AA
    
class Processor:
    def __init__(self):
        # Cutoff for using spectra to propose a new modification:
        self.PValueCutoff = 0.05
        # Cutoff for reporting spectra:
        self.PValueReportCutoff = 0.08
        self.SiteList = []
        self.PTMFrequencyMatrix = {} # (DBPos, Mass)->Count
        self.PTMBestScoreMatrix = {} # (DBPos, Mass)->BestScore
        self.NTerminalFlag = 0
        self.PTMSummaryDir = "PTMSummary"
        self.DB = ""
        self.MinSpectraForSite = 1 # can override
        self.MaxSiteCount = 1000 # can override
        self.GenerateSpectrumImagesFlag = 0 # disabled by default
        self.CysteineProtection = 57
        self.MinimumPTMSize = 3
        self.DeltaScoreCutoff = -2
        self.MQScoreCutoff = -3
        # how many peptides to report for a PTM:
        self.ReportPeptideCount = 10
        self.KnownPTMFileName = None
        self.KnownPTMs = []
        self.KnownPTMDict = {} # (AA, Mass, Terminus) -> PTMClass instance
        self.BuildPTMFrequencyMatrix = 0
        self.MinimumPeptideLength = 7
    def ReadKnownPTMs(self):
        if not self.KnownPTMFileName:
            return
        if not os.path.exists(self.KnownPTMFileName):
            print "** Known PTM file '%s' not found, ignoring!"%self.KnownPTMFileName
            return
        File = open(self.KnownPTMFileName, "rb")
        # Parse a line of the form: mod,+88,*,nterminal
        for FileLine in File.xreadlines():
            FileLine = FileLine.strip()
            if not FileLine:
                continue
            Bits = FileLine.split(",")
            if len(Bits)<3:
                continue
            if Bits[0].lower() != "mod":
                continue
            if len(Bits) > 3:
                PTMType = Bits[3]
            else:
                PTMType = "opt"
            if PTMType[:3].lower() == "fix":
                continue
            Mass = int(Bits[1])
            PTM = PTMClass(Mass)
            Aminos = Bits[2]
            if Aminos == "*":
                Aminos = "ACDEFGHIKLMNPQRSTVWY"
            for Amino in Aminos:
                PTM.AA[Amino] = 1
            if PTMType.lower() == "nterminal":
                PTM.Terminus = "N"
            if PTMType.lower() == "cterminal":
                PTM.Terminus = "C"
            if len(Bits) > 4:
                PTM.Name = Bits[4]
            self.KnownPTMs.append(PTM)
            PTM.BuildPTModClass()
            for Amino in Aminos:
                Key = (Amino, int(round(PTM.Mass)), PTM.Terminus)
                self.KnownPTMDict[Key] = PTM
                if PTM.Terminus == "":
                    # A non-terminal PTM is still legal at a terminus:
                    Key = (Amino, int(round(PTM.Mass)), "C")
                    self.KnownPTMDict[Key] = PTM
                    Key = (Amino, int(round(PTM.Mass)), "N")
                    self.KnownPTMDict[Key] = PTM
                    
    def ReadSpectrumAnnotations(self, FileName):
        "Parse annotations from a file (or a directory containing many results files)"
        self.LinesReadCount = 0
        self.AnnotationFileName = FileName
        if not os.path.exists(FileName):
            print "* Error in PTMChooser: Results file '%s' does not exist!"%FileName
            return
        if os.path.isdir(FileName):
            print "Parsing results files from directory %s..."%FileName
            SubFileNames = os.listdir(FileName)
            SubFileNames.sort()
            for SubFileNameIndex in range(len(SubFileNames)):
                SubFileName = SubFileNames[SubFileNameIndex]
                print "File %s/%s: %s"%(SubFileNameIndex, len(SubFileNames), SubFileName)
                Path = os.path.join(FileName, SubFileName)
                if os.path.isdir(Path):
                    print "Skip subdirectory %s"%Path
                else:
                    self.ReadSpectrumAnnotationsFromFile(Path)
                if MaxLineCount != None and self.LinesReadCount > MaxLineCount:
                    break                
        else:
            self.ReadSpectrumAnnotationsFromFile(FileName)
    def ReadPTMWitnesses(self, FileName):
        self.LinesReadCount = 0
        Path = os.path.join(self.PTMSummaryDir, "PTMAnnotations.txt")
        self.OutputAnnotationFile = open(Path, "wb")
        "Parse annotations from a file (or a directory containing many results files)"
        self.AnnotationFileName = FileName
        if not os.path.exists(FileName):
            print "* Error in PTMChooser: Results file '%s' does not exist!"%FileName
            return
        if os.path.isdir(FileName):
            print "Parsing results files from directory %s..."%FileName
            SubFileNames = os.listdir(FileName)
            for SubFileNameIndex in range(len(SubFileNames)):
                SubFileName = SubFileNames[SubFileNameIndex]
                print "File %s/%s: %s"%(SubFileNameIndex, len(SubFileNames), SubFileName)
                Path = os.path.join(FileName, SubFileName)
                if os.path.isdir(Path):
                    print "Skip subdirectory %s"%Path
                else:
                    self.ReadPTMWitnessesFromFile(Path)
                if MaxLineCount != None and self.LinesReadCount > MaxLineCount:
                    break
        else:
            self.ReadPTMWitnessesFromFile(FileName)
        self.OutputAnnotationFile.close()
    def TweakIncorrectEndpoints(self, Peptide):
        """
        Some putative modifications can be explained away by altering the endpoints of
        a peptide.  Examples include "K.AYGSTNPINIVR-71A.T" (right endpoint off by one),
        and "S.D+87KFSTVEQQASYGVGR.Q" (left endpoint off by one).  If we can explain away
        a modification by shifting the endpoint, then we'll do so, and in doing so get
        rid of a major source of delta-correct annotations.
        """
        if not Peptide.Modifications.keys():
            return Peptide 
        if self.KnownPTMFileName:
            # Check whether this peptide's PTMs match known PTMs. If so, tweak them
            # if necessary, and return the fixed PTMs.
            UnknownPTMFlag = 0
            NewModifications = {}
            for (Index, ModList) in Peptide.Modifications.items():
                Terminus = ""
                if Index == 0:
                    Terminus = "N"
                elif Index == len(Peptide.Aminos) - 1:
                    Terminus = "C"
                for Mod in ModList:
                    Key = (Peptide.Aminos[Index], Mod.Mass, Terminus)
                    if self.KnownPTMDict.has_key(Key):
                        # Acceptable!
                        if not NewModifications.has_key(Index):
                            NewModifications[Index] = []
                        NewModifications[Index].append(Mod)
                        continue
                    # Look for a nearby PTM:
                    MinIndex = max(0, Index - 3)
                    MaxIndex = min(len(Peptide.Aminos) - 1, Index + 4)
                    FoundFlag = 0
                    for NearIndex in range(MinIndex, MaxIndex):
                        if FoundFlag:
                            break
                        for NearMass in range(Mod.Mass - 1, Mod.Mass + 2):
                            NearTerminus = ""
                            if NearIndex == 0:
                                NearTerminus = "N"
                            elif NearIndex == len(Peptide.Aminos) - 1:
                                NearTerminus = "C"
                            Key = (Peptide.Aminos[NearIndex], NearMass, NearTerminus)
                            PTM = self.KnownPTMDict.get(Key, None)
                            if PTM:
                                # Aha!  This appears to be a delta-correct annotation.
                                if not NewModifications.has_key(NearIndex):
                                    NewModifications[NearIndex] = []
                                NewModifications[NearIndex].append(PTM.PTMod)
                                FoundFlag = 1
                                break
                    if not FoundFlag:
                        UnknownPTMFlag = 1 # known PTMs don't explain this annotation!
            # Loop is finished.  Did we see any with no explanation?
            if UnknownPTMFlag == 0:
                OldName = Peptide.GetFullModdedName()
                Peptide.Modifications = NewModifications
                NewName = Peptide.GetFullModdedName()
                #print "MASSAGED:", OldName, NewName
                return Peptide
        Q17Mod = PTModClass("-17")
        Q17Mod.Mass = -17
        #print "Tweaking incorrect annotation endpoints."
        EditThisAnnot = 0
        Len = len(Peptide.Aminos)
        if not Peptide.UnexplainedModList or len(Peptide.UnexplainedModList) != 1:
            return Peptide
        (AA, Mass, Pos, Terminus) = Peptide.UnexplainedModList[0]
        Endpoint = Peptide.DBPos + len(Peptide.Aminos)
        # Try moving endpoint left, to repair things like X.XXXX-57G.X:
        if Pos >= len(Peptide.Aminos) - 3:
            Diff = abs(Mass + Global.AminoMass[Peptide.Aminos[-1]])
            if Diff < 1.1:
                NewPeptide = GetPeptideFromModdedName(Peptide.Aminos[:-1])
                NewPeptide.DBPos = Peptide.DBPos
                NewPeptide.Prefix = Peptide.Prefix
                NewPeptide.Suffix = self.DB[Peptide.DBPos + len(NewPeptide.Aminos)]
                NewPeptide.UnexplainedModList = []
                return NewPeptide
        # Try moving startpoint left by 1-3 bases, to repair thinks like A.X+71XXX.X
        if (Pos < 3 and Mass > 0):
            ExtraMass = 0
            for AACount in range(1, 4):
                DBPos = Peptide.DBPos - AACount
                if (DBPos < 0):
                    break
                ExtraMass += Global.AminoMass.get(self.DB[DBPos], 9999)
                Diff = abs(Mass - ExtraMass)
                if Diff < 1.1:
                    NewPeptide = GetPeptideFromModdedName(self.DB[DBPos:Endpoint])
                    NewPeptide.DBPos = DBPos
                    NewPeptide.Prefix = self.DB[DBPos-1]
                    NewPeptide.Suffix = Peptide.Suffix
                    NewPeptide.UnexplainedModList = []
                    return NewPeptide
                # Consider using Q-17 here, instead of a spurious +111:
                if self.DB[DBPos] == "Q":
                    Diff = abs(Mass - (ExtraMass - 17))
                    if Diff < 1.1:
                        NewPeptide = GetPeptideFromModdedName(self.DB[DBPos:Endpoint])
                        NewPeptide.DBPos = DBPos
                        NewPeptide.Prefix = self.DB[DBPos-1]
                        NewPeptide.Suffix = Peptide.Suffix
                        NewPeptide.Modifications[0] = [Q17Mod]
                        NewPeptide.UnexplainedModList = [("Q", -17, 0, "N")]
                        NewPeptide.ComputeMasses()
                        return NewPeptide
        # Try moving endpoint right by 1-3 bases, to repair things like X.XXX+128.K
        if (Pos > len(Peptide.Aminos) - 3 and Mass > 0):
            ExtraMass = 0
            for AACount in range(1, 4):
                DBPos = Endpoint + AACount - 1
                if (DBPos >= len(self.DB)):
                    break
                ExtraMass += Global.AminoMass.get(self.DB[DBPos], 9999)
                Diff = abs(Mass - ExtraMass)
                if Diff < 1.1:
                    NewPeptide = GetPeptideFromModdedName(self.DB[Peptide.DBPos:DBPos + 1])
                    NewPeptide.DBPos = Peptide.DBPos
                    NewPeptide.Prefix = Peptide.Prefix
                    NewPeptide.Suffix = self.DB[DBPos + 1]
                    NewPeptide.UnexplainedModList = []
                    return NewPeptide
        return Peptide
    def ReadPTMWitnessesFromFile(self, FileName):
        """
        Read annotations (again!) from the specified file.  This time around, we know
        which PTM sites we accept, and we count how many spectra are present.
        """
        try:
            File = open(FileName, "rb")
        except:
            print "* Error in PTMChooser: Cannot open results file '%s'!"%FileName
            return
        LineNumber = 0
        AnnotationCount = 0
        OldSpectrumName = None
        AnnotatedFlag = 0
        File = open(FileName, "r")
        for FileLine in File.xreadlines():
            LineNumber += 1
            self.LinesReadCount += 1
            if LineNumber%10000 == 0:
                print "Line#%s %s annotations accepted"%(LineNumber, AnnotationCount)
                sys.stdout.flush()
                if MaxLineCount != None and self.LinesReadCount > MaxLineCount:
                    break
            if FileLine[0]=="#":
                continue # skip comment-line                
            Bits = FileLine.strip().split("\t")
            ##################################################################
            # Skip invalid lines, or poor annotations:
            if len(Bits)<16:
                # This isn't a valid annotation line!
                continue
            try:
                MQScore = float(Bits[5])
                PValue = float(Bits[10])
                DeltaScore = float(Bits[11])
            except:
                print "** Warning: Invalid annotation line in %s line %s"%(FileName, LineNumber)
                continue
            if PValue > self.PValueCutoff or DeltaScore < self.DeltaScoreCutoff or MQScore < self.MQScoreCutoff:
                continue
            SpectrumName = (Bits[0], Bits[1])
            if SpectrumName != OldSpectrumName:
                # It's a new spectrum; reset the AnnotatedFlag
                AnnotatedFlag = 0
            OldSpectrumName = SpectrumName
            if AnnotatedFlag:
                continue                
            Peptide = GetPeptideFromModdedName(Bits[2][2:-2])
            Peptide.UnexplainedModList = []
            if len(Peptide.Aminos) < self.MinimumPeptideLength:
                continue # Short peptides are too likely to be spurious!  (Length 1-4 is rubbish, 5 is marginal)
            ##################################################################
            Peptide.MQScore = MQScore
            Peptide.DeltaScore = float(Bits[12])
            Peptide.PValue = PValue
            Peptide.SpectrumName = Bits[0].replace("/","\\").split("\\")[-1]
            Peptide.SpectrumPath = Bits[0]
            Peptide.ScanNumber = Bits[1]
            Peptide.ProteinName = Bits[3]
            Peptide.ScanByteOffset = Bits[15]
            Peptide.DBPos = self.DB.find(Peptide.Aminos)
            Peptide.Prefix = Bits[2][0]
            Peptide.Suffix = Bits[2][-1]
            if Peptide.DBPos == -1:
                print "** Warning: Annotation '%s' for spectrum '%s' not found in database!"%(Peptide.Aminos, SpectrumName)
                continue
            # Accept modless peptides immediately:
            if len(Peptide.Modifications.keys()) == 0:
                self.AcceptPTMWitness(Peptide, Bits)
                AnnotatedFlag = 1
                AnnotationCount += 1
                continue
            # Fixup endpoints, and if we removed all mods, accept:
            Peptide = self.TweakIncorrectEndpoints(Peptide)
            if len(Peptide.Modifications.keys()) == 0:
                self.AcceptPTMWitness(Peptide, Bits)
                AnnotatedFlag = 1
                AnnotationCount += 1
                continue
            # Check to see whether all the PTMs in the peptide are correct,
            # or at least delta-correct.  Note that SiteDict contains
            # "shadow" entries already!
            OKSiteList = []
            InvalidPTM = 0
            for (Index, ModList) in Peptide.Modifications.items():
                DBPos = Peptide.DBPos + Index
                for Mod in ModList:
                    Site = self.SiteDict.get((DBPos, Mod.Mass))
                    # Check that Site.DBPos is in the range [Peptide.DBPos, Peptide.DBpos + len(Peptide.Aminos)),
                    # because Site.DBPos must actually fall within the peptide!
                    if Site and Site.DBPos >= Peptide.DBPos and Site.DBPos <= (Peptide.DBPos + len(Peptide.Aminos) - 1):
                        OKSiteList.append((Site, Index))
                        continue
##                    # We didn't find anything at (DBPos, Mod.Mass), so consider shadows:
##                    MinDBPos = DBPos - min(Index, 3)
##                    MaxDBPos = DBPos + min(3, len(Peptide.Aminos) - Index - 1)
##                    FoundFlag = 0
##                    for NearMass in (Mod.Mass - 1, Mod.Mass, Mod.Mass + 2):
##                        if FoundFlag:
##                            break
##                        for NearDBPos in range(MinDBPos, MaxDBPos):
##                            Site = self.SiteDict.get((NearDBPos, NearMass))
##                            if Site:
##                                OKSiteList.append((Site, Index))
##                                FoundFlag = 1
##                                print "Accept close:", DBPos, Mod.Mass, Site.DBPos, Site.Mass, Peptide.GetFullModdedName()
##                                break
##                    if not FoundFlag:
                    InvalidPTM = 1
                    break
            if not InvalidPTM:
                for (Site, Index) in OKSiteList:
                    self.AcceptPTMWitness(Peptide, Bits, Site)
                AnnotationCount += 1
                AnnotatedFlag = 1
    def AcceptPTMWitness(self, Peptide, Bits, AnnotatedSite = None):
        """
        Second pass: We found a legal peptide annotation.  If Index==None and AnnotatedSite==None,
        the peptide is unmodified.  Otherwise AnnotatedSite is a legal PTM which this
        peptide uses (although it may need tweaking!)  
        """
        Bits = list(Bits)
        # Add extra bits for the modification site:
        if AnnotatedSite:
            Bits.append(str(AnnotatedSite.Residue))
            Bits.append(str(AnnotatedSite.Mass))
        else:
            Bits.append("")
            Bits.append("")
        # Add extra bit for the ORIGINAL annotation:
        Bits.append(Bits[2])
        # Tweak the peptide annotation, if necessary:
        DBStart = Peptide.DBPos
        DBEnd = Peptide.DBPos + len(Peptide.Aminos)
        ScoredTuple = (Peptide.PValue, -Peptide.MQScore, Peptide)
        if AnnotatedSite == None:
            # Note this unmodified spectrum overlapping modified sites:
            for Site in self.SiteList:
                if Site.DBPos >= DBStart and Site.DBPos < DBEnd:
                    Site.BestModlessPeptides.append(ScoredTuple)
                    Site.BestModlessPeptides.sort()
                    Site.BestModlessPeptides = Site.BestModlessPeptides[:self.ReportPeptideCount]
                    Site.ModlessAnnotationCount += 1
        else:
            # Tweak the protein if necessary:
            TweakFlag = 0
            for (Index, ModList) in Peptide.Modifications.items():
                if TweakFlag:
                    break
                for Mod in ModList:
                    ModDBPos = Peptide.DBPos + Index
                    if (ModDBPos != AnnotatedSite.DBPos or Mod.Mass != AnnotatedSite.Mass):
                        # This isn't the same as the modification.  If it's CLOSE, then
                        # tweak it:
                        if abs(AnnotatedSite.DBPos - ModDBPos) <= 3 and abs(AnnotatedSite.Mass - Mod.Mass) < 1.2:
                            ModList.remove(Mod)
                            if not ModList:
                                del Peptide.Modifications[Index]
                            NewIndex = AnnotatedSite.DBPos - Peptide.DBPos
                            if not Peptide.Modifications.has_key(NewIndex):
                                Peptide.Modifications[NewIndex] = []
                            NewMod = PTModClass("%+d"%AnnotatedSite.Mass)
                            NewMod.Mass = AnnotatedSite.Mass
                            Peptide.Modifications[NewIndex].append(NewMod)
                            break
            # Note this spectrum:
            AnnotatedSite.BestPeptides.append(ScoredTuple)
            AnnotatedSite.BestPeptides.sort()
            AnnotatedSite.BestPeptides = AnnotatedSite.BestPeptides[:self.ReportPeptideCount]
            AnnotatedSite.AnnotationCount += 1
            AnnotatedSite.ModdedSpecies[Peptide.Aminos] = AnnotatedSite.ModdedSpecies.get(Peptide.Aminos, 0) + 1
            # Note the terminus:
            PeptidePos = Peptide.DBPos - AnnotatedSite.DBPos
            if PeptidePos == 0:
                AnnotatedSite.TerminalCount[0] += 1
            elif PeptidePos == len(Peptide.Aminos) - 1:
                AnnotatedSite.TerminalCount[2] += 1
            else:
                AnnotatedSite.TerminalCount[1] += 1
            # And note this alternative modification for other sites:
            for Site in self.SiteList:
                if Site != AnnotatedSite and Site.DBPos >= DBStart and Site.DBPos < DBEnd:
                    Site.BestOtherModPeptides.append(ScoredTuple)
                    Site.BestOtherModPeptides.sort()
                    Site.BestOtherModPeptides = Site.BestOtherModPeptides[:self.ReportPeptideCount]
                    Site.OtherModAnnotationCount += 1
        Bits[2] = Peptide.GetFullModdedName()
        Str = string.join(Bits, "\t")
        self.OutputAnnotationFile.write(Str + "\n")
    def ReadSpectrumAnnotationsFromFile(self, FileName):
        """
        Parse annotations.  We've already verified that it's a file (not a directory) and it exists.
        ASSUMPTION: All annotations for the same spectrum appear consecutively. 
        """
        try:
            File = open(FileName, "rb")
        except:
            print "* Error in PTMChooser: Cannot open results file '%s'!"%FileName
            return
        LineNumber = 0
        AnnotationCount = 0
        OldSpectrumName = None
        AnnotatedFlag = 0
        MatrixEntryCount = 0
        File = open(FileName, "r")
        for FileLine in File.xreadlines():
            LineNumber += 1
            self.LinesReadCount += 1
            if LineNumber%10000 == 0:
                print "Line#%s %s modless %s matrix entries"%(LineNumber, AnnotationCount, MatrixEntryCount)
                sys.stdout.flush()
                if MaxLineCount != None and self.LinesReadCount > MaxLineCount:
                    break
            if FileLine[0]=="#":
                continue # skip comment-line                
            Bits = FileLine.strip().split("\t")
            ##################################################################
            # Skip invalid lines, or poor annotations:
            if len(Bits)<16:
                # This isn't a valid annotation line!
                continue
            try:
                MQScore = float(Bits[5])
                PValue = float(Bits[10])
                DeltaScore = float(Bits[11])
            except:
                print "** Warning: Invalid annotation line in %s line %s"%(FileName, LineNumber)
                continue
            if PValue > self.PValueCutoff or DeltaScore < self.DeltaScoreCutoff:
                ##print "%s Ignore match %s %s"%(LineNumber, PValue, DeltaScore) #%%%
                continue
            SpectrumName = (Bits[0], Bits[1])
            if SpectrumName != OldSpectrumName:
                # It's a new spectrum; reset the AnnotatedFlag
                AnnotatedFlag = 0
            OldSpectrumName = SpectrumName
            Peptide = GetPeptideFromModdedName(Bits[2][2:-2])
            Peptide.UnexplainedModList = None
            if len(Peptide.Aminos) < self.MinimumPeptideLength:
                ##print "%s Ignore short peptide %s"%(LineNumber, Bits[2]) #%%%
                continue # Short peptides are too likely to be spurious!  (Length 1-4 is rubbish, 5 is marginal)
            Peptide.Prefix = Bits[2][0]
            Peptide.Suffix = Bits[2][-1]
            ##################################################################
            # If this peptide is unmodified, then ignore any further (lower-scoring) peptides for
            # the same spectrum:
            Keys = Peptide.Modifications.keys()
            if len(Keys) == 0:
                AnnotatedFlag = 1
                AnnotationCount += 1
                ##print "%s Accept modless %s"%(LineNumber, Bits[2]) #%%%
                continue
            if AnnotatedFlag:
                continue
            Peptide.DBPos = self.DB.find(Peptide.Aminos)
            if Peptide.DBPos == -1:
                print "** Warning: Annotation '%s' for spectrum '%s' not found in database!"%(Peptide.Aminos, SpectrumName)
                continue
            UnknownPTMSeen = 0
            for (Index, ModList) in Peptide.Modifications.items():
                for Mod in ModList:
                    Terminus = None
                    if Index == 0:
                        Terminus = "N"
                    if Index == len(Peptide.Aminos)-1:
                        Terminus = "C"
                    Key = (Peptide.Aminos[Index], Mod.Mass, Index, Terminus)
                    if Peptide.UnexplainedModList == None:
                        Peptide.UnexplainedModList = []
                    Peptide.UnexplainedModList.append(Key)
                    Key = (Peptide.Aminos[Index], Mod.Mass, Terminus)
                    if not self.KnownPTMDict.has_key(Key):
                        UnknownPTMSeen = 1
            # Tweak any known mistakes in peptide annotation:
            Peptide = self.TweakIncorrectEndpoints(Peptide)
            # If it's modless now, note that and continue:
            if len(Peptide.Modifications.keys()) == 0:
                AnnotatedFlag = 1
                AnnotationCount += 1
                #print "%s Tweaked %s to %s"%(LineNumber, Bits[2], Peptide.GetFullModdedName()) #%%%
                continue
            # Accumulate entries in PTMFrequencyMatrix:
            for (Index, ModList) in Peptide.Modifications.items():
                for Mod in ModList:
                    if self.BuildPTMFrequencyMatrix:
                        Key = (Peptide.Aminos[Index], Mod.Mass)
                        self.PTMFrequencyMatrix[Key] = self.PTMFrequencyMatrix.get(Key, 0) + 1
                        self.PTMBestScoreMatrix[Key] = max(self.PTMBestScoreMatrix.get(Key, -999), MQScore)
                        if Index == 0:
                            Key = ("^", Mod.Mass)
                            self.PTMFrequencyMatrix[Key] = self.PTMFrequencyMatrix.get(Key, 0) + 1
                            self.PTMBestScoreMatrix[Key] = max(self.PTMBestScoreMatrix.get(Key, -999), MQScore)
                        if Index == len(Peptide.Aminos) - 1:
                            Key = ("$", Mod.Mass)
                            self.PTMFrequencyMatrix[Key] = self.PTMFrequencyMatrix.get(Key, 0) + 1
                            self.PTMBestScoreMatrix[Key] = max(self.PTMBestScoreMatrix.get(Key, -999), MQScore)
                    else:
                        Key = (Peptide.DBPos + Index, Mod.Mass)
                        self.PTMFrequencyMatrix[Key] = self.PTMFrequencyMatrix.get(Key, 0) + 1
                        self.PTMBestScoreMatrix[Key] = max(self.PTMBestScoreMatrix.get(Key, -999), MQScore)
                        #print "%s Peptide %s %s key %s"%(LineNumber, Bits[2], Peptide.GetFullModdedName(), Key) #%%%
                        MatrixEntryCount += 1
            if not UnknownPTMSeen:
                AnnotatedFlag = 1 # ignore all subsequent annotations
        File.close()
        return AnnotationCount
    def SelectSites(self):
        """
        Iterate: Find the largest entry in self.PTMFrequencyMatrix.  Remove entries
        from this cell and neighboring cells, and append a new SiteClass instance
        to self.SiteList.  Stop when the next entry is too small, or when we have
        already generated enough sites.
        """
        while (1):
            BestCount = 0
            BestMQScore = -999
            BestKey = None
            for (Key, Count) in self.PTMFrequencyMatrix.items():
                (AA, Mass) = Key
                MQScore = self.PTMBestScoreMatrix.get(Key, -999)
                # Filter out +1, -1 here:
                if abs(Mass) >= self.MinimumPTMSize:
                    if (Count > BestCount) or (Count == BestCount and MQScore > BestMQScore):
                        BestCount = Count
                        BestMQScore = MQScore
                        BestKey = Key
                        #print BestCount, BestMQScore, Key
            if not BestKey:
                break
            if BestCount < self.MinSpectraForSite:
                print "Next PTM explains %s<%s spectra, stop now"%(BestCount, self.MinSpectraForSite)
                break
            (DBPos, Mass) = BestKey
            Site = SiteClass()
            Site.DBPos = DBPos
            Site.Mass = Mass
            (ProteinName, ProteinNumber, ResidueNumber) = self.GetProteinInfo(DBPos)
            Site.ProteinName = ProteinName
            Site.Residue = "%s%s"%(self.DB[DBPos], ResidueNumber)
            Site.AA = self.DB[DBPos]
            print "%s Accept PTM: %s on %s from %s"%(BestCount, Mass, Site.Residue, ProteinName[:40])
            self.SiteList.append(Site)
            if len(self.SiteList) >= self.MaxSiteCount:
                print "Acquired %s sites - stop now"%self.MaxSiteCount
                break
            # Remove matrix entries:
            for NearPos in range(DBPos - 3, DBPos + 4):
                if NearPos in (DBPos-1, DBPos, DBPos+1):
                    Masses = (Mass-1, Mass, Mass+1)
                else:
                    Masses = (Mass,)
                for NearMass in Masses:
                    Key = (NearPos, NearMass)
                    if self.PTMFrequencyMatrix.has_key(Key):
                        print "Absorb adjacent entry:", Key
                        del self.PTMFrequencyMatrix[Key]
        # Keep a dictionary of the accepted sites, for easy lookup:
        self.SiteDict = {}
        for Site in self.SiteList:
            for NearPos in range(Site.DBPos - 3, Site.DBPos + 4):
                if NearPos in (DBPos-1, DBPos, DBPos+1):
                    Masses = (Mass-1, Mass, Mass+1)
                else:
                    Masses = (Mass,)
                for NearMass in range(Site.Mass - 1, Site.Mass + 2):
                    Key = (Site.DBPos, NearMass)
                    if not self.SiteDict.has_key(Key):
                        self.SiteDict[Key] = Site
    def GetProteinInfo(self, DBPos):
        "Return the protein# and the residue# for this file position."
        for Index in range(1, len(self.ProteinNames)):
            if self.ProteinStartPositions[Index] > DBPos:
                ResidueNumber = DBPos - self.ProteinStartPositions[Index - 1] + 1
                #return (self.ProteinNames[Index - 1], ResidueNumber)
                return (self.ProteinNames[Index - 1], Index - 1, ResidueNumber)
        # The match must come from the last protein:
        ResidueNumber = DBPos - self.ProteinStartPositions[-1] + 1
        return (self.ProteinNames[-1], len(self.ProteinNames) - 1, ResidueNumber)
    def OutputResults(self):
        # Remove existing files AllSiteSummary and AllSiteDetails, so we start them fresh:
        Path = os.path.join(self.PTMSummaryDir, "AllSiteSummary.html")
        print Path
        if os.path.exists(Path):
            os.remove(Path)
        Path = os.path.join(self.PTMSummaryDir, "AllSiteDetails.html")
        print Path
        if os.path.exists(Path):
            os.remove(Path)
        # Sort the sites by annotation-count:
        SortedSites = []
        for Site in self.SiteList:
            if Site.AnnotationCount:
                SortedSites.append((Site.AnnotationCount, Site))
        SortedSites.sort()
        SortedSites.reverse()
        self.TotalSpectraForPTM = {} # (AA, Mass) -> Count
        self.SitesForPTM = {} # (AA, Mass) -> list of Site instances
        self.TerminusForPTM = {} # (AA, Mass) -> terminus-tuple
        for (Count, Site) in SortedSites:
            # Note this site in the PTM lists:
            Key = (Site.AA, Site.Mass)
            if not self.SitesForPTM.has_key(Key):
                self.SitesForPTM[Key] = []
            self.SitesForPTM[Key].append(Site)
            self.TotalSpectraForPTM[Key] = self.TotalSpectraForPTM.get(Key, 0) + Site.AnnotationCount
            if not self.TerminusForPTM.has_key(Key):
                self.TerminusForPTM[Key] = [0, 0, 0]
            for X in range(3):
                self.TerminusForPTM[Key][X] += Site.TerminalCount[X]
            # Write a table summarizing this sites to the PTM page, and to the
            # overall details page:
            HTML = self.WriteSiteSummary(Site, 1)
            DetailsFilePath = os.path.join(self.PTMSummaryDir, "%s%sDetails.html"%(Site.AA, Site.Mass))
            if len(self.SitesForPTM[Key]) == 1:
                File = open(DetailsFilePath, "w")
            else:
                File = open(DetailsFilePath, "a")
            File.write(HTML)
            File.close()
            File = open(os.path.join(self.PTMSummaryDir, "AllSiteDetails.html"), "a")
            File.write(HTML)
            File.close()
            #
        #######################################
        # Write the index file, which summarizes things by PTM (possibly several
        # different sites correspond to each row)
        IndexFilePath = os.path.join(self.PTMSummaryDir, "index.html")
        IndexFile = open(IndexFilePath, "w")
        IndexFile.write("<h3>PTM Summary Report</h3>\n")
        if not SortedSites:
            IndexFile.write("<b> * * * No PTMs found * * *</b>\n")
            return
        IndexFile.write("<a href=\"AllSiteSummary.html\">Summary table for all sites</a>")
        IndexFile.write("&nbsp;&nbsp;&nbsp;<a href=\"AllSiteDetails.html\">Details for all sites</a><br><br>\n")
        IndexFile.write("<table><tr><td><b>Terminus</b></td><td><b>AA</b></td><td><b>Mass<br>delta</b></td>")
        IndexFile.write("<td><b>Spectra</b></td><td><b>Sites</b></td><td><b>Top-site<br>spectra</b></td>")
        IndexFile.write("<td><b>Results</b></td><td><b>Possible explanations</b></td></tr>\n")
        ############
        SortedPTMs = []
        for (Key, Count) in self.TotalSpectraForPTM.items():
            SortedPTMs.append((Count, Key))
        SortedPTMs.sort()
        SortedPTMs.reverse()
        for (Count, Key) in SortedPTMs:
            (AA, Mass) = Key
            if self.TotalSpectraForPTM.get(Key, 0) < 1:
                continue # Skip this, we don't have a single spectra for it!
            print "Write summary for %s %s"%(AA, Mass)
            # Decide whether we think it's terminal:
            N = self.TerminusForPTM[Key][0]
            Body = self.TerminusForPTM[Key][1]
            C = self.TerminusForPTM[Key][2]
            if N > Body:
                Terminus = "N"
            elif C > Body:
                Terminus = "C"
            else:
                Terminus = ""
            ######################################################################
            # Write terse records for each site for this PTM:
            HTML = self.WriteTerseSummary(self.SitesForPTM[Key])
            File = open(os.path.join(self.PTMSummaryDir, "%s%sSummary.html"%(AA, Mass)), "w")
            File.write(HTML)
            File.close()
            File = open(os.path.join(self.PTMSummaryDir, "AllSiteSummary.html"), "a")
            File.write(HTML)
            File.close()
            ######################################################################
            # Add links to the index page:
            DetailLink = "%s%sDetails.html"%(AA, Mass)
            SummaryLink = "%s%sSummary.html"%(AA, Mass)
            ExplanationList = self.GetKnownPTMExplanation(AA, Mass, Terminus)
            if AA == "C":
                ExplanationList.extend(ExplainPTMs.GetExplanation(AA, Mass, Terminus, BasePTM = self.CysteineProtection))
            else:
                ExplanationList.extend(ExplainPTMs.GetExplanation(AA, Mass, Terminus))
            if len(ExplanationList) == 0:
                Explanations = "Unknown"
            else:
                Explanations = ""
                for Entry in ExplanationList[:3]:
                    Explanations += "%s, "%Entry.GetNameWithLink()
                Explanations = Explanations[:-2] # remove trailing comma+space
            IndexFile.write("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(\
                Terminus, AA, Mass, self.TotalSpectraForPTM[Key], len(self.SitesForPTM[Key]),
                self.SitesForPTM[Key][0].AnnotationCount))
            IndexFile.write("<td><a href=\"%s\">Details</a> <a href=\"%s\">Summary</a></td><td>%s</td></tr>\n"%(DetailLink, SummaryLink, Explanations))
        IndexFile.close()
    def GetKnownPTMExplanation(self, AA, Mass, Terminus):
        """
        Return a list of known PTMs that fit this description.  Mostly just so
        that we can report their correct names.
        """
        ExplanationList = []
        for PTM in self.KnownPTMs:
            if PTM.Mass != Mass:
                continue
            if PTM.Terminus == Terminus and PTM.AA.has_key(AA):
                ExplanationList.append(PTM)
        return ExplanationList
    def WriteTerseSummary(self, SiteList):
        if not SiteList:
            return ""
        HTML = ""
        AA = self.DB[SiteList[0].DBPos]
        Mass = SiteList[0].Mass
        HTML += "<h3>Sites for %+d on %s</h3>"%(Mass, AA)
        TotalSpectra = 0
        for Site in SiteList:
            TotalSpectra += Site.AnnotationCount
        HTML += "<b>%s spectra in all<br>\n"%TotalSpectra
        HTML += "<table><tr><td><b>Protein</b></td><td><b>Residue</b></td><td><b>Spectra</b></td><td><b>Species</b></td><td><b>Unmodified</b></td></tr>\n"
        for Site in SiteList:
            (ProteinName, ProteinIndex, ResidueNumber) = self.GetProteinInfo(Site.DBPos)
            Residue = "%s%s"%(AA, ResidueNumber)
            HTML += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(ProteinName, Residue, Site.AnnotationCount, len(Site.ModdedSpecies.keys()), Site.ModlessAnnotationCount)
        HTML += "</table>"
        return HTML
            
    def WriteSiteSummaryLine(self, Notes, Peptide):
        Annotation = Peptide.GetFullModdedName()
        #print "WriteSiteSummaryLine: Notes %s Pval %s score %s Pep %s"%(Notes, Peptide.PValue, Peptide.MQScore, Peptide.GetFullModdedName())
        WroteLine = 0
        HTML = ""
        if self.GenerateSpectrumImagesFlag:
            try:
                ImageFileName = "%s%s.png"%(Peptide.SpectrumName, Peptide.ScanNumber)
                ImagePath = os.path.join(self.PTMSummaryDir, "Images", ImageFileName)
                SpecFilePath = self.GetSpectrumFilePath(Peptide.SpectrumPath)
                FileName = "%s:%s"%(SpecFilePath, Peptide.ScanByteOffset)
                LabeledSpectrum = Label.LabelDTAFile(Peptide, FileName, None)
                Maker = MakeImage.MSImageMaker()
                Maker.ConvertSpectrumToImage(LabeledSpectrum, ImagePath, Peptide)
                HTML = "<tr><td>%s</td><td>%s</td><td>%s</td><td><a href=\"Images/%s\">%s</a></td>"%(Notes, Peptide.SpectrumName, Peptide.ScanNumber, ImageFileName, Annotation)
                HTML += "<td>%s</td><td>%s</td><td>%s</td></tr>\n"%(Peptide.MQScore, Peptide.DeltaScore, Peptide.PValue)
                WroteLine = 1
            except:
                # Error generating image - perhaps the file isn't available on disk?
                print SpecFilePath, Peptide.ScanByteOffset, Peptide.SpectrumPath, Peptide.ScanNumber
                traceback.print_exc()
                #pass
        if not WroteLine:
            HTML = "<tr><td>%s</td><td>%s</td><td>%s</td>"%(Notes, Peptide.SpectrumName, Peptide.ScanNumber)
            HTML += "<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(Annotation, Peptide.MQScore, Peptide.DeltaScore, Peptide.PValue)
        return HTML
    def WriteSiteSummary(self, Site, VerboseFlag):
        """
        Write out a verbose summary of this putative modification site to the specified file.
        """
        ModlessPeptides = []
        OtherModPeptides = []
        Site.SpectrumCount = 0
        # Sort the peptide species:
        SortedSpecies = []
        for (Aminos, Count) in Site.ModdedSpecies.items():
            SortedSpecies.append((Count, Aminos))
        SortedSpecies.sort()
        ###############################################################
        # Report up to 10 annotations per species:
        HTML = ""
        (ProteinName, ProteinIndex, ResidueNumber) = self.GetProteinInfo(Site.DBPos)
        SortedSpecies.sort()
        HTML += "<h3>%+d on Residue %s of protein %s</h3>\n"%(Site.Mass, Site.Residue, ProteinName)
        HTML += "<b>%s spectra</b> annotated this residue with %+d <br>\n"%(Site.AnnotationCount, Site.Mass)
        HTML += "<b>%s spectra</b> cover this site without modification<br>\n"%Site.ModlessAnnotationCount
        if Site.OtherModAnnotationCount:
            HTML += "<b>%s spectra</b> containing different modifications cover this site<br>\n"%Site.OtherModAnnotationCount
        HTML += "Details for the top-scoring spectra follow:<br>\n"
        HTML += "<table><tr><td><b>Notes</b></td><td><b>Spectrum</b></td>"
        HTML += "<td><b>Scan</b></td><td><b>Annotation</b></td>"
        HTML += "<td><b>MQScore</b></td><td><b>Delta-score</b></td><td><b>p-value</b></td></tr>\n"
        for (Dummy1, Dummy2, Peptide) in Site.BestPeptides:
            HTML += self.WriteSiteSummaryLine("", Peptide)
        ######################################################
        # Without PTM:
        ModlessPeptides.sort()
        for (Dummy1, Dummy2, Peptide) in Site.BestModlessPeptides:
            HTML += self.WriteSiteSummaryLine("No PTM", Peptide)
        ######################################################
        # Other PTMs:
        OtherModPeptides.sort()
        for (Dummy1, Dummy2, Peptide) in Site.BestOtherModPeptides:
            HTML += self.WriteSiteSummaryLine("Other PTM", Peptide)
        HTML += "</table><hr>"
        return HTML                
    def ReadDatabase(self, DBPath):
        try:
            File = open(DBPath, "rb")
        except:
            print "** Unable to open database file '%s'!"%DBPath
            raise
        self.DB = File.read()
        File.close()
        # Read the database index, if found:
        self.ProteinStartPositions = []
        self.ProteinNames = []
        IndexPath = os.path.splitext(DBPath)[0] + ".index"
        if os.path.exists(IndexPath):
            File = open(IndexPath, "rb")
            while (1):
                Data = File.read(92)
                if not Data:
                    break
                Tuple = struct.unpack("<qi80s", Data)
                self.ProteinStartPositions.append(Tuple[1])
                Name = Tuple[2]
                NullPos = Name.find(chr(0))
                if NullPos != -1:
                    Name = Name[:NullPos]
                self.ProteinNames.append(Name)
            File.close()
        else:
            print "** Error: Database index file '%s' not found!"%IndexPath
    def GetSpectrumFilePath(self, FileName):
        # this can be overridden, if spectra are moved
        #Bits = FileName.replace("/", "\\").split("\\")
        #return os.path.join(r"E:\ms\OMICS04", Bits[-2], Bits[-1])
        return FileName 
    def PerformIterativeNSSSelection(self, MinExplanationCount):
        self.NSSPTMList = []
        Matrix = self.PTMFrequencyMatrix.copy()
        while (1):
            SortedList = []
            for (Key, Count) in Matrix.items():
                if Key[0] in ("$","^"):
                    continue
                SortedList.append((Count, Key))
            SortedList.sort()
            SortedList.reverse()
            if not SortedList:
                return
            (Count, Key) = SortedList[0]
            if Count < MinExplanationCount:
                return
            # Grab nearby 'shadow' entries:
            (AA, Mass) = Key
            for NearMass in (Mass - 1, Mass + 1):
                NearKey = (AA, NearMass)
                Matrix[Key] += Matrix.get(NearKey, 0)
                Matrix[NearKey] = 0
            Matrix[Key] = 0 # selected already
            PTM = PTMClass(Mass)
            PTM.AA = AA
            self.NSSPTMList.append(PTM)
    def PerformNonSiteSpecificPTMSelection(self, ResultsFileName):
        print "\n\nRead spectrum annotations:"
        self.ReadSpectrumAnnotations(ResultsFileName)
        # Output the PTM frequency matrix:
        FileName = os.path.join(self.PTMSummaryDir, "NonSiteSpecific.html")
        HTMLFile = open(FileName, "w")
        self.WriteHTMLMatrix(self.PTMFrequencyMatrix, HTMLFile)
        #####
        FileName = os.path.join(self.PTMSummaryDir, "NonSiteSpecific.txt")
        TextFile = open(FileName, "w")
        self.WriteTextMatrix(self.PTMFrequencyMatrix, TextFile)
        TextFile.close()
        #######################################################
        # Now, perform iterative PTM selection.  This will tidy up the matrix significantly.
        # We'll stop selecting PTMs when the next one explains fewer than X entries, where X
        # is twice the median matrix entry:
        OrderedEntries = []
        for (Key, Count) in self.PTMFrequencyMatrix.items():
            if Key[0] not in "^$":
                OrderedEntries.append(Count)
        OrderedEntries.sort()
        MinExplanationCount = self.LightShadingCutoff #max(OrderedEntries[len(OrderedEntries)/2] * 4, 10)
        self.PerformIterativeNSSSelection(MinExplanationCount)
        #######################################################
        # Write details on each PTM.
        HTMLFile.write("<hr>")
        #self.GeneratePTMFrequencyMatrix(1)
        HTMLFile.write("<h3>Putative modifications</h3>\n")
        # Get a list of PTMs, sorted by the number of spectra they explain:
        SortedList = []
        for NSSPTM in self.NSSPTMList:
            if NSSPTM.AA:
                Count = self.PTMFrequencyMatrix.get((NSSPTM.AA, NSSPTM.Mass), 0)
            else:
                if NSSPTM.Terminus == "N":
                    Count = self.PTMFrequencyMatrix.get(("^", NSSPTM.Mass), 0)
                elif NSSPTM.Terminus == "C":
                    Count = self.PTMFrequencyMatrix.get(("$", NSSPTM.Mass), 0)
            SortedList.append((Count, NSSPTM))
        SortedList.sort()
        SortedList.reverse()
        for (Count, NSSPTM) in SortedList:
            if Count < self.LightShadingCutoff:
                continue # garbage PTM
            ModStr = "%s%+d"%(NSSPTM.AA, NSSPTM.Mass)
            HTMLFile.write("Modification %s applied to %s spectra<br>\n"%(ModStr, Count))
            HTMLFile.write("&nbsp;&nbsp;&nbsp;")
            if NSSPTM.AA == "C":
                ExplanationList = ExplainPTMs.GetExplanation(NSSPTM.AA, NSSPTM.Mass, "", BasePTM = self.CysteineProtection)
            else:
                ExplanationList = ExplainPTMs.GetExplanation(NSSPTM.AA, NSSPTM.Mass, "")
            if not ExplanationList:
                HTMLFile.write("(unknown mass-delta)<br><br>\n")
            else:
                Str = ""
                for Explanation in ExplanationList:
                    Str += "%s, "%Explanation.GetNameWithLink()
                Str = Str[:-2] # remove trailing comma
                HTMLFile.write("Possible annotations: %s<br><br>\n"%Str)
##        #######################################################
##        # Write the cleaned-up matrix:
##        #self.GeneratePTMFrequencyMatrix(0)
##        TabbedMatrixFileName = os.path.join(self.PTMSummaryDir, "ProcessedMatrix.txt")
##        TabbedMatrixFile = open(TabbedMatrixFileName, "w")
##        self.WriteTextMatrix(self.PTMFrequencyMatrix, TabbedMatrixFile)
##        TabbedMatrixFile.close()
##        HTMLFile.write("<h3>Resultant PTM frequency matrix</h3>")
##        self.WriteHTMLMatrix(self.Matrix, HTMLFile)
##        # Finish and cleanup:
##        Path = os.path.join(self.PTMSummaryDir, "NonSiteSpecificAnnotations.txt")
##        self.OutputAnnotations(Path)
##        HTMLFile.close()
        
    def WriteHTMLMatrix(self, Matrix, HTMLFile):
        """
        Write PTM frequency matrix to a webpage, with shading on well-filled cells.
        """
        AAList = "^ACDEFGHIKLMNPQRSTVWY$"
        # First, let's decide what the cutoffs are for heavy, medium, and light shading.
        EntryList = []
        for (Key, Value) in Matrix.items():
            if Key[0] not in ("^$"):
                EntryList.append(Value)
        EntryList.sort()
        if not len(EntryList):
            HTMLFile.write("<b>** Error - no entries, so no PTM matrix written<br>\n")
            self.LightShadingCutoff = 1
            return
        MaximumEntry = EntryList[-1]
        HeavyShadingCutoff = max(10, MaximumEntry / 2.0)
        MediumShadingCutoff = max(5, MaximumEntry / 10.0)
        self.LightShadingCutoff = max(2, MaximumEntry / 100.0)
        MedianEntry = EntryList[len(EntryList) / 2]
        Str = "Maximum entry %s, median entry %s.<br>\nRows containing an entry of <b>%d</b> or larger are displayed.<br>\n"
        HTMLFile.write(Str%(MaximumEntry, MedianEntry, int(self.LightShadingCutoff + 1.0)))
        HTMLFile.write("<table><tr>")
        ####################
        # Write the header:
        HeaderRow = ""
        HeaderRow += "<td><b>Mass</b></td>"
        for AA in AAList:
            if AA == "^":
                AA = "&nbsp;(N)"
            elif AA == "$":
                AA = "&nbsp;(C)"
            else:
                AA = "&nbsp;&nbsp;&nbsp;" + AA
            HeaderRow += "<td><b>%s</b></td>"%AA
        HeaderRow += "</tr>\n"
        HTMLFile.write(HeaderRow)
        # Get mass range:
        MinimumMass = 999
        MaximumMass = -999
        for Key in Matrix.keys():
            MinimumMass = min(MinimumMass, Key[1])
            MaximumMass = max(MaximumMass, Key[1])
        # Write out one row for each feasible mass:
        RowsPrinted = 0
        for Mass in range(MinimumMass, MaximumMass + 1):
            # Get the total number of entries on this row.  If it's low, then skip the row!
            EntriesForThisRow = 0
            BestEntryThisRow = 0
            for AA in AAList[1:-1]:
                EntriesForThisRow += Matrix.get((AA, Mass), 0)
                BestEntryThisRow = max(BestEntryThisRow, Matrix.get((AA, Mass), 0))
            # Only display a row if it has an entry equal to at least twice the median cell:
            if BestEntryThisRow <= self.LightShadingCutoff:
                continue
            HTMLFile.write("<tr><td>%s</td>"%Mass)
            for AA in AAList:
                Key = (AA, Mass)
                Count = Matrix.get(Key, 0)
                if Count < 10:
                    CountStr = "&nbsp;&nbsp;&nbsp;%s"%Count
                elif Count < 100:
                    CountStr = "&nbsp;&nbsp;%s"%Count
                elif Count < 1000:
                    CountStr = "&nbsp;%s"%Count
                else:
                    CountStr = "%s"%Count
                if Count > HeavyShadingCutoff:
                    HTMLFile.write("<td bgcolor=\"#999999\">%s</td>"%CountStr)
                elif Count > MediumShadingCutoff:
                    HTMLFile.write("<td bgcolor=\"#bbbbbb\">%s</td>"%CountStr)
                elif Count > self.LightShadingCutoff:
                    HTMLFile.write("<td bgcolor=\"#dddddd\">%s</td>"%CountStr)
                else:
                    HTMLFile.write("<td>%s</td>"%CountStr)
            HTMLFile.write("</tr>\n")
            RowsPrinted += 1
            if RowsPrinted%25 == 0:
                HTMLFile.write(HeaderRow)
        HTMLFile.write("</table>\n")
    def WriteTextMatrix(self, Matrix, TabbedMatrixFile):
        """
        Write PTM frequency matrix, in tab-delimited format (for easy parsing).  Similar code
        in WriteHTMLMatrix, for easy reading by eye.
        """
        AAList = "^ACDEFGHIKLMNPQRSTVWY$"
        HeaderLine = "Mass\t"
        for AA in AAList:
            if AA == "^":
                AA = "(N)"
            if AA == "$":
                AA = "(C)"            
            HeaderLine += "%s\t"%AA
        HeaderLine += "\n"
        TabbedMatrixFile.write(HeaderLine)
        MinimumMass = 999
        MaximumMass = -999
        for Key in Matrix.keys():
            MinimumMass = min(MinimumMass, Key[1])
            MaximumMass = max(MaximumMass, Key[1])
        # Write out one row for each feasible mass:
        for Mass in range(MinimumMass, MaximumMass + 1):
            Str = "%s\t"%Mass
            for AA in AAList:
                Key = (AA, Mass)
                Str += "%s\t"%Matrix.get(Key, 0)
            Str += "\n"
            TabbedMatrixFile.write(Str)
        
        
def Main(PTMProcessor):
    global MaxLineCount
    if len(sys.argv) < 3:
        print UsageInfo
        sys.exit(1)
    ResultsFileName = None
    #PTMProcessor = Processor()
    (Options, Args) = getopt.getopt(sys.argv[1:], "r:d:s:c:iv:w:t:l:m:k:p")
    OptionsSeen = {}
    for (Option, Value) in Options:
        OptionsSeen[Option] = 1
        if Option == "-r":
            # -r results file(s)
            ResultsFileName = Value
        elif Option == "-c":
            # -c Mass of cysteine protecting group (57 by default)
            PTMProcessor.CysteineProtection = int(Value)
        elif Option == "-k":
            # -k File specifying known, non-site-specific PTMs
            PTMProcessor.KnownPTMFileName = Value
        elif Option == "-t":
            # -t Max number of sites to report (1000 by default)
            PTMProcessor.MaxSiteCount = int(Value)
        elif Option == "-v":
            # -v p-value cutoff (0.01 by default)
            PTMProcessor.PValueReportCutoff = float(Value)
            if PTMProcessor.PValueReportCutoff <= 0 or PTMProcessor.PValueReportCutoff > 1:
                print "** Error: Invalid p-value cutoff '%s'"%Value
                print UsageInfo
                sys.exit(1)
        elif Option == "-w":
            # -w p-value cutoff for the spectra used to pick a ptm (same as -v by default)
            PTMProcessor.PValueCutoff = float(Value)
            if PTMProcessor.PValueCutoff <= 0 or PTMProcessor.PValueCutoff > 1:
                print "** Error: Invalid p-value cutoff '%s'"%Value
                print UsageInfo
                sys.exit(1)
        elif Option == "-d":
            # -d database
            print "Read database:", Value
            Path = FixupPath(Value)
            PTMProcessor.ReadDatabase(Path)
        elif Option == "-s":
            # -s SummaryDir
            PTMProcessor.PTMSummaryDir = Value
        elif Option == "-i":
            # -i -> generate spectrum images
            PTMProcessor.GenerateSpectrumImagesFlag = 1
        elif Option == "-l":
            # -l -> Maximum number of lines to read in
            MaxLineCount = int(Value)
        elif Option == "-m":
            # -m -> Minimum PTM size (defaults to 2)
            PTMProcessor.MinimumPTMSize = int(Value)
        elif Option == "-p":
            # -p -> Generate PTM frequency matrix
            PTMProcessor.BuildPTMFrequencyMatrix = 1
        else:
            print "Option not understood: '%s' '%s'"%(Option, Value)
    if not OptionsSeen.get("-r"):
        print "** Please specify a search results file (-r)"
        print UsageInfo
        sys.exit(1)
    if not OptionsSeen.get("-d"):
        print "** Please specify a database file (-d)"
        print UsageInfo
        sys.exit(1)
    if not OptionsSeen.get("-w"):
        PTMProcessor.PValueCutoff = PTMProcessor.PValueReportCutoff
    # Make necessary directories:
    try:
        os.makedirs(PTMProcessor.PTMSummaryDir)
    except:
        pass
    try:
        Dir = os.path.join(PTMProcessor.PTMSummaryDir, "Images")
        os.makedirs(Dir)
    except:
        pass
    if PTMProcessor.BuildPTMFrequencyMatrix:
        PTMProcessor.PerformNonSiteSpecificPTMSelection(ResultsFileName)
        return
    PTMProcessor.ReadKnownPTMs()
    # Read annotations, generate the PTM frequency matrix:
    print "\n\nRead spectrum annotations:"
    sys.stdout.flush()
    PTMProcessor.ReadSpectrumAnnotations(ResultsFileName)
    # Select sites by 'peak finding' among large matrix entries:
    print "\n\nSelect sites:"
    sys.stdout.flush()
    PTMProcessor.SelectSites()
    # Re-read annotations, keeping a few in memory:
    print "\n\nRead PTM witnesses:"
    sys.stdout.flush()    
    PTMProcessor.ReadPTMWitnesses(ResultsFileName)
    # Output our findings:
    print "\n\nOutput results:"
    sys.stdout.flush()    
    PTMProcessor.OutputResults()
    
if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except:
        print "(psyco optimization system not loaded - running normally)"
    Main(Processor())
