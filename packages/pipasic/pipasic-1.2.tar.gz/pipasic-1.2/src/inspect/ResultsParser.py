#Title:          ResultsParser.py
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
Constants and methods for parsing (Inspect) search results
"""
import os
import random
class Columns:

    DefaultInspectHeader = "#SpectrumFile\tScan#\tAnnotation\tProtein\tCharge\tMQScore\tLength\tTotalPRMScore\tMedianPRMScore\tFractionY\tFractionB\tIntensity\tNTT\tInspectFDR\tF-Score\tDeltaScore\tDeltaScoreOther\tRecordNumber\tDBFilePos\tSpecFilePos\tPrecursorMZ\tPrecursorMZError\tSpecIndex"


    def __init__(self):
        self.header = self.initializeHeaders(self.DefaultInspectHeader)

    def initializeHeaders(self,Header):
        if Header[0] == '#':
            Header = Header[1:]

        self.headers = Header.lower().split("\t")
        
    def getIndex(self,headerVal):
        
        for i in range(0,len(self.headers)):
            if headerVal.lower() == self.headers[i]:
                return i

        return -1
        

#    "Constants for which columns contain which data"
#    SpectrumFile = 0
#    ScanNumber = 1
#    Annotation = 2
#    ProteinName = 3
#    Charge = 4
#    MQScore = 5
#    Length = 6
#    NTT = 12
#    PValue = 13
#    FScore = 14
#    DeltaScoreAny = 15
#    DeltaScore = 16
#    ProteinID = 17
#    DBPos = 18
#    FileOffset = 19 #Spectrum File pos
#    ParentMZ = 20 #Corrected, associated with tweak
#    MZError = 21

#    #More columns for splicing
#    Chromosome = 22
#    Strand = 23
#    GenomicPost = 24
#    SplicedSequence = 25
#    Splices = 26
#    SearchDB = 27



class SpectrumOracleMixin:
    def __init__(self):
        self.SpectrumOracle = {}
    def FixSpectrumPath(self, Path):
        FileName = os.path.split(Path)[-1]
        Stub = os.path.splitext(FileName)[0]
        return self.SpectrumOracle.get(Stub, Path)
    def PopulateSpectrumOracle(self, RootDirectory):
        """
        Used when mzxml files are spread over multiple subdirectories.
        MZXMLOracle[Stub] = full path to the corresponding MZXML file
        Used with -M option (not with -s option)
        """
        if not RootDirectory or not os.path.exists(RootDirectory):
            return
        print "Populate oracle from %s..."%RootDirectory
        for SubFileName in os.listdir(RootDirectory):
            # Avoid expensive iteration through results directories:
            if SubFileName[:7] == "Results":
                continue
            SubFilePath = os.path.join(RootDirectory, SubFileName)
            if os.path.isdir(SubFilePath):
                self.PopulateSpectrumOracle(SubFilePath)
                continue
            (Stub, Extension) = os.path.splitext(SubFileName)
            Extension = Extension.lower()
            if Extension == ".mzxml":
                self.SpectrumOracle[Stub] = os.path.join(RootDirectory, SubFileName)
            elif Extension == ".mgf":
                self.SpectrumOracle[Stub] = os.path.join(RootDirectory, SubFileName)
            elif Extension == ".ms2":
                self.SpectrumOracle[Stub] = os.path.join(RootDirectory, SubFileName)
                
class ResultsParser:
    def __init__(self, *args, **kw):
        #self.Columns = Columns
        self.Running = 1
    def ProcessResultsFiles(self, FilePath, Callback, MaxFilesToParse = None, QuietFlag = 0):
        """
        Function for applying a Callback function to one search-reuslts file, or to every
        search-results file in a directory.
        """
        print "ResultsParser:%s"%FilePath
        FileCount = 0
        if os.path.isdir(FilePath):
            FileNames = os.listdir(FilePath)
            random.shuffle(FileNames)
            for FileNameIndex in range(len(FileNames)):
                FileName = FileNames[FileNameIndex]
                if not QuietFlag:
                    print "(%s/%s) %s"%(FileNameIndex, len(FileNames), FileName)
                (Stub, Extension) = os.path.splitext(FileName)
                if Extension.lower() not in (".txt", ".filtered", ".res", ".csv", ".out"):
                    continue
                FileCount += 1
                SubFilePath = os.path.join(FilePath, FileName)
                apply(Callback, (SubFilePath,))
                # Don't parse every single file, that will take too long!
                if MaxFilesToParse != None and FileCount > MaxFilesToParse:
                    break 
        else:
            apply(Callback, (FilePath,))
    
