#!venv/bin/python

from bs4 import BeautifulSoup
from itertools import count
import logging
import os
import re
import requests
from requests_throttler import BaseThrottler

FOOD_PLAN_INDEX = '''http://www.cnpp.usda.gov/USDAFoodPlansCostofFood/reports?field_publication_type_tid=953&field_publication_date_value[value]&page={page_no}'''
ORIGIN_BASE_ADDRESS = '''http://origin.www.cnpp.usda.gov/'''
ORIGIN_TABLE_ADDRESS  = '''http://origin.www.cnpp.usda.gov/USDAFoodCost-Home.htm'''

COF_REPORT_NAME_REGEX = re.compile(r'/(CostofFood\w\w\w(\d){2,4}\.pdf)\b')

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PDF_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, 'pdfs')

THROTTLER = BaseThrottler(name='cof-report-throttler', delay=10.0)

class Report:
    '''A container for report name and link that overrides __hash__ and
    __eq__ for sets to remove reports of the same name'''
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return 'Name: {}\tLink: {}'.format(self.name, self.link)

def get_index_reports():
    '''Retrieves the Cost of Food reports from the index pages at cnpp.usda.gov.
    Note that this set is incomplete due to poor html creation so we redundantly
    scrape origin to get all reports.'''
    # We use a set because the created html contains duplicate reports
    links = set()

    # Indeterminate number of pages, count upwards until no reports found
    for page_no in count(start=0, step=1):
        response = throttle_request(FOOD_PLAN_INDEX.format(page_no=page_no))
        soup = BeautifulSoup(response.content)

        # Grab all attachments in the index: links to reports and other documents
        attachments = soup.find_all("span", class_="file")
        if attachments:
            links.update({attachment.a['href'] for attachment in attachments})
        else:
            break

    # Yield reports from links
    for link in links:
        match = COF_REPORT_NAME_REGEX.search(link)
        if match:
            yield Report(match.group(1), link)
        else:
            logging.warning('Could not process link %s into report name', link)

def get_origin_reports():
    '''Retrieve all COF reports from the origin link. Note this index is
    complete, but lags behind the current date by over a year.'''
    response = throttle_request(ORIGIN_TABLE_ADDRESS)
    soup = BeautifulSoup(response.content)
    # All a_hrefs contained in the table point to reports
    a_hrefs = soup.find(id='table39').find_all('a')

    # Yield reports from links
    for a_href in a_hrefs:
        link = ORIGIN_BASE_ADDRESS + a_href.get('href')
        match = COF_REPORT_NAME_REGEX.search(link)
        if match:
            yield Report(match.group(1), link)
        else:
            logging.warning('Could not process link %s into report name', link)

def download_report(report):
    '''Gets the COF report and save it to PDF_DIRECTORY'''
    response = throttle_request(report.link)
    pdf_content = response.content

    with open(os.path.join(PDF_DIRECTORY, report.name), 'wb') as file:
        file.write(pdf_content)

def throttle_request(url):
    '''Retrieves the response from a url, throttling the request to follow robots.txt'''
    request = requests.Request(method='GET', url=url)
    throttled_request = THROTTLER.submit(request)
    response = throttled_request.response
    return response

def main():
    # Start the throttler's threads
    THROTTLER.start()

    # Retrieve all Cost of Food report links and create a set
    index_reports = get_index_reports()
    origin_reports = get_origin_reports()
    reports = set(index_reports) | set(origin_reports)

    # Download all Cost of Food reports
    for report in reports:
        download_report(report)

    # Shutdown the throttler's threads
    THROTTLER.shutdown()

if __name__ == '__main__':
    main()
