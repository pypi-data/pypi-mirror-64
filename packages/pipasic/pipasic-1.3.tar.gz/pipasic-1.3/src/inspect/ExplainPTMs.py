#Title:          ExplainPTMs.py
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
Once an unrestrictive PTM search has completed, attempt to suggest
possible (bio)chemical explanations for the modifications seen.
"""
import Global
from Utils import *
Initialize()

# Mass delta (in daltons) -> list of PTMs
AllPTMsByMass = {}
InitializeFlag = 0

def FixQuotedString(String):
    if String and String[0] == '"' and String[-1] == '"':
        return String[1:-1]
    return String

class PTMClass:
    def __init__(self, SourceDB, DBID, Name, Residues, Mass):
        self.SourceDB = SourceDB
        self.DBID = DBID
        self.Name = FixQuotedString(Name)
        self.Residues = Residues
        if not self.Residues:
            self.Residues = None # specific to a terminus, not a residue.
        self.Mass = Mass
        self.Terminus = "" # valid values: "C", "N", ""
    def __str__(self):
        return self.Name
    def GetURL(self):
        if self.SourceDB.lower() == "unimod":
            return "http://www.unimod.org/cgi/unimod.cgi?record_id=%s&display_details_view.x=7&display_details_view.y=5&display_details_view=on"%self.DBID
        else:
            return None
    def GetNameWithLink(self):
        URL = self.GetURL()
        if URL:
            return "<a href=\"%s\">%s</a>"%(URL, self.Name)
        else:
            return self.Name
        
def LoadPTMDatabase():
    global InitializeFlag
    global AllPTMsByMass
    if InitializeFlag:
        return
    InitializeFlag = 1
    File = open("PTMDatabase.txt", "rb")
    for FileLine in File.xreadlines():
        Bits = FileLine.split("\t")
        if FileLine[0] == "#" or len(Bits) < 5:
            continue
        try:
            Mass = int(round(float(Bits[2])))
        except:
            # No valid mass? Probably a blank line.
            continue
        PTM = PTMClass(Bits[0], Bits[1], Bits[3], Bits[4], Mass)
        if len(Bits) > 5 and Bits[5]:
            Terminus = Bits[5][0]
            if Terminus in ("C", "N"):
                PTM.Terminus = Terminus
        if not AllPTMsByMass.has_key(Mass):
            AllPTMsByMass[Mass] = []
        AllPTMsByMass[Mass].append(PTM)
    File.close()

def GetExplanation(AA, Mass, Terminus, BasePTM = 0):
    """
    Look for a known PTM that matches this residue, delta mass, and terminus.
    If we don't find any such PTM, then look for a point mutation matching the
    mass shift.  The output of this function is an initial hypothesis, and requires
    verification.
    """
    AllResidues = "ACDEFGHIKLMNPQRSTVWY"
    LoadPTMDatabase()
    Explanations = []
    # If there's a base modification applied to this residue, then we should
    # handle that case specially.  Example: On cysteine, "-57" is a missing protecting
    # group, and "-43" is a methylation!
    if BasePTM:
        if Mass == -BasePTM:
            PTM = PTMClass("ProtectingGroup", None, "Missing %+d fixed mod"%BasePTM, AA, Mass)
            Explanations.append(PTM)
            return Explanations
        Mass = Mass + BasePTM
    PTMList = AllPTMsByMass.get(Mass, [])
    for PTM in PTMList:
        PTMOK = 0
        if PTM.Residues == None:
            if Terminus == PTM.Terminus:
                #Explanations.append(PTM)
                PTMOK = 1
        elif (AA != None) and (AA in PTM.Residues):
            if Terminus == PTM.Terminus or PTM.Terminus == "":
                PTMOK = 1
                #Explanations.append(PTM)
        if not PTMOK:
            continue
        # Don't add multiple explanations with the same name!  (There's some redundancy)
        for OldExplanation in Explanations:
            if OldExplanation.Name == PTM.Name:
                PTMOK = 0
                break
        if PTMOK:
            Explanations.append(PTM)
    # Perhaps we can explain it with a mutation:
    if AA != None:
        for OtherAA in AllResidues:
            Delta = Global.AminoMass[OtherAA] - Global.AminoMass[AA]
            if abs(Delta - Mass) < 1.0:
                PTM = PTMClass("Mutation", None, "Mutation from %s to %s"%(AA, OtherAA), AA, Delta)
                Explanations.append(PTM)
    return Explanations
            
