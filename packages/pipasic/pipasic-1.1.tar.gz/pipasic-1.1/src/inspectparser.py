"""
Extract selected information from InsPecT output files and produce a specified
peptide identification (PSM) list for further analyses.

@author: Anke Penzlin, June 2013 (developed since May 2012)
"""
# get peptides (+ corresponding protein names) from Inspect output
# store specID_sequence_score_isDecoy_fdr_proteinName in a tabular txt-file

import re
import optparse
import sys
import os


def parseInspect(inpath, fdr_listcut=1, fdr_countcut=0.05, multipleFiles=True, silent=True):

	out_name = inpath[:-4]+"_parsed.txt"

	score = 0.0
	sequence = ""
	specID = ""
	isDecoy= ""
	peps = []
	nonDecoyCount = 0
	reliable = True

	#print "Reading the input ..."
	# get [specID ,sequence ,score,isDecoy]
	infile = open(inpath,"r")
	for line in infile:
		if not line.startswith('#'):
			if multipleFiles:
				f_name = os.path.splitext(os.path.basename(line.split("\t")[0]))[0]
				specID = f_name + ".." + line.split("\t")[1]
			else: specID = int(line.split("\t")[1])
			score = float(line.split("\t")[5]) 			# MQScore (choose best one)
			sequence = line.split("\t")[2].split(".")[1]
			sequence = sequence.replace("+","")
			sequence = re.sub('[0-9]', '', sequence)#sequence.replace('[0-9]',"")
			protein = line.split("\t")[3]

			if "REVERSED" in protein: isDecoy = "true"
			else: isDecoy = "false"

			peps.append([specID, sequence, score, isDecoy, protein])

	peps = sorted(peps, key = lambda x : (x[0], x[2]), reverse = True)

	lastspec = -1
	newpeps = []

	# store important peptides in list new_peps
	for elem in peps:
		if elem[0] != lastspec:
			newpeps.append(elem)
			lastspec = elem[0]

	peps = []
	newpeps = sorted(newpeps, key = lambda x : (x[2],x[3]=="false"), reverse = True)

	cutscore = newpeps[0][2] + 0.01

	#calculate FDR
	#print "Calculating FDR and writing the output in : "+ out_name
	countDecoys = 0.0
	counter = 0.0
	#fdr = float(0.0)
	outfile = open(out_name,"w")
	outfile.write("\t Spectrum\t Peptid\t Score\t isDecoy\t FDR\t matchedProtein \n")
	outfile.write("\t --------\t ------\t -----\t -------\t ---\t -------------- \n")
	for elm in newpeps:
		counter +=1
		if elm[3] == "true":
			countDecoys +=1
		fdr = countDecoys/counter
		if fdr > fdr_listcut: break
		if fdr > fdr_countcut: reliable = False
		if reliable:
			nonDecoyCount = counter-countDecoys
			cutscore = elm[2]
		outfile.write("\t"+str(elm[0])+"\t"+elm[1]+"\t")#
		outfile.write(str(elm[2])+"\t"+elm[3]+"\t"+str(fdr)+"\t"+elm[4])
		outfile.write("\n")

	outfile.close()
	if silent: return out_name
	else: return [out_name, nonDecoyCount, len(newpeps), cutscore]	#[total, nonDecoy, output filename]

if __name__=="__main__":
	usage = """%prog INSPECT_OUT

				compute FDR from InsPecT output (txt-file).

				"""

	# configure the command line parser
	command_parser = optparse.OptionParser(usage=usage)
	command_parser.add_option("-f","--fdr",type="float",dest="fdr",default=0.05, help="FDR cut-off for count and cut-off score calculation [default: %default]")
	command_parser.add_option("-l","--list_fdr",type="float",dest="list_fdr",default=1, help="FDR list cut-off for restriction of output lines, overwrites fdr cut-off if smaller [default: %default (= no cut)]")
	command_parser.add_option("-m","--multifile",action="store_true",dest="multifile",default=False,help="use filename to tag spectrum numbers for subsequent mixture of multiple different files")
	command_parser.add_option("-s","--silent",action="store_true",dest="short_out",default=False,help="only print output filename instead of all calculated values")#"don't print status messages to stdout")
	command_parser.add_option('-e', '--easy', type='string', dest='easy', default=None, help='For the beginner, setting the value to True to run this script. Use true or True to activate.')

	# parse arguments
	options, args = command_parser.parse_args()
	silent = options.short_out

	if not options.easy:
		if len(args) == 1:
			inspect_out = args[0]
			if silent: print parseInspect(inpath=inspect_out, fdr_listcut=options.list_fdr, fdr_countcut=options.fdr, multipleFiles=True, silent=silent)
			else:
				outname, count, total, score = parseInspect(inpath=inspect_out, fdr_listcut=options.list_fdr, fdr_countcut=options.fdr, multipleFiles=True, silent=silent)
				print "%i of %i spectra within %.2f FDR, last score: %.3f" %(count, total, options.fdr, score)
				print "selected identification lines written to:", outname

		else:
			command_parser.print_help()
			sys.exit(1)

	# easy mode
	if (options.easy).lower() == 'true':
			spectra = ['example']
			db_list = ['species1', 'species2']
			fdr=0.05
			countList = []

			for spec in spectra:
				sample_counts = []
				for DB in db_list:
					# compose filename of spectra and database (InSpecT results mentioned above)
					inspectOut = '../data/spectra/'+spec + "_" + DB + "_InspectOut.txt"
					try:
						# Extract selected information from InsPecT output files and produce a specified
						# peptide identification (PSM) list for further analyses.
						count = parseInspect(inpath=inspectOut, fdr_countcut=fdr, silent=False)[1]
						sample_counts.append(count)
					except:
						print "Could not find PSM-file for %s and %s" % (spec, DB)
						sample_counts.append(0)
				countList.append(sample_counts)
			np.array(countList).dump(os.path.splitext('DEMO_' + outputFile)[0]+"_counts.dat")
