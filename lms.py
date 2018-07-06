import argparse
import sys
from fetch_data import *
from json_parser import *
from visualize import *

#https://linuxconfig.org/how-to-use-argparse-to-parse-python-scripts-parameters#h4-conventions




class Lms(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Welcome to the wakarimasen help menu.',
            
            usage='''lms <command> [<args>]
            The most commonly used git commands are:
                display    Analyze data with our provided tools
                pull       Download data from other sources
                
            © Copyright LMS., Inc., 2018. All rights reserved.''')

        parser.add_argument('command', help='display, pull')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    def display(self):
        parser = argparse.ArgumentParser(
            description='display')
        
        parser.add_argument('func', help="df, simple, candlestick, movingaverage, model, package")
        args = parser.parse_args(sys.argv[2:3])

        if args.func in ["df", "simple", "candlestick", "movingaverage"]:
            parser = argparse.ArgumentParser(
                description= args.func + ' representation of given symbol')
            parser.add_argument('symbol', help="symbol of desired stock")
            parser.add_argument('-f', '--frame', default=None, help="YYYY-MM-DD:YYYY-MM-DD")
            
            args2 = parser.parse_args(sys.argv[3:])

            if args.func == "df":
                if args2.frame != None:
                    start, end = args2.frame.split(":")[0], args2.frame.split(":")[1]
                    try: print(dataframe(load_json(args2.symbol))[start:end])
                    except KeyError: print("Invalid time frame format.")
                else: print(dataframe(load_json(args2.symbol)))
                
            elif args.func == "simple":
                if args2.frame != None:
                    start, end = args2.frame.split(":")[0], args2.frame.split(":")[1]
                    try: simple_linechart(args2.symbol, start, end, block=True)
                    except KeyError: print("Invalid time frame format.")
                else: simple_linechart(args2.symbol, block=True)
                
            elif args.func == "candlestick":
                if args2.frame != None:
                    start, end = args2.frame.split(":")[0], args2.frame.split(":")[1]
                    try: candlestick(args2.symbol, start, end, block=True)
                    except KeyError: print("Invalid time frame format.")
                else: candlestick(args2.symbol, block=True)
                
            else:
                if args2.frame != None:
                    start, end = args2.frame.split(":")[0], args2.frame.split(":")[1]
                    try: moving_averages(args2.symbol, start, end, block=True)
                    except KeyError: print("Invalid time frame format.")
                else: moving_averages(args2.symbol, block=True)

        elif args.func == "models":
            parser = argparse.ArgumentParser(
                description= 'various representation of given symbol')
            parser.add_argument('type', help="return, growth, increase, change")
            parser.add_argument('-l','--list', nargs='+', type=str, help='-l sym sym sym', required=True)
            parser.add_argument('-f', '--frame', default=None, help="YYYY-MM-DD:YYYY-MM-DD")
            
            args = parser.parse_args(sys.argv[3:])
 
            if args.frame != None:
                start, end = args.frame.split(":")[0], args.frame.split(":")[1]
                try: graph_model(args.list, args.type, start, end, block=True)
                except KeyError: print("Invalid time frame format.")
            else: graph_model(args.list, args.type, block=True)               

    
    def pull(self):
        parser = argparse.ArgumentParser(
            description='download data from other sources')
        
        parser.add_argument('func', help="list, pull, all")
        args = parser.parse_args(sys.argv[2:3])

        if args.func == "list":
            parser = argparse.ArgumentParser(
                description='returns a list of currently avaiable stocks')
            parser.add_argument('-s', '--source', help="nyse, nasdaq, amex", type=str, default="nyse")
            args = parser.parse_args(sys.argv[3:])
        
            stocks = stock_list(url[args.source])
            print("\n".join([", ".join(stocks[i:i+10]) for i in range(0,len(stocks),10)]))

        elif args.func == "stock":
            parser = argparse.ArgumentParser(description='saves stock data given a symbol')
            parser.add_argument('symbol', help="symbol of desired stock")
            parser.add_argument('-c', '--compact', action='store_const', default=False, const=True, help="data of the previous 100 days")   
            args = parser.parse_args(sys.argv[3:])
            
            try:
                if args.compact:
                    write_json(args.symbol, company_daily_adjusted(args.symbol, outputsize="compact"))
                    write_csv(args.symbol, company_daily_adjusted(args.symbol, "csv", outputsize="compact"))
                else:
                    write_json(args.symbol, company_daily_adjusted(args.symbol))
                    write_csv(args.symbol, company_daily_adjusted(args.symbol, "csv"))
                print("Saved to json and csv files.")
                    
            except NameError:
                print(args.symbol + " is not in the Alpha Vantage Database")

        elif args.func == "all":
            parser = argparse.ArgumentParser(description='attempts to pull in all stock information')
            parser.add_argument('start', type=int, help="0th index")
            parser.add_argument('-s', '--source', help="nyse, nasdaq, amex", type=str, default="nyse")
            parser.add_argument('-k', '--key', help="api key", type=str, default="ZQR7B11XFTLJECJU")
            args = parser.parse_args(sys.argv[3:])
        
            pull_data(args.source, args.start, args.key)
            
                
if __name__ == '__main__':
    Lms()






    
            
            
            
