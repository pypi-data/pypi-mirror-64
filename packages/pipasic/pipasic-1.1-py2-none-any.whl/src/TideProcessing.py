# -*- coding: UTF-8 -*-
"""
Tide does not use spectrum numbers using mgf-files, therefore, files are split
into single spectrum files which are processed by all Tide steps and recombined
within output parsing into a list of peptide spectrum matches.

TideProcessing: everything to produce a list of peptide spectrum matches
with Tide (as done with Inspect before) from mgf-file + db(s);
- split mgf into single spectra,
- prepDB (tide-index) and prepSpec (msconvert -> spectrumrecords),
- runTide (tide-search) and
- combine single result files to an identification list by TideParser

@author: Anke Penzlin, April 2013
"""

import os
import sys


def splitMGF(infile, verbose=True):
	"""
Split mgf-file into files containing each a single spectrum, storing the
spectrum numbers (IDs) in corresponding filenames and return overall number of
spectra from original file (= number of new files)
"""

	from readMGF import storeAllSpec
	if verbose: print "Reading spectra from", infile, "..."
	specList = storeAllSpec(infile, verbose=verbose)
	filepath = os.path.splitext(infile)[0]+"_singleSpec/"
	if not os.path.exists(filepath): os.mkdir(filepath)
	if verbose:
		print "Writing single spectrum files to", filepath
		sys.stdout.flush()
	for num, spec in enumerate(specList):
		filename = filepath+"%0.5i.mgf" %(num)
		with open(filename,"w") as out:
			out.write(spec)

	return len(specList), filepath


def prepDB_Tide(db_fasta, params="--enzyme=trypsin --digestion=partial-digest --max_missed_cleavages=1 --monoisotopic_precursor --mods_spec=C+57.021464,1NQ+0.984016,1M+15.994915"):
	return os.system("tide-index %s --fasta=%s" %(params,db_fasta))

def prepSpec_Tide(filepath, nSpec, verbose=False):
	std_dir = os.getcwd()
	os.chdir(filepath)
	if verbose:
		for nr in range(nSpec):
			os.system("msconvert --spectrumrecords -o %s %s%0.5i.mgf" %(filepath, filepath, nr))
	else:
		import subprocess
		with open(os.devnull, "w") as fnull:
			for nr in range(nSpec):
				command = "msconvert --spectrumrecords -o %s %s%0.5i.mgf" %(filepath, filepath, nr)
				subprocess.call(command, stdout = fnull, stderr = fnull, shell = True)
	os.chdir(std_dir)

def runTide(filepath, nSpec, db_fasta, verbose=True, convComments=False):
	"""
"""
	nofile = []

	if not os.path.exists(db_fasta+".pepix"):
		if prepDB_Tide(db_fasta=db_fasta):
			return ["database "+db_fasta+" not found",nofile]

	if verbose:
		print "searching all spectra in", db_fasta
		sys.stdout.flush()
	conv_counter = 0
	std_dir = os.getcwd()
	os.chdir(filepath)
	for id in range(nSpec):
		if not os.path.isfile("%0.5i.spectrumrecords"%id):
			try:
				if convComments:
					os.system("msconvert --spectrumrecords %0.5i.mgf" %id)
				else:
					os.system("msconvert --spectrumrecords %0.5i.mgf > /dev/null" %id)
					'''with open(os.devnull, "w") as fnull:
						command = "msconvert --spectrumrecords %0.5i.mgf" %id
						subprocess.call(command, stdout = fnull, stderr = fnull, shell = True)'''
				conv_counter += 1
			except:
				nofile.append(id)
				continue
		os.system("tide-search --peptides=%s.pepix --proteins=%s.protix --spectra=%0.5i.spectrumrecords --mass_window=0.06 --results=protobuf > results" %(db_fasta,db_fasta,id))
		os.system("tide-results --results_file=results.tideres --proteins=%s.protix --spectra=%0.5i.spectrumrecords --out_format=text --out_filename=results_%0.5i" %(db_fasta,id,id))
	os.chdir(std_dir)
	if verbose and conv_counter: print conv_counter, "mgf-files converted to spectrumrecords"
	return ["", nofile]


def TideParser(filepath, nSpec, db_name="", nofile=[], out_sep="\t", fdr_listcut=1, fdr_countcut=0.05, silent=True, verbose=True):
	import re

	score = 0.0
	seq = ""
	isDecoy = "false"
	fdr = 10.0
	peptides = []
	notFound = [[],[]]

	if verbose: print "reading the input files..."
	for id in range(nSpec):
		if id in nofile: continue
		else:
			try :
				infile = open(filepath+"results_%0.5i.text"%id,"r")
				lines = infile.readlines()
				if lines > 1:
					tmp = lines[1].split('\t')
					# get score
					score = float(tmp[1])
					# get sequence
					seq = tmp[2].strip()
					# get protein name
					prot = lines[2].split('\t')[2]
					# extract decoy information
					if re.match("RRRRR",prot):
						isDecoy = "true"
					else: isDecoy = "false"
					peptides.append([id,seq,score,isDecoy,fdr,prot])
				else: notFound[0].append(id)
				infile.close()
			except:
				notFound[1].append("%.5i"%id)
				if verbose: print("File %.5i not found"%id)


	peptides = sorted(peptides, key = lambda x: x[2], reverse=True)
	#calculate FDR and write output file
	countDecoys = 0.0
	counter = 0.0
	nonDecoyCount = 0.0
	cutscore = peptides[0][2] + 0.01
	fdr = float(0.0)
	out_name =  filepath[:-1] + "_" + db_name + "_TideOut_parsed.txt"
	if verbose: print "writing the output file", out_name, "..."
	outfile = open(out_name,"w")
	# create header
	outfile.write(out_sep+out_sep.join(["Spectrum","Peptid","Score","isDecoy","FDR","matchedProtein"])+"\n")
	outfile.write(out_sep+out_sep.join(["--------","------","-----","-------","---","--------------"])+"\n")
	for pep in peptides:
		counter +=1
		if pep[3] == "true":
			countDecoys +=1
			fdr = countDecoys/counter
		if fdr > fdr_listcut: break
		if fdr < fdr_countcut:
			nonDecoyCount = counter-countDecoys
			cutscore = pep[2]
		pep[4] = fdr
		outfile.write(out_sep+out_sep.join([str(e) for e in pep])+"\n")
	outfile.close()
	if silent: return out_name
	else: return [out_name, nonDecoyCount, len(peptides), cutscore, notFound]	#[output filename, nonDecoy, total, last score, list of unmatched spectra and unknown files]


def runTide_all(spec_mgf, db_list, db_path="", verbose=True):
	"""
spec_mgf: file of spectra in mascot generic format
db_list:  only name, no extension, no path! (_decoy.fasta must be available)
db_path:  directory of all dbs (_decoy.fasta must be available for each)
verbose:  if True (default), print status messages to stdout
"""
	nSpec, filepath = splitMGF(infile=spec_mgf, verbose=verbose)
	counts = []
	testout = []
	for db in db_list:
		db_fasta = db_path+db+"_decoy.fasta"
		succ = runTide(filepath=filepath, nSpec=nSpec, db_fasta=db_fasta, verbose=verbose)
		if succ[0]: # database not found
			print succ[0]
			results = []
			counts.append(None)
		else:
			results = TideParser(filepath=filepath, nSpec=nSpec, db_name=db, nofile=succ[1], silent=False, verbose=verbose)
			counts.append(results[1])
		testout.append([results,succ[1]])
	return counts, testout


if __name__=="__main__":
	usage = """%prog SPEC_MGF DB_LIST

run Tide for each spectrum of SPEC_MGF and construct a list of peptide matches
(including FDR) for each (decoy version of) database given in DB_LIST.

SPEC_MGF  dataset-file in mgf-format (full path!)
DB_LIST   ','-separated list of filenames (as a string) of proteome databases
          in fasta-format (but without file extension!)
"""

	from optparse import OptionParser
	# configure the command line parser
	command_parser = OptionParser(usage=usage)
	#command_parser.add_option("-f","--fdr",type="float",dest="fdr",default=0.05, help="FDR cut-off for count and cut-off score calculation [default: %default]")
	#command_parser.add_option("-l","--list_fdr",type="float",dest="list_fdr",default=1, help="FDR list cut-off for restriction of output lines, overwrites fdr cut-off if smaller [default: %default (= no cut)]")
	command_parser.add_option("-d","--db_path",type="string",dest="db_path",default="",help="common directory of all databases in db_list")
	command_parser.add_option("-q","--quiet",action="store_false",dest="verbose",default=True,help="don't print status messages to stdout")
	# parse arguments
	options, args = command_parser.parse_args()
	verbose=options.verbose

	if len(args) == 2:
		counts, testout = runTide_all(spec_mgf=args[0], db_list=args[1].split(","), db_path=options.db_path, verbose=verbose)
		print "counts: ", counts
		if verbose: print "control parameters:\n", testout
	else:
		command_parser.print_help()
		sys.exit(1)
