import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def json_to_dataframe(data):
    '''Converts json to dataframe format'''
    jdata = json.loads(json.dumps(data))
    df = pd.DataFrame(jdata).transpose().astype(float)
    df["Date"] = pd.to_datetime(df.index)
    df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted close',
                  'Volume', 'Dividend amount', 'Split coefficient', 'Date']

    return df.set_index('Date')



def simple_linechart(symbol, df):
    '''produces line chart from given dataframe for symbol'''

    ax = df.plot(y=df.columns[0:4], title ="Time Series Daily for " + symbol, figsize=(15, 9), legend=True, fontsize=12, grid=True)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Dollars($)", fontsize=12)   
    plt.show(block=False)



from pandas_candlestick_ohlc import *

def candlestick(df):
    '''produces a candlestick of the given dataframe'''
    pandas_candlestick_ohlc(df)



from fetch_data import *

def testcase():    
    symbol = "AAPL"
    datatype = "json"
    data = company_daily_adjusted(symbol, "json", "compact")['Time Series (Daily)']
    df = json_to_dataframe(data)
    simple_linechart(symbol, df)
    candlestick(df)

testcase()

