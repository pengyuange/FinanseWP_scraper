"""
The module contains a set of functions designed to help with scraping stock
data from finanse.wp.pl website.
Author: Adam Giermanowski
"""

import urllib2
import datetime
from xml.dom import minidom


def prepareData(stockName, timeRange, interval):
    """ Prepares stock data to be drawn on a chart. Takes whole stock data and returns only price and date lists.

    :param stockName: stock to be displayed
    :param timeRange: data time range
    :param interval: data interval
    :return: price and date lists
    """
    try:
        stockID = getIDforStock(stockName)
        print "Downloading data..."
        stockData = getStockData(stockID, timeRange, interval) # TODO describe params

        dates = []
        prices = []

        for day in stockData:
            dates.append(day[0])
            prices.append(day[1])

        return dates, prices

    except Exception, e:
        print "Could not get the stock."
        print e


def getStockNames():
    """ Parses an XML document with stock names and their IDs on finanse.wp.pl website.

    :return: list names, list ids.
    """
    page = urllib2.urlopen("http://finanse.wp.pl/isin,PLOPTTC00019,stocks.xml")
    dom = minidom.parse(page)
    stocks = dom.getElementsByTagName('item')

    names = []
    ids = []

    for name in stocks:
        names.append(str(name.getAttribute('name')))
        ids.append(str(name.getAttribute('value')))

    return names, ids



def getIDforStock(stockName):
    """ Tries to find stock ID assigned to given universal stock name on finanse.wp.pl.

    :param stockName: Universal name(symbol) of stock on WSE(GPW). Examples: PKNORLEN, CDPROJEKT
    :return: Returns stock ID on wp.pl
    """
    names, ids = getStockNames()
    i = 0
    for name in names:
        if name == stockName:
            return ids[i]
        i+=1
    return "Could not find the stock."



def getStockData(stockID, timeRange, interval):
    """ Downloads and parses stock data for the given stock ID.

    :param stockID: wp.pl stock ID.
    :param timeRange: example: 1D, 1M, 3M, 1R, 3R. NOT ALL timeRange/interval pairs work!
    :param interval: example: 1day, 1min, 30min. NOT ALL timeRange/interval pairs work!
    :return: a list of lists with stock data day by day
    """
    url = 'http://finanse.wp.pl/isin,' + stockID + ',range,' + timeRange + ',split,1,int,' + interval + ',graphdata.xml'

    print "Visited URL: " + url

    xml = urllib2.urlopen(url)
    dom = minidom.parse(xml)
    dataByDays = dom.getElementsByTagName('item')

    dates, closePrices, highPrices, lowPrices, openPrices, volume = [], [], [], [], [], []

    for day in dataByDays:
        raw_day = day.getAttribute('time').split(' ')[0]
        day_formatted = datetime.datetime.strptime(raw_day, "%Y-%m-%d")  # 2011-11-14
        dates.append(day_formatted)
        closePrices.append(float(day.getAttribute('kurs1_2')))
        highPrices.append(float(day.getAttribute('max')))
        lowPrices.append(float(day.getAttribute('min')))
        openPrices.append(float(day.getAttribute('kurs1_1')))
        volume.append(float(day.getAttribute('vol')))

    returnList = []

    i = 0
    for date in dates:
        dayItem = [date, closePrices[i], highPrices[i], lowPrices[i], openPrices[i], volume[i]]
        returnList.append(dayItem)
        i += 1

    return returnList



def saveStockDataToFile(stockID, timeRange, interval):
    """ Saves stock data to a text file.

    :param stockID: wp.pl stock ID.
    :return: Saves "workfile.txt"
    """
    stockData = getStockData(stockID)  # TODO FIX PARAMS
    f = open("output.txt", "w")

    for listItem in stockData:
        f.write(str(listItem) + "\n")



def calculatePercentChange(stockID, date1, date2):
    """ Calculates percent change between two days for a given stock.

    :param stockID: wp.pl stock ID.
    :param date1: First Date. Datetime date format.
    :param date2: Second Date. Datetime date format
    :return: returns percent change.
    """
    data = getStockData(stockID) # TODO FIX PARAMS
    dates = []
    prices = []

    for day in data:
        dates.append(day[0])
        prices.append(day[1])

    try:
        priceAtDate1 = prices[dates.index(date1)]
        priceAtDate2 = prices[dates.index(date2)]
    except:
        print "Could not find any data. Is it weekend day?"

    percentChange = (priceAtDate2 - priceAtDate1)/priceAtDate1

    return percentChange
