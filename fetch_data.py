
url = {"nyse": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download",
        "nasdaq": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download",
        "amex": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download"}

import pandas as pd
def stock_list(url):
    '''returns a list of all avaiable stocks from given url'''
    df = pd.read_csv(url)
    stocks = df["Symbol"].tolist()[10:]
    return stocks


#Python wrapper --> https://github.com/RomelTorres/alpha_vantage


#https://www.alphavantage.co/documentation/#
import requests
import json
import pprint

def company_daily_adjusted(symbol, datatype, outputsize="full"):
    '''returns daily stock information in json format of given company'''
    
    url = "https://www.alphavantage.co/query"

    function = "TIME_SERIES_DAILY_ADJUSTED"
    api_key = "ZQR7B11XFTLJECJU"

    data = { "function": function, 
             "symbol": symbol, 
             "apikey": api_key,
             "outputsize": outputsize,
             "datatype": datatype}
    
    data = requests.get(url, params = data)
    #pprint.pprint(data.json())
    return data if datatype == "csv" else data.json()



import csv

def write_csv(symbol, csv_data):
    '''creates csv file'''
    
    rep = "csv_2018_07_04/"
    with open(rep + symbol + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        reader = csv.reader(csv_data.text.splitlines())

        for row in reader:
            writer.writerow(row)



import json, codecs

def write_json(symbol, json_data):
    '''creates json file'''

    rep = "json_2018_07_04/"
    with open(rep + symbol + '.txt', 'w') as f:
        json.dump(json_data, f)


import time
def pull_data(name):
    counter = 0
    for symbol in stock_list(url[name]):
        write_csv(symbol, company_daily_adjusted(symbol, "csv"))
        write_json(symbol, company_daily_adjusted(symbol, "json"))
        time.sleep(15)
        counter += 1
        print(counter, symbol)



        

        
