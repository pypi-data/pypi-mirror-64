#Title:          ProteinGrouper.py
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

#Updated 1-3-2012 to allow column header based lookup (NEC)

import os
import sys
import ResultsParser
import TrieUtils
import Utils
import getopt

UsageInfo = """ProteinGrouper.py version 2012.01.03
ProteinGrouper updates the 'Protein' field for Inspect annotations, replacing
the single protein name with a '!' delimited list of protein names.  For each 
Inspect results file specified, a new file is created with the updated 'Protein'
field.  
[REQUIRED]
-r [File or Dir] File or directory containing Inspect annotations
-t [File] Trie file used to search spectra, assumes an index file exists of the same name
-w [Dir] Directory where updated Inspect annotations are written

[OPTIONAL]:
-p Assign peptides to a parsimonious set of proteins.  
-a Assign peptides to a parsimonious set of proteins.  This protein will
appear first in the list of proteins contained by the peptide.
"""
DELIM = "!"

class ProteinGrouper(ResultsParser.ResultsParser):
    def __init__(self):
        ResultsParser.ResultsParser.__init__(self)
        self.Columns = ResultsParser.Columns()
        Utils.Initialize()
        self.TrieFiles = []
        self.IndexFiles = []
        self.DoParsimony = 0
        self.DoParsimonyAndGroup = 0
        self.TUtils = TrieUtils.TrieUtils()


        self.Peptide2ProteinID = {} #Peptide sequence -> (TrieIndex,ProteinIDS)
        self.Peptide2SpectralCount = {} #Peptide sequence -> Spectral Count
        self.Protein2Peptides = {} # (TrieIndex,ProteinID) -> Peptide sequences
        #self.ProteinNames = {} #(TrieIndex,ProteinID) -> ProteinName

        #Populated only if parsimony
        self.SelectedProteins = {}
        self.HeaderLine = None
        

    def Main(self):

        #Load peptides
        for FileName in self.InputFiles:
            print "Loading peptides from %s"%FileName
            self.LoadPeptides(FileName)
        if self.DoParsimony == 1 or self.DoParsimonyAndGroup == 1:
            self.ChoosePeptides()
        for FileName in self.InputFiles:
            self.WritePeptides(FileName)
            

    #We assume that if multiple peptides are listed for a spectrum, then they appear together in the file and in decreasing order of
    #confidence
    def LoadPeptides(self,FileName):
        #print "Loading peptides!!"
        #raw_input()
        LocalDebug = 1

        RawFileName = os.path.basename(FileName)
        
        File = open(FileName,'r')
        #OutputFile = os.path.join(self.OutputDir,RawFileName)
        #OutFile = open(OutputFile ,'w')
        PeptideList = {}
        
        PrevSpectrum = None
        
        
        for Line in File:
            Line = Line.strip()
            if Line == "":
                continue
            if Line[0] == "#":
                self.HeaderLine = Line
                continue
            
            if LocalDebug:
                print Line
            
            Bits = Line.split("\t")
            ModdedPeptide = Bits[self.Columns.getIndex("Annotation")]
            Peptide = Utils.GetPeptideFromModdedName(ModdedPeptide).Aminos

            #if Peptide == "YGPLLDLPELPFPELER":
            #    LocalDebug = 1
            #else:
            #    LocalDebug = 0
            CurrSpectrum = (Bits[0],Bits[1])
            if CurrSpectrum == PrevSpectrum:
                continue
            PrevSpectrum = CurrSpectrum

            #Update the spectral count for this peptide
            if not self.Peptide2SpectralCount.has_key(Peptide):
                self.Peptide2SpectralCount[Peptide] = 0
            self.Peptide2SpectralCount[Peptide] += 1

            if LocalDebug:
                print self.Peptide2SpectralCount[Peptide]
                #raw_input()

            if self.Peptide2ProteinID.has_key(Peptide):
                if LocalDebug:
                    print "Already searched for peptide %s"%Peptide
                    raw_input()
                continue
                
            else:
                PeptideList[Peptide] = 1
                if LocalDebug:
                    print "Searching %s for the first time!"%Peptide


                #See if we've reached enough peptides to search
                if len(PeptideList.keys()) >= TrieUtils.MIN_TRIE_SEARCH_SIZE:
                    if LocalDebug:
                        print "Reached %s peptides to search"%(len(PeptideList.keys()))
                        #raw_input()
                    
                    #Loop through each trie file that we have
                    for TrieIndex in range(0,len(self.TrieFiles)):
                        if LocalDebug:
                            print "Searching trieDB: %s"%(self.TrieFiles[TrieIndex])
                        Locations = self.TUtils.GetAllLocations(PeptideList.keys(),self.TrieFiles[TrieIndex])
                        if LocalDebug:
                            print "Finished searching"
                        #For each peptide that we searched, add it's locations and proteins
                        for Pep in PeptideList.keys():
                            #if Pep == "AAGARPLTSPESLSR" or Pep == "GFFDPNTHENLTYLQLLR" or Pep == "EMAVPDVHLPDVQLPK" or Pep == "YGPLLDLPELPFPELER":
                            #    LocalDebug = 1
                            #else:
                            #    LocalDebug = 0
                            if LocalDebug:
                                print Pep
                                print "Total Locations: %s"%(len(Locations[Pep]))
                            if len(Locations[Pep]) == 0:
                                print "No locations found for %s"%Pep
                                continue
                            if not self.Peptide2ProteinID.has_key(Pep):
                                self.Peptide2ProteinID[Pep] = []
                            for (ID,Res) in Locations[Pep]:

                                if LocalDebug:
                                    print "%s appear in %s at pos %s"%(Pep,ID,Res)
                                #Get the protein name
                                #if not self.ProteinNames.has_key((TrieIndex,ID)):
                                ProteinName = self.TUtils.GetProteinName(self.IndexFiles[TrieIndex],ID)
                                    
                                #else:
                                #    ProteinName = self.ProteinNames[(TrieIndex,ID)]
                                if LocalDebug:
                                    print "Hit to protine %s"%ProteinName
                                if ProteinName[0:3] == "XXX": #Skip hits to reverse DB
                                    continue
                                if ProteinName.find(DELIM) >= 0:
                                    print "ERROR: Protein %s contains delim %s"%(ProteinName,DELIM)
                                    sys.exit(0)
                                #self.ProteinNames[(TrieIndex,ID)] = ProteinName

                                if self.Peptide2ProteinID[Pep].count((TrieIndex,ID)) == 0:
                                    self.Peptide2ProteinID[Pep].append((TrieIndex,ID))
                               
                                if not self.Protein2Peptides.has_key((TrieIndex,ID)):
                                    self.Protein2Peptides[(TrieIndex,ID)] = []
                                if self.Protein2Peptides[(TrieIndex,ID)].count(Pep) == 0:
                                    self.Protein2Peptides[(TrieIndex,ID)].append(Pep)

                    PeptideList = {}
        if len(PeptideList.keys()) > 0:
            if LocalDebug:
                print "Reached %s peptides to search"%(len(PeptideList.keys()))
                
            for TrieIndex in range(0,len(self.TrieFiles)):
                Locations = self.TUtils.GetAllLocations(PeptideList.keys(),self.TrieFiles[TrieIndex])
                    
                for Pep in PeptideList.keys():
                    if LocalDebug:
                        print Pep
                        
                    if len(Locations[Pep]) == 0:
                        print "No locations found for %s"%Pep
                        continue
                    if not self.Peptide2ProteinID.has_key(Pep):
                        self.Peptide2ProteinID[Pep] = []

                    for (ID,Res) in Locations[Pep]:

                        #Get the protein name
                        #if not self.ProteinNames.has_key((TrieIndex,ID)):
                        ProteinName = self.TUtils.GetProteinName(self.IndexFiles[TrieIndex],ID)

                        #else:
                        #    ProteinName = self.ProteinNames[(TrieIndex,ID)]

                        if ProteinName[0:3] == "XXX": #Skip hits to reverse DB
                            continue
                        if ProteinName.find(DELIM) >= 0:
                            print "ERROR: Protein %s contains delim %s"%(ProteinName,DELIM)
                            sys.exit(0)
                        #self.ProteinNames[(TrieIndex,ID)] = ProteinName

                        if self.Peptide2ProteinID[Pep].count((TrieIndex,ID)) == 0:
                            self.Peptide2ProteinID[Pep].append((TrieIndex,ID))
                        
                        if not self.Protein2Peptides.has_key((TrieIndex,ID)):
                            self.Protein2Peptides[(TrieIndex,ID)] = []
                        if self.Protein2Peptides[(TrieIndex,ID)].count(Pep) == 0:
                            self.Protein2Peptides[(TrieIndex,ID)].append(Pep)
                        

                        
                   
            
        File.close()
        

    def ChoosePeptides(self):
        
        LocalDebug = 1
        if LocalDebug:
            print "Total peptides: %s"%(len(self.Peptide2ProteinID.keys()))
            print "Total protiens: %s"%(len(self.Protein2Peptides.keys()))


        ProteinCounts = {}
        for (TrieIndex,ID) in self.Protein2Peptides.keys():
            SpecCount = 0
            for Pep in self.Protein2Peptides[(TrieIndex,ID)]:
                SpecCount += self.Peptide2SpectralCount[Pep]
            ProteinCounts[(TrieIndex,ID)] = (len(self.Protein2Peptides[(TrieIndex,ID)]),SpecCount)

        self.SelectedProteins = {}
        self.FinalPeptideProteins = {} #peptide -> final protein selection
        
        while (1):
            BestCandidate = None
            BestScore = None
            BestProteinName = None
            #Find the next best protein (best = most peptides)
            for (TrieIndex,ProteinID) in ProteinCounts.keys():

                #We've already added this guy
                if self.SelectedProteins.has_key((TrieIndex,ProteinID)):
                    continue
                Score = ProteinCounts[(TrieIndex,ProteinID)]
                CurrProteinName = self.TUtils.GetProteinName(self.IndexFiles[TrieIndex],ProteinID)

                if Score > BestScore or BestScore == None or (Score == BestScore and CurrProteinName < BestProteinName):
                    BestScore = Score
                    BestCandidate = (TrieIndex,ProteinID)
                    BestProteinName = CurrProteinName
                    #print "New Best %s, score %s"%(ProteinID,BestScore)
            if not BestScore:
                break
            (PeptideCount, SpectrumCount) = BestScore
            if PeptideCount == 0:
                break
            #%%%
            ProteinName = BestProteinName
            print "Accept protein %s (%s)\n  Gets %s peptides, %s spectra"%(BestCandidate, ProteinName, PeptideCount, SpectrumCount)
            self.SelectedProteins[BestCandidate] = BestScore
            # Lay claim to all the (not-yet-claimed) peptides:
            for Peptide in self.Protein2Peptides[BestCandidate]:
                if LocalDebug:
                    print "  Grab %s spectra from peptide %s"%(self.Peptide2SpectralCount[Peptide], Peptide)
                self.FinalPeptideProteins[Peptide] = BestCandidate
                # Other proteins (if not already accepted) lose a peptide, and some spectra:
                for (OtherTrieIndex,OtherID) in self.Peptide2ProteinID[Peptide]:
                    if self.SelectedProteins.has_key((OtherTrieIndex,OtherID)):
                        continue
                    #if LocalDebug:
                    #    print "Removing spectra from other Protein %s/%s (%s)"%(OtherTrieIndex,OtherID,self.ProteinNames[(OtherTrieIndex,OtherID)])
                    (pCount,sCount) = ProteinCounts[(OtherTrieIndex,OtherID)]

                    if LocalDebug:
                        print "Old counts: %s peptides %s spectra"%(pCount,sCount)
                    self.Protein2Peptides[(OtherTrieIndex,OtherID)].remove(Peptide)
                    pCount -= 1
                    sCount -= self.Peptide2SpectralCount[Peptide]
                    if LocalDebug:
                        print "New counts: %s peptides %s spectra"%(pCount,sCount)
                    ProteinCounts[(OtherTrieIndex, OtherID)] = (pCount,sCount)
        # Sanity check - the selected proteins have peptides, the unselected proteins have 0
        for Protein in self.Protein2Peptides.keys():
            #ProteinName = self.ProteinNames[Protein]
            PeptideCount = len(self.Protein2Peptides[Protein])
            SpectrumCount = ProteinCounts.get(Protein, 0)
            if self.SelectedProteins.has_key(Protein) and PeptideCount <= 0:
                print "** Warning: Selected protein %s has %s peptides!"%(Protein, PeptideCount)
            if not self.SelectedProteins.has_key(Protein) and PeptideCount != 0:
                print "** Warning: Unelected protein %s has %s peptides!"%(Protein, PeptideCount)
            
        

    def WritePeptides(self,FileName):
        RawFileName = os.path.basename(FileName)
        InputFile = open(FileName,'r')
        OutputFile = os.path.join(self.OutputDir,RawFileName)
        OutFile = open(OutputFile ,'w')
        
        MissCount = 0
        LineCount = 0
        for Line in InputFile:
            Line = Line.strip()
            if Line == "":
                continue
            if Line[0] == "#":
                OutFile.write(Line + "\n")
                continue
            Bits = Line.split("\t")
            ModdedPeptide = Bits[self.Columns.getIndex("Annotation")]
            Peptide = Utils.GetPeptideFromModdedName(ModdedPeptide).Aminos


            #See if we are doing parsimony
            if self.DoParsimonyAndGroup == 1:
                if not self.Peptide2ProteinID.has_key(Peptide) or len(self.Peptide2ProteinID[Peptide]) == 0:
                    print "ERROR: Peptide %s of %s has no locations!!!"%(Peptide,Line)
                    MissCount += 1
                    continue

                if not self.FinalPeptideProteins.has_key(Peptide):
                   print "ERROR: Peptide %s of %s has no selected protein!!!"%(Peptide,Line)
                   print "Formerly found in:"
                   for (TrieIndex,ID) in self.Peptide2ProteinID[Peptide]:
                       print "(%s,%s)"%(TrieIndex,ID)
                   continue 
                Protein = self.FinalPeptideProteins[Peptide]
                (TrieIndex,ProtID) = Protein
                
                #Add other proteins

                

                Locations = self.Peptide2ProteinID[Peptide]
                LocStr = self.TUtils.GetProteinName(self.IndexFiles[TrieIndex],ProtID)
                for Prot in Locations:
                    if Prot != Protein:
                        (TIndex,PID) = Prot
                        LocStr += DELIM + self.TUtils.GetProteinName(self.IndexFiles[TIndex],PID)
                Bits[self.Columns.getIndex("Protein")] = LocStr

            elif self.DoParsimony == 1:
                if not self.FinalPeptideProteins.has_key(Peptide):
                   print "ERROR: Peptide %s of %s has no selected protein!!!"%(Peptide,Line)
                   MissCount += 1
                   continue 
                Protein = self.FinalPeptideProteins[Peptide]
                (TrieIndex,ProtID) = Protein
                Bits[self.Columns.getIndex("Protein")] = self.TUtils.GetProteinName(self.IndexFiles[TrieIndex],ProtID) 
                Bits[self.Columns.getIndex("RecordNumber")] = str(Protein[1])
            else:
                if not self.Peptide2ProteinID.has_key(Peptide) or len(self.Peptide2ProteinID[Peptide]) == 0:
                    print "ERROR: Peptide %s of %s has no locations!!!"%(Peptide,Line)
                    MissCount += 1
                    continue

                Locations = self.Peptide2ProteinID[Peptide]
                LocStr = ""
                for Prot in Locations:
                    (TIndex,PD) = Prot
                    LocStr += self.TUtils.GetProteinName(self.IndexFiles[TIndex],PID) + DELIM
                LocStr = LocStr[0:-1*len(DELIM)]
                
                Bits[self.Columns.getIndex("Protein")] = LocStr
            Str = "\t".join(Bits)
            OutFile.write("%s\n"%Str)
            #print Str
            LineCount += 1

        print "Total peptides omitted: %s"%MissCount
        print "Wrote %s lines to %s"%(LineCount,OutputFile)
        OutFile.close()
        InputFile.close()
                    
            

    def ParseCommandLine(self,Arguments):
        (Options,Args) = getopt.getopt(Arguments,"r:w:t:pa")
        OptionsSeen = {}
        for (Option,Value) in Options:
            OptionsSeen[Option] = 1
            
            if Option == "-r":
                if not os.path.exists(Value):
                    print "ERROR: %s is not a valid file or directory"%Value
                    sys.exit(0)
                
                if not os.path.isdir(Value):
                    self.InputFiles = [Value]
                
                else:
                    Files = os.listdir(Value)
                    self.InputFiles = []
                    for FileName in Files:
                        self.InputFiles.append(os.path.join(Value,FileName))

            elif Option == "-w":
                if not os.path.exists(Value):
                    os.makedirs(Value)
                self.OutputDir = Value
            elif Option == "-t":
                if not os.path.isfile(Value):
                    print "ERROR: %s is not a valid database file"%Value
                    sys.exit(0)

                IndexFileName = os.path.splitext(Value)[0] + ".index"
                if not os.path.isfile(IndexFileName):
                    print "ERROR: Unable to find index file %s for trie file %s"%(IndexFileName,Value)
                    sys.ext(0)
                self.TrieFiles.append(Value)
                self.IndexFiles.append(IndexFileName)
            elif Option == "-p":
                self.DoParsimony = 1
            elif Option == "-a":
                self.DoParsimonyAndGroup = 1

            else:
                print "ERROR %s is not a valid argument"%Option
        
        if not OptionsSeen.has_key("-r") or not OptionsSeen.has_key("-w") or not OptionsSeen.has_key("-t"):
            print "ERROR: Missing arguments"
            print UsageInfo
            sys.exit(0)


if __name__ == "__main__":
    Grouper = ProteinGrouper()
    Grouper.ParseCommandLine(sys.argv[1:])
    Grouper.Main()
