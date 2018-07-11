import pandas as pd
import numpy as np


def single_back_test(adj_long_profits, cash=1000000, port_value=.1, batch=100, stoploss=.2, fee=10):
    """
    :param adj_long_profits:
    :param cash:
    :param port_value: max proportion of portfolio bet on any trade
    :param batch: number of shares bought per batch
    :param stoploss: percentage of trade loss that would trigger a stop loss
    :param fee: transaction fee per trade
    :return:
    """

    backtest = pd.DataFrame({"Start Port. Value": [],
                             "End Port. Value": [],
                             "End Date": [],
                             "Shares": [],
                             "Share Price": [],
                             "Trade Value": [],
                             "Profit per Share": [],
                             "Total Profit": [],
                             "Stop-Loss Triggered": []})

    for index, row in adj_long_profits.iterrows():
        batches = np.floor(cash * port_value) // np.ceil(batch * row["Price"])  # Calculate maximum number of batches
        trade_val = batches * batch * row["Price"] # How much money is put on the line with each trade

        if row["Low"] < (1 - stoploss) * row["Price"]:  # Account for the stop-loss
            share_profit = np.round((1 - stoploss) * row["Price"], 2)
            stop_trig = True
        else:
            share_profit = row["Profit"]
            stop_trig = False
        profit = round(share_profit * batches * batch - fee, 2)  # Compute profits
        # Add a row to the backtest data frame containing the results of the trade
        backtest = backtest.append(pd.DataFrame({
            "Start Port. Value": cash,
            "End Port. Value": cash + profit,
            "End Date": row["End Date"],
            "Shares": batch * batches,
            "Share Price": row["Price"],
            "Trade Value": trade_val,
            "Profit per Share": share_profit,
            "Total Profit": profit,
            "Stop-Loss Triggered": stop_trig
        }, index=[index]))
        cash = max(0, cash + profit)
    return backtest
