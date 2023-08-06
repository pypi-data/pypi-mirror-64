# -*- coding: UTF-8 -*-
"""
Sequence based Similarity (Alternative to Simulator)
----------------------------------------------------
using tryptic peptide sequences instead of spectra

Including:
trypticCut:
  produce trypsin digested peptides of all proteins in fasta-file
peptideSearch:
  search all sequences from a given fasta-file in a given database (fasta);
  get the number of tryptic peptides from proteome A also matching proteome B
cutNsearch:
  combine trypticCut and peptideSearch
weightPeptides:
  search identified peptides in tryptic peptide list of a proteome in order to
  weight each peptide by its frequency (using 3 normalization steps)
weightedMatching:
  use weighted peptides to calculate a weighted proteome similarity summing up
  weights of tryptic peptides from proteome A also matching proteome B
weightedMatrix:
  perform weightPeptides and weightedMatching for a number of proteomes
  combining all pairs of proteomes
weightedMatrix_short:
  short version of weightedMatrix using already weighted peptides
filterParsed:
  specialized sampling of peptide spectrum identifications; on the basis of
  readMGF.filterFDR, but for identifications instead of spectra, also using
  spectrum numbers from readMGF.getFilterIDs

still contained, but out of use:
uniqPeptides:
  for each sequence found in a fasta-file, copy only the first occurrence to a
  new file [actually no use in further analyses]
decoyFilter:
  copy only non-decoy peptide matches from InspectParser_uniq.py output or
  Inspect output identification list to a new file
  [actually no use in further analyses]
getSharedDic:
  create a dictionary of potentially ambiguous peptide sequences
  [very time-consuming! Dictionary constructed on the way where required]


@author: Anke Penzlin, May 2013
"""

import numpy as np
import os
import re
import optparse
import sys
from Bio import SeqIO

def trypticCut(fastaFile, verbose=True):
	"""
	cut all protein sequences from a given fasta-file into tryptic peptides.
	Peptide sequences (+ protein description) are written to a new fasta file.
	(return: path to peptide file, number of peptides)

	fastaFile: protein sequences to be cut
	"""
	nprot = 0   # number of proteins (in fastaFile)
	peptLs = [] # tryptic peptides
	protLs = [] # description (ID/name) of the respective protein from db
	if verbose: print 'Reading and cutting protein sequences from '+fastaFile+' ...'
	for record in SeqIO.parse(open(fastaFile, "rU"), "fasta") :
		nameP = record.description
		# cut after lysine:
		pepsLys = [pep+"K" for pep in str(record.seq).upper().split("K")]
		pepsLys[-1] = pepsLys[-1][:-1] # last read was added a "K", which did not exist in the sequence.
		# remove cut before proline:
		pepsLysP = [pepsLys[0]]
		for pe in range(1,len(pepsLys)):
			if re.match("P",pepsLys[pe]): # if a sequence starts with P [...., "xxxxk", "Pyyyyk", ... ]
				pepsLysP[-1] += pepsLys[pe] # [..., "xxxxkPyyyk", ....]
			else: pepsLysP.append(pepsLys[pe])
		# cut after arginine:
		for pept in pepsLysP:
			pepsArg = [pep+"R" for pep in pept.split("R")]
			pepsArg[-1] = pepsArg[-1][:-1]
			# remove cut before proline:
			pepsArgP = [pepsArg[0]]
			for pe in range(1,len(pepsArg)):
				if re.match("P",pepsArg[pe]):
					pepsArgP[-1] += pepsArg[pe]
				else: pepsArgP.append(pepsArg[pe])
			# only accept peptides of length 7 - 25
			for pep in pepsArgP:
				if len(pep) > 6 and len(pep) < 26:
					peptLs.append(pep) # store peptide sequence
					protLs.append(nameP) # store corresponding description
		nprot += 1
	PeptProtLs = zip(peptLs,protLs)
	if verbose: print "Found %i proteins, obtained %i peptides" %(nprot,len(peptLs))

	outpath = os.path.dirname(fastaFile) + "/peptides_" + os.path.basename(fastaFile)
	if verbose: print 'Writing peptides to '+outpath+" ..."
	outF = open(outpath,"w")
	for pep in PeptProtLs:
		outF.write(">"+pep[1]+"\n")
		outF.write(str(pep[0])+"\n")
	outF.close()
	return outpath,len(peptLs)


def peptideSearch(peptFile,dbFile,total=50000,verbose=True):
	"""
	search all peptide sequences from a given fasta-file in a given database
	and count matches (return: number of matches, number of searched peptides)

	peptFile: peptide sequences (fasta-format)
	dbFile:   protein database (fasta-format)
	total:    number of peptides in peptFile
	"""

	DB = [] # list of protein sequences from dbFile
	cPept = 0 # number of peptides
	cMatch = 0 # number of matches (peptide <-> DB sequence)

	if verbose: print "reading DB sequences ..."
	# store all protein sequences from DB in a list
	for record in SeqIO.parse(open(dbFile, "rU"), "fasta") :
		DB.append(str(record.seq).upper())

	if verbose: print "reading and searching peptide sequences ..."
	# search each peptide sequence from peptFile in DB and count matches
	for pept in SeqIO.parse(open(peptFile, "rU"), "fasta") :
		if verbose and cPept%100 == 0:
			msg = "Peptide %i of %i"%(cPept,total)
			sys.stdout.write("\r" + " "*(len(msg)+5) + "\r" + msg)
			sys.stdout.flush()
		cPept += 1
		for DBi in DB:
			if str(pept.seq).upper() in str(DBi):
				cMatch += 1
				break # only one match per peptide is counted
	if verbose: print "\r%i of %i peptides found" %(cMatch,cPept)
	return cMatch,cPept

def cutNsearch(proteinFile,dbFile):
	"""
	produce tryptic peptides from proteinFile and search them in the sequences
	of dbFile. (return: ratio of matches/peptides)
	"""
	peptFile, nr = trypticCut(proteinFile)
	cMatch, cPept = peptideSearch(peptFile,dbFile,total=nr)
	return float(cMatch)/cPept

def unweightedMatrix(dbList, verbose=True):
	"""
	for all proteomes, run pairwise peptide search to construct an unweighted
	similarity matrix. (return: proteome similarity matrix)
	using:    trypticCut
	          peptideSearch

	dbList:       list of protein database files (fasta-format, full path),
	              ","-separated
	"""

	dbList = dbList.split(",")
	Mx = np.zeros([len(dbList),len(dbList)]) # proteome similarity matrix
	for i,DBi in enumerate(dbList):
		if verbose: print "\n"
		# compose filename of spectra and database
		trypticPeptides, nr = trypticCut(DBi, verbose=verbose) # database peptides
		for j,DBj in enumerate(dbList):
			cMatch, cPept = peptideSearch(trypticPeptides,DBj,total=nr,verbose=verbose)
			Mx[i,j] = float(cMatch)/cPept
	return Mx # proteome similarity matrix


# not further used.
# simply ignores all but the first occurrence of shared peptide sequences.
def uniqPeptides(peptFile):
	"""
	create a fasta-file of non-redundant peptide sequences from peptFile.
	(return: path to created file)

	peptFile: peptide sequences (fasta-format)
	"""

	outfile = os.path.dirname(peptFile) + "/uniq_" + os.path.basename(peptFile)
	newls = []
	peps = []
	n_peps = 0

	print "reading peptide sequences ..."
	for pept in SeqIO.parse(open(peptFile, "rU"), "fasta") :
		#if ilqk: #later on
		#	pept = pept.replace("I", "L").replace("Q", "K")
		if not str(pept.seq) in peps:
			peps.append(str(pept.seq))
			newls.append(pept)
		n_peps += 1
	print "%i different peptide sequences out of %i peptides" %(len(peps),n_peps)
	output_handle = open(outfile, "w")
	for record in newls:
		SeqIO.write(record, output_handle, "fasta")
	output_handle.close()
	return outfile


# not further used, replaced by a single line while file reading where required
def decoyFilter(peptFile):
	"""
	parse list of non-decoy peptide matches from Inspect output list.
	(return: path to the new list file)

	peptFile: peptide list from Inspect output or InspectParser_uniq.py output
	          (protein name must be contained in each line!)
	"""

	outfile = os.path.dirname(peptFile) + "/nondecoy_" + os.path.basename(peptFile)
	newls = []
	n_peps = 0

	print "reading sequences of identified peptides ..."
	inF = open(peptFile,"r")
	inF.readline()
	inF.readline()
	for line in inF:
		if not "REVERSED" in line: # part of protein names for decoy entries
			newls.append(line)
		n_peps += 1
	print "%i of %i peptides are non-decoy matches" %(len(newls),n_peps)
	outF = open(outfile, "w")
	for line in newls:
		outF.write(line)
	outF.close()
	return outfile


# not further used - long runtime!!
def getSharedDic(peptList):
	"""
	create a dictionary of peptide sequences and their occurrences in peptList
	"""
	peps = np.array(peptList)
	peps_u = np.unique(peps)
	u_dict = dict()
	for u in peps_u:
		u_dict[u] = np.where(peps == u)
	return u_dict


# based on inspectparser.py output
# (list of peptide hits and corresponding protein names)
def weightPeptides(identifiedPeptides, trypticPeptides, fdr=1, init=0, ilqk=False, sep="\t", decoy_tag= "REVERSED|DECOY", verbose=True):
	"""
	search identified peptides in tryptic peptide list of a proteome in order
	to weight each peptide
	(return: path to output file with line structure: "weight	sequence")

	identifiedPeptides: inspectparser.py output (experimental spectra)
	trypticPeptides:    typticCut result of proteome in question
	fdr:                cut-off controlling false discovery rate (1 = no cut)
	init:               initial weight for all peptides
	ilqk:               handle isoleucine as leucine and glutamine as lysine
	                    (because of their equal/very similar mass), if true
	sep:                seperator for split of identifiedPeptides input lines,
	                    do not change unless your input type has the same
                        content as inspectparser.py output
	decoy_tag:          string that specifies how decoy sequences in the DB
	                    are labeled. By default, "REVERSED" or "DECOY" are
			    accepted.
	"""

	outfile = os.path.dirname(identifiedPeptides) + "/matched_init_"+ str(init) + "_" + os.path.splitext(os.path.basename(trypticPeptides))[0] + "_to_" + os.path.basename(identifiedPeptides)
	trypList = [] # list of tryptic peptides
	trypDic = dict() # dictionary of all peptide sequences and corresponding indices in trypList
	protDic = dict() # dictionary of protein names and corresponding indices in trypList
	idx = 0 # index of current peptide read from trypticPeptides used in trypList

	if verbose: print "reading sequences of tryptic peptides ..."
	for pept in SeqIO.parse(open(trypticPeptides, "rU"), "fasta") :
		# dictionary of protein names (descriptions)
		p_name = str(pept.description)

		if p_name in protDic: # add peptide (by index) to its protein
			protDic[p_name].append(idx) # 'Function: Hypothetical protein # pI:9.61 MW:13750': [871, 872, 873, 874, 875]
		else: # add new protein name (+ first entry) to dictionary
			protDic[p_name] = [idx]

		# peptide sequence
		'''if ilqk:
			pept = str(pept.seq).replace("I", "L").replace("Q", "K")
		else:
			pept = str(pept.seq)'''
		pept = str(pept.seq)#!!! .replace("I", "L")
		trypList.append(pept)
		# dictionary of peptide sequences indicating unique and shared peptides
		if pept in trypDic: # add index of current peptide to already known sequence
			trypDic[pept].append(idx)
		else: # add new entry to sequence dictionary
			trypDic[pept] = list([idx])
		idx += 1
	if verbose: print len(trypDic), "different sequences out of", len(trypList), "peptides from", len(protDic), "proteins"
	# array for peptide match counts
	counts = [init]*len(trypList)
	# counter for peptides not in tryptic peptide list
	notfound = 0

	'''# monitoring not found sequences
	with open("/data/NG4/anke/spectra/Shigella_dysenteriae/out/testOutput.txt","w") as f:
		f.write("")'''
	if verbose: print "reading and searching sequences of identified peptides ..."
	inF = open(identifiedPeptides,"r")
	inF.readline()
	inF.readline()
	for line in inF:
		if float(line.split(sep)[5]) > fdr: break # use only reliable part of peptide list
		if not re.search(decoy_tag,line.split(sep)[6]): # use only non decoy hits
			'''pept = line.split(sep)[2] # read identified peptide sequence
			if ilqk:
				pept = pept.upper().replace("I", "L").replace("Q", "K")'''
			pept = (line.split(sep)[2])#!!! .replace("I", "L") # read identified peptide sequence
			# split identified peptide into tryptic peptides (if neccessary)
			# cut after lysine:
			pepsLys = [pep+"K" for pep in pept.split("K")]
			pepsLys[-1] = pepsLys[-1][:-1]
			# remove cut before proline:
			pepsLysP = [pepsLys[0]]
			for pe in range(1,len(pepsLys)):
				if re.match("P",pepsLys[pe]):
					pepsLysP[-1] += pepsLys[pe]
				else: pepsLysP.append(pepsLys[pe])
			# cut after arginine:
			for pept in pepsLysP:
				pepsArg = [pep+"R" for pep in pept.split("R")]
				pepsArg[-1] = pepsArg[-1][:-1]
				# remove cut before proline:
				pepsArgP = [pepsArg[0]]
				for pe in range(1,len(pepsArg)):
					if re.match("P",pepsArg[pe]):
						pepsArgP[-1] += pepsArg[pe]
					else: pepsArgP.append(pepsArg[pe])
				for pep in pepsArgP:
					# only accept peptides of length 7 - 25
					if len(pep) > 6 and len(pep) < 26:
						# search each peptide in list of proteome tryptic peptides
						if pep in trypList:
							counts[trypList.index(pep)] += 1
						else:
							notfound += 1
							'''# monitoring not found sequences
							with open("/data/NG4/anke/spectra/Shigella_dysenteriae/out/testOutput.txt","a") as f:
								f.write(pep + "\tfrom\t" + line.split(sep)[2] + "\n")'''
	# calculate weights from counts
	if verbose: print "not found: %i of %i"%(notfound,sum(counts)+notfound), 'against the database with ', len(trypList), ' peptides'

	if sum(counts) > 0:
		if verbose: print "recalculating counts for shared peptides ..."
		for t in trypList: # equally distribute counts for peptides of same sequence
			t_ind = trypDic.get(t) # Example: [19109, 20150, 20515, 21608, 23335]
			x = sum([counts[c] for c in t_ind])/float(len(t_ind))
			for i in t_ind:
				counts[i] = x

		sum_c = sum(counts)
		for p in protDic: # equally distribute counts for peptides of same protein
			# normalized by the sum of all counts (sum_c)
			p_ind = protDic.get(p)
			x = sum([counts[c] for c in p_ind])/float(len(p_ind))/sum_c
			for i in p_ind:
				counts[i] = x
	else:
		print "Warning: no peptides identified!"
	if verbose: print "writing resulting weights ..."
	cPos = 0 # number of positively weighted peptides
	outF = open(outfile,"w")
	# output file line structure: "weight	sequence"
	for idx, seq in enumerate(trypList):
		outF.write(str(counts[idx])+"\t"+seq+"\n")
		if not counts[idx] == 0:
			cPos += 1
	outF.close()
	if verbose: print cPos,"of",len(trypList),"peptides got positive weight."
	return outfile


def weightedMatching(weightedPeptFile,dbFile,total,sum_all=True, verbose=True):
	"""
	search all weighted peptide sequences from a given file in a given database
	(return: weighted sum of matches, number of matches, number of peptides)

	weightedPeptFile: textfile of weighted peptide sequences
	         (weightPeptides output file line structure: "count	sequence")
	dbFile:  protein database (fasta-format)
	total:   number of peptides in weightedPeptFile (only relevant for
	         progress display)
	sum_all: add up weights of matching peptides; if false, set count of
	         matching peptides with weight > 0 to 1 (only suitable for init=0)
	"""

	DB = [] #list of protein sequences from dbFile
	cPept = 0 # number of peptides
	cMatch = 0 # number of matches (weighted peptide <-> DB peptide)
	pMatch = float(0) # weighted sum of matches

	if verbose: print "reading DB sequences ..."
	for record in SeqIO.parse(open(dbFile, "rU"), "fasta") :
		DB.append(str(record.seq).upper())#.replace("I", "L"))#!!! .replace("Q", "K"))
	if not sum_all: prot_count = [0]*len(DB)
	if verbose: print "reading and mapping peptide sequences ..."
	for line in open(weightedPeptFile, "rU"):
		if verbose and cPept%100 == 0: # progress display
			msg = "Peptide %i of %i"%(cPept,total)
			sys.stdout.write("\r" + " "*(len(msg)+5) + "\r" + msg)
			sys.stdout.flush()
		cPept += 1
		for i,DBi in enumerate(DB): # search process (weighted peptide in DB)
			if line.split("\t")[1].rstrip().upper() in str(DBi): # to see where parsed peptides in proteins or not
				cMatch += 1
				if sum_all: pMatch += float(line.split("\t")[0])
				elif (float(line.split("\t")[0]) > 0): prot_count[i] = 1
				break
	if not sum_all: #normalization (neccessary for count data)
		pMatch = float(sum(prot_count))/len(DB)

	if verbose: print "\r%i of %i peptides found" %(cMatch,cPept)
	return pMatch, cMatch, cPept # weighted sum of matches, #matches, #peptides


def weightedMatrix(spectra_name, dbList, fdr=0.05, init_weight=0, Tide=False, decoy_tag="REVERSED|DECOY", verbose=True):
	"""
	Based on InsPecT output (or output parsed by inspectparser)
	for dataset and all proteomes, construct a weighted similarity matrix
	(return: proteome similarity matrix weighted by dataset)
	using:    inspectparser or corresponding output
	          trypticCut
	          weightPeptides
	          weightedMatching
	requires: InsPecT output file named nameSpectra'_'nameDB'_InspectOut.txt'
	          or a '_parsed.txt' version (used preferably) of this file in the
	          directory given in spectra_name

	spectra_name: name of spectra dataset used to identify peptides via Inspect
	              (path of Inspect output)
	dbList:       list of protein database files (fasta-format, full path),
	              ","-separated
	fdr:          cut-off controlling false discovery rate (1 = no cut)
	init_weight:  initial weight for all peptides (see weightPeptides), default=0
	"""

	from inspectparser import parseInspect

	dbList = dbList.split(",")
	Mx = np.zeros([len(dbList),len(dbList)]) # proteome similarity matrix
	for i,DBi in enumerate(dbList):
		if verbose: print "\n"
		# compose filename of spectra and database
		if Tide:
			identifiedPeptides = os.path.splitext(spectra_name)[0] +"_"+ os.path.splitext(os.path.basename(DBi))[0] +"_TideOut_parsed.txt"
			if not os.path.exists(identifiedPeptides):
				print "Could not find PSM-file for %s and %s" %(spectra_name,DBi)
				continue
		else:
			inspectOut = os.path.splitext(spectra_name)[0] +"_"+ os.path.splitext(os.path.basename(DBi))[0] +"_InspectOut.txt"
			identifiedPeptides = inspectOut[:-4]+"_parsed.txt" # dataset peptides
			if not os.path.exists(identifiedPeptides):
				try:
					identifiedPeptides = parseInspect(inpath=inspectOut,fdr_countcut=fdr,multipleFiles=True,silent=True)
				except:
					print "Could not find PSM-file for %s and %s" %(spectra_name,DBi)
					print "Current task:"
					print weightedMatrix.__doc__
					continue
		trypticPeptides, nr = trypticCut(DBi, verbose=verbose) # cut database peptides
		weightedPeptFile = weightPeptides(identifiedPeptides, trypticPeptides, fdr=fdr, init=init_weight, decoy_tag=decoy_tag, verbose=verbose)
		for j,DBj in enumerate(dbList):
			pMatch, cMatch, cPept = weightedMatching(weightedPeptFile,DBj,total=nr,verbose=verbose)
			Mx[i,j] = pMatch
	print Mx
	return Mx # proteome similarity matrix


# Short matrix calculation if weights are known (from previous calculations),
# e.g. counting matching peptides with weight > 0 (sum_all=False) using known init=0 weights.
def weightedMatrix_short(spectra_name, dbList, sum_all=False):
	"""
	construct a weighted similarity matrix based on files of weighted peptides
	for each combination of dataset and proteome (db).
	(return: proteome similarity matrix weighted by dataset)
	using: weightedMatching

	spectra_name: name of spectra dataset used to identify peptides via Inspect
	              (path of Inspect output)
	dbList:       list of protein database files (fasta-format, full oath),
	              ","-separated
	sum_all:      see weightedMatching, except for default: False
	"""

	dbList = dbList.split(",")
	Mx = np.zeros([len(dbList),len(dbList)])
	for i,DBi in enumerate(dbList):
		print "\n"
		identifiedPeptides = os.path.splitext(spectra_name)[0] +"_"+ os.path.splitext(os.path.basename(DBi))[0] +"_InspectOut_parsed.txt"
		weightedPeptFile = os.path.dirname(identifiedPeptides) + "/matched_peptides_" + os.path.splitext(os.path.basename(DBi))[0] + "_to_" + os.path.basename(identifiedPeptides)
		for j,DBj in enumerate(dbList):
			#if DBj == DBi:
			#	Mx[i,j] = 1.
			#else:
			pMatch, cMatch, cPept = weightedMatching(weightedPeptFile,DBj,total=50000,sum_all=sum_all)
			Mx[i,j] = pMatch
	return Mx


# sampling peptide spectrum matches using quality filter (getFilterIDs in readMGF.py)
def filterParsed(spectra,filterIDs, verbose=True):
	"""
	from a given inspectparser output select spectra according to
	corresponding Inspect score using filterIDs sampled by readMGF.getFilterIDs
	(return: path to sample file)

	spectra:   file of peptide spectrum matches in parsed format
	           (inspectparser output)
	filterIDs: spectrum numbers sampled by readMGF.getFilterIDs
	"""
	notfound = 0 # print warning if any spectrum could not be found
	specDic = dict() # datastructure for fast access on spectra by number
	with open(spectra) as f: allSpectra = f.readlines()
	del allSpectra[0:2] # delete header of inspectparser output file
	for nr,line in enumerate(allSpectra):
		list = line.split("\t") # spectrum number (1) and match score (3) easily accessible
		# ignore file name if prefix of id (concatenated by '..'); ids must be unique (no mixed files)
		id = int(list[1].split("..")[1]) if len(list[1].split("..")) > 1 else int(list[1])
		# insert index of line in allSpectra and split line into dictionary, key = id
		specDic[id] = [nr,list]
	# name of sample file includes '_filter' and number of samples:
	newfile = os.path.splitext(spectra)[0] + "_filter" + str(len(filterIDs)) + os.path.splitext(spectra)[1]
	if verbose: print 'Writing '+str(len(filterIDs))+' spectra to '+newfile+" ..."
	outlist = [] # list of sampled dictionary entries
	for z in filterIDs:
		z = int(z)
		if z in specDic: outlist.append(specDic[z])
		else: notfound += 1
	# restore order by match scores:
	outlist.sort(key = lambda x : float(x[1][3]), reverse = True)
	outfile = open(newfile,"w")
	# write sampled lines of input file to newfile using list index for allSpectra
	for entry in outlist: outfile.write(allSpectra[entry[0]])
	outfile.close()
	if notfound > 0: print "!! %i spectra could not be found" %notfound
	return newfile
'''# slow because of specID search:
def filterParsed(spectra,filterIDs):#, fdrfile, scoreTab, maxN=1000):
	"""
	from a given InspectParser_FDR_uniq output select spectra according to corresponding Inspect score.
	"""
	#from readMGF import getFilterIDs
	#rnum, n = getFilterIDs(fdrfile=fdrfile, scoreTab=scoreTab, maxN=maxN)
	with open(spectra) as f: allSpectra = f.readlines()
	del allSpectra[0:2]
	newfile = os.path.splitext(spectra)[0] + "_filter" + str(len(filterIDs)) + os.path.splitext(spectra)[1]
	print 'Writing '+str(len(filterIDs))+' spectra to '+newfile+" ..."
	outlist = []
	for z in filterIDs:
		x = np.array(map(lambda y: y.split("\t")[1].find(str(z)), allSpectra))
		idx = np.where(x >= 0)[0]
		if len(idx) > 0: outlist.append(allSpectra[idx[0]])
	outlist.sort(key = lambda x : float(x.split("\t")[3]), reverse = True)
	outfile = open(newfile,"w")
	for line in outlist: outfile.write(line)
	outfile.close()
	return newfile
'''

if __name__=="__main__":
	usage = """%prog PROTFILE DBFILE

		Command line interface of 'cutNsearch', producing tryptic peptides of the fasta
		sequences in PROTFILE and counting occurrences of these peptides in DBFILE.
		(Most functions of corresponding script file are not included in the interface)

		Using the easy mode (--easy) to have a quick understand of this function.

		"""

	# configure the command line parser
	command_parser = optparse.OptionParser(usage=usage)
	#command_parser.add_option('-f', '--fdr', type='float', dest='fdr', default=1, help='list will be cut at FDR-value [default: %default (means no cut)]')
	command_parser.add_option('-e', '--easy', type='string', dest='easy', default=None, help='For the beginner, setting the value to True to run this script. Use true or True to activate.')

	# parse arguments and options
	options, args = command_parser.parse_args()

	if not options.easy:
		if len(args) == 2:
			print cutNsearch(args[0],args[1])
		else:
			command_parser.print_help()
	if (options.easy).lower() == 'true':
		M_list_wtd = []
		for spec in ['example']:
			M_list_wtd.append(weightedMatrix(spectra_name='../data/spectra/' + spec,
																				dbList='../data/reference/species1.fasta,../data/reference/species2.fasta',
																				fdr=0.05, init_weight=0,
																				verbose=True,
																				Tide=False,
																				decoy_tag='REVERSED|DECOY'))
			np.array(M_list_wtd).dump('../../result'+"_mList_weighted.dat")

	'''resulting sequence similarity (matching tryptic peptides to refDB):
	peptides_EcoliDH10B -> Shigelladys: 0.6282523791187634 (34263/54537)
	peptides_Shigelladys -> EcoliDH10B: 0.7151272577996716 (34841/48720)
	spectral similarity (MSSim): simShig = np.array([[1.0,  0.58696331], [0.71932158,  1.0]])

	weighted by exp. spectra "Ecoli_12189_filter20000":
	peptides_EcoliDH10B -> Shigelladys: 0.8793818269104893 (34263/54537) #weightedMatching("../../spectra/Shigella_dysenteriae/out/matched_peptides_EcoliDH10B_to_Ecoli_12189_filter20000_EcoliDH10B_InspectOut_parsed.txt","../../proteome/Shigelladys.fasta",54537)
	peptides_Shigelladys -> EcoliDH10B: 0.9236761034288927 (34841/48720) #weightedMatching("../../spectra/Shigella_dysenteriae/out/matched_peptides_Shigelladys_to_Ecoli_12189_filter20000_Shigelladys_InspectOut_parsed.txt","../../proteome/EcoliDH10B.fasta",48720)
	peptides_x -> x: all found

	weighted by exp. spectra "Shigelladys_1_all_filter20000":
	peptides_EcoliDH10B -> Shigelladys: (0.9528234762832758, 34263, 54537) # weightedMatching(searchExperimental("../../spectra/Shigella_dysenteriae/out/Shigelladys_1_all_filter20000_EcoliDH10B_InspectOut_parsed.txt","../../proteome/peptides_EcoliDH10B.fasta",fdr=0.05),"../../proteome/Shigelladys.fasta",54537)
	peptides_Shigelladys -> EcoliDH10B: (0.9092465576969604, 34841, 48720) # weightedMatching(searchExperimental("../../spectra/Shigella_dysenteriae/out/Shigelladys_1_all_filter20000_Shigelladys_InspectOut_parsed.txt","../../proteome/peptides_Shigelladys.fasta",fdr=0.05),"../../proteome/EcoliDH10B.fasta",48720)
	peptides_EcoliDH10B -> EcoliDH10B: (1.0000000000001164, 54537, 54537) # weightedMatching(searchExperimental("../../spectra/Shigella_dysenteriae/out/Shigelladys_1_all_filter20000_EcoliDH10B_InspectOut_parsed.txt","../../proteome/peptides_EcoliDH10B.fasta",fdr=0.05),"../../proteome/EcoliDH10B.fasta",54537)

	matching tryptic peptides to refDB:
	Bacicer -> Bacisub168: 0.03248105914484546
	Bacisub168 -> Bacisub: 0.037594533029612756
	spectral similarity (MSSim): simB_800_l3 = np.array([[ 1.0 , 0.01346487],[ 0.01373776, 1.0 ]])
		simBac = np.array([[1.0, 0.024390243902439025, 0.0040650406504065045],[0.024473147518694765, 1.0, 0.003399048266485384],[0.0006747638326585695, 0.0006747638326585695, 1.0]])
	'''

	'''
	Example result:
									Reading and cutting protein sequences from ../../example/ref/species2.fasta ...
									Found 2409 proteins, obtained 27847 peptides
									Writing peptides to ../../example/ref/peptides_species2.fasta ...
									reading sequences of tryptic peptides ...
									24542 different sequences out of 27847 peptides from 2373 proteins
									reading and searching sequences of identified peptides ...
									not found: 12 of 296
									recalculating counts for shared peptides ...
									writing resulting weights ...
									1885 of 27847 peptides got positive weight.
									reading DB sequences ...
									reading and mapping peptide sequences ...
									5226 of 27847 peptides found
									reading DB sequences ...
									reading and mapping peptide sequences ...
									27847 of 27847 peptides found
	'''
