#Title:          PrepDB.py
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
Translate a protein database to a good format for trie-based searching.
The source database should be in either FASTA format or in swiss-prot format.
The output database will be in "concatenated format" - peptide strings with
asterisks delimiting the peptides, no whitespace.
We also save a binary file indexing into the concatenated DB.

Index file format is record-based, with one record per peptide:
- original DB position (int); the START of a record (>)
- concatenated DB file position (int); the START of a record (first peptide)
- Peptide ID (string, 80 chars)
"""
import sys
import struct
import traceback
import os
import string

class SwissCompressor:
    """
    Convert a protein database into concatenated format.
    Processes the SwissProt database format.
    """
    def __init__(self, SourceFileName, SquishedFileName, IndexFileName, Species = None):
        self.SourceFile = open(SourceFileName,"rb")
        self.SquishedFile = open(SquishedFileName,"wb")
        self.IndexFile = open(IndexFileName,"wb")
        self.FASTA = 0
        self.Species = Species
    def Compress(self):
        """
        The parts of swiss-prot we care about look like this:
SQ   SEQUENCE   296 AA;  34077 MW;  B0D7CD175C7A3625 CRC64;
     FNSNMLRGSV CEEDVSLMTS IDNMIEEIDF YEKEIYKGSH SGGVIKGMDY DLEDDENDED
     EMTEQMVEEV ADHITQDMID EVAHHVLDNI THDMAHMEEI VHGLSGDVTQ IKEIVQKVNV
     AVEKVKHIVE TEETQKTVEP EQIEETQNTV EPEQTEETQK TVEPEQTEET QNTVEPEQIE
     ETQKTVEPEQ TEEAQKTVEP EQTEETQKTV EPEQTEETQK TVEPEQTEET QKTVEPEQTE
     ETQKTVEPEQ TEETQKTVEP EQTEETQKTV EPEQTEETQN TVEPEPTQET QNTVEP
//
        """        
        self.InSequence = 0
        RecordNumber = 0
        LineNumber = 0
        CorrectSpecies = 0
        while (1):
            LineNumber += 1
            SourceFilePos = self.SourceFile.tell()
            RawFileLine  = self.SourceFile.readline()
            if not RawFileLine:
                break # end o' file!
            FileLine = RawFileLine.strip()
            if self.InSequence:
                # // marks end of sequence; anything else is sequence data.
                # ...but in some cases, the // marker isn't present, so we
                # stop when we see the "ID" tag from the next record.
                #if FileLine[:2] == "//":
                #print self.InSequence, FileLine
                if RawFileLine[:2] != "  ":
                    self.InSequence = 0
                    if self.FASTA:
                        pass
                    else:
                        self.SquishedFile.write("*")
                    RecordNumber += 1
                else:
                    Stripped = FileLine.replace(" ","")
                    self.SquishedFile.write(Stripped)
            else:
                if FileLine[:3] == "OS ":
                    if self.Species == None or FileLine.lower().find(self.Species)!=-1:
                        CorrectSpecies = 1
                    else:
                        CorrectSpecies = 0
                if FileLine[:3] == "ID ":
                    SourceFileRecordStart = SourceFilePos
                    ID = FileLine.split()[1]
                    ID = ID[:80]
                    if self.FASTA:
                        self.SquishedFile.write("\n>%s\n"%ID)
                if FileLine[:3] == "SQ ":
                    if CorrectSpecies:
                        self.InSequence = 1
                        SquishedFilePos = self.SquishedFile.tell()
                        Str = struct.pack("<qi80s", SourceFileRecordStart, SquishedFilePos, ID)
                        self.IndexFile.write(Str)
            if LineNumber%1000 == 0:
                print "Processed line %d."%LineNumber
                #self.SquishedFile.flush()
                #self.IndexFile.flush()
                #sys.stdin.readline()
        print "Total records seen:", RecordNumber

class FASTACompressor:
    """
    Convert a protein database into concatenated format.
    Processes FASTA format.
    """
    def __init__(self, SourceFileName, SquishedFileName, IndexFileName, Species = None):
        self.SourceFile = open(SourceFileName,"rb")
        self.SquishedFile = open(SquishedFileName,"wb")
        self.IndexFile = open(IndexFileName,"wb")
        self.SquishedFileName = SquishedFileName
        self.IndexFileName = IndexFileName
    def Compress(self):
        RecordNumber = 0
        LineNumber = 0
        FirstRecord = 1
        LineNumberWarnings = 0
        DummyTable = string.maketrans("", "")
        while (1):
            LineNumber += 1
            SourceFilePos = self.SourceFile.tell()
            FileLine  = self.SourceFile.readline()
            if not FileLine:
                break # end o' file!
            FileLine = FileLine.strip()
            if not FileLine:
                continue # empty lines (whitespace only) are skipped
            if FileLine[0] == ">":
                RecordNumber += 1
                if not FirstRecord:
                    self.SquishedFile.write("*")                
                ID = FileLine[1:81].strip()
                # Fix weird characters in the ID:
                ID = ID.replace("\t", " ")
                # Note: Important to call tell() *after* writing the asterisk!  (Fixed a bug 1/20/5)
                SquishedFilePos = self.SquishedFile.tell() 
                Str = struct.pack("<qi80s", SourceFilePos, SquishedFilePos, ID)
                self.IndexFile.write(Str)
                FirstRecord = 0
            else:
                WarnFlag = 0
                FileLine = string.translate(FileLine, DummyTable, " \r\n\t*")
                FileLine = FileLine.upper()
                Str = ""
                for Char in FileLine:
                    if Char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        WarnFlag = 1
                    else:
                        Str += Char
                #FileLine = FileLine.replace("*","")
                if WarnFlag and LineNumberWarnings < 10:
                    print "* Warning: line %s contains non-amino-acid characters:"%LineNumber
                    print FileLine
                    LineNumberWarnings += 1
                    if LineNumberWarnings >= 10:
                        print "(omitting further warnings)"
                self.SquishedFile.write(Str)
        print "Converted %s protein sequences (%s lines) to .trie format."%(RecordNumber + 1, LineNumber)
        print "Created database file '%s'"%self.SquishedFileName

class MS2DBCompressor:
    """
    Creates the index file for a splice graph, no modification is made to the original database
    """
    def __init__(self, SourceFileName, SquishedFileName, IndexFileName, Species = None):
        self.SourceFile = open(SourceFileName,"rb")
        
        self.IndexFile = open(IndexFileName,"wb")
        self.IndexFileName = IndexFileName
    def Compress(self):
        RecordNumber = 0
        LineNumber = 0
        FirstRecord = 1
        LineNumberWarnings = 0
        DummyTable = string.maketrans("", "")
        while (1):
            LineNumber += 1
            SourceFilePos = self.SourceFile.tell()
            FileLine  = self.SourceFile.readline()
            if not FileLine:
                break # end o' file!
            FileLine = FileLine.strip()
            if not FileLine:
                continue # empty lines (whitespace only) are skipped
            if FileLine[0:6] == "<Gene ":
                RecordNumber += 1
                
                ID = ""
                Bits = FileLine[6:].split(" ")
                for B in Bits:
                    (Item,Value) = B.split("=")
                    if Item == "Name":
                        ID = Value[1:-1]
                        break

                if ID == "":
                    print "No valid ID found in %s"%FileLine
                    raw_input()
                
                # Note: Important to call tell() *after* writing the asterisk!  (Fixed a bug 1/20/5)
                Str = struct.pack("<qi80s", SourceFilePos, SourceFilePos, ID)
                self.IndexFile.write(Str)
                FirstRecord = 0
            
        print "Converted %s protein sequences (%s lines) to .ms2index format."%(RecordNumber + 1, LineNumber)
        print "Created index file '%s'"%self.IndexFileName


def PrintUsage():
    print "Please supply a database filename."
    print "Usage: PrepDB.py <format> <OriginalDB> [NewDB] [IndexFile]"
    print "Example: Prepdb.py FASTA Drome.fasta"
    print "  The source format can be either FASTA or SWISS or MS2DB"
    print "  New DB file name defaults to original filename with .trie appended (no new file is created for MS2DB)"
    print "  Index file name defaults to original filename with .index appended (or .ms2index for MS2DB)"

if __name__ == "__main__":    
    if len(sys.argv)<3:
        PrintUsage()
        sys.exit()
    try:
        import psyco
        psyco.full()
    except:
        print "(psyco not found - running in non-optimized mode)"
    # First argument: Original database file format
    Format = sys.argv[1].lower()
    if Format == "fasta":
        CompressorClass = FASTACompressor
    elif Format == "swiss":
        CompressorClass = SwissCompressor
    elif Format == "ms2db":
        CompressorClass = MS2DBCompressor
    else:
        print "Unknown source database format '%s'"%Format
        PrintUsage()
        sys.exit()
    # Second argument: Original database file
    SourceFileName = sys.argv[2]
    # Optional third argument: New database file name
    if len(sys.argv) > 3:
        SquishedFileName = sys.argv[3]
    elif Format == "ms2db":
        SquishedFileName = None
    else:
        SquishedFileName = "%s.trie"%os.path.splitext(SourceFileName)[0]
    # Optional third argument: Index file name
    if len(sys.argv) > 4:
        IndexFileName = sys.argv[4]
    elif Format == "ms2db":
        IndexFileName = "%s.ms2index"%os.path.splitext(SourceFileName)[0]
    else:
        IndexFileName = "%s.index"%os.path.splitext(SourceFileName)[0]
    # Use FASTACompressor for FASTA format, Compressor for the weird swiss-prot format
    # If "species" is a string, then the Swiss-prot reader will filter out any records
    # that don't contain that string.  For example, set Species = "sapiens" to grab only
    # human proteins.
    Species = None
    Squasher = CompressorClass(SourceFileName, SquishedFileName, IndexFileName, Species)
    Squasher.Compress()
