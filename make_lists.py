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

def getStockNames():
    """ Parses an XML document with stock names and their IDs on finanse.wp.pl website.

    :return: list names, list ids.
    """
    try:
        page = urllib2.urlopen("http://finanse.wp.pl/isin,PLOPTTC00019,stocks.xml")
        dom = minidom.parse(page)
        stocks = dom.getElementsByTagName('item')
    except Exception, e:
        print "Could not parse stocks from: http://finanse.wp.pl/isin,PLOPTTC00019,stocks.xml"
        print e

    names = []
    ids = []

    for name in stocks:
        names.append(str(name.getAttribute('name')))
        ids.append(str(name.getAttribute('value')))

    return names, ids


def saveStockNamesToFile():
    names, ids = getStockNames()

    try:
        os.remove(u'PATH/TO/CSV.csv')
    except:
        pass

    lists = zip(names, ids)
    with open(u'PATH/TO/CSV.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(lists)


def getFundsNames():
    """ Gets 2 lists - fund names and fund IDs in finanse.wp.pl
    """
    page = urllib2.urlopen("http://finanse.wp.pl/fundslist.xml")
    dom = minidom.parse(page)
    funds = dom.getElementsByTagName('item')

    names = []
    ids = []

    for fund in funds:
        names.append(str(fund.getAttribute('name').encode('utf-8')))
        ids.append(str(fund.getAttribute('value').encode('utf-8')))

    return names, ids


def saveFundNamesToFile():
        names, ids = getFundsNames()

        try:
            os.remove(u'PATH/TO/CSV.csv')
        except:
            pass

        lists = zip(names, ids)
        with open(u'PATH/TO/CSV.csv', 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(lists)
