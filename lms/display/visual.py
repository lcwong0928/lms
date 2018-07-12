from . import parse, candlestick
from ..backtest import ma
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def nearest(items, pivot):
    """used to serach for items in any collection"""
    return min(items, key=lambda x: abs(x - pivot))


def clip(df, start, end):
    """clips the data frame to provided range"""
    return df[start:end] if (start, end) != (None, None) else df


def simple_linechart(symbol, root_dir, func, start=None, end=None, save=False):
    """produces line chart of symbol from given start and end"""

    load_dir = root_dir + "/lms/data/json/" + func + "/"
    json_data = parse.load_json(symbol, load_dir, func)
    df, metadata = clip(parse.dataframe(json_data, func), start, end), json_data["Meta Data"]

    title = metadata['1. Information'] + " for " + metadata["2. Symbol"] + " as of " + metadata['3. Last Refreshed']
    ax = df.plot(y=df.columns[0:4], title=title, figsize=(10, 7), grid=True)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Dollars($)", fontsize=12)

    if save:
        save_dir = root_dir + "/lms/data/graphs/simple_linechart/" + func + "/"
        plt.savefig(save_dir + symbol + ".png", dpi=100)


def candlesticks(symbol, root_dir, func, start=None, end=None, save=False):
    """produces a candlestick of the given symbol and time frame"""

    load_dir = root_dir + "/lms/data/json/" + func + "/"
    json_data = parse.load_json(symbol, load_dir, func)
    df = clip(parse.dataframe(json_data, func), start, end)
    candlestick.pandas_candlestick_ohlc(df, symbol=symbol)

    if save:
        save_dir = root_dir + "/lms/data/graphs/candlestick/" + func + "/"
        plt.savefig(save_dir + symbol + ".png", dpi=100)


def graph_model(method, symbols, root_dir, func, start=None, end=None, save=False):
    "various models of the given data"

    load_dir = root_dir + "/lms/data/json/" + func + "/"
    data = [clip(parse.dataframe(parse.load_json(
        symbol, load_dir, func), func), start, end)["Adjusted close"] for symbol in symbols]

    df = pd.concat(data, axis=1)
    df = df.dropna()
    df.columns = symbols
    stock_return = df.apply(models[method])

    ax = stock_return.plot(figsize=(10, 7), fontsize=12, grid=True)
    ax.set_xlabel("Date", fontsize=12)
    start = str(df.index[0])

    if func == "return":
        plt.title("Percentage Return starting from " + start)
        ax.set_ylabel("Percentage Return", fontsize=12)
        ax.axhline(y=1, color="black", lw=1)

    elif func == "growth":
        plt.title("Growth starting from " + start)
        ax.set_ylabel("Growth per day", fontsize=12)
        ax.axhline(y=0, color="black", lw=1)

    elif func == "increase":
        plt.title("Increase starting from " + start)
        ax.set_ylabel("Increase per day", fontsize=12)
        ax.axhline(y=0, color="black", lw=1)

    elif func == "change":
        plt.title("Log Change starting from " + start)
        ax.set_ylabel("Change per day", fontsize=12)
        ax.axhline(y=0, color="black", lw=1)

    if save:
        save_dir = root_dir + "/lms/data/graphs/model/" + method + "/" + func + "/"
        plt.savefig(save_dir + str(symbols) + ".png", dpi=100)


def p_return(x):
    """return_t,0 = price_t / price_0"""
    # stock’s return since the beginning of the period of interest

    return x / x[0]


def growth(x):
    """growth_t = (price_t+1 - price_t) / price_t"""
    # Change of each stock per day.

    price = x.copy()
    price[0] = 0
    for t in range(len(x) - 1):
        price[t + 1] = (x[t + 1] - x[t]) / x[t]
    return price


def increase(x):
    """increase_t = (price_t - price_t-1) / price_t"""

    price = x.copy()
    price[0] = 0
    for t in range(1, len(x)):
        price[t] = (x[t] - x[t - 1]) / x[t]
    return price


def change(x):
    """change_t = log(price_t) - log(price_t-1)"""
    # growth of a stock: with log differences

    return np.log(x) - np.log(x.shift(1))


models = {"return": p_return,
          "growth": growth,
          "increase": increase,
          "change": change}


def moving_averages(symbol, moving_averages, root_dir, func, start=None, end=None, save=False):
    """Graphical representation of desired moving averages
    :param symbol string of the company symbol
    :param ma int or list[int] of moving averages
    :param start, end string of date in YEAR-MN-DY format
    :return candlestick representation of the data"""

    load_dir = root_dir + "/lms/data/json/" + func + "/"
    stock = ma.ohlc_adj(parse.dataframe(parse.load_json(symbol, load_dir, func), func))
    otherseries = []
    for num in list(moving_averages):
        day = str(num) + "d"
        otherseries.append(day)
        stock[day] = np.round(stock["Close"].rolling(window=num, center=False).mean(), 2)

    candlestick.pandas_candlestick_ohlc(stock.loc[start:end, :], otherseries=otherseries, symbol=symbol)

    if save:
        save_dir = root_dir + "/lms/data/graphs/moving_averages/" + func + "/"
        plt.savefig(save_dir + symbol + ".png", dpi=100)

