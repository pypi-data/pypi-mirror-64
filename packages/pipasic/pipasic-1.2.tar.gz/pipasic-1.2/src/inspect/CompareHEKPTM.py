#Title:          CompareHEKPTM.py
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
Compare the collection of PTMs found in the HEK293 data-set with the PTMs reported
in external databases (HPRD and Uniprot)
"""

import os
import getopt
import string
import sys
import struct
import traceback
import cPickle
import xml.dom.minidom
import xml.sax.handler
from xml.dom.minidom import Node
from TrainPTMFeatures import FormatBits
from Utils import *
Initialize()

AminoAcidLetters = "ACDEFGHIKLMNPQRSTVWY"

# HEK options:
InspectOutputFileName = r"C:\Documents and Settings\swt\Desktop\SWTPapers\PTMScoring\SupplementalTables\STHEKSitesK2.txt"
IPIDatabasePath = os.path.join("Database", "IPISubDB.trie")
FDRPValueCutoff = 0.270065269846

# LENS options:
##InspectOutputFileName = r"C:\Documents and Settings\swt\Desktop\SWTPapers\PTMScoring\SupplementalTables\ST1LensSitesFullK2.txt"
##IPIDatabasePath = os.path.join("Database", "Lens99.trie")
##FDRPValueCutoff = 0.580962281

UniprotXMLFileName = r"F:\Uniprot\uniprot_sprot.xml"
HPRDDir = r"f:\ftproot\HPRD\HPRD_XML_010107\HPRD_XML_010107"

SkipModificationNames = {"proteolytic cleavage":1,
                         "disulfide bridge":1,
                         }


def GetXMLText(NodeList, Strip = 0):
    """
    Gets the text associated with an XML Node
    <a>RETURNS THIS TEXT </a>
    """
    BodyText = ""
    for Node in NodeList:
        if Node.nodeType == Node.TEXT_NODE:
            BodyText += Node.data
    if Strip: # strip all white space, those included below
        BodyText = BodyText.replace(" ","")
        BodyText = BodyText.replace("\r","")
        BodyText = BodyText.replace("\n","")
        BodyText = BodyText.replace("\t","")
    return BodyText

def FindDBLocations(DB, Aminos):
    """
    Find all occurrences of this peptide in the database.
    Return DB indices.
    """
    PrevPos = -1
    LocationList = []
    while (1):
        Pos = DB.find(Aminos, PrevPos + 1)
        if Pos == -1:
            break
        LocationList.append(Pos)
        PrevPos = Pos
    return LocationList


class CompareMaster:
    """
    This class keeps track of the proteins in the canonical HEK database,
    as well as the modifications from various sources.
    """ 
    def __init__(self):
        pass
    def InitializeModMasses(self):
        """
        Initialize self.ModMasses, which maps (lower-case) PTM names to masses.
        Because the list is rather long, it has been moved to a table in
        ExternalPTMNames.txt
        """
        self.ModMasses = {}
        File = open("ExternalPTMNames.txt", "rb")
        for FileLine in File.xreadlines():
            Bits = FileLine.split("\t")
            Bits = list(Bits)
            # Repair Excel's broken columns:
            if Bits[0][0] == '"':
                Bits[0] = Bits[0][1:-1]
            if FileLine[0] == "#" or len(Bits) < 2:
                continue
            Name = Bits[0].lower()
            Mass = int(Bits[1])
            self.ModMasses[Name] = Mass
        File.close()
    def LoadDatabase(self):
        self.ProteinPos = []
        self.DB = ""
        File = open(IPIDatabasePath, "rb")
        self.DB = File.read()
        File.close()
        PrevPos = -1
        while 1:
            NextPos = self.DB.find("*", PrevPos + 1)
            if NextPos == -1:
                break
            self.ProteinPos.append(PrevPos + 1)
            PrevPos = NextPos
        # Read protein names, too:
        IndexPath = os.path.splitext(IPIDatabasePath)[0] + ".index"
        BlockSize = struct.calcsize("qi80s")
        IndexFile = open(IndexPath, "rb")
        self.ProteinNames = []
        while 1:
            Block = IndexFile.read(BlockSize)
            if not Block:
                break
            Tuple = struct.unpack("qi80s", Block)
            self.ProteinNames.append(Tuple[2])
        
    def GetDBPosInfo(self, Pos):
        """
        Return (ProteinName, ProteinResidueNumber)
        """
        for ProteinIndex in range(len(self.ProteinPos)):
            ProteinStart = self.ProteinPos[ProteinIndex]
            if Pos < ProteinStart:
                continue
            if ProteinIndex < len(self.ProteinPos) - 1:
                ProteinEnd = self.ProteinPos[ProteinIndex + 1]
                if Pos >= ProteinEnd:
                    continue
            else:
                pass
            ResidueNumber = Pos - ProteinStart
            return (self.ProteinNames[ProteinIndex], ResidueNumber)
    def FindPeptideLocations(self, Aminos):
        """
        Given an amino acid string, find all locations in the database.
        Return a list of the form (ProteinIndex, ResidueNumber)
        """
        PrevPos = -1
        LocationList = []
        while (1):
            Pos = self.DB.find(Aminos, PrevPos + 1)
            if Pos == -1:
                break
            # Which protein does Pos lie in?
            LowIndex = 0
            HighIndex = len(self.ProteinPos) - 1
            # Pos >= ProteinPos[LowIndex] and Pos < ProteinPos[HighIndex]
            # Special case - last protein:
            if Pos > self.ProteinPos[HighIndex]:
                ProteinID = HighIndex
                ResidueNumber = Pos - self.ProteinPos[HighIndex]
            else:
                while (1):
                    if LowIndex + 1 == HighIndex:
                        ProteinID = LowIndex
                        ResidueNumber = Pos - self.ProteinPos[LowIndex]
                        break
                    MidIndex = (LowIndex + HighIndex) / 2
                    if Pos >= self.ProteinPos[MidIndex]:
                        LowIndex = MidIndex
                    else:
                        HighIndex = MidIndex
            LocationList.append((ProteinID, ResidueNumber))
            PrevPos = Pos
        return LocationList
    def ParsePTMsInspect5(self):
        return self.ParsePTMsInspect(0.05)
    def ParsePTMsInspect(self, PValueThreshold = None):
        if not PValueThreshold:
            PValueThreshold = FDRPValueCutoff
        PTMDictionary = {}
        File = open(InspectOutputFileName, "rb")
        LineNumber = 0
        for FileLine in File.xreadlines():
            LineNumber += 1
            if LineNumber % 1000 == 0:
                print "Line %s..."%LineNumber
            if FileLine[0] == "#":
                continue
            Bits = FileLine.strip().split("\t")
            try:
                ProteinName = Bits[FormatBits.ProteinName]
                #DeltaMass = int(Bits[FormatBits.ModificationMass])
                DeltaMass = int(Bits[49])
                Annotation = Bits[FormatBits.Peptide]
                PeptidePValue = Bits[FormatBits.ModelPValue]
                SitePValue = float(Bits[FormatBits.SitePValue])
                KnownAnnotation = Bits[FormatBits.KnownPTMAnnotation]
                KnownFlag = int(Bits[47])
                if KnownFlag:
                    KeepAnnotation = KnownAnnotation
                else:
                    KeepAnnotation = Annotation
                Peptide = GetPeptideFromModdedName(KeepAnnotation)
            except:
                traceback.print_exc()
                continue
            try:
                SitePValue = float(Bits[50])
            except:
                pass
            if PValueThreshold != None and SitePValue >= PValueThreshold:
                continue
            # If the protein is shuffled (protein name starts with XXX), ignore the PTM:
            if ProteinName[:3] == "XXX":
                continue
            if not Peptide.Modifications.keys():
                continue # it's actually unmodified!
            ModPos = Peptide.Modifications.keys()[0]
            FullAminos = Peptide.Aminos
            if Peptide.Prefix in AminoAcidLetters:
                FullAminos = Peptide.Prefix + FullAminos
            if Peptide.Suffix in AminoAcidLetters:
                FullAminos = FullAminos + Peptide.Suffix
            DBHitList = FindDBLocations(self.DB, FullAminos)
            if not DBHitList:
                print "*** Warning: Peptide '%s' not found in database!"%FullAminos
                continue
            for DBPos in DBHitList:
                ModDBPos = DBPos + ModPos
                if Peptide.Prefix in AminoAcidLetters:
                    ModDBPos += 1
                if not PTMDictionary.has_key(ModDBPos):
                    PTMDictionary[ModDBPos] = []
                # Avoid adding redundant records:
                FoundFlag = 0
                for (OldMass, OldName) in PTMDictionary[ModDBPos]:
                    if OldMass == DeltaMass:
                        FoundFlag = 1
                        break
                if not FoundFlag:
                    PTMDictionary[ModDBPos].append((DeltaMass, "%+d"%DeltaMass))
                    print ModDBPos, DeltaMass, KeepAnnotation
        File.close() 
        self.PTMDictionaryInspect = PTMDictionary
        print "Inspect parse: Found %s modified residues in %s file lines"%(len(PTMDictionary.keys()), LineNumber)
        return PTMDictionary
    def ParsePTMsUniprot(self):
        SAXParser = xml.sax.make_parser()
        UniprotParser = UniprotXMLParser(self.DB)
        UniprotParser.ModMasses = self.ModMasses
        SAXParser.setContentHandler(UniprotParser)
        print "Parse %s..."%UniprotXMLFileName
        SAXParser.parse(UniprotXMLFileName)
        self.PTMDictionaryUniprot = UniprotParser.PTMDictionary
        print "Reporting UNKNOWN PTM names..."
        UniprotParser.ReportUnknownPTMs("UnknownPTMs.Uniprot.txt")
        return self.PTMDictionaryUniprot
    def ParsePTMsHPRD(self):
        SAXParser = xml.sax.make_parser()
        HPRDParser = HPRDXMLParser(self.DB)
        HPRDParser.ModMasses = self.ModMasses
        SAXParser.setContentHandler(HPRDParser)
        #print "Parse %s..."%HPRDXMLFileName
        FileNames = os.listdir(HPRDDir)
        for FileNameIndex in range(len(FileNames)):
            FileName = FileNames[FileNameIndex]
            print "%s/%s: %s"%(FileNameIndex, len(FileNames), FileName)
            XMLFilePath = os.path.join(HPRDDir, FileName)
            try:
                SAXParser.parse(XMLFilePath)
            except:
                traceback.print_exc()
                print "* Error parsing %s"%XMLFilePath
        self.PTMDictionaryHPRD = HPRDParser.PTMDictionary
        print "Reporting UNKNOWN PTM names..."
        HPRDParser.ReportUnknownPTMs("UnknownPTMs.HPRD.txt")
        return self.PTMDictionaryHPRD
    def ComparePTMDictionariesOneWay(self, DictA, DictB,
        MaxMassDiff = 2, MaxPosDiff = 2, LimitMassFlag = None):
        """
        Determine how many of A's PTMs are found in B:
        """
        HitA = 0
        MissA = 0
        TotalA = 0
        for (Pos, ModList) in DictA.items():
            for (Mass, Name) in ModList:
                # LimitMassFlag == 1: Skip very small and very large PTMs.
                if LimitMassFlag == 1:
                    if abs(Mass) < 5 or abs(Mass) >= 250:
                        continue
                elif LimitMassFlag != None:
                    if Mass != LimitMassFlag:
                        continue
                TotalA += 1
                HitFlag = 0
                AllowedPositions = [Pos]
                for Diff in range(1, MaxPosDiff + 1):
                    AllowedPositions.append(Pos + Diff)
                    AllowedPositions.append(Pos - Diff)
                for NearPos in AllowedPositions:
                    List = DictB.get(NearPos, [])
                    for (OtherMass, OtherName) in List:
                        if abs(Mass - OtherMass) <= MaxMassDiff:
                            HitFlag = 1
                if HitFlag:
                    HitA += 1
                else:
                    MissA += 1
        return (HitA, MissA, TotalA)
    def ComparePTMDictionaries(self, DictA, DictB,
        MaxMassDiff = 2, MaxPosDiff = 2, LimitMassFlag = None):
        """
        Simple comparison: How many sites are shared between these two
        dictionaries of PTMs?
        """
        (HitA, MissA, TotalA) = self.ComparePTMDictionariesOneWay(DictA, DictB,
            MaxMassDiff, MaxPosDiff, LimitMassFlag)
        (HitB, MissB, TotalB) = self.ComparePTMDictionariesOneWay(DictB, DictA,
            MaxMassDiff, MaxPosDiff, LimitMassFlag)
        print "ComparePTMDictionaries:"
        SharedPercent = 100 * HitA / float(max(TotalA, 1))
        print "A: %s total.  %s (%.2f%%) shared, %s not shared)"%(TotalA, HitA, SharedPercent, MissA)
        SharedPercent = 100 * HitB / float(max(TotalB, 1))
        print "B: %s total.  %s (%.2f%%) shared, %s not shared)"%(TotalB, HitB, SharedPercent, MissB)
        OverallSharedPercent = (HitA + HitB) / float(max(1, TotalA + TotalB))
        print "Overall shared percent: %.2f"%(100 * OverallSharedPercent)
    def ParseAndOrPickle(self, ParseMethod, PickleFileName):
        """
        Parse PTMs from a file, OR unpickle them from a pre-parsed binary file.
        (Parsing is slow, so we do it just once)
        """
        if os.path.exists(PickleFileName):
            print "Loading PTM dictionary from %s..."%PickleFileName
            File = open(PickleFileName, "rb")
            Dictionary = cPickle.load(File)
            File.close()
        else:
            Dictionary = ParseMethod()
            print "Saving PTM dictionary to %s..."%PickleFileName
            File = open(PickleFileName, "wb")
            cPickle.dump(Dictionary, File)
            File.close()
        return Dictionary 
    def DebugReportPTMs(self):
        """
        For debugging purposes, print a file showing all the PTMs found in any source.
        """
        AllKeyDict = {}
        for Key in self.PTMDictionaryInspect.keys():
            AllKeyDict[Key] = 1
##        for Key in self.PTMDictionaryInspect5.keys():
##            AllKeyDict[Key] = 1
        for Key in self.PTMDictionaryHPRD.keys():
            AllKeyDict[Key] = 1
        for Key in self.PTMDictionaryUniprot.keys():
            AllKeyDict[Key] = 1
        AllKeys = AllKeyDict.keys()
        AllKeys.sort()
        for Key in AllKeys:
            DBStart = max(0, Key - 7)
            DBEnd = min(len(self.DB), Key + 8)
            Aminos = "%s.%s.%s"%(self.DB[DBStart:Key], self.DB[Key], self.DB[Key + 1:DBEnd])
            MassInspect = self.PTMDictionaryInspect.get(Key, "")
            #MassInspect5 = self.PTMDictionaryInspect5.get(Key, "")
            MassHPRD = self.PTMDictionaryHPRD.get(Key, "")
            MassUniprot = self.PTMDictionaryUniprot.get(Key, "")
            if MassHPRD == "" and MassUniprot == "":
                continue
            Str = "%s\t%s\t%s\t%s\t%s\t"%(Key, Aminos, MassInspect, MassHPRD, MassUniprot)
            print Str
    def DebugPrintDict(self, Dict):
        OverallCount = 0
        for (Key, List) in Dict.items():
            OverallCount += len(List)
        print "Overall count:", OverallCount
    def Main(self):
        self.LoadDatabase()
        self.InitializeModMasses()
        self.PTMDictionaryInspect = self.ParseAndOrPickle(self.ParsePTMsInspect, "PTMDictionaryInspect.pickle")
        #self.PTMDictionaryInspect5 = self.ParseAndOrPickle(self.ParsePTMsInspect5, "PTMDictionaryInspect5.pickle")
        self.PTMDictionaryHPRD = self.ParseAndOrPickle(self.ParsePTMsHPRD, "PTMDictionaryHPRD.pickle")
        self.PTMDictionaryUniprot = self.ParseAndOrPickle(self.ParsePTMsUniprot, "PTMDictionaryUniprot.pickle")
        print len(self.PTMDictionaryInspect.keys())
        #print len(self.PTMDictionaryInspect5.keys())
        for Dict in (self.PTMDictionaryInspect, self.PTMDictionaryHPRD, self.PTMDictionaryUniprot):
            self.DebugPrintDict(Dict)
        #self.DebugCountPTMs(Dict)
        print "\n\nUniprot and HPRD: EXACT"
        self.ComparePTMDictionaries(self.PTMDictionaryUniprot, self.PTMDictionaryHPRD, 0, 0, LimitMassFlag = None)
        print "\n\nUniprot and HPRD: EXACT, omit bad masses"
        self.ComparePTMDictionaries(self.PTMDictionaryUniprot, self.PTMDictionaryHPRD, 0, 0, LimitMassFlag = 1)
        print "\n\nUniprot and HPRD: omit bad masses"
        self.ComparePTMDictionaries(self.PTMDictionaryUniprot, self.PTMDictionaryHPRD, LimitMassFlag = 1)

##        print "\n\nHEK293 best and uniprot, omit bad masses"
##        self.ComparePTMDictionaries(self.PTMDictionaryInspect5, self.PTMDictionaryUniprot, LimitMassFlag = 1)
##        print "\n\nHEK293 best and hprd, omit bad masses"
##        self.ComparePTMDictionaries(self.PTMDictionaryInspect5, self.PTMDictionaryHPRD, LimitMassFlag = 1)
        print "\n\nHEK293 and uniprot, omit bad masses"
        self.ComparePTMDictionaries(self.PTMDictionaryInspect, self.PTMDictionaryUniprot, LimitMassFlag = 1)
        print "\n\nHEK293 and hprd, omit bad masses"
        self.ComparePTMDictionaries(self.PTMDictionaryInspect, self.PTMDictionaryHPRD, LimitMassFlag = 1)
        for KeyMass in (14, 28, 42, 80):
            print "\n\nUniprot and HPRD: Mass %s"%KeyMass
            self.ComparePTMDictionaries(self.PTMDictionaryUniprot, self.PTMDictionaryHPRD, LimitMassFlag = KeyMass)
            print "HEK293 and Uniprot, mass %s"%KeyMass
            self.ComparePTMDictionaries(self.PTMDictionaryInspect, self.PTMDictionaryUniprot, LimitMassFlag = KeyMass)
            print "HEK293 and HORD, mass %s"%KeyMass
            self.ComparePTMDictionaries(self.PTMDictionaryInspect, self.PTMDictionaryHPRD, LimitMassFlag = KeyMass)
            
        ################################################
        # Supplemental table: Inspect PTMs that match Uniprot *or* hprd
        self.ReportInspectMatchedSites()
    def ReportInspectMatchedSites(self):
        """
        Output a verbose report of all Inspect sites which were also seen in HPRD and/or uniprot.
        """
        HitA = 0
        MissA = 0
        TotalA = 0
        MaxPosDiff = 2
        MaxMassDiff = 3
        LimitMassFlag = 0
        ReportedAlreadyDict = {}
        FilterFlag = 1 #%%%
        if FilterFlag:
            OutputFile = open("HEKPTM-InspectAndDB.txt", "wb")
        else:
            OutputFile = open("HEKPTM-InspectAndDB.unfiltered.txt", "wb")
        for (Pos, ModList) in self.PTMDictionaryInspect.items():
            for (Mass, Name) in ModList:
                # LimitMassFlag == 1: Skip very small and very large PTMs.
                if LimitMassFlag == 1:
                    if abs(Mass) < 5 or abs(Mass) >= 250:
                        continue
                HPRDHitFlag = 0
                HPRDMass = ""
                HPRDName = ""
                UniprotHitFlag = 0
                UniprotMass = ""
                UniprotName = ""
                HPRDHitPos = ""
                UniprotHitPos = ""
                AllowedPositions = [Pos]
                for Diff in range(1, MaxPosDiff + 1):
                    AllowedPositions.append(Pos + Diff)
                    AllowedPositions.append(Pos - Diff)
                for NearPos in AllowedPositions:
                    List = self.PTMDictionaryHPRD.get(NearPos, [])
                    for (OtherMass, OtherName) in List:
                        if abs(Mass - OtherMass) <= MaxMassDiff:
                            HPRDHitFlag = 1
                            HPRDHitPos = NearPos
                            HPRDMass = OtherMass
                            HPRDName = OtherName
                    List = self.PTMDictionaryUniprot.get(NearPos, [])
                    for (OtherMass, OtherName) in List:
                        if abs(Mass - OtherMass) <= MaxMassDiff:
                            UniprotHitFlag = 1
                            UniprotHitPos = NearPos
                            UniprotMass = OtherMass
                            UniprotName = OtherName
                if HPRDHitFlag or UniprotHitFlag:
                    ReportMass = HPRDMass
                    HitPos = HPRDHitPos
                    if ReportMass == "":
                        ReportMass = UniprotMass
                        HitPos = UniprotHitPos
                    ReportKey = (HitPos, ReportMass)
                    if ReportedAlreadyDict.has_key(ReportKey):
                        if FilterFlag:
                            continue
                    ReportedAlreadyDict[ReportKey] = 1
                    #(ProteinName, ProteinResidue) = self.GetDBPosInfo(Pos)
                    (ProteinName, ProteinResidue) = self.GetDBPosInfo(HitPos)
                    Residue = self.DB[HitPos]
                    NearAminos = self.DB[HitPos - 10:HitPos + 11]
                    Str = "%s\t%s\t%s\t%s\t"%(Pos, Mass, ProteinName, ProteinResidue)
                    Str += "%s\t%s\t"%(Residue, NearAminos)
                    Str += "%s\t%s\t"%(HPRDMass, HPRDName)
                    #Str += "%s\t%s\t%s\t"%(HPRDHitPos, HPRDMass, HPRDName)
                    Str += "%s\t%s\t"%(UniprotMass, UniprotName)
                    #Str += "%s\t%s\t%s\t"%(UniprotHitPos, UniprotMass, UniprotName)
                    OutputFile.write(Str + "\n")
        OutputFile.close()
        
class UXStates:
    """
    States for the [U]niprot [X]ml parser.  State can change when we START or END a tag.
    Most of the time we're in the SKIP state. 
    """
    Skip = 0
    Sequence = 1
    Feature = 2
    Accession = 3

class TabularXMLParser(xml.sax.handler.ContentHandler):
    """
    Simple subclass of SAX XML parser: Employs dictionaries to look up the 
    handlers for tag start, tag end, body text.  Keeps a current State.
    """
    def __init__(self):
        self.startElement = self.StartElement
        self.endElement = self.EndElement
        self.characters = self.HandleCharacters
        self.State = None
        if not hasattr(self, "StartHandlers"):
            self.StartHandlers = {}
        if not hasattr(self, "EndHandlers"):
            self.EndHandlers = {}
        if not hasattr(self, "StringHandlers"):
            self.StringHandlers = {}
        xml.sax.handler.ContentHandler.__init__(self)
    def StartElement(self, Name, Attributes):
        Handler = self.StartHandlers.get(Name, None)
        if Handler:
            apply(Handler, (Attributes,))
    def EndElement(self, Name):
        Handler = self.EndHandlers.get(Name, None)
        if Handler:
            apply(Handler)
    def HandleCharacters(self, String):
        Handler = self.StringHandlers.get(self.State, None)
        if Handler:
            apply(Handler, (String,))


class PTMXMLParser(TabularXMLParser):
    """
    Simple subclass of TabularXMLParser, adding the ability to look up modification
    sites in self.DB; relies heavily on subclass methods!
    """
    def AddPendingPTMs(self):
        # Add pending PTMs:
        for (Name, Position) in self.PendingPTMs:
            #print "Pending PTM:", Name, Position
            # Get flanking amino acids:
            StartPos = max(0, Position - 7)
            EndPos = min(len(self.Sequence), Position + 8)
            # If we're next to the edge, extend farther in the other direction:
            Len = EndPos - StartPos
            if Len < 15:
                StartPos = max(0, EndPos - 16)
                Len = EndPos - StartPos
            if Len < 15:
                EndPos = min(len(self.Sequence), StartPos + 16)
                #StartPos = max(0, Position - 14)
            Aminos = self.Sequence[StartPos:EndPos]
            PrefixLength = Position - StartPos
            if len(Aminos) < 10:
                print "* Warning: Aminos %s...%s from %s not distinct enough!"%(StartPos, EndPos, self.Accession)
                print "Sequence length is %s, position is %s"%(len(self.Sequence), Position)
            # Determine the mass:
            LowerName = Name.lower()
            if SkipModificationNames.has_key(LowerName):
                continue                
            Mass = self.ModMasses.get(LowerName, 0)
            if Mass == 0:
                # Try removing any parenthetical portions:
                # Example: n6,n6,n6-trimethyllysine (alternate)
                ParenPos = LowerName.find("(")
                if ParenPos != -1:
                    PreParen = LowerName[:ParenPos].strip()
                    if SkipModificationNames.has_key(PreParen):
                        continue                
                    
                    #print "Try removing parens: '%s' to '%s'"%(LowerName, PreParen)
                    Mass = self.ModMasses.get(PreParen, 0)
            if Mass == 0:
                # Try the first bit of the mod, it might have the form "phosphoserine (by ck1)"
                #print "try first bit: '%s' to '%s'"%(LowerName, LowerName.split()[0])
                FirstBit = LowerName.split()[0]
                Mass = self.ModMasses.get(FirstBit, 0)
                if SkipModificationNames.has_key(FirstBit):
                    continue                                
            if Mass == 0:
                print "* Warning - mass not known for: %s (accession %s)"%(LowerName, self.Accession)
                if Position - 1 < 0 or Position - 1 >= len(self.Sequence):
                    print "Found on residue %s (ILLEGAL NUMBER)"%Position
                else:
                    print "  Found on residue %s%s"%(self.Sequence[Position - 1], Position)
                self.UnknownPTMDictionary[LowerName] = self.UnknownPTMDictionary.get(LowerName, 0) + 1
            else:
                #print "Adding ptm of size %s at dbpos %s"%(Mass, DBPos)
                pass            
            # Get database positions:
            #print "Aminos:", Aminos
            DBHitList = FindDBLocations(self.DB, Aminos)
            #print "Peptide %s found in %s positions"%(Aminos, len(DBHitList))
            for AminosDBPos in DBHitList:
                DBPos = AminosDBPos + PrefixLength
                if not self.PTMDictionary.has_key(DBPos):
                    self.PTMDictionary[DBPos] = []

                #print "ModMass %s at position %s, dbpos %s, flanking aminos from %s...%s: %s"%(\
                #    Mass, Position, DBPos, StartPos, EndPos, Aminos)
                # Avoid adding REDUNDANT records:
                FoundFlag = 0
                for (OldMass, OldName) in self.PTMDictionary[DBPos]:
                    if OldMass == Mass:
                        FoundFlag = 1
                        break
                if not FoundFlag:
                    self.PTMDictionary[DBPos].append((Mass, Name))
    def ReportUnknownPTMs(self, OutputFileName):
        SortedList = []
        for (Name, Count) in self.UnknownPTMDictionary.items():
            SortedList.append((Count, Name))
        SortedList.sort()
        SortedList.reverse()
        File = open(OutputFileName, "wb")
        for (Count, Name) in SortedList:
            File.write("%s\t%s\t\n"%(Name, Count))
        File.close()

class UniprotXMLParser(PTMXMLParser):
    """
    Simple XML parser.  Because the start and body and end handlers are handled by various
    sub-functions, we use a dictionary to map tags to their handlers.
    Note: Remember that XML parse routines return unicode, hence the calls to str().
    """
    def __init__(self, DB):
        self.DB = DB
        self.EntryCount = 0
        self.UnknownPTMDictionary = {}
        self.PTMDictionary = {}
        self.StartHandlers = {"entry":self.StartEntry, "sequence": self.StartSequence,
                              "feature":self.StartFeature, "position": self.StartPosition,
                              "accession":self.StartAccession, }
        self.EndHandlers = {"sequence": self.EndSequence, "feature":self.EndFeature,
                            "entry":self.EndEntry,"accession":self.EndAccession, }
        self.StringHandlers = {UXStates.Sequence: self.HandleStringSequence,
                               UXStates.Accession: self.HandleStringAccession}
        PTMXMLParser.__init__(self)
    def StartAccession(self, Attributes):
        self.State = UXStates.Accession
        self.Accession = ""
    def EndAccession(self):
        self.State = UXStates.Skip
    def StartSequence(self, Attributes):
        self.Sequence = ""
        self.State = UXStates.Sequence
    def EndSequence(self):
        self.State = UXStates.Skip
    def StartEntry(self, Attributes):
        """
        A new top-level <entry> tag for a protein record.  As we start the new record, we reset any
        accumulated info.
        """
        self.Sequence = ""
        self.Accession = ""
        # PendingPTMs is a list of tuples of the form (Name, SequencePosition).
        self.PendingPTMs = []
    def EndEntry(self):
        self.AddPendingPTMs()
        self.EntryCount += 1
        if self.EntryCount % 1000 == 0:
            print "Handled entry #%d"%self.EntryCount
    def HandleStringSequence(self, String):
        "Handle the body of the <sequence> tag"
        self.Sequence += str(String.strip())
    def HandleStringAccession(self, String):
        "Handle the body of the <accession> tag"
        self.Accession += str(String.strip())
    def StartFeature(self, Attributes):
        """
        Handle a <Feature>, ignoring it unless it's of type "modified residue".
        """
        Type = Attributes["type"].lower()
        if Type != "modified residue":
            return
        self.CurrentModification = str(Attributes["description"])
        self.State = UXStates.Feature
    def EndFeature(self):
        self.State = UXStates.Skip
    def StartPosition(self, Attributes):
        """
        Handle tag of the form <position position="123"/>
        """
        if self.State == UXStates.Feature:
            # Subtract 1, to go from 1-based to 0-based numbering:
            Position = int(Attributes["position"]) - 1
            # Add a PTM to our pending list:
            self.PendingPTMs.append((self.CurrentModification, Position))
            #print "Added PTM:", self.PendingPTMs[-1]


class HPRDXStates:
    Skipping = 0
    Sequence = 1
    PTMSite = 2

class HPRDXMLParser(PTMXMLParser):
    """
    Parser for HPRD records.  Similar to UniprotXMLParser.
    """
    def __init__(self, DB):
        self.DB = DB
        self.EntryCount = 0
        self.UnknownPTMDictionary = {}
        self.PTMDictionary = {}
        self.State = UXStates.Skip
        self.StartHandlers = {"protein_sequence":self.StartSequence,
                              "isoform":self.StartIsoform,
                              "protein":self.StartProtein,
                              "modification":self.StartModification,
                              "ptm_site":self.StartPTMSite,}
        self.EndHandlers = {"isoform":self.EndIsoform,
                            "ptm_site":self.EndPTMSite,
                            "protein_sequence":self.EndSequence}
        self.StringHandlers = {HPRDXStates.Sequence: self.HandleStringSequence,
                               HPRDXStates.PTMSite: self.HandleStringPTMSite
                               }
        self.DummyTable = string.maketrans("", "")
        PTMXMLParser.__init__(self)
    def StartSequence(self, Attributes):
        self.Sequence = ""
        self.State = HPRDXStates.Sequence
    def EndSequence(self):
        self.State = HPRDXStates.Skipping
        self.Sequence = self.Sequence.upper()
        #print "Obtained sequence of length %s"%len(self.Sequence)
    def HandleStringSequence(self, String):
        "Handle the body of the <sequence> tag"
        try:
            Block = str(String)
        except:
            print "wtf?"
            print "%d: '%s'"%(len(String), String)
            return
        Block = Block.translate(self.DummyTable, " \r\n\t")
        #Block = self.StripWhitespace(String).upper()
        self.Sequence += Block
    def HandleStringPTMSite(self, String):
        self.CurrentSite += String
##    def StripWhitespace(self, String):
##        return String.translate(self.DummyTable, " \r\n\t")
    def StartProtein(self, Attributes):
        self.Accession = str(Attributes["id"])
    def StartIsoform(self, Attributes):
        """
        Start a protein record.  Clear any accumuated data:
        """
        self.PendingPTMs = []
        self.Sequence = ""
        #self.Accession = ""
    def StartModification(self, Attributes):
        self.CurrentModType = str(Attributes["type"])
        #print "START modification '%s'"%self.CurrentModType
    def StartPTMSite(self, Attributes):
        self.State = HPRDXStates.PTMSite
        self.CurrentSite = ""
    def EndPTMSite(self):
        # subtract one, to go from 1-based to 0-based numbering.
        #print "FINISH ptm_site"
        Position = int(self.CurrentSite) - 1 
        self.PendingPTMs.append((self.CurrentModType, Position))
        self.State = HPRDXStates.Skipping
    def EndIsoform(self):
        """
        End a protein record.  Save any accumulated modifications:
        """
        #print "END ISOFORM: add pending PTMs"
        self.AddPendingPTMs()
        self.EntryCount += 1
        if self.EntryCount % 1000 == 0:
            print "Handled entry #%d"%self.EntryCount

        
if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except:
        print "(Warning: psyco not found, running non-optimized)"
    Master = CompareMaster()
    Master.Main()
