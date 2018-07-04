import requests
import json
import pprint

url = "https://www.alphavantage.co/query"

function = "TIME_SERIES_DAILY"
symbol = "MSFT"
api_key = "ZQR7B11XFTLJECJU"

data = { "function": function, 
         "symbol": symbol, 
         "apikey": api_key } 
page = requests.get(url, params = data)
pprint.pprint(page.json())
