import requests
import csv
import time
from . import write, symbols


def stock_time_series(symbol, func="TIME_SERIES_DAILY_ADJUSTED", outputsize="full",
                      datatype="json", api_key="ZQR7B11XFTLJECJU"):
    """
    :param symbol: name of the equity
    :param func: TIME_SERIES_INTRADAY, TIME_SERIES_DAILY_ADJUSTED, TIME_SERIES_WEEKLY_ADJUSTED, TIME_SERIES_MONTHLY_ADJUSTED
    :param outputsize: full, compact(previous 100 data points)
    :param datatype: json, csv
    :param api_key: Visit https://www.alphavantage.co/support/#api-key

    Refer to https://www.alphavantage.co/documentation/#
    """

    symbol = symbol.upper()
    data = {
        "function": func,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": outputsize,
        "datatype": datatype}

    if func == "TIME_SERIES_INTRADAY":
        data["interval"] = "1min"

    url = "https://www.alphavantage.co/query"
    data = requests.get(url, params=data)

    # Attempts to try again until success
    if datatype == "json":
        data = data.json()
        if "Information" in data.keys():
            time.sleep(10)
            stock_time_series(symbol, function, outputsize, datatype, api_key)
    else:
        reader = csv.reader(data.text.splitlines())
        for row in reader:
            if row[0] == "{":
                time.sleep(10)
                stock_time_series(symbol, function, outputsize, datatype, api_key)

    return data


def write_all(source, root_dir, start=0, function="TIME_SERIES_DAILY_ADJUSTED", api_key="ZQR7B11XFTLJECJU", datatype="json"):
    """
    :param source: nyse, nasdaq, amex
    :param start: starting index
    :param function: TIME_SERIES_INTRADAY, TIME_SERIES_DAILY_ADJUSTED, TIME_SERIES_WEEKLY_ADJUSTED, TIME_SERIES_MONTHLY_ADJUSTED
    :param api_key: Visit https://www.alphavantage.co/support/#api-key
    :param datatype: json, csv
    """

    directory = root_dir + "/lms/data/" + datatype + "/" + function + "/"
    outputsize = "full"
    counter = start
    for symbol in symbols.retrieve(source, root_dir, save=False)[start:]:
        if symbol.isalpha():
            time.sleep(5)
            data = stock_time_series(symbol, function, outputsize, datatype, api_key)
            write.json_file(directory, symbol, data) if datatype == "json" else write.csv_file(directory, symbol, data)
            time.sleep(5)
            print(counter, symbol, function, datatype)
        counter += 1

