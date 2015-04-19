#!/usr/bin/env bash

for file in cofpdfs/*.pdf
	do pdftotext "$file"
done

mv cofpdfs/*.txt txts/