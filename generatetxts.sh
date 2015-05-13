#!/usr/bin/env bash

for file in pdfs/*.pdf
	do pdftotext "$file"
done

mv pdfs/*.txt txts/
