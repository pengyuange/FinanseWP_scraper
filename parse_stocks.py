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
import datetime
from xml.dom import minidom


def _format_date(date_str):
    datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date_str


def get_date_and_price_data(stock_name, time_range, interval):
    """ Returns two lists: dates and prices.

    :param stock_name: stock to be displayed
    :param time_range: data time range. example: 1D, 1M, 3M, 1R, 3R, OP. NOT ALL timeRange/interval pairs work!
    :param interval: data interval. example: 1day, 1min, 30min. NOT ALL timeRange/interval pairs work!
    :return: price and date lists
    """
    try:
        stock_id = get_id_for_stock(stock_name)
        stock_data = get_stock_data(stock_id, time_range, interval)

        dates = [day[0] for day in stock_data]
        prices = [day[1] for day in stock_data]

        return dates, prices

    except Exception, e:
        print "Could not get the stock.", e


def get_stock_names():
    """ Parses an XML document with stock names and their IDs on finanse.wp.pl website.

    :return: list names, list ids.
    """
    page = urllib2.urlopen("http://finanse.wp.pl/isin,PLOPTTC00019,stocks.xml")
    dom = minidom.parse(page)
    stocks = dom.getElementsByTagName('item')

    names = [str(name.getAttribute('name')) for name in stocks]
    ids = [str(name.getAttribute('value')) for name in stocks]

    return names, ids


def get_id_for_stock(stock_name):
    """ Tries to find stock ID assigned to given universal stock name on finanse.wp.pl.

    :param stock_name: Universal name(symbol) of stock on WSE(GPW). Examples: PKNORLEN, CDPROJEKT
    :return: Returns stock ID on wp.pl
    """
    names, ids = get_stock_names()
    i = 0
    for name in names:
        if name == stock_name:
            return ids[i]
        i+=1
    return "Could not find the stock."


def get_stock_data(stock_id, time_range="1R", interval="1d"):
    """ Downloads and parses stock data for the given stock ID.

    :param stock_id: wp.pl stock ID.
    :param time_range: example: 1D, 1M, 3M, 1R, 3R, OP. NOT ALL time_range/interval pairs work!
    :param interval: example: 1day, 1min, 30min. NOT ALL time_range/interval pairs work!
    :return: a list of lists with stock data day by day
    """
    url = 'http://finanse.wp.pl/isin,' + stock_id + ',range,' + time_range + ',split,1,int,' + interval + ',graphdata.xml'

    print "Visited URL: " + url

    xml = urllib2.urlopen(url)
    dom = minidom.parse(xml)
    xml_data = dom.getElementsByTagName('item')

    dates = [_format_date(day.getAttribute('time').split(' ')[0]) for day in xml_data]
    close_prices = [float(day.getAttribute('kurs1_2')) for day in xml_data]
    high_prices = [float(day.getAttribute('max')) for day in xml_data]
    low_prices = [float(day.getAttribute('min')) for day in xml_data]
    open_prices = [float(day.getAttribute('kurs1_1')) for day in xml_data]
    volume = [float(day.getAttribute('vol')) for day in xml_data]

    parsed_data = []

    for date in dates:
        parsed_data.append([date, close_prices[date], high_prices[date], low_prices[date], open_prices[date], volume[date]])

    return parsed_data


def save_data_to_file(stock_id, time_range, interval):
    """ Saves stock data to a text file.

    :param stock_id: wp.pl stock ID.
    :return: Saves "workfile.txt"
    """
    stock_data = get_stock_data(stock_id, time_range, interval)
    f = open("output.txt", "w")

    for day in stock_data:
        f.write(str(day) + "\n")


def calculate_percent_change(stock_id, date1, date2):
    """ Calculates percent change between two days for a given stock.

    :param stock_id: wp.pl stock ID.
    :param date1: First Date. Datetime date format.
    :param date2: Second Date. Datetime date format
    :return: returns percent change.
    """
    data = get_stock_data(stock_id, 'OP', '1d')

    dates = [day[0] for day in data]
    prices = [day[1] for day in data]

    try:
        price_at_date1 = prices[dates.index(date1)]
        price_at_date2 = prices[dates.index(date2)]
    except Exception, e:
        print "Could not find any data. Is it weekend day?", e

    percentChange = (price_at_date2 - price_at_date1)/price_at_date1

    return percentChange
