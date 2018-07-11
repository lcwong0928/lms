from single_back_test import *
from multi_backtest import *
from visualize import *
import numpy as np

'''Analysis via moving averages'''


def ohlc_adj(dat):
    """Adjust the prices to account for stock splits and dividend payments
    :param dat pandas DataFrame with stock data including "Open", "High", "Low", "Close", and "Adj Close"
    :return pandas DataFrame with adjusted stock data"""

    return pd.DataFrame({"Open": dat["Open"] * dat["Adjusted close"] / dat["Close"],
                         "High": dat["High"] * dat["Adjusted close"] / dat["Close"],
                         "Low": dat["Low"] * dat["Adjusted close"] / dat["Close"],
                         "Close": dat["Adjusted close"]})


def regime(df, fast, slow, start=None, end=None, show=False):
    """Determines when the fast MA is below the slow MA and vice versa."""

    stock_adj = ohlc_adj(clip(df, start, end))
    # Get the moving averages, both fast and slow, along with the difference in the moving averages
    fast_str, slow_str = str(fast) + "d", str(slow) + "d"
    diff = fast_str + "-" + slow_str

    # regime is sign of this difference; bullish if the fast moving average is above the slow moving average
    stock_adj[fast_str] = np.round(stock_adj["Close"].rolling(window=fast, center=False).mean(), 2)
    stock_adj[slow_str] = np.round(stock_adj["Close"].rolling(window=slow, center=False).mean(), 2)
    stock_adj[diff] = stock_adj[fast_str] - stock_adj[slow_str]

    # np.where() is a vectorized if-else function(cond, pass, fail)
    # 1's for bullish, -1's for bearish
    stock_adj["Regime"] = np.where(stock_adj[diff] > 0, 1, 0)
    stock_adj["Regime"] = np.where(stock_adj[diff] < 0, -1, stock_adj["Regime"])

    if show:
        print(stock_adj["Regime"].value_counts())
        stock_adj["Regime"].plot(ylim=(-2, 2)).axhline(y=0, color="black", lw=1)
        plt.title("Regime Data")
        plt.show(block=True)

    return stock_adj


def add_signals(stock_adj, show=False):
    """adds trading signals via at regime changes"""

    # today = today - yesterday, skips the first row to avoid error message caused by sign(NaN) during shift
    stock_adj["Signal"] = np.sign((stock_adj["Regime"] - stock_adj["Regime"].shift(1)).iloc[1:])

    # Changes the last row to -1 to signal a sell at the end, may want to not do this!
    stock_adj.loc[stock_adj.index[-1], 'Signal'] = -1.0

    # removes NaN overhangs caused by moving average
    stock_adj = stock_adj.dropna()

    if show:
        print(stock_adj["Signal"].value_counts())
        stock_adj["Signal"].plot(ylim=(-2, 2))
        plt.title("Signals")
        plt.show(block=True)

    return stock_adj


def get_signal(stock_adj, show=False, sort=False, filter=False):
    """return a new data frame only with the buy and sell days along with adjusted stock prices"""

    # Consider filtering out 0s
    if filter:
        # signal = 1
        for index, row in stock_adj.iterrows():
            if row["Regime"] == 0:
                stock_adj = stock_adj.drop(index)
        #     elif row["Signal"] != signal:
        #         stock_adj = stock_adj.drop(index)
        #     else:
        #         signal = -1 if signal == 1 else 1


    signals = pd.concat([
        pd.DataFrame({"Price": stock_adj.loc[stock_adj["Signal"] == 1, "Close"],
                      "Regime": stock_adj.loc[stock_adj["Signal"] == 1, "Regime"],
                      "Signal": "Buy"}),
        pd.DataFrame({"Price": stock_adj.loc[stock_adj["Signal"] == -1, "Close"],
                      "Regime": stock_adj.loc[stock_adj["Signal"] == -1, "Regime"],
                      "Signal": "Sell"}),
    ])

    if sort:
        signals.sort_index(inplace=True)
    if show:
        print(signals.to_string())

    return signals


def add_profit(signals, show=False):
    """profitability of long trades"""

    long_profits = pd.DataFrame({
        "End Date": signals["Price"].loc[
            signals.loc[(signals["Signal"].shift(1) == "Buy") & (signals["Regime"].shift(1) == 1)].index
        ].index,
        "Price": signals.loc[(signals["Signal"] == "Buy") &
                             signals["Regime"] == 1, "Price"],
        "Profit": pd.Series(signals["Price"] - signals["Price"].shift(1)).loc[
            signals.loc[(signals["Signal"].shift(1) == "Buy") & (signals["Regime"].shift(1) == 1)].index
        ].tolist()
    })

    if show:
        print(long_profits.to_string())
    return long_profits


def add_low(df, long_profits, show=False):
    """adds in the low of each trade"""
    df = ohlc_adj(df)
    trade_periods = pd.DataFrame({"Start": long_profits.index, "End": long_profits["End Date"]})
    long_profits["Low"] = trade_periods.apply(lambda x: min(df.loc[x["Start"]:x["End"], "Low"]), axis=1)

    if show:
        print(long_profits.to_string())

    return long_profits


def back_test(long_profits, cash=1000000, port_value=.1, batch=100, stoploss=.1, fee=10, show=False):
    backtest = single_back_test(long_profits, cash=cash, port_value=port_value, batch=batch, stoploss=stoploss, fee=fee)
    if show:
        print(backtest.to_string())
        backtest["End Port. Value"].plot()
        plt.show(block=True)
    return backtest


def multicrossover(stocks, fast, slow, start=None, end=None):
    trades = pd.DataFrame({"Price": [], "Regime": [], "Signal": []})
    for symbol in stocks:
        stock = ohlc_adj(dataframe(load_json(symbol)))
        reg = regime(stock, fast, slow, start=start, end=end, show=False)
        signals = get_signal(add_signals(reg))
        signals.index = pd.MultiIndex.from_product([signals.index, [symbol.upper()]], names=["Date", "Symbol"])
        trades = trades.append(signals)

    trades.sort_index(inplace=True)
    trades.index = pd.MultiIndex.from_tuples(trades.index, names=["Date", "Symbol"])
    return trades


if __name__ == '__main__':
    start = "2017-07-09"
    end = "2018-07-09"
    df = dataframe(load_json("AAPL"))
    for i in range(1, 2):
        stock_adj = regime(df, 10, 18, start, end, show=False)
        stock_adj_signals = add_signals(stock_adj, show=False)
        signals = get_signal(stock_adj_signals, show=False, sort=True, filter=True)
        stock = add_profit(signals, False)
        stock = add_low(df, stock, False)
        stock = back_test(stock, show=True, cash=1000, port_value=1, batch=1, stoploss=.1, fee=10)

    #print(multi_backtest(multicrossover(["aapl", "AMZN", "GOOG", "HPQ"], 20, 50, start, end), 100000).to_string())
