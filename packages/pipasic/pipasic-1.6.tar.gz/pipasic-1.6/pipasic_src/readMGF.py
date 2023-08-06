# -*- coding: UTF-8 -*-
"""
Processing spectra files in mascot generic format
-------------------------------------------------

Including:
storeAllSpec:
  spectra from mgf-file to a python list of strings ()
sampleMGF:
  use list of spectra to write a certain number of them to a new mgf-file
filterCharge:
  filter spectra from mgf-file removing with charge > 3
plotQ (+ auxiliary function Quantile):
  visualize match qualities from Inspect results
getFilterIDs:
  specialized sampling procedure according to (Inspect) quality scores;
  spectrum IDs are sampled facilitating the selection of peptides in different
  formats (filterFDR for mgf, trypticPeptides.filterParsed for identifications)
filterFDR:
  from a given mgf-file select spectra according to spectrum IDs obtained from
  getFilterIDs
"""

import re
import random
import numpy as np
#import os # former use in creating new filenames (in filterFDR)


def storeAllSpec(mgf, verbose=True):
	"""
	write spectra from a given mgf-file to a python list of strings.
	Each spectrum is delimited by BEGIN IONS and END IONS statements and  will
	be represented by a string including line breaks.
	(return: list of spectra as mgf-strings)

	mgf: filename of input spectra in mascot generic format (mgf)
	"""
	if verbose: print "reading spectra from %s ..." %mgf
	MGF_handle = open(mgf,"r")
	specList = [] # initialize output list
	for line in MGF_handle:
		spec = ""
		if re.search("BEGIN IONS",line): #start of next spectrum
			spec += line
			for line2 in MGF_handle: #add lines of current spectrum description
				spec += line2
				if re.search("END IONS",line2): #end of current spectrum
					spec += "\n"
					break
			specList.append(spec) # add full spectrum description as list entry
	if verbose: print "found %i spectra" %len(specList)
	return specList


def sampleMGF(infile, n, outfile = ""):
	"""
	randomly choose a given number of spectra from an mgf file.
	(return: filename of sampling result)
	using: storeAllSpec

	infile:  mgf-file of input spectra
	n:       desired number of randomly sampled spectra; if 0, no sampling
	outfile: name of output file; if "", a filename including n is generated
	"""
	spectra = storeAllSpec(infile) # write spectra from input file to a list
	nprot = len(spectra) # overall number of provided spectra
	#print "Found %i spectra" % nprot
	if n == 0 or n > nprot:
		print "Take the complete list of %i spectra" %nprot
		return infile
	else:
		rnum = random.sample(range(nprot),n) # sample n list indices
		if outfile == "": outfile = infile[:-4] + "_sample"+str(n)+".mgf"
		print 'Writing '+str(n)+' spectra to '+outfile+" ..."
		f_out = open(outfile,"w")
		for z in rnum: # write file of spectra corresponding to sampled indices
			f_out.write(spectra[z])
		f_out.close()
		print "done"
		return outfile


def filterCharge(spectra, value=3, outfile="", mgf=True):
	"""
	from a given mgf-file select spectra with charge <= 3 (for Inspect)

	spectra: mgf-file containing the spectra (default) or list object as
	         produced in storeAllSpec() with mgf=False
	value:   upper limit to restrict charge, default=3 (used with Inspect)
	outfile: name of new mgf-file; if "", a filename is generated if an input
	         filename is given in spectra
	mgf:     specification of input type; True (default) if spectra contains an
	         mgf-file, False for a list object as produced in storeAllSpec()
	"""
	if mgf: # read data from file
		if outfile=="": outfile = spectra[:-4] + "_charge_max"+str(value)+".mgf"
		spectra = storeAllSpec(spectra)
	print "Writing spectra with charge < "+str(value+1)+" to "+outfile+" ..."
	handle_out = open(outfile,"w")
	for entry in spectra: # write spectra except with charge > value to outfile
		if int(entry[entry.find("CHARGE=")+7]) < value+1:
			handle_out.write(entry)
	handle_out.close()
	print "done"
	return outfile


# java-InspectParser-Output!
def plotQ(scoreTab, outfile="testplot.pdf", fdrfile="", java=True, fdrcut=0.05):
	"""
	produce a histogram of Inspect quality scores with marked FDR cut-off score
	and quantiles at lower 75% and 95%.
	(return: name of the file containing the resulting figure)
	requires: (the first two) output files from java-InspectParser
	          - peptide table (tableFilename) containing quality scores and
	          - summary of identification list (extractFilename) containing FDR
	            cut-off score (if not given, histogram without marked cut-off)
	using:    Quantile

	scoreTab: tableFilename; path to the peptide spectrum match file including
	          a table of '|Spectrum|Peptid|Score|isDecoy|FDR|'
	outfile:  output file, different image file formats possible; if no
	          specification given, create "testplot.pdf"
	fdrfile:  extractFilename; path to the summary file including
	          'score:'cut-off score in its second line
	"""

	#import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt # required plotting library
	scoreList = [] # initialize list of score values
	if java: sep = "|"
	else:
		sep = "\t"
		fdrScore = 120
	with open(scoreTab) as f: # specific for table file (skip 2 lines header)
		next(f)
		next(f)
		if java:
			for line in f: # read score value from column 3 of each identification
				scoreList.append(float(line.split(sep)[3]))
		else:
			for line in f: # read score value from column 3 of each identification
				recScore = float(line.split(sep)[3])
				scoreList.append(recScore)
				if float(line.split(sep)[5]) < fdrcut and recScore < fdrScore:
					fdrScore = recScore
	plt.clf() # initialize figure
	n, bins, patches = plt.hist(scoreList, 50, facecolor='green', alpha=0.75) # histogram of scores
	plt.axvline(Quantile(scoreList,0.95),color='grey',lw=1.3) # add lower 95%-quantile
	plt.axvline(Quantile(scoreList,0.75),color='grey',lw=1.3) # add lower 75%-quantile
	if java:
		if fdrfile != "": # if no FDR-file given, no cut-off score will be marked
			with open(fdrfile) as f: # get cut-off score (from fdrfile)
				ls = f.readlines()
				fdrScore = float(ls[1][6:]) # defined position of score in fdrfile
			plt.axvline(fdrScore,color='b') # show cut-off score in blue
	else: plt.axvline(fdrScore,color='b',lw=1.3) # show cut-off score in blue
	plt.savefig(outfile) # resulting figure will not be displayed but saved to file
	return outfile

def Quantile(data, q, precision=1.0):
	"""
	Returns the q'th percentile of the distribution given in the argument
	'data'. Uses the 'precision' parameter to control the noise level.
	source: https://gist.github.com/1840407
	[an alternative would be scipy.stats.mstats.mquantiles(), which does NOT
	 yield exactly the same results(!)]
	"""

	N, bins = np.histogram(data, bins=precision*np.sqrt(len(data)))
	norm_cumul = 1.0*N.cumsum() / len(data)

	return bins[norm_cumul > q][0]


def readIdentificationFile(infile, sep="\t"):
	"""
	read lines from a peptide identification file and store the column split version
	of those lines (without header) in a list.
	(return: list of peptide identifications as list of identification )

	infile: file containing identification lines (like output of
	        InspectParser_FDR_uniq.py or InspectParser.java Table)
	sep:    separator for splitting input identification lines,
	        default="\t" for python parser output, "|" for java Tab
	"""

	with open(infile) as f: peptList = [line.split(sep) for line in f]
	del peptList[0:2]
	return peptList

def getFilterIDs_direct(scoreTab, fdrcut=0.05, sep="\t", maxN=1000):
	"""
	specialized sampling procedure for spectra from different datasets;
	auxiliary function for filterFDR and trypticPeptides.filterParsed.
	The FDR cut-off divides the identification list into peptides considered
	reliable (higher score) and peptides with a lower score (not further analysed).
	Spectra are sampled equally from both parts.
	(return:  list of sampled SpecIDs, number of samples from each list part)
	using:    bootstrapping.readIdentificationFile

	scoreTab: tableFilename; path to the peptide spectrum match file including
	          a table of 'sepSpectrumsepPeptidsepScoresepisDecoysepFDRsep[...]'
	fdrcut:   cut-off controlling FDR in identification lists
	sep:      separator for split of scoreTab input lines,
	          default="\t" for python parser output, "|" for java Tab
	maxN:     desired sampling number of spectrum IDs from each list part,
	          if one part contains less spectra the maximum possible number is
			  used (default: 1000)
	"""
	#from bootstrapping import readIdentificationFile
	ls = readIdentificationFile(infile=scoreTab, sep=sep)
	ls.sort(key = lambda x : float(x[3]), reverse = True)
	# split input list into SpecIDs of entries with scores above / under FDR
	ls1 = [] # sub-cut-off score part of identification list
	ls2 = [] # high score part of identification list
	counter = 0.0
	countDecoys = 0.0
	fdr = 0.0
	for line in ls:
		# ignore file name if prefix of id (concatenated by '..'); ids must be unique (no mixed files)
		id = int(line[1].split("..")[1]) if len(line[1].split("..")) > 1 else int(line[1])
		counter +=1
		if line[4] == "true":
			countDecoys +=1
			fdr = countDecoys/counter
		if fdr < fdrcut:
			ls1.append(id)
		else: ls2.append(id)
	n = min(len(ls1),len(ls2),maxN) # calculate the maximum list length
	rnum1 = random.sample(ls1,n) # sample the same number from lower and
	rnum2 = random.sample(ls2,n) # from upper list part
	return rnum1+rnum2, n # concatenated list of sampled SpecIDs, number of samples from each part

'''
# based on getFilterIDs using a score value independent from identification list
# actually never used, since filterIDs are always taken from the same list as score
def getFilterIDs_val(fdrScore, scoreTab, sep="\t", maxN=1000, verbose=True):
	"""
	specialized sampling procedure for spectra from different datasets;
	auxiliary function for filterFDR and trypticPeptides.filterParsed.
	The FDR cut-off score divides the identification list into peptides considered
	reliable (higher score) and peptides with a lower score (not further analysed).
	Spectra are sampled equally from both parts.
	(return: list of sampled SpecIDs, number of samples from each list part)
	using:    bootstrapping.readIdentificationFile

	fdrScore: a float-value defining the FDR cut-off score
	scoreTab: tableFilename; path to the peptide spectrum match file including
	          a table of 'sepSpectrumsepPeptidsepScoresepisDecoysepFDRsep[...]'
	maxN:     desired sampling number of spectrum IDs from each list part,
	          if one part contains less spectra the maximum possible number is
			  used (default: 1000)
	sep:      separator for split of scoreTab input lines,
	          default="\t" for python parser output, "|" for java Tab
	maxN:     desired sampling number of spectrum IDs from each list part,
	          if one part contains less spectra the maximum possible number is
			  used (default: 1000)
	verbose:  if True, status messages and comments are printed to stdout
	"""
	from bootstrapping import readIdentificationFile

	if verbose: print "split list of spectra by cut-off score %f" %fdrScore
	# read SpecIDs and corresponding scores from scoreTab
	ls = readIdentificationFile(infile=scoreTab, sep=sep)
	# split input list into SpecIDs of entries with scores above / under FDR
	ls1 = [] # sub-cut-off score part of identification list
	ls2 = [] # high score part of identification list
	for en in ls:
		if float(en[3]) < fdrScore:
			ls1.append(en[1])
		else: ls2.append(en[1])
	n = min(len(ls1),len(ls2),maxN) # calculate the maximum list length
	rnum1 = random.sample(ls1,n) # sample the same number from lower and
	rnum2 = random.sample(ls2,n) # from upper list part
	return rnum1+rnum2, n # concatenated list of sampled SpecIDs, number of samples from each part

# auxiliary function connecting old getFilterIDs input to new getFilterIDs_val
# actually never used
def getCutScore(fdrfile, fdrcut=0.05, java=False):
	"""
	get cut-off score from java-InspectParser output extractFile or
	python-InspectParser identification list

	fdrfile:  if java, extractFilename; path to the summary file including
	          'score:'cut-off score in its second line;
			  else, identification list filename
	"""
	if verbose: print "get cut-off score from "+fdrfile
	if java:
		with open(fdrfile) as f:
		ls = f.readlines()
		fdrScore = float(ls[1][6:])
	else:
		from bootstrapping import readIdentificationFile
		ls = readIdentificationFile(infile=fdrfile, sep="\t")
		ls.sort(key = lambda x : float(x[3]), reverse = True)
		counter = 0.0
		countDecoys = 0.0
		fdr = 0.0
		for line in ls:
			counter +=1
			if line[4] == "true":
				countDecoys +=1
				fdr = countDecoys/counter
			if fdr > fdrcut: break
			fdrScore = line[3]
	return fdrScore
'''

# deprecated since strongly relying on java-InspectParser output
def getFilterIDs(fdrfile, scoreTab, maxN=1000, verbose=True):
	"""
	specialized sampling procedure for spectra from different datasets;
	auxiliary function for filterFDR and trypticPeptides.filterParsed.
	The FDR cut-off score (from fdrfile) divides the identification list into
	peptides considered reliable (higher score) and peptides with a lower score
	(not further analysed). Spectra are sampled equally from both parts.
	(return: list of sampled SpecIDs, number of samples from each list part)
	requires: (the first two) output files from java-InspectParser
	          (extractFilename and tableFilename)

	fdrfile:  extractFilename; path to the summary file including
	          'score:'cut-off score in its second line
	scoreTab: tableFilename; path to the peptide spectrum match file including
	          a table of '|Spectrum|Peptid|Score|isDecoy|FDR|'
	maxN:     desired sampling number of spectrum IDs from each list part,
	          if one part contains less spectra the maximum possible number is
			  used (default: 1000)
	"""
	# get cut-off score (from fdrfile)
	if verbose: print "get cut-off score from "+fdrfile
	with open(fdrfile) as f:
		ls = f.readlines()
		fdrScore = float(ls[1][6:])
	if verbose: print "split list of spectra by cut-off score %f" %fdrScore
	# read SpecIDs and corresponding scores from scoreTab
	with open(scoreTab) as f:
		ls = [line.rstrip().split("|") for line in f]
		del ls[0:2] # skip header (2 lines)
	# split input list into SpecIDs of entries with scores above / under FDR
	ls1 = [] # sub-cut-off score part of identification list
	ls2 = [] # high score part of identification list
	for en in ls:
		if float(en[3]) < fdrScore:
			ls1.append(en[1])
		else: ls2.append(en[1])
	n = min(len(ls1),len(ls2),maxN) # calculate the maximum list length
	rnum1 = random.sample(ls1,n) # sample the same number from lower and
	rnum2 = random.sample(ls2,n) # from upper list part
	return rnum1+rnum2, n # concatenated list of sampled SpecIDs, number of samples from each part

def filterFDR(spectra, scoreTab, fdrfile="", maxN=1000, verbose=True):
	"""
	from a given mgf-file select spectra according to corresponding Inspect
	scores and write them to a new mgf-file. For more information on the
	specialized sampling procedure see getFilterIDs.
	(return: new filename)
	requires: (the first two) output files from java-InspectParser
	          (extractFilename and tableFilename)
	using:    storeAllSpec, getFilterIDs

	spectra:  mgf-file containing exactly the spectra used for Inspect analysis
	          resulting in fdrfile and scoreTab using java-InspectParser
			  (SpecIDs must be consistent)
	scoreTab: tableFilename; path to the peptide spectrum match file including
	          a table of '|Spectrum|Peptid|Score|isDecoy|FDR|'
	fdrfile:  extractFilename; path to the summary file including
	          'score:'cut-off score in its second line
	maxN:     desired number of samples from each part of identification list,
	          maximum in case of a shorter list part (default=1000)
	"""

	# read input mgf-file and create a python list of all spectra
	allSpectra = storeAllSpec(spectra, verbose=verbose)
	# sample spectrum numbers (SpecIDs)
	if fdrfile: SpecIDs, n = getFilterIDs(fdrfile=fdrfile, scoreTab=scoreTab, maxN=maxN, verbose=verbose)
	else: SpecIDs, n = getFilterIDs_direct(scoreTab=scoreTab, maxN=maxN)
	# include number of contained spectra into new filename
	newfile = spectra[:-4] + "_filter" + str(2*n) + ".mgf" # since filterFDR processes only mgf-files
	#newfile = os.path.splitext(spectra)[0] + "_filter" + str(2*n) + os.path.splitext(spectra)[1] # obsolete
	if verbose: print 'Writing '+str(n)+"+"+str(n)+' spectra to '+newfile+" ..."
	outfile = open(newfile,"w")
	# take SpecIDs as indices to write sampled entries of allSpectra to file
	for z in SpecIDs:
		outfile.write(allSpectra[int(z)])
	outfile.close()
	if verbose: print "done"
	return newfile
