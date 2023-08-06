#Title:          BasicStats.py
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
import math

def ComputeROCCurve(List):
    """
    Compute the ROC curve for a set of tuples of the form (reading, truthflag)
    """
    List.sort()
    List.reverse()
    AllPositive = 0 
    AllNegative = 0
    for (Score, Truth) in List:
        if (Truth):
            AllPositive += 1
        else:
            AllNegative += 1
    Area = 0
    TPCount = 0
    FPCount = 0
    for (Score, Truth) in List:
        if (Truth):
            TPCount += 1
        else:
            FPCount += 1
            TPRate = TPCount / float(AllPositive)
            Area += TPRate
    Area /= float(AllNegative)
    return Area

def GetMedian(List):
    LocalCopy = List[:]
    LocalCopy.sort()
    Len = len(LocalCopy)
    if Len % 2:
        return LocalCopy[Len / 2]
    return (LocalCopy[Len / 2] + LocalCopy[(Len / 2) - 1]) / 2.0
        
def Sum(List):
    Total = 0
    for Entry in List:
        Total += Entry
    return Total

def GetMedian(List):
    SortedList = List[:]
    SortedList.sort()
    Len = len(SortedList)
    if Len % 2 == 1:
        return SortedList[Len / 2]
    Score = (SortedList[Len / 2] + SortedList[(Len / 2) - 1]) / 2.0
    return Score

def GetMean(List):
    if not len(List):
        return None
    Mean = 0
    for Entry in List:
        Mean += Entry
    Mean /= float(len(List))
    return Mean

def GetMeanStdDev(List):
    "Computes mean, standard deviation for a list of numbers"
    if not len(List):
        return (0, 0)
    Mean = 0
    for Entry in List:
        Mean += Entry
    Mean /= float(len(List))
    StdDev = 0
    for Entry in List:
        StdDev += (Entry - Mean) ** 2
    StdDev = math.sqrt(StdDev / float(len(List)))
    return (Mean, StdDev)


def GetStdDev(List):
    "Computes standard deviation for a list of numbers"
    if not len(List):
        return 0.0
    Mean = 0
    for Entry in List:
        Mean += Entry
    Mean /= float(len(List))
    StdDev = 0
    for Entry in List:
        StdDev += (Entry - Mean) ** 2
    StdDev = math.sqrt(StdDev / float(len(List)))
    return StdDev

