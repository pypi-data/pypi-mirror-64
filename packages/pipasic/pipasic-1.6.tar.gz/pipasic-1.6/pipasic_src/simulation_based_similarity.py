# -*- coding: UTF-8 -*-
# in: ProteinDBs with and without decoys, number of samples for simulation and Inspect
# out: FDR-matrix (and several result files)

# Attention: For using Inspect, this script must be called out of the Inspect-directory! The
# "cd /home/franziska/bin/Inspect" command is called be the main routine of the script

# procedure:
# 1. sample sequences from Protein-DB (for faster simulation)
# 2. call the simulator with these sequences
# 3. convert spectra to mgf-format (input format Inspect and Biceps)
# 4. sample spectra from simulated ones
# 5. run Inspect
# 6. evaluate results from Inspect to calculate an FDR-matrix

import re
import random
from Bio import SeqIO
import os
import sys
import optparse
import time
import platform

from inspectparser import parseInspect


# 1. sampling from DB (def)
def samplProt(inpath, n):
	"""
	Sampling a given number of protein sequences from a given fasta-file

	inpath: fasta-file, protein DB which will be sampled from
	n: 		number of samples
	"""

	protIDs = [] # IDs of all proteins from db
	print 'Reading protein IDs from '+inpath+' ...'
	for record in SeqIO.parse(open(inpath, "rU"), "fasta") :
		# Add ID of this record to protIDs list
		protIDs.append(record.id)
	nprot = len(protIDs)
	print "Found %i proteins" % nprot

	if n == 0 or n > nprot:
		print "Take the complete list of %i proteins" %nprot
		return inpath
	else:
		print 'Choosing %i proteins ...' %n
		rprot = random.sample(protIDs,n)

		if inpath[-3] == '.': outpath = inpath[:-3] + "_sample" + str(n) +".fasta"
		else: outpath = inpath[:-6] + "_sample" + str(n) +".fasta"
		print 'Writing selected proteins to '+outpath+" ..."
		output_handle = open(outpath, "w")
		for record in SeqIO.parse(open(inpath, "rU"), "fasta") :
			if record.id in rprot: # for every selected protein
				SeqIO.write(record, output_handle, "fasta")
		output_handle.close()
		print "done"
		return outpath

# 2. use OpenMS simulator (def)
def run_MSSim(DBfasta, outmzML, ini="/data/NG4/anke/MSSim/mscconf_sebio02.ini", param=""):
	command = "MSSimulator -in {inp} -out {out} -ini {ini} {param}".format(inp=DBfasta, out=outmzML, ini=ini, param=param)
	print "Executing:",command
	sys.stdout.flush()
	os.system(command)
	return 1

# 3. convert mzML to mgf format (def)
def convertSpectra(mzMLfile, param=""):
	mgf = mzMLfile[:-5]+".mgf"
	command = "FileConverter -in {infile} -in_type mzML -out {outfile} -out_type mgf {param}".format(infile=mzMLfile, outfile=mgf, param=param)
	print "Executing: ",command
	sys.stdout.flush()
	os.system(command)
	return mgf

# 4. sampling from simulated spectra (def)
from readMGF import sampleMGF as samplSpecs
'''def samplSpecs(inpath, n):
	"""
	Sampling a given number of spectra from a given mgf-file

	inpath: mgf-file which will be sampled from
	n: 		number of samples
	"""

	infile = open(inpath,"r")
	specs = [] # names of all spectra

	print 'Reading specTitles ...'
	for line in infile:
		if re.search("TITLE",line):
			specs.append(line.rstrip())
	if n == 0 or n > len(specs):
		print "Take the complete list of %i spectra" %len(specs)
		return inpath
	else:
		print 'Choosing %i spectra ...' %n
		rspecs = random.sample(specs,n)
		infile.seek(0)
		outpath = inpath[:-4] + "_sample" + str(n) +".mgf"
		print 'Writing selected specs to '+outpath+" ..."
		outfile = open(outpath,"w")
		for line in infile:
			if line.rstrip() in rspecs: # for ervery selected title write spectrum to new file
				outfile.write("BEGIN IONS\n")
				outfile.write(line)
				for line2 in infile:
					if re.search("BEGIN IONS",line2): break
					outfile.write(line2)
		outfile.close()
		print "done"
		return outpath
'''

def prepDB(fastaDB, path="/home/franziska/bin/Inspect/"):
	""" 5.a prepare decoyDB input for Inspect (def)

			The function will use the decoyDB to create

			Args:
					fastaDB: decoy fasta file
					path: where inspect is put
			Returns:
					This creates two files which will be used by
					InsPecT: myDB.trie and myDB.index. Once these files are created,
					they can be reused for later InsPecT runs.
	"""
	if not os.path.exists(os.path.join(path,"PrepDB.py")):
		print "InsPecT files not found, please correct path!"
		return 0
	# PrepDB.py from inSpecT source code:
	# Convert a protein database into concatenated format.
	# Processes FASTA format.
	command = "python {path} FASTA {db}".format(path=os.path.join(path, 'PrepDB.py'), db=fastaDB)
	print "Executing: ",command
	sys.stdout.flush()
	os.system(command)
	return 1

# 5. match spectra against database with Inspect (def)
def run_inspect(configfile, outputfile, path="", param=""):
	if platform.system() == 'Windows':
			inspect_path = os.path.join(path, 'inspect.exe')
	else:
			inspect_path = os.path.join(path, 'inspect')
	if len(path) > 0:
		command = inspect_path + " -i {input} -o {output} -r {path} {param}".format(input=configfile, output=outputfile, path=path, param=param)
	else:
		command = inspect_path + " -i {input} -o {output} {param}".format(input=configfile, output=outputfile, param=param)
	print "Executing: ",command , "\n"

	sys.stdout.flush()
	os.system(command)
	return 1

# 1.-6. go all steps
def calculateSimilarityMatrix(DBs, db_path="/data/NG4/anke/proteome/", nProt=100, nSpec=1000,
	sim_out_path="/data/NG4/anke/MSSim/sampled_data/", MSSim_ini="/data/NG4/anke/MSSim/mscconf_sebio02.ini",
	inspect_config="/data/NG4/anke/Inspect/config_Inspect_MSSim.txt", inspect_dir="/home/franziska/bin/Inspect/"):
	"""
	"""
	rng = range(len(DBs))
	simMat = [ [0 for i in rng] for j in rng ] # initializing output

	configfile = inspect_config[:-4]+"_py.txt" # Inspect configuration file (final version)

	for i in rng:
		# 1. sampling from DB (run)
		prot_path = samplProt(db_path+DBs[i]+".fasta",nProt)
		# 2. use OpenMS simulator with sampled proteins (run)
		out_path = sim_out_path+DBs[i]+"_sampl"+str(nProt)+"MSSim.mzML"
		run_MSSim(prot_path, out_path, ini=MSSim_ini, param="-threads 4")
		# 3. convert mzML to mgf format
		sampl_path = convertSpectra(out_path)
		# 4. sampling from simulated spectra
		spec_path = samplSpecs(sampl_path,nSpec)
		# (*) with runInspect_user_config.runInspect_config for all DBs
		# runInspect_config(spectra=spec_path, DBs=DBs, spec_path="", db_path=db_path, inspect_dir=inspect_dir, conf=configfile, user_mods="")
		for j in rng:
			# 5. calling InSpecT (*)
			db_j = db_path+DBs[j]+"_decoy.trie"
			# 5.a create trie if necessary
			if not os.path.exists(db_j):
				prepDB(db_path+DBs[j]+"_decoy.fasta",path=inspect_dir)
			inspect_out = spec_path[:-4] +"_"+DBs[j]+"_InspectOut.txt" # (!!)
			# prepare configfile # <-- call runInspect_user_config.runInspect_config instead!! (bei 5. ansetzen, j-Schleife nur mit inspect_out behalten)
			conf_in = open(inspect_config,'r')
			conf_out = open(configfile,'w')
			for line in conf_in:
				if re.match("spectra,",line):
					conf_out.write("spectra,"+spec_path+"\n")
				elif re.match("DB,",line):
					conf_out.write("DB,"+db_j+"\n")
				else:
					conf_out.write(line)

			conf_in.close()
			conf_out.close()

			run_inspect(configfile, inspect_out, path=inspect_dir)# from 5. remove all but (!!) up to here
			# 6. evaluate results from Inspect to calculate an FDR-matrix
			simMat[i][j] = parseInspect(inspect_out, silent=False)[1]
	normSimMat = [ [0 for i in rng] for j in rng ]
	for k in rng:
		for l in rng:
			normSimMat[k][l] = simMat[k][l] / simMat[k][k]
	return simMat, normSimMat


if __name__=="__main__":
	usage = """%prog DB_LIST -d DB_DIR -p NPROT -n NSPEC -i INIFILE

Sample a given number of proteins from DB for simulation of spectra,
sample a given number of spectra from simulation for running inspect
and calculate FDR from Inspect output.

"""

	t0 = time.time()
	print time.strftime("%Y/%m/%d, %H:%M:%S: Starting whole procedure and overall time measurement", time.localtime(t0))
	sys.stdout.flush()
	# configure the parser
	optparser = optparse.OptionParser(usage=usage)
	optparser.add_option('-d', '--dbdir', type='string', dest='db_dir', default="/data/NG4/anke/proteome/", help='directory of proteinDBs. [default: %default]')
	optparser.add_option('-p', '--proteinnumber', type='int', dest='nprot', default=100, help='number of samples from proteinDB. [default: %default]')
	optparser.add_option('-n', '--numberspectra', type='int', dest='nspec', default=1000, help='number of samples from spectra. [default: %default]')
	optparser.add_option('-c', '--configfile', type='string', dest='MSSim_ini', default="/data/NG4/anke/MSSim/mscconf_sebio02.ini", help='configuration file for MSSImulator. [default: %default]')
	optparser.add_option('-i', '--inspectdir', type='string', dest='insp_dir', default="/home/franziska/bin/Inspect/", help="path to 'inspect.exe'. [default: %default]")
	optparser.add_option('-o', '--outfile', type='string', dest='out', default="/data/NG4/anke/Inspect/collectOutput.txt", help='name of file resulting matrix is written to. [default: %default]')
	# parse options and arguments
	options, args = optparser.parse_args()

	if len(args) == 1:
		db_list = args[0].split(',')
		sim_out_path = "/data/NG4/anke/MSSim/sampled_data/"
		nProt = options.nprot # nr. of sampled proteins (from DB)
		nSpec = options.nspec # nr. of sampled spectra (from simulation)
		config_path = "/data/NG4/anke/Inspect/config_Inspect_MSSim.txt" # Inspect configuration file (initial version)

		M, M_n = calculateSimilarityMatrix(DBs = db_list, db_path = options.db_dir, nProt=nProt, nSpec=nSpec, sim_out_path=sim_out_path, MSSim_ini=options.MSSim_ini, inspect_config=config_path, inspect_dir=options.insp_dir)#print db_list
	else:
		optparser.print_help()
		sys.exit(1)

	outfile = open(options.out,"a")
	outfile.write("normalized similarity matrix derived from InSpect with %i sampled spectra "%nSpec)
	outfile.write("(from simulation with %i sampled proteins): \n"%nProt)
	print "normalized: \n"
	for line in M_n:
		print line
		outfile.write(str(line)+"\n")
	outfile.write("\n\n\n")
	outfile.close()
	print time.strftime("%Y/%m/%d, %H:%M:%S: all done\n", time.localtime(time.time()))
	print "took %.3f seconds overall (that's %.3f minutes)"%(time.time() - t0, (time.time() - t0)/60)
	print "----------------------------------------------------------------------------------------------------\n\n\n"
