#!/usr/bin/env python3

"""
    download articles from the legacy website of the turnverein oberi
"""

import pdfkit
from requests_html import HTMLSession
import string
from datetime import datetime
import os
import sys, traceback

##
# GLOBAL 
##

BASE_URL="https://legacy.tvo.ch"
REPORT_PAGES = [
    "{}/index.php/berichte-2018.html".format(BASE_URL),
    "{}/index.php/berichte-2017.html".format(BASE_URL),
    "{}/index.php/berichte-2016-2.html".format(BASE_URL),
    "{}/index.php/berichte-2015-2.html".format(BASE_URL),
    "{}/index.php/berichte-2014-2.html".format(BASE_URL),
    "{}/index.php/berichte-2013-3.html".format(BASE_URL),
    "{}/index.php/berichte-2012-3.html".format(BASE_URL),
    "{}/index.php/berichte-2011-3.html".format(BASE_URL),
    "{}/index.php/berichte-2010-3.html".format(BASE_URL),
    "{}/index.php/berichte-2009-3.html".format(BASE_URL),
    "{}/index.php/berichte-2008-3.html".format(BASE_URL),
]

##
# FUNCTIONS
##

def get_report_links(report_page):
    """
        get all links pointing to reports
    """
    session = HTMLSession()
    reports = session.get(report_page).html.find('.category-module_berichtgesamt', first=True)
    if not reports:
        raise ValueError("No links found in reports page.")
    return reports.absolute_links

def get_report_page(report_page):
    """
        retrieve report page content, return ReportPage object
    """
    session = HTMLSession()

    # retrieve the page content (no navigation, no reports list etc)
    page = session.get(report_page).html.find('.item-page', first=True)
    if not page:
        raise ValueError("Unable to retrieve report page content.")


    # get title from page content
    title = page.find('h2', first=True)
    if not title:
        raise ValueError("Unable to retrieve title from page content.")

    # get creation date and time from page
    creation_date = page.find('time', first=True)
    if not creation_date:
        raise ValueError("Unable to retrieve creation date from page content.")
    creation_date = datetime.strptime(creation_date.attrs['datetime'], '%Y-%m-%dT%H:%M:%S+00:00')

    # get the pages html content
    # replace all relative img tags with absolute paths
    body = page.html
    body = body.replace('<img src="/', '<img src="{}/'.format(BASE_URL))

    # return page object
    return ReportPage(title.text, creation_date, body)

##
# CLASSES
##

class ReportPage(object):
    def __init__(self, title, creation_date, body):
        self.title = title
        self.creation_date = creation_date
        # setup fake html body to pass meta arguments
        self.body = """
            <html>
                <head>
                    <meta name="pdfkit-page-size" content="A4"/>
                    <meta name="pdfkit-orientation" content="Portrait"/>
                    <meta charset="utf-8">
                </head>
                <body>
                    {}
                </body>
            </html>
        """.format(body)

        self._generate_filename()

    def _generate_filename(self):
        """
            create a valid filename from date and title
        """
        self.filename = "{}_{}.pdf".format(
            self.creation_date.strftime('%Y%m%d'),
            self._format_filename(self.title)
        )

    def _format_filename(self, s):
        # https://gist.github.com/seanh/93666
        valid_chars = "-_.()öäü %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ','_')
        return filename

##
# MAIN
##

if __name__ == "__main__":
    try:
        # loop trough all report pages
        for reportpage in REPORT_PAGES:
            print("Parsing reports in {}".format(reportpage))
            # loop trough all pages found
            for page in get_report_links(reportpage):
                print("Parse report page {}".format(page))
                # retrieve content from pages and create pdf
                p = get_report_page(page)
                pdfkit.from_string(p.body, os.path.join('data', p.filename))
    except:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
