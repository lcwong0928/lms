import argparse
import datetime
import sys
from visualize import *
from ma import *

# https://linuxconfig.org/how-to-use-argparse-to-parse-python-scripts-parameters#h4-conventions
class Lms(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Welcome to the lms help menu.',
            usage='''lms <mode> <func>
            The most commonly used git commands are:
                display    Analyze data with our provided tools
                pull       Download data from other sources
                
            © Copyright LMS., Inc., 2018. All rights reserved.''')

        parser.add_argument('mode', help='display, pull')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.mode):
            parser.print_help()
            exit(1)
        getattr(self, args.mode)()

    def display(self):
        parser = argparse.ArgumentParser(
            description='display data given various methods')
        parser.add_argument('func', help="df, simple, candlestick, ma, model, ribbon")
        args = parser.parse_args(sys.argv[2:3])

        if not hasattr(self, "display_" + args.func):
            parser.print_help()
            exit(1)
        getattr(self, "display_" + args.func)()

    def display_df(self):
        parser = argparse.ArgumentParser(
            description=' raw data representation of provided symbol')
        parser.add_argument('symbol', help="symbol of desired stock")
        parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
        parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
                            help="end date formatted as YYYY-MM-DD")

        args = parser.parse_args(sys.argv[3:])

        if args.start is not None:
            try:
                print(dataframe(load_json(args.symbol))[args.start:args.end])
            except KeyError:
                print("Invalid date time format.")
        else:
            print(dataframe(load_json(args.symbol)))

    def display_simple(self):
        parser = argparse.ArgumentParser(
            description='simple line chart representation of provided symbol')
        parser.add_argument('symbol', help="symbol of desired stock")
        parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
        parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
                            help="end date formatted as YYYY-MM-DD")

        args = parser.parse_args(sys.argv[3:])

        if args.start is not None:
            try:
                simple_linechart(args.symbol, args.start, args.end, block=True)
            except KeyError:
                print("Invalid date time format.")
        else:
            simple_linechart(args.symbol, block=True)

    def display_candlestick(self):
        parser = argparse.ArgumentParser(
            description='Japanese candlestick plot of provided symbol')
        parser.add_argument('symbol', help="symbol of desired stock")
        parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
        parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
                            help="end date formatted as YYYY-MM-DD")

        args = parser.parse_args(sys.argv[3:])

        if args.start is not None:
            try:
                candlestick(args.symbol, args.start, args.end, block=True)
            except KeyError:
                print("Invalid date time format.")
        else:
            candlestick(args.symbol, block=True)

    def display_ribbon(self):
        parser = argparse.ArgumentParser(
            description='moving average ribbon of provided symbol')
        parser.add_argument('symbol', help="symbol of desired stock")
        parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
        parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
                            help="end date formatted as YYYY-MM-DD")

        args = parser.parse_args(sys.argv[3:])

        ma = [i for i in range(10, 210, 10)]
        if args.start is not None:
            try:
                moving_averages_adv(args.symbol, ma, args.start, args.end, block=True)
            except KeyError:
                print("Invalid date time format.")
        else:
            moving_averages_adv(args.symbol, ma, block=True)

    def display_ma(self):
        parser = argparse.ArgumentParser(
            description='Japanese candlestick plot of provided symbol with moving average 20d, 50d, 200d')
        parser.add_argument('symbol', help="symbol of desired stock")
        parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
        parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
                            help="end date formatted as YYYY-MM-DD")

        args = parser.parse_args(sys.argv[3:])

        if args.start is not None:
            try:
                moving_averages(args.symbol, args.start, args.end, block=True)
            except KeyError:
                print("Invalid date time format.")
        else:
            moving_averages(args.symbol, block=True)

    def display_model(self):
        parser = argparse.ArgumentParser(
            description='various plot of provided symbol')
        parser.add_argument('type', help="return, growth, increase, change")
        parser.add_argument('-l', '--list', nargs='+', type=str, help='-l sym sym sym', required=True)
        parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
        parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
                            help="end date formatted as YYYY-MM-DD")

        args = parser.parse_args(sys.argv[3:])

        if args.start is not None:
            try:
                graph_model(args.list, args.type, args.start, args.end, block=True)
            except KeyError:
                print("Invalid date time format.")
        else:
            graph_model(args.list, args.type, block=True)

    def pull(self):
        parser = argparse.ArgumentParser(
            description='download data from other sources')
        parser.add_argument('func', help="list, stock, all")
        args = parser.parse_args(sys.argv[2:3])

        if not hasattr(self, "pull_" + args.func):
            parser.print_help()
            exit(1)
        getattr(self, "pull_" + args.func)()

    def pull_list(self):
        parser = argparse.ArgumentParser(description='returns a list of currently available stocks')
        parser.add_argument('-s', '--source', help="nyse, nasdaq, amex", type=str, default="nyse")
        parser.add_argument('-sv', '--save', action='store_const', default=False, const=True,
                            help="saves list of stocks")
        parser.add_argument('-l', '--length', action='store_const', default=False, const=True,
                            help="display number of stocks")
        args = parser.parse_args(sys.argv[3:])

        result = stocks(url_dict[args.source])
        print("\n".join([", ".join(result[i:i + 10]) for i in range(0, len(result), 10)]))
        if args.length:
            print(len(result))
        if args.save:
            write_json("stocks", result)
            print("Saved stocks as json file.")

    def pull_all(self):
        parser = argparse.ArgumentParser(
            description='attempts to pull in all stock information')
        parser.add_argument('start', type=int, help="0th index")
        parser.add_argument('-s', '--source', help="nyse, nasdaq, amex", type=str, default="nasdaq")
        parser.add_argument('-f', '--func', help="refer to alpha vantage", type=str,
                            default="TIME_SERIES_DAILY_ADJUSTED")
        parser.add_argument('-k', '--key', help="api key", type=str, default="ZQR7B11XFTLJECJU")
        parser.add_argument('-c', '--csv', action='store_const', default=False, const=True,
                            help="option to also save as csv")
        args = parser.parse_args(sys.argv[3:])

        pull(args.source, args.start, args.key, args.func, args.csv)

    def pull_stock(self):
        parser = argparse.ArgumentParser(
            description='saves stock data given a symbol')
        parser.add_argument('symbol', help="symbol of desired stock")
        parser.add_argument('-c', '--compact', action='store_const', default=False, const=True,
                            help="data of the previous 100 days")
        parser.add_argument('-f', '--func', help="refer to alpha vantage", type=str,
                            default="TIME_SERIES_DAILY_ADJUSTED")
        parser.add_argument('-k', '--key', help="api key", type=str, default="ZQR7B11XFTLJECJU")
        args = parser.parse_args(sys.argv[3:])

        try:
            if args.compact:
                write_json(args.symbol, company_daily_adjusted(
                    args.symbol, outputsize="compact", func=args.func, api_key=args.key))
                write_csv(args.symbol, company_daily_adjusted(
                    args.symbol, "csv", outputsize="compact", func=args.func, api_key=args.key))
            else:
                write_json(args.symbol, company_daily_adjusted(
                    args.symbol, func=args.func, api_key=args.key))
                write_csv(args.symbol, company_daily_adjusted(
                    args.symbol, "csv", func=args.func, api_key=args.key))
            print("Saved as json and csv files.")

        except NameError:
            print(args.symbol + " is not in the Alpha Vantage Database")


if __name__ == '__main__':
    Lms()
