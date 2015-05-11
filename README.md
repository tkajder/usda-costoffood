# usda-costoffood

usda-costoffood is a collection of scripts to retrieve and analyze monthly [USDA Cost of Food Reports](http://www.cnpp.usda.gov/USDAFoodPlansCostofFood/reports) which are distributed as `.pdf` files.

Setup Requirements
------------------
All scripts are tested in Python 2.7 and Python 3.4.
The required python packages specified in the requirements.txt file should be downloaded into a virtualenv in the project directory like so:

```bash
$ virtualenv venv
```

This project relies on the `pdftotext`version 0.26.5 executable from [xpdf](http://www.foolabs.com/xpdf/download.html).

Downloading USDA Cost of Food Reports
-------------------------------------
USDA Cost of Food Reports are published monthly in `.pdf` format. To download all available reports run:

```bash
$ ./downloadcofpdfs.py
```

`downloadcofpdfs.py` will take some time as there are more than 240 published reports and this script respects crawl-delay of 10 seconds in the robots.txt.

Creating `.txt` Files from `.pdf`
---------------------------------
Generating `.txt` files relies on `pdftotext`. To generate all `.txt` files from the downloaded reports run:

```bash
$ ./generate_txts.sh
```
Currently `pdftotext` generates empty files for report earlier than May 1997 making this data inaccessible.

Creating `.csv` Files from `.txt`
---------------------------------
The generated `.txt` files from `pdftotext` are poorly organized due to the formatting of USDA Cost of Food reports. The generation of `.csv` files is handled by the script `coftxttocsv.py` which is called for each `.txt` file by `generate_csvs.sh`. To generate usable `.csv` files run:

```bash
$ ./generate_csvs.sh
```
Note that the `.csv` files can have different age cutoffs due to changes in reporting. The most notable of these changes occurs between the reports February 2007 and Sep 2007.

Errors
------
Due to incorrect pdf generation of the USDA Cost of Food reports from the period March 2007 to August 2007 the files from this period are unusable as data.