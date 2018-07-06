from fetch_data import *
import json
def load_json(symbol):
    '''loads json file associated with symbol'''
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



import pandas as pd

def dataframe(jdata):
    '''Converts json to dataframe format'''
    
    try:
        df = pd.DataFrame(jdata['Time Series (Daily)']).transpose().astype(float)
        df["Date"] = pd.to_datetime(df.index)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted close',
                      'Volume', 'Dividend amount', 'Split coefficient', 'Date']
    
        df = df.set_index('Date')
        return df
    
    except KeyError:
        print("Data is corrupted or not found.")



def nearest(items, pivot):
      return min(items, key=lambda x: abs(x - pivot))



def frame(df, start, end):
    '''returns the data frame with the nearest given start and end'''
    return df[start:end]

if __name__ == "__main__":
    pass
