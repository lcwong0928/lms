from fetch import *
import json
import pandas as pd


def load_json(symbol):
    """loads json file associated with symbol"""
    symbol = symbol.upper()
    directory = "json_2018_07_04/"

    try:
        with open(directory + symbol + ".json") as f:
            jdata = json.load(f)
            return jdata

    except FileNotFoundError:
        jdata = company_daily_adjusted(symbol)
        write_json(symbol, jdata)
        return jdata


def dataframe(jdata):
    """Converts json to dataframe format"""

    try:
        df = pd.DataFrame(jdata['Time Series (Daily)']).transpose().astype(float).iloc[::-1]
        df["Date"] = pd.to_datetime(df.index)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted close',
                      'Volume', 'Dividend amount', 'Split coefficient', 'Date']

        df = df.set_index('Date')
        return df

    except KeyError:
        print("Data is corrupted or not found.")


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


if __name__ == "__main__":
    pass
