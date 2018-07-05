from json_parser import symbol_data



import matplotlib.pyplot as plt

def simple_linechart(symbol, start=None, end=None):
    '''produces line chart of symbol from given start and end'''
    df, metadata = symbol_data(symbol) if (not start and not end) else symbol_data(symbol, True, start, end)

    title = metadata['1. Information'] + " for " + metadata["2. Symbol"] + " as of " + metadata['3. Last Refreshed']
    
    ax = df.plot(y=df.columns[0:4], title=title, figsize=(15, 10), legend=True, fontsize=12, grid=True)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Dollars($)", fontsize=12)   
    plt.show(block=False)



from pandas_candlestick_ohlc import *

def candlestick(symbol, start=None, end=None):
    '''produces a candlestick of the given symbol and timeframe'''
    df, metadata = symbol_data(symbol) if (not start and not end) else symbol_data(symbol, True, start, end)
    pandas_candlestick_ohlc(df)


def multiple_adjusted_close(symbols):
    '''provides data for relative changes'''
    data = [symbol_data(symbol, False)["Adjusted close"] for symbol in symbols]
    df = pd.concat(data, axis=1)
    df.columns = symbols
    
    ax = df.plot(secondary_y=df.columns[0:2], figsize=(15, 10), legend=True, fontsize=12, grid=True)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Dollars($)", fontsize=12)
    plt.show(block=False)
    


if __name__ == "__main__":
    symbol = "FCX"
 
    #simple_linechart(symbol, "2018-07-03", "2018-01-03")
    #candlestick(symbol, "2018-07-03", "2018-01-03")
    multiple_adjusted_close(["FCX", "BEN", "FT"])
    
