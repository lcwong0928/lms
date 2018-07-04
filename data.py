url_nyse = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"
url_nasdaq = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download"
url_amex = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download"

import pandas as pd
def stock_list(url):
    '''returns a list of all avaiable stocks from given url'''
    df = pd.DataFrame.from_csv(url)
    stocks = df.index.tolist()
    return stocks



#https://www.alphavantage.co/documentation/#

import requests
import json
import pprint

def company_daily(symbol):
    '''returns daily stock information in json format of given company'''
    
    url = "https://www.alphavantage.co/query"

    function = "TIME_SERIES_DAILY"
    symbol = "MSFT"
    api_key = "ZQR7B11XFTLJECJU"

    data = { "function": function, 
             "symbol": symbol, 
             "apikey": api_key } 
    page = requests.get(url, params = data)
    #pprint.pprint(page.json())
    return page.json()




import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def json_to_dataframe(data):
    '''Converts json to dataframe format'''
    jdata = json.loads(json.dumps(data))
    df = pd.DataFrame(jdata).transpose().astype(float)
    df["Date"] = pd.to_datetime(df.index)
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date']

    return df.set_index('Date')



def simple_linechart(symbol, df):
    '''produces line chart from given dataframe for symbol'''

    ax = df.plot(y=df.columns[0:4], title ="Time Series Daily for " + symbol, figsize=(15, 9), legend=True, fontsize=12, grid=True)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Dollars($)", fontsize=12)   
    plt.show(block=False)



from pandas_candlestick_ohlc import *

def candlestick(df):
    '''produces a candlestick of the given dataframe'''
    pandas_candlestick_ohlc(df)


def testcase():    
    symbol = "AAPL"
    data = company_daily(symbol)['Time Series (Daily)']
    df = json_to_dataframe(data)
    simple_linechart(symbol, df)
    candlestick(df)

testcase()

