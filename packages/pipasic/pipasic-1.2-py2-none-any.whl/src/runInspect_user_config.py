# -*- coding: UTF-8 -*-
"""
Automatized configuration and execution of Inspect peptide identification for
a list of spectrum files and a list of reference proteomes. Specifications of
posttranslational modifications can either be directly passed by the user or
assigned to the dataset by its filename (if dataset group is already known).

@author: Anke Penzlin, June 2013
"""

import re
import os
import sys
import optparse

#from InspectParser_FDRcut import parseInspect
from simulation_based_similarity import prepDB, run_inspect

def runInspect_config(spectra,
					DBs,
					spec_path,
					db_path="/data/NG4/anke/proteome/",
					inspect_dir = "/home/franziska/bin/Inspect/",
					conf = "/data/NG4/anke/Inspect/config_Inspect_py.txt",
					user_mods=""):
	"""
	run Inspect for each pair of spectrum dataset and proteome database using
	modifications according to the dataset in the configuration file.
	"""

	rngDB = range(len(DBs)) # 3 for example
	rngSpc = range(len(spectra)) # 2 for example
	simMat = [ [0 for i in rngDB] for j in rngSpc ] # initializing output: [[0, 0, 0], [0, 0, 0]]

	for i in rngSpc:
		specs = spec_path+spectra[i]+".mgf"
		for j in rngDB:
			db_j = db_path+DBs[j]+"_decoy.trie"

			# create trie if necessary (.trie and .index created simultaneously)
			if not os.path.exists(db_j):
				# a prepare decoyDB input for Inspect (def)
				go_on = prepDB(db_path+DBs[j]+"_decoy.fasta", path=inspect_dir) # Convert a protein database into concatenated format.
				if not go_on: return
			inspect_out = specs[:-4] +"_"+DBs[j]+"_InspectOut.txt" # -4 to remove file extension: .mgf


			# prepare configfile for InspecT
			conf_out = open(conf,'w')
			conf_out.write("spectra,"+specs+"\n")
			conf_out.write("instrument,FT-Hybrid\n")
			conf_out.write("protease,Trypsin\n")
			conf_out.write("DB,"+db_j+"\n")
			if not user_mods == "":
				conf_out.write(user_mods)
			elif re.search("Lacto_131",spectra[i]):
				conf_out.write("mod,46.0916,C,fix\n")
				conf_out.write("mod,15.994915,M\n")
				conf_out.write("# iTraq\n")
				conf_out.write("mod,144.1544,K,fix\n")
				conf_out.write("mod,144.1544,*,nterminal\n")
				print "modifications according to acc. nr. 13105-13162"
				sys.stdout.flush()
			elif re.search("Shigelladys",spectra[i]):
				conf_out.write("mod,46.0916,C,fix\n")
				conf_out.write("mod,15.994915,M\n")
				print "modifications according to http://www.biomedcentral.com/1471-2180/11/147#sec2"
				sys.stdout.flush()
			else:
				conf_out.write("# Protecting group on cysteine\n")
				conf_out.write("mod,57.021464,C,fix\n")
				if re.search("Bacicer_113",spectra[i]):
					conf_out.write("mod,15.994915,M\n")
					print "modifications according to acc. nr. 11339-11362"
					sys.stdout.flush()
				elif re.search("Bacisub_175",spectra[i]):
					conf_out.write("mod,15.994915,M\n")
					conf_out.write("mod,119.1423,C\n")
					conf_out.write("mod,396.37,C\n")
					print "modifications according to acc. nr. 17516-17659"
					sys.stdout.flush()
				elif re.search("Ecoli_12",spectra[i]):
					conf_out.write("mod,32,M,opt\n")
					print "modifications according to acc. nr. 12189-12199"
					sys.stdout.flush()
				elif re.search("Strepyo_1923",spectra[i]):
					conf_out.write("mod,15.994915,M\n")
					conf_out.write("mod,79.9799,STY\n")
					print "modifications according to acc. nr. 19230/19231"
					sys.stdout.flush()
				elif re.search("CPXV_",spectra[i]):
					conf_out.write("mod,15.994915,M\n")#oxidation
					conf_out.write("mod,42.010565,*,nterminal\n")#acetylation
					print "modifications according to standard configuration (for pox)"
				elif re.search("MSSim",spectra[i]):
					conf_out.write("mod,0.984016,NQ\n")
					conf_out.write("mod,15.994915,M\n")
					print "modifications according to (simulation) standard configuration"
					sys.stdout.flush()
				else:
					# conf_out.write("mod,15.994915,M\n")#oxidation
					# conf_out.write("mod,42.010565,*,nterminal\n")#acetylation
					#conf_out.write("mod,0.984016,NQ\n")
					print "modifications according to (unspecified) standard configuration"
					sys.stdout.flush()
			conf_out.write("mods,2\n")
			if re.search("Shigelladys",spectra[i]):
				conf_out.write("PMTolerance,1.4\n")
				conf_out.write("IonTolerance,0.5\n")
				conf_out.write("MultiCharge,3\n")
			else:
				conf_out.write("ParentPPM,10\n")
				conf_out.write("IonTolerance,0.8\n")
			conf_out.close()

			# run Inspect: match spectra against database
			if re.search( "Ecoli_12", spectra[i] ):
				AA_file = inspect_dir + "AminoAcidMasses_15N.txt"
				if os.path.exists(AA_file):
					run_inspect(conf, inspect_out, inspect_dir, "-a "+AA_file)
					print "amino acid masses according to 15N (because of special e.coli data set)."
					sys.stdout.flush()
				else:
					run_inspect(conf, inspect_out, inspect_dir)
					print "WARNING: file containing amino acid masses according to 15N not found!\nDatabase search using usual file disregarding special e.coli data set)."
					sys.stdout.flush()
			else:
				run_inspect(conf, inspect_out, inspect_dir)
	# 		# evaluate results from Inspect to calculate an FDR-matrix
	# 		simMat[i][j] = parseInspect(inspect_out)[2]

	# for line in simMat:
	# 	print line


if __name__=="__main__":
	usage = """%prog SPECTRA DB_LIST -s SPEC_DIR -d DB_DIR

					run InsPecT (for multiple spectrum datasets and references),
					using known modification options (assigned by filename),
					and calculate FDR-corrected identification counts from InsPecT output.

					SPECTRA: ','-separated spectrum-filenames (mgf-format) without file extension
					DB_LIST: ','-separated proteome-filenames (fasta-format) without file extension

					Using the easy mode (--easy) to have a quick understand of this function.
					"""

	# configure the parser
	optparser = optparse.OptionParser(usage=usage)
	optparser.add_option('-s', '--specdir', type='string', dest='spec_dir', default="/data/NG4/anke/spectra/", help='directory of specFiles (absolute path!). [default: %default]')
	optparser.add_option('-d', '--dbdir', type='string', dest='db_dir', default="/data/NG4/anke/proteome/", help='directory of proteinDBs (absolute path!). [default: %default]')
	optparser.add_option('-c', '--configfile', type='string', dest='config', default="/data/NG4/anke/Inspect/config_Inspect_py.txt", help='a txt-file for Inspect configuration, will be written. [default: %default]')
	optparser.add_option('-m', '--mods', type='string', dest='mods', default="", help='a string containing all modifications in question, modification choice by filename if "". [default: %default]')
	optparser.add_option('-i', '--inspect_dir', type='string', dest='ins_dir', default="/home/franziska/bin/Inspect", help='directory of Inspect.exe. [default: %default]')
	optparser.add_option('-e', '--easy', type='string', dest='easy', default=None, help='For the beginner, setting the value to True to run this script. Use true or True to activate.')

	# parse options and arguments
	options, args = optparser.parse_args()

	if not options.easy:
		if len(args) == 2:
			spectra = args[0].split(',')
			db_list = args[1].split(',')
		else:
			optparser.print_help()
			sys.exit(1)

		'''db_path = options.db_dir
		spec_path = options.spec_dir
		configfile = options.config # Inspect configuration file
		mods = options.mods
		inspect_dir = options.ins_dir'''
		runInspect_config(spectra=spectra, DBs=db_list, spec_path=options.spec_dir, db_path=options.db_dir, inspect_dir=options.ins_dir, conf=options.config, user_mods=options.mods)
	# Easy mode
	if (options.easy).lower() == 'true':
		runInspect_config(
			spectra=['example'],
			DBs=['species1', 'species2'],
			spec_path='../data/spectra/',
			db_path='../data/reference/',
			inspect_dir='./inspect/',
			conf='./config_files/config_Inspect_py.txt',
			user_mods='')
