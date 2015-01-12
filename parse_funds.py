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

import urllib2
from xml.dom import minidom
import datetime

def getFundsList():
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


def getIDforFund(fundName):
    """ Tries to find stock ID assigned to given fund name on finanse.wp.pl.

    :param stockName: Descriptive name of fund. Examples: Agio Market Neutral FIZ
    :return: Returns fund ID on finanse.wp.pl
    """
    names, ids = getFundsList()
    i = 0
    for name in names:
        if name == fundName:
            return ids[i]
        i += 1
    return "Could not find the fund."


def getFundData(fundID, timeRange="1R", interval="1day"):
    """ Downloads and parses fund data for the given fund ID.

    :param fundID: finanse.wp.pl fund ID.
    :param timeRange: example: 1R. NOT ALL timeRange/interval pairs work!
    :param interval: example: 1day. NOT ALL timeRange/interval pairs work!
    :return: a list of lists with stock data day by day
    """

    # sample DATA url: http://finanse.wp.pl/fundCode,ALT24,range,3L,fundsdata.xml
    url = 'http://finanse.wp.pl/fundCode,' + fundID + ',range,' + timeRange + ',fundsdata.xml'
    print "Url visited: " + url
    xml = urllib2.urlopen(url)
    dom = minidom.parse(xml)
    dataByDays = dom.getElementsByTagName('item')

    dates, prices = [], []

    for day in dataByDays:
        raw_day = day.getAttribute('time')
        day_formatted = datetime.datetime.strptime(raw_day, "%Y-%m-%d")  # 2011-11-14
        dates.append(day_formatted)
        prices.append(float(day.getAttribute('kurs1_1')))

    returnList = []

    i = 0
    for date in dates:
        dayItem = [date, prices[i]]
        returnList.append(dayItem)
        i += 1

    return returnList


def prepareData(fundName, timeRange="1R", interval="1day"):
    """ Prepares stock data to be drawn on a chart. Takes whole stock data and returns only price and date lists.

    :param fundName: fund to be displayed
    :return: price and date lists
    """
    try:
        fundID = getIDforFund(fundName)
        print "Downloading data..."
        fundData = getFundData(fundID, timeRange, interval)

        dates = []
        prices = []

        for day in fundData:
            dates.append(day[0])
            prices.append(day[1])

        return dates, prices

    except Exception, e:
        print "Could not get fund data."
        print e
