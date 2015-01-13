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

import get_names


def _format_date(date_str):
    datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date_str


def get_id_for_fund(fund_name):
    """ Tries to find stock ID assigned to given fund name on finanse.wp.pl.

    :param fund_name: Descriptive name of fund. Examples: Agio Market Neutral FIZ
    :return: Returns fund ID on finanse.wp.pl
    """
    names, ids = get_names.get_fund_names()
    if fund_name in names:
        index = names.index(fund_name)
        return ids[index]
    else:
        raise Exception('No fund found.')


def get_fund_data(fund_id, time_range="1R", interval="1day"):
    """ Downloads and parses fund data for the given fund ID.

    :param fund_id: finanse.wp.pl fund ID.
    :param time_range: example: 1R. NOT ALL time_range/interval pairs work!
    :param interval: example: 1day. NOT ALL time_range/interval pairs work!
    :return: a list of lists with stock data day by day
    """

    # sample DATA url: http://finanse.wp.pl/fundCode,ALT24,range,3L,fundsdata.xml
    url = 'http://finanse.wp.pl/fundCode,' + fund_id + ',range,' + time_range + ',fundsdata.xml'
    xml = urllib2.urlopen(url)
    dom = minidom.parse(xml)
    xml_data = dom.getElementsByTagName('item')

    dates = [_format_date(day.getAttribute('time')) for day in xml_data]
    prices = [float(day.getAttribute('kurs1_1')) for day in xml_data]

    fund_data = [[date, prices[dates.index(date)]] for date in dates]

    return fund_data


def get_date_and_price_data(fund_name, time_range="1R", interval="1day"):
    """ Prepares stock data to be drawn on a chart. Takes whole stock data and returns only price and date lists.

    :param fund_name: fund to be displayed
    :return: price and date lists
    """
    try:
        fund_id = get_id_for_fund(fund_name)
        fund_data = get_fund_data(fund_id, time_range, interval)

        dates = [day[0] for day in fund_data]
        prices = [day[1] for day in fund_data]

        return dates, prices

    except:
        raise Exception('Could not get the data in get_date_and_price_data()')
