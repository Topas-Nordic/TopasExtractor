# Topas Extractor

Topas Extractor is mainly a CLI tool for extracting refined and non-refined parameters from Topas .OUT files directly, and export them
as a csv file. The tool works with both single refinement files and BIG.OUT files which we typically generate
when setting up a surface refinement. By default Topas Extractor does not extract non-refined paramters. To do this see further down.

Although Topas has good support to export parameters, I and many others prefer to extract parameters directly from
the .OUT file. Topas Extractor is an aid for this type of workflow.

## Installation

```
git clone https://github.com/Topas-Nordic/TopasExtractor.git

cd TopasExtractor
pip install -e .
```
Alternativly if you do not have git installed:
```
pip install git+https://github.com/Topas-Nordic/TopasExtractor.git
```

## Using the CLI

Topas extrator is primarily a CLI based tool. After installing the package simply:

```
tpextract path-to-your.OUT results.csv
```

Topas Extract allows you to exclude or select specific refined parameters to be exported. __Remember to
exclude any white-spaces between the commas__.

```
tpextract ref.OUT results.csv -sct "a,b,c,scale"   # This selects parameters starting with the letter b, a, c and the scale factor.
```

```
tpextract ref.OUT results.csv -exc "Zero_Error,Si,O1"  # Excludes Zero_Error, and refined params for Si and O atoms.
```

You can combine a select and exclude statement to yield exactly what you want:

```
tpextract ref.OUT results.csv -sct "a,b,c" -exc "be,bkg" #This gives only the lattive parameters a, b, and c.
```

To see all the options of Topas Exract then use the help menu:

```
tpextract -h
usage: tpextract [-h] [-exc EXC] [-sct SCT] [-xdd] [-big] topas-out output

Tool for extracting TP data.

positional arguments:
  topas-out   Path to the topas out file.
  output      Output filename.

optional arguments:
  -h, --help  show this help message and exit
  -exc EXC    Parameters to exclude from Topas OUT file. Written as a comma seperated list: E.g: "c,a,scale"
  -sct SCT    Parameters to select specifically from Topas OUT file. Written as a commar separated list. E.g.: "c,a,b"
  -xdd        Include the xdd file name in the extraction.
  -big        For surface refined BIG.INP topas files.
```

## Using Topas Extract in JupyterLab

Topas Extract can also be imported into your own python scripts, or be used inside
a jupyter notebook.

```
import tpextraxt as te

tp_file = te.read_topas(tpfile=r".OUT")
extracted_params = te.extract_refined(tp_file)  # returns a dictionary of the refined parameters
```

## Extracting non-refined parameters.

Topas Extractor does not by default extract non-refined parameters. To do this simply add '# after the non-refined number.

```
x_calculation_step 0.02'# This parameters will now be extracted.
bkg @  41.8829404`  70.7020173`
Zero_Error(,-0.01103)
start_X  2.2'#   This parameters will now be extracted.
finish_X  26
LP_Factor( 0)
One_on_X(@, 522.60385`)

```

## Disclamer
The Topas Extractor has been tested with many different .OUT files. But, this is not a guarantee that
the Topas Extractor always will be able to find every refined parameter without issues. If you stumble upon a problem,
please leave an "Issue" ticket or contact me.


