#from __future__ import division
import threading

import time

from yahoo_finance import Share
import math
import pyvse2
import pause
import datetime
import requests
import json
import pprint
import urllib2
from bs4 import BeautifulSoup
from urllib import urlopen
from delorean import Delorean
import sys

#### ADD DAY, after month in wait time
#print ystockquote.get_price("GOOG")
print ("\rInitializing BenBot v.01 ..... Please wait"),
#time.sleep(2)
print "\rWelcome to the BenBot auto trader! Starting up now."

sys.stdout.write('Starting test')
sys.stdout.flush()
sys.stdout.write('\rtest2')
sys.stdout.flush()


OpenHour = 8
CloseHour = 15
#datetime.datetime()

def getTime():
    return int(time.time())

BiggestGainPercent = 0.0
BiggestGainName = str("None!")
BiggestGainShares = 0



List = open("stocks.txt").readlines()

stocks = {}

def Start_Tracking_Stocks():
    global stocks

    StocksAdded = 0
    for stockSymb in List:
        thestock = str(stockSymb).strip("\n")
        time.sleep(1/4)
        #print Share(thestock).get_avg_daily_volume()
        #print Share(thestock).get_price()
        stocks[thestock] = {}
       # print stocks.get(thestock)
        StocksAdded += 1



    #stocks = { "GOOG": {}, "RCKY": {}}
    #print stocks
    print StocksAdded,
    print " stocks being tracked.\n"

Start_Tracking_Stocks()

def PostMarketWait():
    CST = "US/Central"
    #Delorean.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day+1,OpenHour,30)
    #d = Delorean(timezone=CST)
    #return datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day+1,OpenHour,30)
    return 1000

def get_stock_quote(ticker):
    url = '%s%s' % ('http://www.google.com/finance/info?q=', ticker)
    doc = urlopen(url)
    content = doc.read()
    quote = json.loads(content[3:])
    quote = float(quote[0][u'l'])
    return quote

def CurrentStockTracker():
    GoogShares = 0
    while True:
        global BiggestGainName
        global BiggestGainShares
        global BiggestGainPercent

        username = "hockeymikey@grottomc.com"
        password = "bendorman"

        my_session = pyvse2.VSESession()
        my_session.login(username, password)

        my_game = my_session.game("bendormanse")

        CurShares = 0
        CurStock = "None!"

        print "Selling Goog placeholder stocks."
        my_game.sell("GOOG", GoogShares)

        #while datetime.datetime.now().hour is not 14 and datetime.datetime.now().minute < 55:
        while True:




            #print "party"
            ExTime = getTime()

            #If we already have a stock
            if CurStock != 'None!':

                price1 = {}
                price2 = {}

                L = 0

                inv = {}
                #print "test1"
                #print stocks[CurStock]
                #print stocks.get(CurStock)
                for inv in stocks[CurStock].iteritems():
                    print inv
                    if price1 == {}:
                        price1 = inv
                    else:
                        price2 = inv
                print "price 1 and 2"
                print price1
                print price2

                if price2.keys() > price1.keys():
                    L = math.sqrt((price2.keys() - price1.keys())**2 + (price2[price2.keys()] - price1[price1.keys()])**2)
                else:
                    L = math.sqrt((price1.keys() - price2.keys())**2 + (price1[price1.keys()] - price2[price2.keys()])**2)

                if L < 0:
                    my_game.sell(CurStock, CurShares)

                    BiggestGainName = CurStock

                    CurStockHook = Share(CurStock)

                    FinalBuy = 0

                    shareAmount = int(math.floor(my_game.value - 3000.0 ) / get_stock_quote(CurStock)   )

                    CurShare = shareAmount

                    BiggestGainShares = CurShares

                    if (int(CurStockHook.get_avg_daily_volume())) / 10 < shareAmount:

                        MaxVol = ((int(CurStockHook.get_avg_daily_volume()) / 10 )-10 )

                        toBuy = shareAmount / MaxVol

                        if not toBuy % 0:
                            left = shareAmount / CurStockHook.get_avg_daily_volume() % 10
                            toBuy = toBuy - left
                            FinalBuy = math.floor(shareAmount / (1/left))

                        for x in range(1, toBuy):
                            my_game.buy(CurStock, MaxVol )

                        my_game.buy(CurStock, FinalBuy )
                        print "Bought "+CurStock+" \n"

                    else:
                        my_game.buy(CurStock, shareAmount )
                        print "Bought "+CurStock+" \n"

            #We don't have a stock we are currently trading.


            elif BiggestGainName != 'None!':
                print "now we here"
                #print BiggestGainName
                CurStock = BiggestGainName


                CurStockHook = Share(CurStock)

                #FinalBuy = 0

                shareAmount = int(math.floor(my_game.value - 3000.0 ) / get_stock_quote(CurStock)  )

                #print shareAmount,
                #print " the shares"

                BiggestGainShares = shareAmount
                CurShares = BiggestGainShares
                #print "sh "
                #print shareAmount

                #print "v"
                #print ystockquote.get_volume(CurStock)

                if (int(CurStockHook.get_avg_daily_volume()) / 100) <= shareAmount:

                    MaxVol = int( int(int(CurStockHook.get_avg_daily_volume()) / 100)-10 )

                    toBuy = int(math.floor(shareAmount / MaxVol))

                    FinalBuy = 0

                    if shareAmount % MaxVol != 0:
                        left = shareAmount % MaxVol
                       # toBuy = toBuy - left
                       # FinalBuy = math.floor(shareAmount / (1/left))

                    for x in range(1, toBuy):
                        my_game.buy(CurStock, MaxVol )
                    #print "finalbuy",
                    #print FinalBuy

                    if FinalBuy != 0:
                        my_game.buy(CurStock, FinalBuy )
                    print "Bought "+CurStock+" \n"

                else:
                    my_game.buy(CurStock, shareAmount )
                    #print "wow"+CurStock+"wow"
                    #print CurStock,
                    print "Bought "+CurStock+" \n"

                    #print "test\n",

                    # my_game.buy(CurStock, shareAmount )

            else:
                print "Waiting for warmer weather :/"

            if getTime() - ExTime < 60:
                time.sleep(60 - (getTime() - ExTime))
            else:
                print "[Warning]: Running behind in Current Stock!"


        my_game.sell(CurStock, CurShares)

        shareAmount = int(math.floor(my_game.value - 3000.0 ) / float(Share("GOOG").get_price())  )
        my_game.buy("GOOG", shareAmount )

        GoogShares = shareAmount
        pause.until(PostMarketWait())




def get_quote(symbol):


    while True:
        #while datetime.datetime.now().hour != 14 and datetime.datetime.now().minute < 55:
        while True:
           # print "tracking now!"
            thetime = getTime()
            #price = Share(symbol).get_price()

            price = get_stock_quote(symbol)
            #print price
            oldestPrice = 0

            for oldPrice in stocks[symbol].keys():
                if len(stocks[symbol].keys()) < 2:
                    break

                if oldestPrice == 0:
                    oldestPrice = oldPrice

                if oldPrice < oldestPrice:
                    oldestPrice = oldPrice
            stocks[symbol].pop(oldestPrice, None)

            stime = str(thetime)
            stocks[symbol].update({thetime: price})

            time.sleep(60)


        stocks[symbol].clear()
        #while datetime.datetime.now() is not
        pause.until(PostMarketWait())





for key in stocks.keys():
    print key+" has started tracking."
    t = threading.Thread(target=get_quote, args = (key,))
    t.daemon = True
    t.start()


def MainThread():
    print "hi mike"
    global BiggestGainName
    global BiggestGainShares
    global BiggestGainPercent


    while True:
        #print "Main Start"
        CurrentStockStarted = False
        firstrun = True


        #main thread
        while True:
            #print "starting!"

            if firstrun == True:
                time.sleep(5)
                firstrun = False
            curtime = getTime()

            AStock = {}

            #AStock will return a tuple (stock {dict))
            for AStock in stocks.viewitems():
                #print "Astock"
                #print AStock
                xtime1 = 0
                xtime2 = 0

                yPrice1 = 0
                yPrice2 = 0


                gain = 0

                inv = {}

                stockvalues = AStock[1]

                for inv in stockvalues.iteritems():
                    #print "inv"
                    #print(inv)

                    if xtime1 == 0:
                        #print inv[1]
                        xtime1 = int(inv[0])
                        yPrice1 = float(inv[1])
                    else:
                        xtime2 = int(inv[0])
                        yPrice2 = float(inv[1])

                if xtime2 > xtime1:
                    gain = math.sqrt((xtime2 - xtime1)**2 + (yPrice2 - yPrice1)**2)
                else:
                    gain = math.sqrt((xtime1 - xtime2)**2 + (yPrice1 - yPrice2)**2)

                if gain > BiggestGainPercent:
                    BiggestGainPercent = gain
                    BiggestGainName = AStock[0]

            if getTime() - curtime < 62:
                time.sleep(62 - (getTime() - curtime))
            else:
                print "[Warning]: Running behind in updating stocks!"

            #print "starting?"
            if CurrentStockStarted == False:
                print "Starting the buyer"
                t = threading.Thread(target=CurrentStockTracker)
                t.daemon = True
                t.start()
                CurrentStockStarted = True

        pause.until(PostMarketWait())
        Start_Tracking_Stocks()

MainThread()

# old code, ignore
if __name__ == "__main__":
    username = "michaelhajostek@isd593.org"
    password = "Bantam22"

    my_session = pyvse2.VSESession()
    my_session.login(username, password)

    my_game = my_session.game("bendormanse")

    goog = pyvse2.Stock("GOOGL","NASDAQ:GOOGL", 1, "bendormanse")
    my_game.buy("DNDNQ", 22)
