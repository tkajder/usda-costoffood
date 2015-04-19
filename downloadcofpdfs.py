#!/usr/bin/env python3

from bs4 import BeautifulSoup
from itertools import count
from multiprocessing import Pool
import os
import re
import requests

FOOD_PLAN_INDEX = 'http://www.cnpp.usda.gov/USDAFoodPlansCostofFood/reports?field_publication_type_tid=953&field_publication_date_value[value]&page={page_no}'
COF_REPORT_REGEX = re.compile(r'CostofFood\w\w\w\d\d')
FILE_NAME_REGEX = re.compile(r'/(\w+\d+\.pdf)\b')
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PDF_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, 'cofpdfs')

def get_cof_report_links(content):
    '''Retrieves the Cost of Food reports from a page of the USDA tables'''
    soup = BeautifulSoup(content)
    attachments = soup.find_all("span", class_="file")

    # Using a set comprehension due to duplicated months in the tables
    links = {attachment.a['href'] for attachment in attachments}

    cof_report_links = filter(is_cof_report, links)

    return list(cof_report_links)

def is_cof_report(link):
    '''Checks if a given link points to a Cost of Food report'''
    match = COF_REPORT_REGEX.search(link)

    if match:
        return True
    else:
        return False

def get_cof_report(link):
    '''Gets the Cost of Food report and saves it to PDF_DIRECTORY'''
    response = requests.get(link)
    pdf = response.content

    file_name = FILE_NAME_REGEX.search(link).group(1)

    with open(os.path.join(PDF_DIRECTORY, file_name), 'wb') as file:
        file.write(pdf)

def main():
    '''Retrieves the Cost of Food Report pdfs from the USDA website'''
    processing_pool = Pool()

    # There are a growing number of pages as time goes on
    # We iterate until there are no more Cost of Food reports on the page
    for page_no in count(start=0, step=1):
        response = requests.get(FOOD_PLAN_INDEX.format(page_no=page_no))

        cof_report_links = get_cof_report_links(response.content)

        # Check if there were links on the given page
        if cof_report_links:
            processing_pool.map_async(get_cof_report, cof_report_links)
        else:
            break

    processing_pool.close()
    processing_pool.join()

if __name__ == '__main__':
    main()
