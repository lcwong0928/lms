import json
def load_json(symbol):
    '''loads json file associated with symbol'''
    sym_upper = symbol.upper()
    directory = "json_2018_07_04/"
    
    try:
        with open(directory + sym_upper + ".json") as f:
            jdata = json.load(f)
            return jdata
        
    except FileNotFoundError:
        print(symbol + " does not exist in database.")
        return False
    



import pandas as pd

def json_to_dataframe(jdata):
    '''Converts json to dataframe format and retrieves metadata'''

    df = pd.DataFrame(jdata['Time Series (Daily)']).transpose().astype(float)
    df["Date"] = pd.to_datetime(df.index)
    df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted close',
                  'Volume', 'Dividend amount', 'Split coefficient', 'Date']
    
    df = df.set_index('Date')
    return df



def json_to_metadata(jdata):
    '''retrives relevant informiration about the symbol'''
    
    metadata = jdata["Meta Data"]
    return metadata



def symbol_data(symbol, metadata=True, start=None, end=None):
    '''start, end formated as YEAR-MONTH_DAY'''
    
    jdata = load_json(symbol)
    if jdata != False:
        
        df = json_to_dataframe(jdata)
        if start != None and end != None:
            df = df[start:end]

        metadata = json_to_metadata(jdata)
        return df, metadata if metadata else df
    


if __name__ == "__main__":
    symbol = "FCX"
    #print(symbol_data(symbol))
