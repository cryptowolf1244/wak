
import time
from  binance.client import Client
import pandas as pd
import numpy as np
import backtrader as bt
from binance.client import Client
import time
import os
from datetime import datetime
import matplotlib as mp

def get_historical_candles(client: Client, symbol, interval, start_time, end_time = None, market = "spot", alwaysUpdate = False):
    # - Get historical klines from binance
    # - Start and End times has to be in this format: 2022-03-12 00:00:00
    # - when alwaysUpdate is true, teh app will always try to get the most recent data 
    # But when it is false, the app first will try to get data from saved files. if 
    # there is no suitable data found, the app will catch the data from api. this helps 
    # app to run faster 
    # - Market can be spot or futures. The default if spot

    # Start the timer
    startTime = time.time()
    
    # First check to see if we have the data
    modulePath = os.path.dirname(os.path.abspath(__file__))

    # Make a "Datas" folder if there is none
    if(not os.path.exists(os.path.join(modulePath, "Datas"))):
        os.mkdir(os.path.join(modulePath, "Datas"))        

    fileName = modulePath + '/Datas/' + symbol + '_'+ market + '_' + interval + '_' + start_time + ("-" + end_time if end_time else "") + '.csv'
    
    if (not os.path.exists(fileName) or alwaysUpdate):
        print("Getting the calndles")
        intervals = {
            "12h": client.KLINE_INTERVAL_12HOUR,
            "15m": client.KLINE_INTERVAL_15MINUTE,
            "1D": client.KLINE_INTERVAL_1DAY,
            "1h": client.KLINE_INTERVAL_1HOUR,
            "1M": client.KLINE_INTERVAL_1MONTH,
            "1m": client.KLINE_INTERVAL_1MINUTE,
            "2h": client.KLINE_INTERVAL_2HOUR,
            "30m": client.KLINE_INTERVAL_30MINUTE,
            "3m": client.KLINE_INTERVAL_3MINUTE,
            "4h": client.KLINE_INTERVAL_4HOUR,
            "5m": client.KLINE_INTERVAL_5MINUTE,
            "6h": client.KLINE_INTERVAL_6HOUR,
            "8h": client.KLINE_INTERVAL_8HOUR,
            "1W": client.KLINE_INTERVAL_1WEEK,
        }

        # Check teh market
        if(market == "spot"):
            kline = client.get_historical_klines(symbol, intervals[interval], start_str= start_time, end_str=end_time)
        elif(market == "futures"):
            kline = client.futures_historical_klines(symbol, intervals[interval], start_str= start_time, end_str=end_time)

        
        # Creating a dataframe to fill with klines
        df = pd.DataFrame(kline).astype(str).astype(float)
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Vol', 'Close_time', 'Qav', 'Num_trades',
                      'Taker_base_vol', 'Taker_quote_vol', 'Ignore']
        df["Date"] = pd.to_datetime(df['Date'], unit="ms")
        df = df.drop(["Ignore", "Taker_quote_vol", "Taker_base_vol", "Num_trades", "Qav", "Close_time"], axis=1)

        # Save the df to a CSV file
        df.to_csv(fileName, index=False)
        
        endTime = time.time()
        print("{} candles loaded. Elapsede time: {}s\n".format(symbol ,round(endTime-startTime,3)))
    else:
        df = pd.read_csv(fileName)
        df["Date"] = pd.to_datetime(df['Date'])
        
        endTime = time.time()
        print("{} candles loaded. Elapsede time: {}s\n".format(symbol ,round(endTime-startTime,3)))

    return df