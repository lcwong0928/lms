import pandas as pd
import numpy as np


def multi_backtest(signals, cash=1000000, port_value=.1, batch=100, stop_loss=.2, fee=10):
    """
    This function backtests strategies, with the signals generated by the strategies being passed in the
    signals DataFrame. A fictitious portfolio is simulated and the returns generated by this portfolio are reported.

    :param signals: pandas DataFrame containing buy and sell signals with stock prices and symbols
    :param cash: integer for starting cash value
    :param port_value:  maximum proportion of portfolio to risk on any single trade
    :param batch: integer trading batch sizes
    :param stop_loss: percentage of trade loss that would trigger a stop loss
    :param fee: transaction fee per trade
 
    :return: pandas DataFrame with backtesting results
    """

    SYMBOL = 1  # Constant for which element in index represents symbol
    portfolio = dict()  # Will contain how many stocks are in the portfolio for a given symbol
    port_prices = dict()  # Tracks old trade prices for determining profits

    results = pd.DataFrame({"Start Cash": [],
                            "End Cash": [],
                            "Portfolio Value": [],
                            "Type": [],
                            "Shares": [],
                            "Share Price": [],
                            "Trade Value": [],
                            "Profit per Share": [],
                            "Total Profit": []})

    for index, row in signals.iterrows():
        # These first few lines are done for any trade
        shares = portfolio.setdefault(index[SYMBOL], 0)
        trade_val = 0
        batches = 0
        cash_change = row["Price"] * shares  # Shares could potentially be a positive or negative number
        # (cash_change will be added in the end; negative shares indicate a short)
        portfolio[index[SYMBOL]] = 0  # For a given symbol, a position is effectively cleared
        old_price = port_prices.setdefault(index[SYMBOL], row["Price"])
        portfolio_val = 0

        for key, val in portfolio.items():
            portfolio_val += val * port_prices[key]

        if row["Signal"] == "Buy" and row["Regime"] == 1:  # Entering a long position
            batches = np.floor(cash * port_value) // np.ceil(batch * row["Price"])  # maximum number of batches
            trade_val = batches * batch * row["Price"]  # money on line with each trade
            cash_change -= trade_val  # We are buying shares so cash will go down
            portfolio[index[SYMBOL]] = batches * batch  # Recording how many shares are currently invested in the stock
            port_prices[index[SYMBOL]] = row["Price"]  # Record price
            old_price = row["Price"]

        elif row["Signal"] == "Sell" and row["Regime"] == -1:  # Entering a short
            pass
            # Do nothing; can we provide a method for shorting the market?

        # else:
        # raise ValueError("I don't know what to do with signal " + row["Signal"])

        pprofit = row["Price"] - old_price  # Compute profit per share;
        # old_price is set in such a way that entering a position results in a profit of zero

        # Update report
        results = results.append(pd.DataFrame({
            "Start Cash": cash,
            "End Cash": cash + cash_change,
            "Portfolio Value": cash + cash_change + portfolio_val + trade_val,
            "Type": row["Signal"],
            "Shares": batch * batches,
            "Share Price": row["Price"],
            "Trade Value": abs(cash_change),
            "Profit per Share": pprofit,
            "Total Profit": batches * batch * pprofit
        }, index=[index]))
        cash += cash_change  # Final change to cash balance

    results.sort_index(inplace=True)
    results.index = pd.MultiIndex.from_tuples(results.index, names=["Date", "Symbol"])

    return results
