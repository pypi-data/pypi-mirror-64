"""
Barplot for given observed counts and correction results (optional plus weighted
correction) for a number of proteomes.

@author: Anke Penzlin, June 2013
"""

import numpy as np

def barplotPASiC(names, obs, corr, weighted=[], filename='results_correction.pdf',
	leg_tags=['Observed fraction','Estimated fraction','Fraction estimated by weighting']):
	"""
	names:    organism names for labeling (x-axis) and legend; must have same
	          length as the data lists (number of organisms)
	obs:      observed counts, normalized to sum=1 for all organisms
	corr:     results of (unweighted) correction, normalized sum=1 for all orgs
	weighted:      results of weighted correction, normalized to sum=1 for all orgs;
	          if [] (default), only obs and corr will be plotted
	filename: outputfile (image format like .png or .pdf), 'results_correction.pdf'
	          is created in working directory by default
	leg_tags: description of data given in obs, corr and weighted for legend
	"""
	import matplotlib.pyplot as plt
	rng = np.arange(len(names))
	cl1 = np.array([215, 25, 28])/255.
	cl2 = np.array([253, 174, 97])/255.
	cl3 = np.array([171, 221, 164])/255.
	cl4 = np.array([63, 151, 206])/255.

	plt.figure()
	plt.bar(3*rng, obs, 1, color=cl1, label=leg_tags[0])
	plt.bar(3*rng+1, corr, 1, color=cl4, label=leg_tags[1])
	if weighted != []: plt.bar(3*rng+2, weighted,1, color=cl2, label=leg_tags[2])
	#plt.text(0.5, unique[0]+ 0.1*unique[0], "Unique / all mapped reads", color='k', rotation=90, horizontalalignment='center', verticalalignment='bottom')
	#plt.text(1.5, corr[0]*total+ 0.1*unique[0], "GASiC estimate", rotation=90, horizontalalignment='center', verticalalignment='bottom')
	plt.xticks(3*rng+1, names)#, rotation=90)
	plt.ylabel('Fraction of PSMs')
	plt.xlim(xmin=0, xmax=3*len(names))
	plt.ylim(ymax=1.5)#ymin=-0.05*total)
	plt.legend(loc='upper left')
	plt.savefig(filename,  bbox_inches='tight')


if __name__ == "__main__":
	usage = """%prog OBSERVED CORRECTED [WEIGHTED]

plot PASiC results.
"""

	from optparse import OptionParser
	command_parser = OptionParser(usage=usage)
	command_parser.add_option("-d","--dir",type="string",dest="f_dir",default="",help="common directory of all input files. [default: No common path]")
	command_parser.add_option("-o","--out_file",type="string",dest="outfile",default="results_correction.pdf",help="specify an output filename for the produced graphic. [default: %default]")
	command_parser.add_option("-t","--tags",type="string",dest="tags",default="Observed fraction,Estimated fraction,Fraction estimated by weighting",help="string of ','-separated legend line names. [default: %default]")
	command_parser.add_option("-n","--names",type="string",dest="names",default="",help="string of ','-separated proteome names. [default: org_1,..,org_n]")
	options, args = command_parser.parse_args()

	if len(args) < 2:
		command_parser.print_help()
		sys.exit(1)
	obs  = np.load(options.f_dir+args[0])
	corr = np.load(options.f_dir+args[1])
	if len(args) > 2: weighted = np.load(options.f_dir+args[2])
	else: weighted = []
	input_tags = options.tags.split(",")
	if options.names: names = options.names.split(",")
	else: names = ["org%i" for i in range(len(obs))]
	barplotPASiC(names=names, obs=obs, corr=corr, weighted=weighted, filename=options.outfile, leg_tags=input_tags)
