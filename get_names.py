'''
Copyright (c) 2014 Adam Giermanowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import os
import csv
import urllib2
from xml.dom import minidom

def get_stock_names():
    """ Returns 2 lists - fund names and fund IDs

    :return: list names, list ids.
    """
    try:
        page = urllib2.urlopen("http://finanse.wp.pl/isin,PLOPTTC00019,stocks.xml")
        dom = minidom.parse(page)
        stocks = dom.getElementsByTagName('item')
    except:
        raise Exception('Could not parse stocks from: http://finanse.wp.pl/isin,PLOPTTC00019,stocks.xml')

    names = [str(name.getAttribute('name')) for name in stocks]
    ids = [str(name.getAttribute('value')) for name in stocks]

    return names, ids


def get_stock_names_csv():
    """ Saves a list of stock names to csv
    """

    names, ids = get_stock_names()

    try:
        os.remove('names.csv')
    except:
        pass

    lists = zip(names, ids)
    with open('names.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(lists)


def get_fund_names():
    """ Returns 2 lists - fund names and fund IDs
    """
    page = urllib2.urlopen("http://finanse.wp.pl/fundslist.xml")
    dom = minidom.parse(page)
    funds = dom.getElementsByTagName('item')

    names = [str(fund.getAttribute('name').encode('utf-8')) for fund in funds]
    ids = [str(fund.getAttribute('value').encode('utf-8')) for fund in funds]

    return names, ids


def get_fund_names_csv():
    """ Saves a list of fund names to csv
    """
    names, ids = get_fund_names()

    try:
        os.remove('funds.csv')
    except:
        pass

    lists = zip(names, ids)
    with open('funds.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(lists)
