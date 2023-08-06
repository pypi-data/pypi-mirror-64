# -*- coding: UTF-8 -*-

# -*- coding: UTF-8 -*-
"""
Aggregation of pipasic functionalities (by import) to a single command line tool.

@author: Anke Penzlin, June 2013
@lastChange: January 2014
"""

#import re
#import random
#from Bio import SeqIO
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pkg_resources


def main():
    print "打印"
    inspect = pkg_resources.resource_filename(__name__ , 'inspect/inspect')
    config = pkg_resources.resource_filename(__name__ , 'inspect/config_files')
    print config
    print inspect
    os.system(inspect)

def pipasic():
    usage = """%prog SPECTRA DB [module options] [input and configuration options]

            Overall pipasic calling tool, including:
            - weighted (always) and unweighted (optional) similarity estimation
              (both sequence based)
            - correction, using matrix from similarity estimation
            - peptide Identification by InsPecT or Tide

            SPECTRA: Comma-separated string of spectrum files (mgf) - without file-extension!
            DB:      Comma-separated string of reference proteomes (fasta-files) - without file-extension!
                     if -S or -I: decoy database must exist as db_name+"_decoy.fasta"

            Note: Pipasic requires two .fasta for each reference proteome <ref>:
            - "<ref>.fasta" containing the protein sequences only.
            - "<ref>_decoy.fasta" containing BOTH the protein AND decoy sequences. Decoy
              sequences must be tagged in their name with "REVERSED" or "DECOY" or any
              other tag specified by "-t".
            """
    # enable command line parsing
    from optparse import OptionParser
    optparser = OptionParser(usage=usage)

    # modules:
    optparser.add_option("-U", "--Unweighted", action="store_true", dest="unweighted",
                         default=False, help="calculate unweighted similarities for all given proteomes")
    optparser.add_option("-I", "--Identify", action="store_true", dest="id",
                         default=False, help="identify given spectra with all given proteomes")
    optparser.add_option("-T", "--Tide", action="store_true",
                         dest="Tide", default=False, help="use Tide instead of InsPecT")
    optparser.add_option("-V", action="store_true", dest="viz",
                         default=False, help="Visualize results using matplotlib")
    #optparser.add_option("-S","--Simulation",action="store_true",dest="simul",default=False,help="use simulation to calculate unweighted similarities, sequence based otherwise")
    #optparser.add_option("-W","--Weighted",action="store_true",dest="weighted",default=True,help="calculate weighted similarities for a dataset and all given proteomes")

    # input parameters:
    optparser.add_option('-o', '--outputFile', type='string', dest='outputFile', default="results.txt",
                         help='Output filename for results. Also serves as trunk for other result files (graphics, data).  [default: %default]')
    optparser.add_option('-s', '--spec_dir', type='string', dest='spec_dir', default=None,
                         help='Directory of SPECTRA (mgf) files. Search in current directory, if not given. [default: %default]')
    optparser.add_option('-d', '--db_dir', type='string', dest='db_dir', default=None,
                         help='Directory of proteinDBs. Search for DB files current directory, if not given. [default: %default]')
    optparser.add_option('-m', '--mods', type='string', dest='mods', default=None,
                         help='A string containing all modifications in question, modification choice by filename if not given. [default: %default]')
    optparser.add_option('-i', '--inspect_dir', type='string', dest='insp_dir',
                         default=None, help='Inspect directory. [default: %default]')
    optparser.add_option('-f', '--fdr_cutoff', type='float', dest='fdr', default=0.05,
                         help='False discovery rate cut-off for identification lists. [default: %default]')  # -l : list_fdr_cutoff ??
    optparser.add_option('-t', '--decoy_tag', type='str', dest='decoy_tag', default="REVERSED|DECOY",
                         help='Tag to identify decoy sequences in the database. Regular expressions may be used. This tag must be used in the name of all decoy sequences in the file "<DB>_decoy.fasta". [default: %default]')
    #optparser.add_option('-n', '--numberspectra', type='int', dest='nspec', default=1000, help='number of samples from simulated spectra. [default: %default]')
    optparser.add_option('-l', '--labels', type='string', dest='labels', default=None,
                         help='Comma-separated string of short names for organisms in the reference proteomes. If not given, the file name is used. [default: %default]')
    optparser.add_option('-N', '--N_spectra', type='string', dest='num_spectra_orginal', default=None,
                         help='Number of spectra in original dataset, comma-separated list if multiple datasets. [default: %default]')
    optparser.add_option('-c', '--C_spectra', type='string', dest='counts', default=None,
                         help='File containing numbers of spectra found by identification (Numpy Array dump). [default: %default]')

    # flags:
    optparser.add_option("-q", "--quiet", action="store_false", dest="verbose",
                         default=True, help="don't print status messages to stdout")

    # parse options and arguments
    options, args = optparser.parse_args()
    # if not any([options.id, options.unweighted, options.simul , options.weighted]):
    #	optparser.print_help()
    #	sys.exit(1)

    # process documentation
    '''if options.time_mes:
        import time
        t0 = time.time()
        print time.strftime("%Y/%m/%d, %H:%M:%S: Starting whole procedure and overall time measurement", time.localtime(t0))
		sys.stdout.flush()'''
    import time
    t0 = time.time()
    print time.strftime("\n\n%Y/%m/%d, %H:%M:%S: Starting whole procedure and overall time measurement\n\n", time.localtime(t0))
    sys.stdout.flush()

    # scanning some options
    verbose = options.verbose
    unweighted = options.unweighted
    weighted = True
    correction = True
    fdr = options.fdr
    decoy_tag = options.decoy_tag
    outputFile = options.outputFile
    if not outputFile:
        print "No output filename given. Writing all output to working directory, 'output'-files\n"
        outputFile = "output.txt"
    labels = options.labels
    if labels:
        labels = labels.split(",")
    Counts = options.counts
    # config_path = os.path.dirname(os.path.realpath(__file__))+"/config_files/"
    config_path = pkg_resources.resource_filename(__name__ , 'config_files')

    if not options.spec_dir:
        options.spec_dir = ""
    if not options.db_dir:
        options.db_dir = ""
    if not options.mods:
        options.mods = ""
    if not options.insp_dir: # no InSpecT is given, default InSpecT in the package is used
        options.insp_dir = pkg_resources.resource_filename(__name__ , 'inspect')

    # #####################################
    # Identify spectra [-I]
    # #####################################
    if options.id:
        if len(args) == 2:
            spectra = args[0].split(',')
            db_list = args[1].split(',')
            countList = []
            if options.Tide:  # use Tide
                from TideProcessing import runTide_all
                for spec in spectra:
                    print "Started Tide for "+spec
                    sample_counts = runTide_all(
                        spec_mgf=options.spec_dir+spec+".mgf", db_list=db_list, db_path=options.db_dir, verbose=verbose)[0]
                    countList.append([count for count in sample_counts])
            else:  # use InSpect
                from runInspect_user_config import runInspect_config
                insp_config = os.path.join(config_path, "config_Inspect_py.txt")  # configuration file for InSpect
                # Automatized configuration and execution of Inspect peptide identification for
                # a list of spectrum files and a list of reference proteomes.
                runInspect_config(spectra=spectra,
                                  DBs=db_list,
                                  spec_path=options.spec_dir,
                                  db_path=options.db_dir,
                                  inspect_dir=options.insp_dir,
                                  conf=insp_config,
                                  user_mods=options.mods)  # output and/or variable? <- may not be necessary (since spectra enough)
                from inspectparser import parseInspect
                correction = False
                for spec in spectra:
                    sample_counts = []
                    for DB in db_list:
                        # compose filename of spectra and database (InSpecT results mentioned above)
                        inspectOut = options.spec_dir+spec + "_" + DB + "_InspectOut.txt"
                        try:
                            # Extract selected information from InsPecT output files and produce a specified
                            # peptide identification (PSM) list for further analyses.
                            count = parseInspect(
                                inpath=inspectOut, fdr_countcut=fdr, silent=False)[1]
                            sample_counts.append(count)
                            correction = True
                        except:
                            print "Could not find PSM-file for %s and %s" % (spec, DB)
                            sample_counts.append(0)
                    countList.append(sample_counts)
            # number of peptides not in decoy
            np.array(countList).dump(
               os.path.splitext(outputFile)[0]+"_counts.dat")
        else:
            print "Aborting. - Spectra and reference proteomes needed as the arguments!"
            optparser.print_help()
            sys.exit(1)

    # unweighted similarity (sequence based) [-U]
    if unweighted: # default is false
        if len(args) > 1:
            spectra = args[0].split(',')
            db_list = args[1].split(',')
        elif len(args) > 0:
            db_list = args[0].split(',')
        else:
            print "Aborting. - Reference proteomes needed as (only or 2nd) argument!"
            optparser.print_help()
            sys.exit(1)
        dbList = ",".join([options.db_dir+db+".fasta" for db in db_list])
        from trypticpeptides import unweightedMatrix
        simiMat_unw = unweightedMatrix(dbList=dbList, verbose=verbose)
        np.array(simiMat_unw).dump(
            os.path.splitext(outputFile)[0]+"_M_unw.dat")

    # weighted similarity (sequence based)
    if weighted:  # this is the default
        if len(args) == 2:
            spectra = args[0].split(',')
            db_list = args[1].split(',')
            dbList = ",".join([options.db_dir+db+".fasta" for db in db_list])
        else:
            print "Aborting. - Spectra and reference proteomes needed as the arguments!"
            optparser.print_help()
            sys.exit(1)
        from trypticpeptides import weightedMatrix
        M_list_wtd = []
        for spec in spectra:
            M_list_wtd.append(weightedMatrix(spectra_name=options.spec_dir+spec,
                                             dbList=dbList,
                                             fdr=fdr, init_weight=0,
                                             verbose=verbose,
                                             Tide=options.Tide,
                                             decoy_tag=decoy_tag))
        np.array(M_list_wtd).dump(
            os.path.splitext(outputFile)[0]+"_mList_weighted.dat")

    # prep correction (1) - load/generate list of counts
    if correction:
        print ''
        from PASiC import PASiC
        if Counts:
            Counts = np.load(Counts)
        elif options.id:
            Counts = np.array(countList)
        elif options.Tide:
            print "Correction impossible! - With Tide, do the identification in the same run as the correction or provide (with '-c') counts from a previous run."
            correction = False
        else:
            from inspectparser import parseInspect
            countList = []
            for spec in spectra:
                sample_counts = []
                for DB in db_list:
                    # compose filename of spectra and database
                    inspectOut = options.spec_dir+spec + "_" + DB + "_InspectOut.txt"
                    try:
                        count = parseInspect(
                            inpath=inspectOut, fdr_countcut=fdr, silent=False)[1]
                        sample_counts.append(count)
                    except:
                        print "Could not find PSM-file for %s and %s" % (spec, DB)
                        sample_counts.append(0)
                countList.append(sample_counts)  # np.transpose(sample_counts))
                Counts = np.array(countList)
                Counts.dump(os.path.splitext(outputFile)[0]+"_counts.dat")

    # prep correction (2) - generate list of sample sizes
    if correction:
        if options.num_spectra_orginal:
            N_list = [int(N) for N in options.num_spectra_orginal.split(",")]
            if len(spectra) != len(N_list) or not all(N_list):
                print "Number of spectra required for each input dataset!"
                print "datasets:", len(spectra), "dataset sizes:", len(N_list)
                correction = False
        elif len(args) > 1:
            def countSpec_mgf(spec):
                spec_path = os.path.join(options.spec_dir, spec+".mgf")
                num_spec = os.popen('grep -c "END IONS" %s' % spec_path).read()
                print "\n", spec_path, num_spec, "\n\n"
                return int(num_spec)
            try:
                N_list = [countSpec_mgf(s) for s in spectra]
            except:
                print "Correction impossible! -  input spectra could not be counted, number required with '-N'."
                correction = False
        else:
            print "Correction impossible! - Number of input spectra required with '-N'."
            correction = False

    # run correction
    if correction:
        normCorr = []
        norm_wtd = []
        wtd_cnts = []
        for i, spec in enumerate(spectra):
            N = N_list[i]
            if unweighted:
                corrAbunds, normCorr_i = PASiC(simiMat=simiMat_unw, counts=Counts[i], N=N)
                normCorr.append(normCorr_i)
            if weighted:
                wtd_Abunds, norm_wtd_i = PASiC(simiMat=M_list_wtd[i], counts=Counts[i], N=N)
                wtd_cnts.append(wtd_Abunds * N)
                norm_wtd.append(norm_wtd_i)

    # Write all results to text file
    oFile = open(outputFile, 'w')

    # process documentation
    '''if options.time_mes:
    	oFile.write(time.strftime("%Y/%m/%d, %H:%M:%S\n", time.localtime(time.time())))
    '''
    ops = ["Identification", "Unweighted Similarity",
           "Weighted Similarity", "Correction"]
    for i, op in enumerate([options.id, unweighted, weighted, correction]):
        if op:
            oFile.write(ops[i]+"\tdone.\n")

    # resulting values
    if correction:
        if not labels:
            labels = db_list
        for i, spec in enumerate(spectra):
            oFile.write("Results for dataset '%s':\n" % spec)
            if unweighted:
                out_table = np.array(
                    zip(labels, Counts[i], wtd_cnts[i], norm_wtd[i], normCorr[i]))
                oFile.write("\t".join(["Name", "Raw counts", "Corrected Counts",
                                       "Relative abundance", "Rel. abundance unweighted corr."])+"\n")
            else:
                out_table = np.array(
                    zip(labels, Counts[i], wtd_cnts[i], norm_wtd[i]))
                oFile.write("\t".join(
                    ["Name", "Raw counts", "Corrected Counts", "Relative abundance"])+"\n")
            for line in out_table:
                oFile.write("\t".join([str(val) for val in line])+"\n")
            oFile.write("\n")

        oFile.write("Counts saved to "+os.path.splitext(outputFile)
                    [0]+"_counts.dat\n")
    if weighted:
        if len(db_list)+len(spectra) < 7:
            oFile.write(str(M_list_wtd)+"\n")
        oFile.write("List of weighted matrices saved to " +
                    os.path.splitext(outputFile)[0]+"_mList_weighted.dat\n")
    if unweighted:
        if len(db_list) < 7:
            oFile.write(str(simiMat_unw)+"\n")
        oFile.write("Unweighted matrix saved to " +
                    os.path.splitext(outputFile)[0]+"_M_unw.dat\n")
    oFile.write("All done.\n\n")
    oFile.close()

    # show results [-V]
    if options.viz:
        if correction and len(spectra) == 1:  # !!!
            from plotting import barplotPASiC
            if not labels:
                labels = db_list
            if not unweighted:
                normCorr = norm_wtd[0]
                norm_wtd = []
            else:
                normCorr = normCorr[0]
                norm_wtd = norm_wtd[0]
            barplotPASiC(names=labels, obs=np.divide(Counts[0], float(sum(
                Counts[0]))), corr=normCorr, weighted=norm_wtd, filename=os.path.splitext(outputFile)[0]+"_correction.pdf")
            print "Graphical output written to:", os.path.splitext(outputFile)[0]+"_correction.pdf"
        elif correction:
            print "Visualization is only provided for a single dataset."

    '''if options.time_mes:
        t1 = time.time()
        print time.strftime("%Y/%m/%d, %H:%M:%S: all done\n", time.localtime(t1))
        print "took %.3f seconds overall (that's %.3f minutes)"%(t1 - t0, (t1 - t0)/60)
		print "--------------------------------------------------------------------------------\n\n\n"
	'''
    t1 = time.time()
    print time.strftime("\n\n%Y/%m/%d, %H:%M:%S: all done\n", time.localtime(t1))
    print "took %.3f seconds overall (that's %.3f minutes)" % (t1 - t0, (t1 - t0)/60)
    print "--------------------------------------------------------------------------------\n\n\n"