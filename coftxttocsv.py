#!/usr/bin/env python3

import argparse
import csv
import re
import sys

HEADERS = ['Group', 'Age', 'Weekly Thrifty Plan', 'Weekly Low-Cost Plan', 'Weekly Moderate-Cost Plan', 'Weekly Liberal Plan', 'Monthly Thrifty Plan', 'Monthly Low-Cost Plan', 'Monthly Moderate-Cost Plan', 'Monthly Liberal Plan']
CHILD_SECTION_REGEX = re.compile('((Child)|(CHILD)):\n(?P<content>.+)(?=\n\nM)', flags=re.DOTALL)
MALE_SECTION_REGEX = re.compile('((Male)|(MALE))( \(M\))?:\n(?P<content>.+)(?=\n\nF)', flags=re.DOTALL)
FEMALE_SECTION_REGEX = re.compile('((Female)|(FE( )?MALE))( \(F\))?:\n(?P<content>.+)(?=\n\nF)', flags=re.DOTALL)

def get_csv_rows(group, section):
	'''Transform a male section into csv male rows'''
	data_rows = get_rows(section)

	# Add the group to each data_row
	csv_rows = map(lambda row: (group, ) + row, data_rows)

	return csv_rows

def get_rows(section):
	'''Transform the text section into tuple rows of data'''
	table_groups = section.split('\n\n')
	columns = map(lambda group: group.split('\n'), table_groups)
	rows = zip(*columns)
	return rows

def command_line():
	'''Define the cli and parse args from stdin'''
	# Define the cli and options
	parser = argparse.ArgumentParser(prog='coftocsv', description='Transforms a Cost of Food report in txt format from given filename to a csv file')
	parser.add_argument('file', help='input file name')
	parser.add_argument('output', help='output file name')

	args = parser.parse_args()

	# Return dict instead of Namespace
	return args

def main():
	args = command_line()

	with open(args.file, 'r') as file:
		contents = file.read()

	# Retrieve the child, male, and female rows
	child_section_match = CHILD_SECTION_REGEX.search(contents)
	if child_section_match:
		child_rows = get_csv_rows('Child', child_section_match.group('content'))
	else:
		print('Could not retrieve Child section from {}'.format(args.file), file=sys.stderr)
		sys.exit(1)

	male_section_match = MALE_SECTION_REGEX.search(contents)
	if male_section_match:
		male_rows = get_csv_rows('Male', male_section_match.group('content'))
	else:
		print('Could not retrieve Male section from {}'.format(args.file), file=sys.stderr)
		sys.exit(1)

	female_section_match = FEMALE_SECTION_REGEX.search(contents)
	if female_section_match:
		female_rows = get_csv_rows('Female', female_section_match.group('content'))
	else:
		print('Could not retrieve Female section from {}'.format(args.file), file=sys.stderr)
		sys.exit(1)

	# Write the csv file using headers, child, male, and female rows
	with open(args.output, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(HEADERS)
		writer.writerows(child_rows)
		writer.writerows(male_rows)
		writer.writerows(female_rows)

if __name__ == '__main__':
	main()
