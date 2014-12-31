# IMPORTANT
# PATHS TO DATA FILES NEED TO BE CHANGED
# FOLLOWING FUNCTIONS SHOULD BE USED TO SIMPLIFY THE USAGE OF PARSING MODULES

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
