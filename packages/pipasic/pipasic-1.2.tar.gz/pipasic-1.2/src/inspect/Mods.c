//Title:          Mods.c
//Authors:        Stephen Tanner, Samuel Payne, Natalie Castellana, Pavel Pevzner, Vineet Bafna
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

#include "CMemLeak.h"
#include "Inspect.h"
#include "Trie.h"
#include "Utils.h"
#include "FreeMod.h"
#include "Mods.h"
#include "Errors.h"
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

// AllKnownPTMods is initialized once and only once.  AllowedPTMods is a sub-array, 
// set before doing a search or batch of searches.  AllPTModCount is the size
// of array AllKnownPTMods, and AllowedPTModCount is the size of array AllowedPTMods.
PTMod AllKnownPTMods[MAX_PT_MODTYPE];
int AllPTModCount = 0;

int g_PhosphorylationMod = -1;

// PTMLimit[n] is a limit on how many modifications of type n can be placed
// on a peptide.  For each n, PTMLimit[n] <= GlobalOptions->MaxPTMods.
int g_PTMLimit[MAX_PT_MODTYPE];

int PlainOldDecorationIndex = 0;

Decoration* AllDecorations = NULL;
int AllDecorationCount = 0;
int AllDecorationAllocation = 0;

int CompareDecorations(const Decoration* A, const Decoration* B)
{
    if (A->Mass < B->Mass)
    {
        return -1;
    }
    if (A->Mass > B->Mass)
    {
        return 1;
    }
    return 0;
}

void ExpandDecorationList(int SourceDecorationIndex, int MinPTModIndex, int* PTMRemaining, int ModsLeft)
{
    int PTModIndex;
    int Decor;
    //
    if (ModsLeft <= 0)
    {
        return;
    }
    for (PTModIndex = MinPTModIndex; PTModIndex < AllPTModCount; PTModIndex++)
    {
        if (PTMRemaining[PTModIndex] <= 0)
        {
            continue;
        }
        // If we have a lot of decorations, expand the memory available for them:
        if (AllDecorationCount == AllDecorationAllocation-1)
        {
            AllDecorationAllocation *= 2;
            AllDecorations = (Decoration*)realloc(AllDecorations, sizeof(Decoration) * AllDecorationAllocation);
        }
        Decor = AllDecorationCount;
        AllDecorationCount++;
        //printf("ExpandDecorationList memcpy\n");
        //fflush(stdout);
	memcpy(AllDecorations[Decor].Mods, AllDecorations[SourceDecorationIndex].Mods, sizeof(int) * MAX_PT_MODTYPE);
        AllDecorations[Decor].Mods[PTModIndex]++;
        AllDecorations[Decor].TotalMods = AllDecorations[SourceDecorationIndex].TotalMods + 1;
        AllDecorations[Decor].Mass = AllDecorations[SourceDecorationIndex].Mass + MassDeltaByIndex[AMINO_ACIDS*MAX_PT_MODTYPE + PTModIndex]->RealDelta; 
	//printf("ExpandDecorationList memcpy done\n");
        //fflush(stdout);
        //printf("Added decoration %d (%.2f) ", Decor, AllDecorations[Decor].Mass);
        //for (ModIndex = 0; ModIndex < AllPTModCount; ModIndex++)
        //{
        //    printf("%d ", AllDecorations[Decor].Mods[ModIndex]);
        //}
        //printf("\n");

        PTMRemaining[PTModIndex] -= 1;
        ExpandDecorationList(Decor, PTModIndex, PTMRemaining, ModsLeft - 1);
        PTMRemaining[PTModIndex] += 1;
	//printf("Considering PTModIndex %d/%d\n",PTModIndex,AllPTModCount);
    }
}


//Populates the AllPTMList as if all 400 mutations were specified in the input file
int PopulatePTMListWithMutations()
{
    int ModFlags;
    
    char* StrAminos = NULL;
    char* StrType = NULL;
    char* StrName = NULL;
    float MassDelta;
    int ScaledMassDelta;
        
    int FromIndex;
    int ToIndex;
    
    int Bin;
    int ModIndex;
    char ModNameBuffer[64];


    AllPTModCount = 0;
    //
    if (!MassDeltas)
    {
        LoadMassDeltas(NULL, 0);
    }
    if (AllPTModCount == MAX_PT_MODTYPE)
    {
        // Too many!
      REPORT_ERROR_S(35, "??");
        return 0;
    }
    

    //printf("Starting to populatePTMList!!!\n");
    StrAminos = (char*)calloc(2,sizeof(char));
    StrName = (char*)calloc(5,sizeof(char));
    for(FromIndex = 0; FromIndex < AMINO_ACIDS; ++FromIndex)
    {
      if(PeptideMass[FromIndex + (int)('A')] == 0)
	continue;
      sprintf(StrAminos,"%c",(char)(FromIndex + 'A'));
      ModFlags = DELTA_FLAG_VALID;
      for(ToIndex = 0; ToIndex < AMINO_ACIDS; ++ToIndex)
	{
	  if(PeptideMass[ToIndex + (int)('A')] == 0)
	    continue;
	  if(FromIndex == ToIndex)
	    continue;
	  
	  ScaledMassDelta = PeptideMass[ToIndex + (int)('A')] - PeptideMass[FromIndex +(int)('A')];
	  
	  MassDelta = ((float)(ScaledMassDelta))/MASS_SCALE;
	  sprintf(StrName,"%c->%c",(char)(FromIndex + 'a'),(char)(ToIndex + 'a'));

	  //printf("Scaled mass of %c->%c = %d, %.3f, %s\n",(char)(FromIndex + 'A'),(char)(ToIndex+'A'),ScaledMassDelta,MassDelta,StrName);
	  // Default modification type is OPTIONAL.
	  if (!StrType)
	    {
	      StrType = "opt";
	    }
	  
	  AllKnownPTMods[AllPTModCount].Flags = ModFlags;
	  strncpy(AllKnownPTMods[AllPTModCount].Name, StrName, 5);
	  AllKnownPTMods[AllPTModCount].Allowed[FromIndex] = 1;
	  // Add to the first still-available slot:
	  for (ModIndex = 0; ModIndex < GlobalOptions->DeltasPerAA; ModIndex++)
	    {
	      if (!MassDeltas[FromIndex][ModIndex].Flags)
		{
		  strncpy(MassDeltas[FromIndex][ModIndex].Name, StrName, 40);
		  MassDeltas[FromIndex][ModIndex].RealDelta = ScaledMassDelta;
		  ROUND_MASS_TO_DELTA_BIN(MassDelta, Bin);
		  MassDeltas[FromIndex][ModIndex].Delta = Bin;
		  MassDeltas[FromIndex][ModIndex].Index = AllPTModCount;
		  MassDeltaByIndex[FromIndex * MAX_PT_MODTYPE + AllPTModCount] = &MassDeltas[FromIndex][ModIndex];
		  MassDeltaByIndex[MDBI_ALL_MODS * MAX_PT_MODTYPE + AllPTModCount] = &MassDeltas[FromIndex][ModIndex];
		  MassDeltas[FromIndex][ModIndex].Flags = ModFlags;
		  break;
		}
	    }
			  
	  AllKnownPTMods[AllPTModCount].Mass = ScaledMassDelta;
	  g_PTMLimit[AllPTModCount] = 1; // allow 1 per peptide by default
	  
	  
	  AllPTModCount++;
	  //printf("Total mods %d\n",AllPTModCount);
	}
    }
    //printf("Populate: MaxPTMods: %d\n",GlobalOptions->MaxPTMods);
    free(StrName);
    free(StrAminos);
    return 1;
}

// Entries of form IsSubDecoration[DecorIndex][OtherDecorIndex]
int** IsSubDecoration = NULL;


// After reading the definitions of all the post-translational modifications, we construct 
// a list of decorations.
// Special case:  If GlobalOptions->MandatoryModName is set, then we set MandatoryModIndex, and
// we only allow decorations that *do* contain that mod.
void BuildDecorations()
{
    int DecorIndex;
    int OtherDecorIndex;
    int ModIndex;
    int ValidSubDecoration;
    int PTMRemaining[MAX_PT_MODTYPE];
    int TotalPTMsPermitted;
    //

    // Free the old IsSubDecoration array, if allocated:
    if (IsSubDecoration)
    {
        for (DecorIndex = 0; DecorIndex < AllDecorationCount; DecorIndex++)
        {
            SafeFree(IsSubDecoration[DecorIndex]);
        }
        SafeFree(IsSubDecoration);
        IsSubDecoration = NULL;
    }
    AllDecorationAllocation = 100;
    SafeFree(AllDecorations); // Remove old ones!
    AllDecorations = NULL;
    AllDecorations = (Decoration*)calloc(AllDecorationAllocation, sizeof(Decoration));
    // AllDecorations[0] is now prepared.  (Mass 0, no mods)
    AllDecorationCount = 1;
    //printf("MAX_PT_MODTYPE: %d\n",MAX_PT_MODTYPE);
    //printf("Command: memcpy(%d,%d,%d)\n",PTMRemaining, g_PTMLimit, sizeof(int) * MAX_PT_MODTYPE);
    //fflush(stdout);
    memcpy(PTMRemaining, g_PTMLimit, sizeof(int) * MAX_PT_MODTYPE);
    TotalPTMsPermitted = GlobalOptions->MaxPTMods;
    //printf("DOne memcopy\n");
    //fflush(stdout);
    ExpandDecorationList(0, 0, PTMRemaining, TotalPTMsPermitted);
    qsort(AllDecorations, AllDecorationCount, sizeof(Decoration), (QSortCompare)CompareDecorations);

    //DEBUG-NEC
    /*for (DecorIndex = 0; DecorIndex < AllDecorationCount; DecorIndex++)
      {
	printf("AllDecorations[%d]: Mass=%d,TotalMods=%d\n",DecorIndex,AllDecorations[DecorIndex].Mass,AllDecorations[DecorIndex].TotalMods);
	for(ModIndex = 0; ModIndex < MAX_PT_MODTYPE; ++ModIndex)
	  printf(" - MassDeltas with Index %d = %d\n",ModIndex,AllDecorations[DecorIndex].Mods[ModIndex]);
      }
    */
    // Locate the index of the unmodified null-decoration.  (Usually it's #0, because
    // it has mass 0, but it's possible for PTMs to have a *negative* mass)
    for (DecorIndex = 0; DecorIndex < AllDecorationCount; DecorIndex++)
    {
        if (AllDecorations[DecorIndex].TotalMods == 0)
        {
            PlainOldDecorationIndex = DecorIndex;
            break;
        }
    }
    for (ModIndex = 0; ModIndex < AllPTModCount; ModIndex++)
    {
        if (!CompareStrings(GlobalOptions->MandatoryModName, MassDeltaByIndex[AMINO_ACIDS*MAX_PT_MODTYPE + ModIndex]->Name))
        {
            GlobalOptions->MandatoryModIndex = ModIndex;
        }
    }

    IsSubDecoration = (int**)calloc(AllDecorationCount, sizeof(int*));
    for (DecorIndex = 0; DecorIndex < AllDecorationCount; DecorIndex++)
    {
        IsSubDecoration[DecorIndex] = (int*)calloc(AllDecorationCount, sizeof(int));
        for (OtherDecorIndex = 0; OtherDecorIndex < AllDecorationCount; OtherDecorIndex++)
        {
            ValidSubDecoration = 1; // default
            for (ModIndex = 0; ModIndex < AllPTModCount; ModIndex++)
            {
                if (AllDecorations[OtherDecorIndex].Mods[ModIndex] < AllDecorations[DecorIndex].Mods[ModIndex])
                {
                    ValidSubDecoration = 0;
                    break;
                }
            }
            if (ValidSubDecoration)
            {
                IsSubDecoration[DecorIndex][OtherDecorIndex] = 1;
            }
        }
    }
}

void FreeIsSubDecoration()
{
    int ModIndex;
    for (ModIndex = 0; ModIndex < AllDecorationCount; ModIndex++)
    {
        SafeFree(IsSubDecoration[ModIndex]);
        IsSubDecoration[ModIndex] = NULL;
    }
    SafeFree(IsSubDecoration);
    IsSubDecoration = NULL;
}

// Returns a PTM with this name.  Returns NULL if no match found.
// Case-insensitive (pHoSpHoRyLaTiOn is ok).
MassDelta* FindPTModByName(char Amino, char* Name)
{
    int ModIndex;
    int AminoIndex = Amino - 'A';
    for (ModIndex = 0; ModIndex < GlobalOptions->DeltasPerAA; ModIndex++)
    {
        if (!MassDeltas[AminoIndex][ModIndex].Flags)
        {
            break;
        }
        if (!CompareStrings(MassDeltas[AminoIndex][ModIndex].Name, Name))
        {
            return &MassDeltas[AminoIndex][ModIndex];
        }
    }
    return NULL;
}
