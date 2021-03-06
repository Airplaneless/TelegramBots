#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import os
import pandas as pd
import linecache
import difflib
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pylab as plt
from pandas_datareader import DataReader
from PIL import Image, ImageOps
from BotTools.config import *

def invert_image(image):
    if image.mode == 'RGBA':
        r,g,b,a = image.split()
        rgb_image = Image.merge('RGB', (r,g,b))

        inverted_image = ImageOps.invert(rgb_image)

        r2,g2,b2 = inverted_image.split()

        final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))

        return final_transparent_image

    else:
        inverted_image = ImageOps.invert(image)
        return inverted_image


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
        return DataReader(ticker, self.name)

    @staticmethod
    def print_results(df):
        ans = ''
        for i in range(len(df[:10])):
            ans += 'Name: ' + str(df.iloc[i]['Name']) + '\n'
            ans += 'Ticker: ' + str(df.iloc[i]['Ticker']) + '\n'
            ans += 'Exchange: ' + str(df.iloc[i]['Exchange']) + '\n'
            ans += 'Category: ' + str(df.iloc[i]['Category Name']) + '\n'
            ans += 'Plot data: /load_{}'.format(str(df.index[i])) + '\n\n'
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

        image = Image.open(path)
        new_image = invert_image(image)
        new_image.save(path)

        return True


class Dictionary:
    """
    Work with dz dicts
    """
    def __init__(self, path):
        self.path = path
        self.text = linecache.getlines(path)
        self.indexes = dict()

        for i in xrange(len(self.text)):
            if self.text[i][0] in {' ', '/'} or i < 20:
                pass
            else:
                self.indexes[self.text[i][:-1]] = i

    def get_translate(self, index):
        translation = self.text[index]
        idx = index + 1
        while True:
            if idx - index > 70:
                return "".join(translation)
            if self.text[idx][0] in {' ', '\n'}:
                translation += self.text[idx].replace('_', '')
                idx += 1
            else:
                return "".join(translation)

    def search_word(self, word):
        res = difflib.get_close_matches(word.lower(), self.indexes.keys(), n=8)
        ans = 'Похожие слова:\n'
        if bool(res):
            for i in res:
                ans += i + ': /get_{}'.format(self.indexes[i]) + '\n\n'
        else:
            ans = None
        return ans
