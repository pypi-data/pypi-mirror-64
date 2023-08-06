#Title:          StripPTM.py
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
A handy function to strip unnecessary modifications from a peptide.
"""
from Utils import *
Initialize()

AMINO_ACIDS = "ACDEFGHIKLMNOPQRSTUVWY" # O and U are included, for now.
INVALID_MASS = 99999

def StripNeedlessModifications(DB, Annotation):
    """
    Replace "*" in annotations with "-".
    Also, correct "unnecessary PTM" annotations.
    Return (DBPos, FixedAnnotation) as a tuple.
    We fix the following:
    Y.A+|Y|BCD.Z   -> YABCD
    XY.A+|XY|BCD.Z -> XYABCD
    JYZ.A+|XYZ|BCD.Z -> JYZABCD
    X.ABCD+|Y|.Y   -> ABCDY
    X.ABCD+|YZ|.YZ -> ABCDYZ
    X.ABCD+|YZJ|.YZH -> ABCDYZJ
    """
    VerboseFlag = 1
    Peptide = GetPeptideFromModdedName(Annotation)
    # Find where this peptide occurs within the database:
    Aminos = Peptide.Aminos
    if Peptide.Prefix in AMINO_ACIDS:
        Aminos = Peptide.Prefix + Aminos
    if Peptide.Suffix in AMINO_ACIDS:
        Aminos += Peptide.Suffix
    DBPos = DB.find(Aminos)
    if Peptide.Prefix in AMINO_ACIDS:
        DBPos += 1
    if not Peptide.Modifications.keys():
        # An unmodified peptide?  We don't deal with those!
        return (DBPos, Annotation.replace("*", "-"))
    # Check whether a simple endpoint-shift can abolish all
    # modifications:
    ModIndex = Peptide.Modifications.keys()[0]
    ModMass = Peptide.Modifications[ModIndex][0].Mass
    # Try a shift to the LEFT:
    if ModIndex < 3:
        FlankMass = 0
        NewAA = ""
        for ShiftCharCount in (1, 2, 3):
            if DBPos - ShiftCharCount < 0:
                break
            AA = DB[DBPos - ShiftCharCount]
            FlankMass += Global.AminoMass.get(AA, INVALID_MASS)
            NewAA = AA + NewAA # prepend to the new chars
            if abs(FlankMass - ModMass) <= 2:
                # The mass matches!  Let's shift the annotation.
                if (DBPos - ShiftCharCount > 0):
                    Prefix = DB[DBPos - ShiftCharCount - 1]
                else:
                    Prefix = "-"
                FixedAnnotation = "%s.%s%s.%s"%(Prefix, NewAA, Peptide.Aminos, Peptide.Suffix)
                if VerboseFlag:
                    print "-%d The fix is in: %s to %s"%(ShiftCharCount, Annotation, FixedAnnotation)
                return (DBPos - ShiftCharCount, FixedAnnotation.replace("*", "-"))
    # Try a shift to the RIGHT:
    if ModIndex >= len(Peptide.Aminos) - 3:
        NewAA = ""
        FlankMass = 0
        OldEndpoint = DBPos + len(Peptide.Aminos) - 1
        for ShiftCharCount in (1, 2, 3):
            if OldEndpoint + ShiftCharCount >= len(DB):
                print "Off the end of the DB with %s shifted by %d"%(Annotation, ShiftCharCount)
                continue
            AA = DB[OldEndpoint + ShiftCharCount]
            FlankMass += Global.AminoMass.get(AA, INVALID_MASS)
            NewAA += AA # append the new amino acid
            if abs(FlankMass - ModMass) <= 2:
                # The mass matches!  Let's shift the annotation.
                if (OldEndpoint + ShiftCharCount + 1)<len(DB):
                    Suffix = DB[OldEndpoint + ShiftCharCount + 1]
                else:
                    Suffix = "-"
                FixedAnnotation = "%s.%s%s.%s"%(Peptide.Prefix, Peptide.Aminos, NewAA, Suffix)
                if VerboseFlag:
                    print "+%d The fix is in: %s to %s"%(ShiftCharCount, Annotation, FixedAnnotation)
                return (DBPos, FixedAnnotation.replace("*", "-"))
    # We can't edit away the PTM.  Just fix any asterisks:
    return (DBPos, Annotation.replace("*", "-"))
