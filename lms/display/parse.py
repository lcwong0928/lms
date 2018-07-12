from ..pull import write, data
import json
import pandas as pd


def load_json(symbol, directory, func):
    """loads symbol.json file from given directory"""

    symbol = symbol.upper()
    try:
        with open(directory + symbol + ".json") as f:
            json_data = json.load(f)
            return json_data

    except FileNotFoundError:
        json_data = data.stock_time_series(symbol, func=func)
        write.json_file(directory, symbol, json_data)
        return json_data


key_to_index = {"TIME_SERIES_INTRADAY": "Time Series (1min)",
                "TIME_SERIES_DAILY_ADJUSTED": "Time Series (Daily)",
                "TIME_SERIES_WEEKLY_ADJUSTED": "Weekly Adjusted Time Series",
                "TIME_SERIES_MONTHLY_ADJUSTED": "Monthly Adjusted Time Series"}


def dataframe(json_data, key):
    """Converts json file to dataframe format"""

    try:
        df = pd.DataFrame(json_data[key_to_index[key]]).transpose().astype(float).iloc[::-1]
        df["Date"] = pd.to_datetime(df.index)

        if key == "TIME_SERIES_INTRADAY":
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date']
        elif key == "TIME_SERIES_DAILY_ADJUSTED":
            df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted close',
                          'Volume', 'Dividend amount', 'Split coefficient', 'Date']
        elif key == "TIME_SERIES_WEEKLY_ADJUSTED":
            df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted close',
                          'Volume', 'Dividend amount', 'Date']
        elif key == "TIME_SERIES_MONTHLY_ADJUSTED":
            df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted close',
                          'Volume', 'Dividend amount', 'Date']
        df = df.set_index('Date')
        return df

    except KeyError:
        print("Data is corrupted or not found.")
