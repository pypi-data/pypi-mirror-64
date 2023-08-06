#Title:          GetByteOffset.py
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
GetByteOffset.py
Utility to find the byte offset of scans in a spectrum file
Has no main
"""

import os
import sys
import xml.sax.handler
import xml.sax

## auxiliary for the mzxml files
class XMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.inOffset = 0
        self.mapping = {}
    def startElement(self, name, attributes):
        if name == "offset":
            self.buffer = ""
            self.scan = attributes["id"]
            self.inOffset = 1
    def characters(self, data):
        if self.inOffset:
            self.buffer += data
    def endElement(self, name):
        if name == "offset":
            self.inOffset = 0
            self.mapping[self.scan] = self.buffer

class Abacus:
    def __init__(self):
        self.ScanOffset = {} #Scan = Offset

    def GetByteOffset(self, FileName):
        self.ScanOffset = {} #reset every time
        (Stub, Ext) = os.path.splitext(FileName)
        if Ext.lower() == ".mzxml":
            return self.GetOffsetsMZXML(FileName)
        elif Ext.lower() == ".mgf":
            return self.GetOffsetsMGF(FileName)

    def GetOffsetsMZXML(self, FilePath):
        """Parses an individual mzXML file and saves the scan num and byte offset
        into an dictionary called self.ScanOffset
        Now uses real XML parsing looking for <offset id="SCAN">OFFSET</offset>
        DOM is slow, so I'll use sax
        """
        print "Opening mzXML file %s"%FilePath
        FileName = os.path.split(FilePath)[1]
        Parser = xml.sax.make_parser()
        Handler = XMLHandler()
        Parser.setContentHandler(Handler)
        Parser.parse(FilePath)
        for (Scan, Offset) in Handler.mapping.items():
            ScanNumber = int(Scan)
            Offset = int(Offset)
            #print (Scan, Offset)
            self.ScanOffset[ScanNumber] = Offset
        return self.ScanOffset

    def GetOffsetsMGF(self, FileName):
        """There is no pleasant way of doing this.  I suppose
        that I can just read in line after line looking for BEGIN
        """
        File = open(FileName, "rb")
        #read in a MEG of the file at a time, and search for beginning <scan tags
        #Text holds the data, SeamText willhold the last few bytes of a block
        #and get appended to the first few (to check for a tag that spans the block
        MEG = 1024*1024
        Text = ""
        SeamText = ""
        FileOffset = 0
        
        Counter = 0
        while 1: # read in blocks loop
            Block = File.read(MEG)
            if not Block: #EOF
                break
            Text += Block
            Pos = -1 #set up as dummy before the loop
            while 1: #look for scans and offsets loop
                ScanPos = Text.find("SCAN", Pos + 1)
                if not ScanPos == -1:
                    ## 1. Get the scan number
                    ActualNumberPos = Text.find("=", ScanPos)
                    EndNumberPos = Text.find("\n", ScanPos)
                    ScanNumber = int (Text[ActualNumberPos + 1:EndNumberPos])
                    #print ScanNumber
                    ## 2. Get the BEGIN tag
                    BeginPos = Text.rfind("BEGIN", 0, ScanPos)
                    ScanOffset = FileOffset + BeginPos
                    if not self.ScanOffset.has_key(ScanNumber):
                        self.ScanOffset[ScanNumber] = ScanOffset
                        #yes I got the above error for who knows why
                else:
                    ##did not find a scan number. Two possibilities
                    ## Can or Cannot find a BEGIN
                    BeginPos = Text.find("BEGIN", Pos + 1)
                    if not BeginPos == -1:
                        #Begin was found, seam text to begin here
                        print "Most recent Scan was %s"%ScanNumber
                        SeamText = Text[BeginPos:]
                        break
                    else:
                        #here it is possible that the word begin spans the break
                        #to prevent that case, we simply make some seam text
                        SeamText = Text[-20:]
                        break
                Pos = EndNumberPos

            #now we've broken out of the finding loop.  Need to reset some vars
            LenBlock = len(Text)                
            Text = SeamText
            FileOffset += LenBlock # can't use MEG here, because Text included some seam text
            FileOffset -= len(SeamText)
        File.close()
        self.Validate(FileName)
        return self.ScanOffset

    def Validate(self, FileName):
        "simple check of scanoffset"
        File = open(FileName, "rb")
        ErrorFound =0
        for (ScanNumber, ScanOffset) in self.ScanOffset.items():
            File.seek(ScanOffset)
            Text = File.read(300)
            Place = Text.find("BEGIN")
            #print "Found begin at place %d"%Place
            if not Text.find("BEGIN") == 0:
                print "Error with scan %d"%ScanNumber
                ErrorFound = 1
                print Text
        if not ErrorFound:
            print "Validation Successful"
        
            
