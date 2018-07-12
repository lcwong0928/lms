import pandas as pd
import datetime
from . import write

urls = {
    "nyse": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download",
    "nasdaq": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download",
    "amex": "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download"}


def retrieve(source, root_dir, save=True):
    """
    :param source: nyse, nasdaq, amex
    :param save: option to save under LMS/lms/data/stock_list/
    :return: name of equities as a list
    """
    dat = pd.read_csv(urls[source])
    symbols = dat["Symbol"].tolist()

    if save:
        directory = root_dir + "/lms/data/symbols/"
        title = source + "_" + str(datetime.date.today())
        write.json_file(directory, title, symbols)

    return symbols
