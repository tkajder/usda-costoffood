# usda-costoffood

usda-costoffood is a collection of scripts to retrieve and analyze monthly [USDA Cost of Food Reports](http://www.cnpp.usda.gov/USDAFoodPlansCostofFood/reports) which are distributed as `.pdf` files.

Setup Requirements
------------------
All scripts run in Python 2.7 and Python 3. 
The required python packages specified in the requirements.txt file should be downloaded into system packages or a virtualenv.

This project relies on the `pdftotext` executable from [xpdf](http://www.foolabs.com/xpdf/download.html).

Downloading USDA Cost of Food Reports
-------------------------------------
USDA Cost of Food Reports are published monthly in `.pdf` format. To download all available reports run:

```bash
$ python downloadcofpdfs.py
```

Although `downloadcofpdfs.py` runs with multi-processing there are more than 240 published reports and the script will take several minutes.

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
Note that the `.csv` files can have different age cutoffs due to changes in reporting. The most notable of these changes occurs between the reports February 2007 and March 2007.
