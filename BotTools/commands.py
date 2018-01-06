import random
import os
import pandas as pd
import matplotlib.pylab as plt
from pandas_datareader import DataReader
from BotTools.config import *


class Quotes:
    """
    Work with quotations
    """
    def __init__(self, source):
        """

        :param source: str
        Path to csv file with quotes
        """
        self.source = source
        self.quotes = pd.read_csv(source).to_dict()['0']

    def random_quote(self):
        idx = random.randint(0, len(self.quotes))
        return self.quotes[idx]


class Stocks:
    """
    Work with stocks data
    """
    def __init__(self, source):
        """
        Stocks constructor
        :param source: str
        Directory with ticker data
        """
        self.source = source
        self.name = source.split('/')[-1]
        self.stock_list = pd.read_csv(
            os.path.join(source, 'Stocks.csv')
        )
        self.etf_list = pd.read_csv(
            os.path.join(source, 'ETF.csv')
        )
        self.currency_list = pd.read_csv(
            os.path.join(source, 'Currency.csv')
        )

    def find_match(self, name, column='Name'):
        """
        Find stock record by name
        :param name: str
        Searching name
        :param column: str
        Name of column in table of tickers
        :return: pd.DataFrame
        Matched tickers
        """
        series = self.stock_list[column]
        new_series = series.where(series.str.contains(name)).dropna()
        if new_series.any():
            return self.stock_list.iloc[new_series.index]
        else:
            return None

    def get_stock_data(self, ticker):
        """
        Download stock data
        :param ticker: str
        Name of ticker
        :return: pd.DataFrame
        """
        if self.find_match(ticker, column='Ticker') is not None:
            return DataReader(ticker, self.name)
        else:
            return None

    @staticmethod
    def print_results(df):
        ans = ''
        for i in range(len(df[:10])):
            ans += 'Name: ' + str(df.iloc[i]['Name']) + '\n'
            ans += 'Ticker: ' + str(df.iloc[i]['Ticker']) + '\n'
            ans += 'Exchange: ' + str(df.iloc[i]['Exchange']) + '\n'
            ans += 'Category: ' + str(df.iloc[i]['Category Name']) + '\n'
            ans += 'Download data: /load_{}'.format(str(df.index[i])) + '\n\n'
        return ans

    @staticmethod
    def data_frame2png(df, path):
        df.to_html(path)
        os.system("cutycapt --url=file://{} --out={}".format(path, path[:-5]+'.png'))
        return True

    def plot_data(self, data, ticker, path):
        """
        Plot and save stock data
        :param data: pd.DataFrame
        :param ticker: str
        :param path: str
        Path for saved image
        """
        kfv = lambda d, v: d.keys()[d.values().index(v)]

        idx = kfv(self.stock_list['Ticker'].to_dict(), ticker)
        info = self.stock_list.loc[idx]

        plt.figure(figsize=(10, 10))
        ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3, rowspan=2)
        ax1.set_title(info['Name'] + '\n' + info['Ticker'] + ', ' + info['Exchange'] + '\nYahooFinance, 2018')
        ax1.plot(data['Open'], label='Open')
        ax1.plot(data['High'], label='High')
        ax1.plot(data['Low'], label='Low')
        ax1.plot(data['Close'], label='Close')
        ax1.plot(data['Adj Close'], label='Adj Close')
        ax1.legend()
        ax1.set_ylabel('Currency in USD')

        ax2 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
        ax2.plot(data['Volume'], label='Volume')
        ax2.set_ylabel('Volume, USD')
        plt.savefig(path)
        return True
