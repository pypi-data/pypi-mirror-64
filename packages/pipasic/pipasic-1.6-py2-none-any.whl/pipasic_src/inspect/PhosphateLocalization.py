#Title:          PhosphateLocalization.py
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


"""PhosphateLocalization.py

This script is a glorified wrapper for Label.py. It calls label and
calculates the PLS score for each spectral annotation in the input set.

1. read in input data.  If it is not in native inspect format, then we
send it to the GetByteOffset part, so that we can use it like Inspect.

2. Label all possible annotations of the string and get their peptide score (think binomial)

3. Find the difference between the top two scores, report. print.
The results are reported by appending two extra columns to the data from the input
file.  These correspond to the top annotation, and it's PLS.
"""

UsageInfo = """PhosphateLocalization.py
Calculates the Phosphate Localization Score (PLS) for each spectral
annotation in the input file.  Make sure to read the tutorial so
that you understand how to use it correctly.

Required Options:
 -r [FileName] File of formatted annotations
 -m [Directory] Directory containing spectra files (not filename)
 -w [FileName] Output of this program

Additional Options:
 -d [Directory] Directory for the images and annotated peak lists
      created during the label process.  Default "LabelSpewage"

"""

import os
import sys
import getopt
import ResultsParser
import GetByteOffset
import string
import Label

class DetectiveClass(ResultsParser.ResultsParser):
    def __init__(self):
        self.InputFilePath = None
        self.OutputFilePath = None
        self.LabeledAnnotationsDir = "LabelSpewage" # for Labeled output
        self.MZXMLDir = None
        self.InspectFormat = 0
        self.ScanOffset = {} # potentially large dictionary for storing the byte offset of each spectrum
        self.OldInspectResults = {} #(file, scan) => (MQScore, Annotation)  #file name only, not! path
        self.PLSDict = {} # self.PLSDict[(SpectrumFile, Scan)] = (PLS, NewPeptide)
        self.Columns = ResultsParser.Columns()
        ResultsParser.ResultsParser.__init__(self)
        
    def Main(self):
        self.CheckInputFormat(self.InputFilePath)
        if not self.InspectFormat:
            self.GetByteOffsetsForSpectra()
        MakeDirectory(self.LabeledAnnotationsDir)
        self.LabelMe()
        self.MakeOutput()


    def MakeOutput(self):
        """The results of Label.py have been put into a folder, and we now have to parse
        those and put them back into the file that people gave us.
        """
        ## get all the stuff from Label
        self.ProcessResultsFiles(self.LabeledAnnotationsDir, self.ParseLabelSpewage)
        # start putting it into the output
        Handle = open(self.InputFilePath, "rb")
        OutHandle = open(self.OutputFilePath, "wb")
        for Line in Handle.xreadlines():
            if not Line.strip():
                continue
            if Line[0] == "#":
                #header
                OutHandle.write("%s\tBetterAnnotation\tPLS\n"%Line.strip())
                continue
            Bits = Line.strip().split("\t")
            SpectrumFullPath = Bits[self.Columns.getIndex("SpectrumFile")]
            SpectrumFile = os.path.split(SpectrumFullPath)[1]
            Scan = Bits[self.Columns.getIndex("Scan#")]
            Annotation = Bits[self.Columns.getIndex("Annotation")]
            Tuple = (SpectrumFile, Scan)
            if not self.PLSDict.has_key(Tuple):
                print "NO KEY, %s, %s"%(SpectrumFile, Scan)
                continue
            (PLS, NewPeptideAnnotation) = self.PLSDict[(SpectrumFile, Scan)]
            #now write stuff out
            Bits.append("%s"%NewPeptideAnnotation)
            Bits.append("%s"%PLS)
            String = "\t".join(Bits)
            OutHandle.write("%s\n"%String)
        OutHandle.close()

    def ParseLabelSpewage(self, FilePath):
        """In each file I am going to grep out
        filename, scan number, PLS, better peptide if such exists
        """
        
        ##in the filename are the scan number and mzxml filename
        if not FilePath[-3:] == "txt":
            return #skip png images
        (Path, FileName) = os.path.split(FilePath)
        Pos = FileName.find("mzXML") + 5
        SpectrumFile = FileName[:Pos]
        Dot = FileName.find(".", Pos+1)
        Scan = FileName[Pos+1:Dot] # string value, not int
        NewPeptide = None
        Handle= open(FilePath, "rb")
        PLS = "N/A" #default, shoudl get overridden for every file
        for Line in Handle.xreadlines():
            Line = Line.strip()
            #hard coded magic
            if Line[:10] == "Phosphate ":
                #Phosphate Localization Score: 52.2
                Colon = Line.find(":")
                PLS = Line[Colon + 1:]
                #print Line
                #print "I parsed out %s"%PLS
            if Line[:7] == "WARNING":
                #parse out new peptide
                ToSplit = Line.replace("WARNING: Better annotation than input.", "")
                (BetterMQScore, NewPeptide) = ToSplit.split(",")
                NewPeptide = NewPeptide.strip()
            if Line[:2] == "b2":
                #this means we've started to get into the rest of the verbose output
                # and past what we care about
                break
        Handle.close()
        Tuple = (SpectrumFile, Scan)
        self.PLSDict[Tuple] = (PLS, NewPeptide)


    def GetByteOffsetsForSpectra(self):
        "Read mzXML from either a single file, or directory, creating the self.ScanOffset dictionary"
        Abacus = GetByteOffset.Abacus()
        if os.path.isdir(self.MZXMLDir):
            for FileName in os.listdir(self.MZXMLDir):
                (Stub, Extension) = os.path.splitext(FileName)
                if Extension.lower() == ".mzxml":
                    Path = os.path.join(self.MZXMLDir, FileName)
                    ScanOffsetSingleFile = Abacus.GetByteOffset(Path)
                    for (ScanNumber, ScanOffset) in ScanOffsetSingleFile.items():
                        self.ScanOffset[(FileName, ScanNumber)] = (Path, ScanOffset)
        else:
            ScanOffsetSingleFile = Abacus.GetByteOffset(self.MZXMLDir)
            FileName = os.path.split(self.MZXMLDir)[1]
            for (ScanNumber, ScanOffset) in ScanOffsetSingleFile.items():
                self.ScanOffset[(FileName, ScanNumber)] = (self.MZXMLDir, ScanOffset)
                #print "Storing value (%s,%s) with key (%s, %s)"%(self.MZXMLDir, ScanOffset, FileName, ScanNumber)

    def LabelMe(self):
        Handle = open(self.InputFilePath, "rb")
        Dymo = Label.LabelClass()
        Count = 0
        GoodScoreCount = 0
        WrongChargeCount = 0
        ScoredWorseCount = 0
        for Line in Handle.xreadlines():
            if Line[0] == "#":
                self.Columns.initializeHeaders(Line)
                continue
            if not Line.strip():
                continue
            Bits = list(Line.strip().split("\t"))
            #Charge = int (Bits[self.Columns.Charge])  I don't thin I need this anymore
            Count +=1
            Annotation = Bits[self.Columns.getIndex("Annotation")]
            #print "Annotation :%s:"%Annotation
            FileName = Bits[self.Columns.getIndex("SpectrumFile")]
            Scan = int(Bits[self.Columns.getIndex("Scan#")])
            if not self.InspectFormat:
                FileNameMinusPath = os.path.split(FileName)[1]
                (FullPathDummy, ByteOffset) = self.ScanOffset[(FileNameMinusPath, Scan)]
                #print (FullPathDummy, ByteOffset)
                #continue
            else:
                ByteOffset = int(Bits[self.Columns.getIndex("SpecFilePos")])
            (Path,File) = os.path.split(FileName)
            FileName = os.path.join(self.MZXMLDir, File)
            VerboseFileName = "%s.%s.%s.verbose.txt"%(File, Scan, Annotation[2:-2])
            ImageFileName = "%s.%s.%s.png"%(File, Scan, Annotation[2:-2])
            VerboseFilePath = os.path.join(self.LabeledAnnotationsDir, VerboseFileName)
            ImageFilePath = os.path.join(self.LabeledAnnotationsDir, ImageFileName)
            ## as we've got a single Dymo object, we must be passing in full args list
            ## -p to suppress the image popup, and -P for the PLS score
            Args = " -r %s -b %d -a %s -v %s -w %s -p -P"%(FileName, ByteOffset, Annotation, VerboseFilePath, ImageFilePath)
            ArgsList = Args.split()
            #print "Parsing Results for %s, scan %s, charge %s"%(FileName, Scan, Charge)
            #print "Args: %s"%Args
            Dymo.ParseCommandLine(ArgsList)
            Dymo.Main()

        Handle.close()
        
    def CheckInputFormat(self, FileName):
        """This method serves to catch input files that are not in the
        proper Inspect format.  If this is the case, then we must convert the
        files to Inspect format.  This basically means that we put a byte offset at the
        end.
        Expected format. (tab delimited, 3 columns)
        Spectrum File          Spectrum Number (int)            Annotation (string, no! numbers!)
        """
        Handle = open (self.InputFilePath, "rb")
        ## 1. get the first line and see if it's already in Inspect Format
        Line = Handle.readline()
        try:
            Bits = Line.strip().split("\t")
        except:
            print "####################################################"
            print "Input file in improper format. Please read tutorial."
            sys.exit(1)
        #if not len(Bits) < self.Columns.getIndex("SpecFilePos"):
        #    self.InspectFormat = 1
        #    return # in inspect format.  it's okay
        ## 2. Check to see if each line of the input file has the proper format
        Reject = 0
        for Line in Handle.xreadlines():
            if Line[0] == "#":
                self.Columns.initializeHeaders(Line)
                continue
            try:
                Bits = Line.strip().split("\t")
            except:
                print "####################################################"
                print "Input file in improper format. Please read tutorial."
                sys.exit(1)
            #now check to see if column 1 is a number, and 2 is a string (with no brackets)
            try:
                SpectrumNumber = int(Bits[self.Columns.getIndex("Scan#")])
            except:
                Reject = 1
                print "Second column must be a integer representing the spectrum number"
            Annotation = Bits[self.Columns.getIndex("Annotation")]
            AcceptArray = string.ascii_letters
            AcceptArray += "."  #for delimiting the prefix/suffix
            AcceptArray += "*"  # for the beginning/end of a protein. should only be in prefix/suffix
            AcceptArray += string.digits
            for Index in range(len(Annotation)):
                if not Annotation[Index] in AcceptArray:
                    print "This annotation is in an improper format %s"%Annotation
                    Reject = 1
                    break
            if Reject:
                print "####################################################"
                print "There were formatting problems with the input file"
                print "We cannot proceed.  Please read the tutorial."
                sys.exit(1)
        print "Input file %s received in the correct format"%FileName
    def ParseCommandLine(self,Arguments):
        (Options, Args) = getopt.getopt(Arguments, "r:w:m:d:")
        OptionsSeen = {}
        for (Option, Value) in Options:
            OptionsSeen[Option] = 1
            if Option == "-r":
                # -r results file(s)
                if not os.path.exists(Value):
                    print "** Error: couldn't find results file '%s'\n\n"%Value
                    print UsageInfo
                    sys.exit(1)
                self.InputFilePath = Value
            if Option == "-d":
                self.LabeledAnnotationsDir = Value
            if Option == "-w":
                self.OutputFilePath = Value
            if Option == "-m":
                self.MZXMLDir = Value
        if not OptionsSeen.has_key("-r") or not OptionsSeen.has_key("-m"):
            print UsageInfo
            sys.exit(1)


def MakeDirectory(Dir):
    if os.path.exists(Dir):
        return 
    try:
        os.makedirs(Dir)
    except:
        raise
    


if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except:
        print "(psyco not found - running in non-optimized mode)"
    MacGyver = DetectiveClass()
    MacGyver.ParseCommandLine(sys.argv[1:])
    MacGyver.Main()
