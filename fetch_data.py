
url = {"nyse": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download",
        "nasdaq": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download",
        "amex": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download"}

import pandas as pd
def stock_list(url):
    '''returns a list of all avaiable stocks from given url'''
    df = pd.read_csv(url)
    stocks = df["Symbol"].tolist()
    return stocks


#Python wrapper --> https://github.com/RomelTorres/alpha_vantage


#https://www.alphavantage.co/documentation/#
import requests
import json
import pprint

def company_daily_adjusted(symbol, datatype="json", outputsize="full", api_key="ZQR7B11XFTLJECJU"):
    '''returns daily stock information in json format of given company'''

    symbol = symbol.upper()
    url = "https://www.alphavantage.co/query"

    function = "TIME_SERIES_DAILY_ADJUSTED"

    data = { "function": function, 
             "symbol": symbol, 
             "apikey": api_key,
             "outputsize": outputsize,
             "datatype": datatype}

    data = requests.get(url, params = data)
    return data if datatype == "csv" else data.json()



import csv

def write_csv(symbol, csv_data):
    '''creates csv file'''
    
    directory = "csv_2018_07_04/"
    with open(directory + symbol + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        reader = csv.reader(csv_data.text.splitlines())

        for row in reader:
            writer.writerow(row)



import json, codecs

def write_json(symbol, json_data):
    '''creates json file'''

    directory = "json_2018_07_04/"
    with open(directory + symbol + '.json', 'w') as f:
        json.dump(json_data, f)


import time

def pull_data(name, start=0, api_key="ZQR7B11XFTLJECJU"):
    counter = start
    for symbol in stock_list(url[name])[start:]:
        if '^' not in symbol:
            time.sleep(10)
            write_csv(symbol, company_daily_adjusted(symbol, "csv", api_key=api_key))
            time.sleep(10)
            write_json(symbol, company_daily_adjusted(symbol, "json", api_key=api_key))
            print(counter, symbol)
        counter += 1


if __name__ == "__main__":
    pass
    
    
    

        

        
