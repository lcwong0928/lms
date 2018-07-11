import pandas as pd
import requests
import csv
import json
import time

url_dict = {
    "nyse": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download",
    "nasdaq": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download",
    "amex": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download"}


def stocks(url):
    """returns a list of all available stocks from given url"""
    df = pd.read_csv(url)
    stock = df["Symbol"].tolist()
    return stock


# Python wrapper --> https://github.com/RomelTorres/alpha_vantage
# https://www.alphavantage.co/documentation/#


def company_daily_adjusted(symbol, datatype="json", outputsize="full",
                           api_key="ZQR7B11XFTLJECJU", func="TIME_SERIES_DAILY_ADJUSTED"):
    """returns daily stock information in json format of given company"""

    symbol = symbol.upper()
    url = "https://www.alphavantage.co/query"

    data = {
        "function": func,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": outputsize,
        "datatype": datatype}

    data = requests.get(url, params=data)

    if datatype == "json":
        data = data.json()
        if "Information" in data.keys():
            time.sleep(10)
            company_daily_adjusted(symbol, datatype, outputsize, api_key)
    else:
        reader = csv.reader(data.text.splitlines())
        for row in reader:
            if row[0] == "{":
                time.sleep(5)
                company_daily_adjusted(symbol, datatype, outputsize, api_key)

    return data


def write_csv(symbol, csv_data):
    """creates csv file"""

    directory = "csv_2018_07_04/"
    with open(directory + symbol + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        reader = csv.reader(csv_data.text.splitlines())
        for row in reader:
            writer.writerow(row)


def write_json(symbol, json_data):
    """creates json file"""

    directory = "json_2018_07_04/"
    with open(directory + symbol + '.json', 'w') as f:
        json.dump(json_data, f)


def pull(name, start=0, api_key="ZQR7B11XFTLJECJU", func="TIME_SERIES_DAILY_ADJUSTED", c=False):
    counter = start
    for symbol in stocks(url_dict[name])[start:]:
        if symbol.isalpha():
            time.sleep(5)
            write_json(symbol, company_daily_adjusted(symbol, "json", api_key=api_key, func=func))
            time.sleep(5)
            if c:
                write_csv(symbol, company_daily_adjusted(symbol, "csv", api_key=api_key, func=func))
            print(counter, symbol)
        counter += 1


if __name__ == "__main__":
    pull("nasdaq")
