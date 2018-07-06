from json_parser import *


import matplotlib.pyplot as plt

def simple_linechart(symbol, start=None, end=None, block=False):
    '''produces line chart of symbol from given start and end'''
    
    json = load_json(symbol)
    df, metadata = dataframe(json), json["Meta Data"]
    if start != None and end != None:
        df = frame(df, start, end)

    title = metadata['1. Information'] + " for " + metadata["2. Symbol"] + " as of " + metadata['3. Last Refreshed']
    
    ax = df.plot(y=df.columns[0:4], title=title, figsize=(8, 5), grid=True)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Dollars($)", fontsize=12)   
    plt.show(block=block)



from pandas_candlestick_ohlc import *

def candlestick(symbol, start=None, end=None, block=False):
    '''produces a candlestick of the given symbol and timeframe'''
    df = dataframe(load_json(symbol))
    if start != None and end != None:
        df = frame(df, start, end)
    pandas_candlestick_ohlc(df, block=block)


def graph_model(symbols, func, ref=None, goal=None, block=False):
    if not isinstance(symbols, list): symbols = [symbols]
    
    if (ref, goal) == (None, None):
        data = [dataframe(load_json(symbol))["Adjusted close"].iloc[::-1] for symbol in symbols]
    else:
        data = [dataframe(load_json(symbol))["Adjusted close"][ref:goal].iloc[::-1] for symbol in symbols]
    
    df = pd.concat(data, axis=1)
    df.columns = symbols
    df = df.dropna()
    stock_return = df.apply(models[func])
    
    ax = stock_return.plot(figsize=(7, 4), fontsize=12, grid=True)
    ax.set_xlabel("Date", fontsize=12)


    if func == "return":
        ax.set_ylabel("Percentage Return", fontsize=12)
        ax.axhline(y = 1, color = "black", lw = 1)
        
    elif func == "growth":
        ax.set_ylabel("Growth per day", fontsize=12)
        ax.axhline(y = 0, color = "black", lw = 1)

    elif func == "change":
        ax.set_ylabel("Change per day", fontsize=12)
        ax.axhline(y = 0, color = "black", lw = 1)
    
    plt.show(block=block)



def p_return(x):
    '''return_t,0 = price_t / price_0'''
    #stock’s return since the beginning of the period of interest
    
    return x / x[0]
    

def growth(x):
    '''growth_t = (price_t+1 - price_t) / price_t'''
    #Change of each stock per day.
    price = x.copy()
    price[0] = 0
    for t in range(len(x)-1):
        price[t+1] = (x[t+1] - x[t]) / x[t]
    return price


def increase(x):
    '''increase_t = (price_t - price_t-1) / price_t'''
 
    price = x.copy()
    price[0] = 0
    for t in range(1,len(x)):
        price[t] = (x[t] - x[t-1]) / x[t]
    return price


import numpy as np
def change(x):
    '''change_t = log(price_t) - log(price_t-1)'''
    #growth of a stock: with log differences
    
    return np.log(x) - np.log(x.shift(1))

    
models = {"return": p_return,
          "growth": growth,
          "increase": increase,
          "change": change}


def moving_averages(symbol, start=None, end=None, block=False):
    stock = dataframe(load_json(symbol))
    
    stock["20d"] = np.round(stock["Close"].iloc[::-1].rolling(window = 20, center = False).mean(), 2)
    stock["50d"] = np.round(stock["Close"].iloc[::-1].rolling(window = 50, center = False).mean(), 2)
    stock["200d"] = np.round(stock["Close"].iloc[::-1].rolling(window = 200, center = False).mean(), 2)
    
    pandas_candlestick_ohlc(stock.loc[start:end,:], otherseries = ["20d", "50d", "200d"], block = block)
    


def package(symbol, start=None, end=None):
    graph_model(symbol, "return", start, end)
    graph_model(symbol, "change", start, end)
    moving_averages(symbol[0], start, end)


    
import sys

if __name__ == "__main__":

    #simple_linechart(symbol, "2018-07-03", "2018-01-03")
    #candlestick(symbol, "2018-07-03", "2018-01-03")
    #graph_model(["Y", "ARE", "DDD"], "return", "2018-07-03", "2018-01-03")
    #graph_model(["Y", "ARE", "DDD"], "growth", "2018-07-03", "2018-01-03")
    #graph_model(["Y", "ARE", "DDD"], "increase", "2018-07-03", "2018-01-03")
    #graph_model(["Y", "ARE", "DDD"], "change", "2018-07-03", "2018-01-03")
    #moving_averages(symbol, '2016-08-07', '2016-01-04')

    pass
