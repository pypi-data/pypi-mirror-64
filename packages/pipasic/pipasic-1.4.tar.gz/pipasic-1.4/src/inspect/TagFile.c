//Title:          IonScoring.h
//Author:         Ari Frank
//Created:        2005
// Copyright 2007,2008,2009 The Regents of the University of California
// All Rights Reserved
//
// Permission to use, copy, modify and distribute any part of this
// program for educational, research and non-profit purposes, by non-profit
// institutions only, without fee, and without a written agreement is hereby
// granted, provided that the above copyright notice, this paragraph and
// the following three paragraphs appear in all copies.
//
// Those desiring to incorporate this work into commercial
// products or use for commercial purposes should contact the Technology
// Transfer & Intellectual Property Services, University of California,
// San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910,
// Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu.
//
// IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY
// FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES,
// INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE, EVEN
// IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY
// OF SUCH DAMAGE.
//
// THE SOFTWARE PROVIDED HEREIN IS ON AN "AS IS" BASIS, AND THE UNIVERSITY
// OF CALIFORNIA HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
// ENHANCEMENTS, OR MODIFICATIONS.  THE UNIVERSITY OF CALIFORNIA MAKES NO
// REPRESENTATIONS AND EXTENDS NO WARRANTIES OF ANY KIND, EITHER IMPLIED OR
// EXPRESS, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
// MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR THAT THE USE OF
// THE SOFTWARE WILL NOT INFRINGE ANY PATENT, TRADEMARK OR OTHER RIGHTS.
//
//TagFile.c is responsible for parsing tag files from an external tagger

#include "TagFile.h"
#include "Trie.h"
#include "Tagger.h"
#include <stdio.h>
#include "Errors.h"


// Global variable
ExternalTagHolder *TagHolder=NULL;

// Reads all the contents of an external tag file
// for each scan we have new tweaks, and new tags


void ReadExternalTags(char *TagFilePath, int verbose)
{
	int MaxScan=0;
	int TotalNumTags=0;
	FILE *InputStream;
	int GlobalTagIndex=0;
	int i;

	int LineNumber = 0;
	char Buff[1024];
	int ScanNumber,NumTags;

	ScanTags *ThisScanTags=NULL;
	
	int NRead=0;	
	int Charge=0;
	float ParentMass = 0;

	char*  TempAA;
	char AnnotationBuffer[256];
	char ModBuffer[256];
	int AminoIndex;
	MassDelta* Delta;
	int ModBufferPos;
	int ModIndex;
	TrieTag *NewTag;
	int   TweakIdx;
	float Score,PrefixMass;
	char  TagSeq[16];

	if (verbose)
		printf("Parsing tags from: %s\n",TagFilePath);

	if (! TagHolder)
	{
		TagHolder = (ExternalTagHolder *)malloc(sizeof(ExternalTagHolder));
	}

	InputStream=fopen(TagFilePath,"r");
	if (! InputStream)
	{
	  //printf("Error: couldn't read external tag file: %s\n",TagFilePath);
	  //exit(1);
	  REPORT_ERROR_S(8, TagFilePath);
	  exit(8);
	}

	// read in two passes: first determine how many scans and tags there are
	// in second passs allocate the memory for all the tag
	
	while (1)
	{
	  i = 0;
	  if (! fgets(Buff,1024,InputStream))
	    break;
		
	  ScanNumber = 0;
	  NumTags = 0;
		
	  if (sscanf(Buff,"%d %d",&ScanNumber,&NumTags) == 2)
	    {
	      MaxScan=ScanNumber;
	      TotalNumTags+=NumTags;
	      LineNumber += 1;
	    }
		else
		{
		  //printf("Error parsing tag file1:\n%s\n",Buff);
		  REPORT_ERROR_IS(14,LineNumber,TagFilePath);
			exit(14);
		}

		// skip tweaks and tags this round
		
		for (i=0; i<TWEAK_COUNT+NumTags; i++)
		  {
		    fgets(Buff,1024,InputStream);
		    LineNumber += 1;
		  }
	}
	fclose(InputStream);

	if (verbose)
		printf("Allocating memory for %d scans and %d tags...\n",MaxScan+1,TotalNumTags);

	TagHolder->MaxScanNumber = MaxScan;
	TagHolder->AllScanTags = (ScanTags *)malloc((MaxScan+1)*sizeof(ScanTags));
	TagHolder->AllExternalTrieTags = (TrieTag *)malloc(TotalNumTags*sizeof(TrieTag));

	if (! TagHolder->AllScanTags || ! TagHolder->AllExternalTrieTags)
	{
	  //printf("Error: coudln't allocate sufficient memory to store all external tags!\n");
	  REPORT_ERROR(1);
		exit(1);
	}

	for (i=0; i<=MaxScan; i++)
	{
		TagHolder->AllScanTags[i].ScanNumber=i;
		TagHolder->AllScanTags[i].NumTags=0;
	}

	// read again, this time store tags
	InputStream=fopen(TagFilePath,"r");
	if (! InputStream)
	{
	  //printf("Error: couldn't read external tag file: %s\n",TagFilePath);
	  REPORT_ERROR_S(8, TagFilePath);
	  exit(8);
	}

	
	while (1)
	{
		ThisScanTags=NULL;
		i = 0;
		NRead=0;
		ScanNumber=0;
		NumTags=0;
		LineNumber = 0;

		if (! fgets(Buff,1024,InputStream))
			break;

		if (sscanf(Buff,"%d %d",&ScanNumber,&NumTags) != 2)
		{
		  //printf("Error parsing tag file2: %s\n",Buff);
		  REPORT_ERROR_IS(14,LineNumber,TagFilePath);
		  exit(14);
		  
		}

		// read tweaks
		ThisScanTags = &(TagHolder->AllScanTags[ScanNumber]);
		for (i=0; i<TWEAK_COUNT; i++)
		{
			Charge=0;
			ParentMass = 0;

			fgets(Buff,1024,InputStream);
			LineNumber += 1;
			if (sscanf(Buff,"%d %f",&Charge,&ParentMass) != 2)
			{
			  //printf("Error parsing tag file3: %s\n",Buff);
			  //exit(1); 
			  REPORT_ERROR_IS(14,LineNumber,TagFilePath);
			  exit(14);
			}

			ThisScanTags->Tweaks[i].Charge = Charge;
			if (Charge>0)
			{
				ThisScanTags->Tweaks[i].ParentMass=(int)(ParentMass* MASS_SCALE + 0.5);
			}
			else
				ThisScanTags->Tweaks[i].ParentMass=0;
		}

		ThisScanTags->NumTags = NumTags;
		ThisScanTags->Tags = &(TagHolder->AllExternalTrieTags[GlobalTagIndex]);

		// read tags (use Stephen's code to parse tags
		for (i=0; i<NumTags; i++)
		{
						
			NewTag = &(TagHolder->AllExternalTrieTags[GlobalTagIndex++]);
			fgets(Buff,1024,InputStream);
			LineNumber += 1;
			if (sscanf(Buff,"%d\t%f\t%f\t%s",&TweakIdx,&Score,&PrefixMass,TagSeq) != 4)
			{
			  //printf("Error parsing tag file4: %s\n",Buff);
			  //printf("Index: %d  ScanNumber: %d   GTI: %d\n",i,ScanNumber,GlobalTagIndex);
			  //	exit(1); 
			  REPORT_ERROR_IS(14,LineNumber,TagFilePath);
			  exit(14);
			}


			//5	24.407	1988.619	SQLK
			memset(NewTag, 0, sizeof(TrieTag));
			for (ModIndex=0; ModIndex<MAX_PT_MODS; ModIndex++)
				NewTag->AminoIndex[ModIndex]=-1;

                // Special code:
                // PepNovo may include MODIFICATIONS in its tags - so, we must parse them.
                // We assume that (a) modifications are written in the form %+d, and (b) we
                // know of the modification type from the inspect input file.
            TempAA = TagSeq;
            AminoIndex = 0;
            ModBufferPos = 0;
                
            while (*TempAA)
            {
	      if (*TempAA >= 'A' && *TempAA <= 'Z')
                {
					// an amino acid - so, finish the modification-in-progress, if there is one.
                    if (ModBufferPos && AminoIndex)
                    {
		      if (NewTag->ModsUsed == MAX_PT_MODS)
                        {
			  printf("** Error tagging scan %d from file %s: Too many PTMs!\n", ScanNumber,TagFilePath);
			  break;
                        }
                        ModBuffer[ModBufferPos] = '\0';
                        Delta = FindPTModByName(NewTag->Tag[AminoIndex - 1], ModBuffer);
                        if (Delta)
                        {
							NewTag->AminoIndex[NewTag->ModsUsed] = AminoIndex - 1;
                            NewTag->ModType[NewTag->ModsUsed] = Delta;
							NewTag->ModsUsed++;
                        }
                        else
                        {
			  printf("** Error tagging scan %d from file %s: Modification %s not understood!\n", ScanNumber, TagFilePath, ModBuffer);
			  break;
                        }
					}
                    ModBufferPos = 0;
                    // Add the AA:
                    NewTag->Tag[AminoIndex++] = *TempAA;
                }// aa
                else
                {
                    ModBuffer[ModBufferPos++] = *TempAA;
                } // not aa
                TempAA++;
            }
            NewTag->Tag[AminoIndex] = '\0';
            // Finish any pending mod (COPY-PASTA FROM ABOVE)
            if (ModBufferPos && AminoIndex)
            {
                if (NewTag->ModsUsed == MAX_PT_MODS)
                {
                    printf("** Error tagging scan %d from file %s: Too many PTMs!\n", ScanNumber, TagFilePath);
                }
                ModBuffer[ModBufferPos] = '\0';
                Delta = FindPTModByName(NewTag->Tag[AminoIndex - 1], ModBuffer);
                if (Delta)
                {
                    NewTag->AminoIndex[NewTag->ModsUsed] = AminoIndex - 1;
                    NewTag->ModType[NewTag->ModsUsed] = Delta;
                    NewTag->ModsUsed++;
                }
				else
                {
                    printf("** Error tagging scan %d from file %s: Modification %s not understood!\n",ScanNumber, TagFilePath, ModBuffer);
                }
            }

            NewTag->Charge = ThisScanTags->Tweaks[TweakIdx].Charge;
            NewTag->ParentMass = ThisScanTags->Tweaks[TweakIdx].ParentMass;
            NewTag->PSpectrum = NULL;
            NewTag->Tweak = ThisScanTags->Tweaks + TweakIdx;
            NewTag->PrefixMass = (int)(PrefixMass * MASS_SCALE + 0.5);
            NewTag->SuffixMass = NewTag->ParentMass - NewTag->PrefixMass - PARENT_MASS_BOOST;
            NewTag->Score = Score;
			NewTag->TagLength =0;
            
			for (TempAA = NewTag->Tag; *TempAA; TempAA++)
            {
                NewTag->SuffixMass -= PeptideMass[*TempAA];
				NewTag->TagLength++;
            }
			
			NewTag->Tag[NewTag->TagLength]='\0';

            for (ModIndex = 0; ModIndex < MAX_PT_MODS; ModIndex++)
            {
                if (NewTag->AminoIndex[ModIndex] >= 0 && NewTag->ModType[ModIndex])
                {
                    NewTag->SuffixMass -= NewTag->ModType[ModIndex]->RealDelta;
                }
            }
		}
	}
	fclose(InputStream);

	if (verbose)
	{
		printf("Done reading %d tags\n",GlobalTagIndex);
		printf("Max ScanNumber with tags %d\n",TagHolder->MaxScanNumber);
	}
}


void FreeExternalTagHolder()
{
	if (TagHolder)
	{
		free(TagHolder->AllScanTags);
		free(TagHolder->AllExternalTrieTags);
		free(TagHolder);
	}
}



void WriteExternalTags(char *OutFile)
{
	int i;
	FILE *OutStream;
	int TweakIdx;
	int TagIdx;
	ScanTags *ThisScan;
	TrieTag * Tag;
	int Index;
	int ModIndex;

	if (! TagHolder)
		return;

	printf("Writing tags to %s..\n",OutFile);

	OutStream=fopen(OutFile,"w");
	if (! OutStream)
	{
	  REPORT_ERROR_S(8, OutFile);
	  exit(8);
	  //printf("Error couldn't open file for writing: %s\n",OutFile);
	  //exit(1);
	}

	for (i=0; i<=TagHolder->MaxScanNumber; i++)
	{
		
		
		ThisScan = &(TagHolder->AllScanTags[i]);
		
		if (ThisScan->NumTags<=0)
			continue;

		//printf("%d %d\n",i,ThisScan->NumTags);
		fprintf(OutStream,"%d\t%d\n",i,ThisScan->NumTags);
		
		for (TagIdx=0; TagIdx<ThisScan->NumTags; TagIdx++)
		{
			Tag = ThisScan->Tags + TagIdx;
			

			fprintf(OutStream,"%d\t%.3f\t%.2f\t",Tag->Charge, (float)(Tag->PrefixMass / (float)MASS_SCALE),
												 (float)(Tag->ParentMass / (float)MASS_SCALE));

			for (Index = 0; Index < Tag->TagLength; Index++)
			{
			  //int ModIndex;
				fprintf(OutStream,"%c", Tag->Tag[Index]);

				for (ModIndex = 0; ModIndex < MAX_PT_MODS; ModIndex++)
				{	
					if (Tag->AminoIndex[ModIndex]==Index)
						fprintf(OutStream,"%s", Tag->ModType[ModIndex]->Name);
				}
			}
			fprintf(OutStream,"\n");
		}
	}

	fclose(OutStream);

	printf("Done writing tags (Max ScanNumber with tags %d)..\n",TagHolder->MaxScanNumber);
}



TrieNode *AddExternalTags(TrieNode *Root, SpectrumNode *Node)
{
	int ScanNumber = Node->ScanNumber;
	MSSpectrum* Spectrum = Node->Spectrum;	
	int DuplicateFlag;
	int NumTags;
	int TagIdx;
	int TweakIdx;
	SpectrumTweak *Tweaks;
	TrieTag * Tags;
	TrieTag *NewTag;
	
		
	//
	if (!Root)
	  {
	    Root = NewTrieNode();
	    Root->FailureNode = Root;
	  }

	for (TweakIdx=0; TweakIdx<TWEAK_COUNT; TweakIdx++)
		Node->Tweaks[TweakIdx].Charge=0;

	if (ScanNumber> TagHolder->MaxScanNumber)
		return Root;
	
	NumTags = TagHolder->AllScanTags[ScanNumber].NumTags;
	if (NumTags<=0)
		return Root;

	Tweaks = TagHolder->AllScanTags[ScanNumber].Tweaks;
	for (TweakIdx=0; TweakIdx<TWEAK_COUNT; TweakIdx++)
	{
		Node->Tweaks[TweakIdx]= Tweaks[TweakIdx];
	}

	Tags = TagHolder->AllScanTags[ScanNumber].Tags;

	// Construct a root, if we don't have one already.  
	if (!Root)
	  {
	    Root = NewTrieNode();
	    Root->FailureNode = Root;
	  }
	for (TagIdx = 0; TagIdx < NumTags; TagIdx++)
	  {
		NewTag = Tags + TagIdx;
		TweakIdx = 0;

		NewTag->PSpectrum = Spectrum; 	// Add pointers from Tag to Spectrum

		// make tag point to the spectrum's Tweak in case they need to share the 
		// later on same information

		for (TweakIdx=0; TweakIdx<TWEAK_COUNT; TweakIdx++)
		{
			if (NewTag->Tweak->Charge == Node->Tweaks[TweakIdx].Charge &&
				NewTag->Tweak->ParentMass == Node->Tweaks[TweakIdx].ParentMass)
			{
				NewTag->Tweak = Node->Tweaks + TweakIdx;
				break;
			}
		}

		if (TweakIdx == TWEAK_COUNT)
		{
			printf("BAD Error: Tweak went missing?!\n");
			exit(1);
		}

		

        AddTagToTrie(Root, NewTag, &DuplicateFlag);
    }
    //DebugPrintTrieTags(Root);
    return Root;
}




