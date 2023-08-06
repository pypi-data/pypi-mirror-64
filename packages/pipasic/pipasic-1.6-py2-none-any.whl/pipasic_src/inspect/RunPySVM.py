#Title:          RunPySVM.py
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
Wrapper for PySVM
"""
import os
import sys
import traceback
try:
    import PySVM
except:
    print "(Warning: PySVM not imported - SVM training not available)"

def Predict(FeaturePath, ModelPath, OutputPath):
    PySVM.LoadModel(ModelPath)
    InputFile = open(FeaturePath, "rb")
    OutputFile = open(OutputPath, "wb")
    for FileLine in InputFile.xreadlines():
        Bits = FileLine.split()
        FeatureVector = []
        for Bit in Bits[1:]:
            ColonPos = Bit.find(":")
            if ColonPos == -1:
                continue
            FeatureIndex = int(Bit[:ColonPos]) - 1
            while len(FeatureVector) <= FeatureIndex:
                FeatureVector.append(0)
            FeatureVector[FeatureIndex] = float(Bit[ColonPos + 1:])
        Score = PySVM.Score(FeatureVector)
        OutputFile.write("%s\n"%Score)
    InputFile.close()
    OutputFile.close()
    

if __name__ == "__main__":
    Predict("TestFeatures.SVMScaled.txt", "SVM.model", "SVMPrediction.pytxt")
