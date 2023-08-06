# pipasic - peptide intensity-weighted proteome abundance similarity correction

## Abstract

Metaproteomic analysis allows studying the interplay of organisms or functional  groups and has become increasingly popular also for diagnostic purposes.  However, difficulties arise due to the high sequence similarity between related organisms. Further, the state of conservation of proteins between species can 
be correlated with their expression level which can lead to significant bias in  results and interpretation. These challenges are similar but not identical to  the challenges arising in the analysis of metagenomic samples and require  specific solutions. 

We developed pipasic (peptide intensity-weighted proteome abundance similarity  correction) as a tool which corrects identification and spectral counting based  quantification results using peptide similarity estimation and expression level  weighting within a non-negative lasso framework. pipasic has distinct advantages  over approaches only regarding unique peptides or aggregating results to the  lowest common ancestor, as demonstrated on examples of viral diagnostics and an  acid mine drainage dataset.

## Requirements

pipasic might be able to work with different software versions, but we tested  it using the given configuration.

**Python environment**

1. Install [Anaconda](https://docs.anaconda.com/anaconda/install/) ( `conda` command shoudl work in your console)

2. ` conda create -n pipasic python=2.7.13` in consoele to create a new `Python` environment

3. `conda activate pipasic`  in console to activate your environment, named pipasic

4. `pip install -r requirements.txt` in console install all `Python` dependencies

   

**Spectrum identification**

Spectrum identification can be done with Inspect or Tide. We used the following
versions:

- [InsPecT](./inspect) version January 2012 [tutorial](http://proteomics.ucsd.edu/Software/Inspect/InspectDocs/InspectTutorial.pdf)
- Tide as part of Crux 1.36


## Usage

Usage: pipasic.py SPECTRA DB [module options] [input and configuration options]

Overall pipasic calling tool, including:
- weighted (always) and unweighted (optional) similarity estimation
- correction, using matrix from similarity estimation
- peptide Identification by InsPecT/Tide

SPECTRA: Comma-separated string of spectrum files (mgf) - without file-extension!
DB:      Comma-separated string of reference proteomes (fasta-files) - without file-extension!
         if -S or -I: decoy database must exist as db_name+"_decoy.fasta"

Options:

```bash
  -h, --help            show this help message and exit
  -U, --Unweighted      calculate unweighted similarities for all given
                        proteomes
  -I, --Identify        identify given spectra with all given proteomes
  -T, --Tide            use Tide instead of InsPecT
  -V                    Visualize results using matplotlib
  -o OUTFILE, --outfile=OUTFILE
                        Output filename for results. Also serves as trunk for
                        other result files (graphics, data).  [default:
                        results.txt]
  -s SPEC_DIR, --spec_dir=SPEC_DIR
                        Directory of SPECTRA (mgf) files. Search in current
                        directory, if not given. [default: none]
  -d DB_DIR, --db_dir=DB_DIR
                        Directory of proteinDBs. Search for DB files current
                        directory, if not given. [default: none]
  -m MODS, --mods=MODS  A string containing all modifications in question,
                        modification choice by filename if not given.
                        [default: none]
  -i INSP_DIR, --inspect_dir=INSP_DIR
                        Inspect directory. [default: none]
  -f FDR, --fdr_cutoff=FDR
                        False discovery rate cut-off for identification lists.
                        [default: 0.05]
  -l LABELS, --labels=LABELS
                        Comma-separated string of short names for organisms in
                        the reference proteomes. If not given, the file name
                        is used. [default: none]
  -N N, --N_spectra=N   Number of spectra in original dataset, comma-separated
                        list if multiple datasets. [default: none]
  -c COUNTS, --C_spectra=COUNTS
                        File containing numbers of spectra found by
                        identification (Numpy Array dump). [default: none]
  -q, --quiet           don't print status messages to stdout
```



## Example run

Data has been prepared in local [example](./example) folder, but you can download from [here](https://sourceforge.net/projects/pipasic/files/example.tar.gz/download) too.

**Test InspecT**

Automatized configuration and execution of Inspect peptide identification for  a list of spectrum files and a list of reference proteomes.

Users can compile `Inspect` from [source code](./inspect) by using `make` command (Linux/MacOS), or build `Inspect.exe` with `Inspect.sln` in Visual Studio (Windows). 

> The executable Inspect or Inspect.exe has been put in the root directory, side by sied with foler `src`,  `example`, ana `inspect`. Please don’t move them.

```bash
# For Linux/MacOS
./inspect -i ./config_files/config_Inspect_py.txt -o ./example/data/example_species2_InspectOut.txt -r ./inspect/
```

```bash
# Windows
 InsPecT.exe -i ./config_files/config_Inspect_py.txt -o ./example/data/example_species2_InspectOut.txt -r ./inspect/
```

> Result:
>
> 1. example_species1_InspectOut.txt
> 2. example_species2_InspectOut.txt
> 3. .index and .trie file of database

**Full workflow**

```bash
# Change directory now.
cd ./src/trunk # change directory to trunk folder
```

```bash
python pipasic.py example species1,species2 -s ../data/spectra/ -d ../data/reference/ -I -i ./inspect/ -o ../result/output -V
```

**Unit test**

```bash
# Change directory now.
cd ./src # change directory to trunk folder
```

1. *match spectra against database with Inspect* 

   ```bash
   python runInspect_user_config.py --easy True
   # Result: 
   # 1. example_species1_InspectOut.txt
   # 2. example_species2_InspectOut.txt
   # 3. .index and .trie file of database
   ```

2. extract selected information from InsPecT output files and produce a specified  peptide identification (PSM) list for further analyses.

   ```bash
   python nspectparser.py --easy True 
   # Result:
   # 1. result_counts.dat: number of peptides not in decoy returned
   # 2. specified  peptide identification: 
   ```

   

3. Search identified peptides in tryptic peptide list of a proteome in order  to weight each peptide  (return: path to output file with line structure: "weight sequence")

   ```bash
   python trypticpeptides.py --easy true
   # Result:
   # 1. peptides_species1.fasta:
   # 2. peptides_species2.fasta
   ```

4. ==Todo==

## License

Copyright (c) 2013, Martin S. Lindner, LindnerM@rki.de, and Anke Penzlin, Robert Koch-Institut, Germany,
**All rights reserved**.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

- Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
-  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
-  The name of the author may not be used to endorse or promote products  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL MARTIN S. LINDNER OR ANKE PENZLIN BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.