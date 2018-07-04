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
    return pprint.pprint(page.json())


company_daily("AAPL")

