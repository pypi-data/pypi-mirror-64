#Title:          TrieUtils.py
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


import os
import sys
import struct

TRIE_FAIL = -1
TRIE_BLOCKSIZE = 4096
MIN_TRIE_SEARCH_SIZE = 512

def Union(List,NewElement):
    for i in range(0,len(List)):
        if List[i] == NewElement:
            return List

    List.append(NewElement)
    return List

def UnionList(List1,List2):
    for i in range(0,len(List2)):
        List1 = Union(List1,List2[i])
    return List1

class TrieUtils:
    def __init__(self):
        #print "New TrieUtils!!"
        return

    def GetProteinSequence(self,ProteinNamePrefix, TrieFileName, IndexFileName):
        if not os.path.exists(TrieFileName):
            print "ERROR: TrieUtils.GetProteinSequence: %s is not a valid file name"%TrieFileName
            return None
        if not os.path.exists(IndexFileName):
            print "ERROR: TrieUtils.GetProteinSequence: %s is not a valid file name"%IndexFileName
            return None

        IndexFile = open(IndexFileName ,'r')
        
        BlockSize = struct.calcsize("<qi80s")
        while (1):
            Block = IndexFile.read(BlockSize)
            if not Block:
                IndexFile.close()
                return None
            
            Info = struct.unpack("<qi80s",Block)
            Name = str(Info[2])
            NullPos = Name.find("\0")
            if NullPos !=- 1:
                Name = Name[:NullPos]
            TriePos = Info[1]
            if Name[0:len(ProteinNamePrefix)] == ProteinNamePrefix:
                TrieFile = open(TrieFileName,'r')
                TrieFile.seek(TriePos)
                Seq = ""
                while Seq.find("*") < 0:
                    Seq += TrieFile.read(256)
                TrieFile.close()
                IndexFile.close()
                return Seq[0:Seq.find("*")]

        IndexFile.close()
        return None
            

    def GetProteinName(self,IndexFileName,ProteinID):
        if not os.path.exists(IndexFileName):
            print "ERROR: TrieUtils.GetProteinSequence: %s is not a valid file name"%IndexFileName
            return None

        IndexFile = open(IndexFileName ,'r')
    
        BlockSize = struct.calcsize("<qi80s")
        IndexFile.seek(BlockSize*ProteinID)
    
        Block = IndexFile.read(BlockSize)
        if not Block:
            IndexFile.close()
            return None
    
        Info = struct.unpack("<qi80s",Block)
        Name = Info[2]
        NullPos = Name.find("\0")
        if NullPos !=- 1:
            Name = Name[:NullPos]
        TriePos = Info[1]
        
        return Name.strip()



    def GetAllLocations(self,Peptides,TrieFileName):

        (Transitions,Output,Failure) = self.BuildTrie(Peptides)
        LocalDebug = 0
        Locations = {}
        for P in Peptides:
            Locations[P] = []

        TrieFile = open(TrieFileName,'r')
        State = 0
        ProteinID = 0
        ResidueNum = 0
        BlockCount = 0
        TrieFile.seek(0,2)
        FileBlocks = TrieFile.tell()/TRIE_BLOCKSIZE
        TrieFile.seek(0)
        pos = 0
        while(1):
            
            TrieLine = TrieFile.read(TRIE_BLOCKSIZE)
            BlockCount += 1
            #print TrieLine
            if not TrieLine:
                print "Done with this file"
                break
            for i in range(0,len(TrieLine)):
                if LocalDebug:
                    print "[%s] - %s"%(i,TrieLine[i])
                    print "%s:%s"%(ProteinID,ResidueNum)
                if TrieLine[i] == '*':
                    ResidueNum = 0
                    ProteinID += 1
                    State = 0
                    if LocalDebug:
                        print "Encountered a *, resetting"
                        #raw_input()
                    continue
                while Transitions.get((State,TrieLine[i]),TRIE_FAIL) == TRIE_FAIL:
                    if LocalDebug:
                        print "Transition[%s,%s]->%s"%(State,TrieLine[i],TRIE_FAIL)
                        print "FailState[%s]->%s"%(State,Failure[State])
                    
                    if(State == Failure[State]):
                        print "Transition[%s,%s]->%s"%(State,TrieLine[i],TRIE_FAIL)
                        print "FailState[%s]->%s"%(State,Failure[State])
                        raw_input()
                    State = Failure[State]
                    
                if LocalDebug:
                    print "Transition[%s,%s]->%s"%(State,TrieLine[i],Transitions[(State,TrieLine[i])])
                    #raw_input()
                State = Transitions[(State,TrieLine[i])]
                if Output.has_key(State):
                    for Pep in Output[State]:
                        if LocalDebug:
                            print "*****%s - %s:%s"%(Pep,ProteinID,ResidueNum)
                            raw_input()
                        Locations[Pep].append((ProteinID,ResidueNum))
                ResidueNum += 1
            print pos
            pos += len(TrieLine)
            if len(TrieLine) < TRIE_BLOCKSIZE:
                break
            if LocalDebug:
                print "Done with block!!"
                #raw_input()
        if LocalDebug:
            print "Done!"
            raw_input()
        print "Finished!!!"
        return Locations


    def BuildTrie(self,Peptides):

        #Build Transition and Output Functions
        Transitions = {}
        Output = {}
        NewState = 0
        #Str = ""
        for Pep in Peptides:
            State = 0
            J = 0
            #print Pep
            #Str += Pep
            while(J < len(Pep) and Transitions.get((State,Pep[J]),TRIE_FAIL) != TRIE_FAIL):
                State = Transitions[(State,Pep[J])]
                J += 1
            for P in range(J,len(Pep)):
                NewState += 1
                Transitions[(State,Pep[P])] = NewState
                State = NewState
        
        
            List = Output.get(State,[])
            List.append(Pep)
            Output[State] = List
        #print Str
        #raw_input()
        #Create a self loop at node 0, back to node 0
        for AA in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            S = Transitions.get((0,AA),TRIE_FAIL)
            if S == TRIE_FAIL:
                Transitions[(0,AA)] = 0
    
        #Create Failure Function
        Queue = []
        Failure = {}
        for AA in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            S = Transitions.get((0,AA),TRIE_FAIL)
            if S != 0:
                Queue = Union(Queue,S)
                Failure[S] = 0
        while len(Queue) > 0:
            R = Queue.pop(0)
            for AA in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
                S = Transitions.get((R,AA),TRIE_FAIL)
                if S != TRIE_FAIL:
                    Queue = Union(Queue,S)
                    State = Failure[R]
                    while(Transitions.get((State,AA),TRIE_FAIL) == TRIE_FAIL):
                        State = Failure[State]
                    Failure[S] = Transitions[(State,AA)]
                    Output[S] = UnionList(Output.get(S,[]),Output.get(Failure[S],[]))

        Failure[0] = 0
        return (Transitions,Output,Failure)
        
                



if __name__=="__main__":
    print "TrieUtils.py"
