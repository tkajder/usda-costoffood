#!/usr/bin/env bash

for file in txts/*.txt
do 
	dirstrippedfile=$(basename "$file")
	extstrippedfile="${dirstrippedfile%.*}"
	./coftxttocsv.py "$file" csvs/"$extstrippedfile".csv
done