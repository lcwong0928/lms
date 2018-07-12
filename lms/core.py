from .pull import data, symbols, write
import argparse
import datetime
import sys
import os

root_dir = os.getcwd()


# Refer to  https://linuxconfig.org/how-to-use-argparse-to-parse-python-scripts-parameters#h4-conventions

class Lms(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Welcome to the lms help menu.',
            usage='''lms <mode> <func>
            The most commonly used git commands are:
                pull       Download data from other sources
                display    Display data with our provided tools
                backtest   Back test on previous data using moving averages
                predict    Predict future stock prices 

            © Copyright LMS., Inc., 2018. All rights reserved.''')

        parser.add_argument('mode', help='display, pull')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.mode):
            parser.print_help()
            exit(1)
        getattr(self, args.mode)()

    def pull(self):
        parser = argparse.ArgumentParser(
            description='download data from other sources')
        parser.add_argument('func', help="symbols, data, all")
        args = parser.parse_args(sys.argv[2:3])

        if not hasattr(self, "pull_" + args.func):
            parser.print_help()
            exit(1)
        getattr(self, "pull_" + args.func)()

    def pull_symbols(self):
        parser = argparse.ArgumentParser(description='retrieves all currently available equities')
        parser.add_argument('-s', '--source', help="nyse, nasdaq, amex", type=str, default="nasdaq")
        parser.add_argument('-v', '--view', action='store_const',
                            default=False, const=True, help="view the symbols")
        parser.add_argument('-l', '--length', action='store_const', default=False, const=True,
                            help="display number of stocks")
        args = parser.parse_args(sys.argv[3:])

        result = symbols.retrieve(args.source, root_dir)
        print("Saved to " + root_dir + "\\data\\json\\symbols \n")

        if args.view:
            print("\n".join([", ".join(result[i:i + 10]) for i in range(0, len(result), 10)]))
        if args.length:
            print("\nThere are " + str(len(result)) + " available equities from " + args.source + ".")

    def pull_data(self):
        parser = argparse.ArgumentParser(
            description='saves stock data given symbol(s)')
        parser.add_argument('symbols', nargs='+', type=str, help="symbol(s) of desired equity")
        parser.add_argument('-f', '--func', help="refer to alpha vantage",
                            type=str, default="TIME_SERIES_DAILY_ADJUSTED")
        parser.add_argument('-d', '--datatype', help="csv, json",
                            type=str, default="json")
        parser.add_argument('-k', '--key', type=str,
                            default="ZQR7B11XFTLJECJU", help="Visit https://www.alphavantage.co/support/#api-key")
        parser.add_argument('-c', '--compact', action='store_const',
                            default=False, const=True, help="retrieve recent 100 data plots")
        args = parser.parse_args(sys.argv[3:])

        directory = root_dir + "/lms/data/" + args.datatype + "/" + args.func + "/"
        outputsize = "compact" if args.compact else "full"

        for symbol in args.symbols:
            symbol = symbol.upper()
            dat = data.stock_time_series(symbol, args.func, outputsize, args.datatype, args.key)
            write.json_file(directory, symbol, dat) if args.datatype == "json" else write.csv_file(directory, symbol, dat)

        print("Saved to " + root_dir + "\\lms\\data\\" + args.datatype + "\\" + args.func + "\n")

    def pull_all(self):
        parser = argparse.ArgumentParser(
            description='all stock data from a given source')
        parser.add_argument('-str', '--start', type=int, help="starting index, 0th indexed", default=0)
        parser.add_argument('-s', '--source', help="nyse, nasdaq, amex",
                            type=str, default="nasdaq")
        parser.add_argument('-f', '--function', help="refer to alpha vantage",
                            type=str, default="TIME_SERIES_DAILY_ADJUSTED")
        parser.add_argument('-k', '--key', type=str,
                            default="ZQR7B11XFTLJECJU", help="Visit https://www.alphavantage.co/support/#api-key")
        parser.add_argument('-c', '--csv', action='store_const', default=False, const=True, help="save as csv")
        args = parser.parse_args(sys.argv[3:])

        datatype = "csv" if args.csv else "json"
        data.write_all(args.source, root_dir, args.start, args.function, args.key, datatype)

    def display(self):
        parser = argparse.ArgumentParser(
            description='display data given various methods')
        parser.add_argument('func', help="df, simple, candlestick, ma, model, ribbon")
        args = parser.parse_args(sys.argv[2:3])

        if not hasattr(self, "display_" + args.func):
            parser.print_help()
            exit(1)
        getattr(self, "display_" + args.func)()

    # def display_df(self):
    #     parser = argparse.ArgumentParser(
    #         description=' raw data representation of provided symbol')
    #     parser.add_argument('symbol', help="symbol of desired stock")
    #     parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
    #     parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
    #                         help="end date formatted as YYYY-MM-DD")
    #
    #     args = parser.parse_args(sys.argv[3:])
    #
    #     if args.start is not None:
    #         try:
    #             print(dataframe(load_json(args.symbol))[args.start:args.end])
    #         except KeyError:
    #             print("Invalid date time format.")
    #     else:
    #         print(dataframe(load_json(args.symbol)))
    #
    # def display_simple(self):
    #     parser = argparse.ArgumentParser(
    #         description='simple line chart representation of provided symbol')
    #     parser.add_argument('symbol', help="symbol of desired stock")
    #     parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
    #     parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
    #                         help="end date formatted as YYYY-MM-DD")
    #
    #     args = parser.parse_args(sys.argv[3:])
    #
    #     if args.start is not None:
    #         try:
    #             simple_linechart(args.symbol, args.start, args.end, block=True)
    #         except KeyError:
    #             print("Invalid date time format.")
    #     else:
    #         simple_linechart(args.symbol, block=True)
    #
    # def display_candlestick(self):
    #     parser = argparse.ArgumentParser(
    #         description='Japanese candlestick plot of provided symbol')
    #     parser.add_argument('symbol', help="symbol of desired stock")
    #     parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
    #     parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
    #                         help="end date formatted as YYYY-MM-DD")
    #
    #     args = parser.parse_args(sys.argv[3:])
    #
    #     if args.start is not None:
    #         try:
    #             candlestick(args.symbol, args.start, args.end, block=True)
    #         except KeyError:
    #             print("Invalid date time format.")
    #     else:
    #         candlestick(args.symbol, block=True)
    #
    # def display_ribbon(self):
    #     parser = argparse.ArgumentParser(
    #         description='moving average ribbon of provided symbol')
    #     parser.add_argument('symbol', help="symbol of desired stock")
    #     parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
    #     parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
    #                         help="end date formatted as YYYY-MM-DD")
    #
    #     args = parser.parse_args(sys.argv[3:])
    #
    #     ma = [i for i in range(10, 210, 10)]
    #     if args.start is not None:
    #         try:
    #             moving_averages_adv(args.symbol, ma, args.start, args.end, block=True)
    #         except KeyError:
    #             print("Invalid date time format.")
    #     else:
    #         moving_averages_adv(args.symbol, ma, block=True)
    #
    # def display_ma(self):
    #     parser = argparse.ArgumentParser(
    #         description='Japanese candlestick plot of provided symbol with moving average 20d, 50d, 200d')
    #     parser.add_argument('symbol', help="symbol of desired stock")
    #     parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
    #     parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
    #                         help="end date formatted as YYYY-MM-DD")
    #
    #     args = parser.parse_args(sys.argv[3:])
    #
    #     if args.start is not None:
    #         try:
    #             moving_averages(args.symbol, args.start, args.end, block=True)
    #         except KeyError:
    #             print("Invalid date time format.")
    #     else:
    #         moving_averages(args.symbol, block=True)
    #
    # def display_model(self):
    #     parser = argparse.ArgumentParser(
    #         description='various plot of provided symbol')
    #     parser.add_argument('type', help="return, growth, increase, change")
    #     parser.add_argument('-l', '--list', nargs='+', type=str, help='-l sym sym sym', required=True)
    #     parser.add_argument('-s', '--start', default=None, type=str, help="start date formatted as YYYY-MM-DD")
    #     parser.add_argument('-e', '--end', default=str(datetime.date.today()), type=str,
    #                         help="end date formatted as YYYY-MM-DD")
    #
    #     args = parser.parse_args(sys.argv[3:])
    #
    #     if args.start is not None:
    #         try:
    #             graph_model(args.list, args.type, args.start, args.end, block=True)
    #         except KeyError:
    #             print("Invalid date time format.")
    #     else:
    #         graph_model(args.list, args.type, block=True)




