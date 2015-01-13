import time
import urllib2
from xml.dom import minidom

import get_names

stock_data = get_names.get_stock_names()


def volume_alert(stock, critical_value, min_av_vol, time_range):
    ''' Generates a alert if stock volume is high.
    stock - a list with stock data
    critical_value - how many times larger than average
    min_av_vol - minimal average volume (to skip very tiny stocks)
    time_range - days for the average calculation. Works like: 365 - time_range = days
    '''

    global stock_data

    return_data = None

    url = 'http://finanse.wp.pl/isin,' + stock_data.get(stock) + ',range,1R,split,1,int,1day,graphdata.xml'
    xml = urllib2.urlopen(url)
    dom = minidom.parse(xml)
    days = dom.getElementsByTagName('item')
    try:
        volume = [float(day.getAttribute('obr')) for day in days]
    except ValueError:
        pass

    if len(days) > time_range:
        days = days[time_range:]
    else:
        return return_data

    try:
        av_turnover = reduce(lambda x, y: x + y, volume) / len(volume)
        last_turnover = volume[-1]
        crit_turnover = av_turnover * critical_value
    except:
        return

    if last_turnover > crit_turnover:
        if av_turnover < min_av_vol:
                return return_data

        percent_change = int(((last_turnover - av_turnover) / av_turnover) * 100)
        return_data = [stock, str(percent_change)]
        return return_data


if __name__ == "__main__":

    data_to_save = []
    print "Report is going to be created..."

    i = 1
    for stock in stock_data:
        print i,'/',len(stock_data)
        single_stock_data = volume_alert(stock, 1.3, 100.0, 180)
        i += 1

        if single_stock_data is not None:
            print 'found',single_stock_data
            data_to_save.append(single_stock_data)

    with open('volume_report.txt', 'w') as file:
        file.seek(0)
        file.truncate()
        file.write("VOLUME REPORT, GENERATED ON: " + time.strftime("%c") + "\n-------------------------------\n")

        for item in data_to_save:
            file.write(str(item) + '\n')

        file.close()
