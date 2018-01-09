#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
from BotTools import Quotes, Stocks, Dictionary

ROOT = os.path.abspath("../")


class QuoteTest(unittest.TestCase):

    def test(self):
        quoter = Quotes(
            os.path.join(ROOT, 'data/Havamal.csv')
        )
        quote = quoter.random_quote()
        print quote
        self.assertEqual(bool(quote), True)


class StockTest(unittest.TestCase):

    def test_match(self):
        updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )

        match = updater.find_match('Microsoft')
        self.assertEqual(match['Name'].values[0], 'Microsoft Corporation')

    def test_get(self):
        updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )

        data = updater.get_stock_data('IBM')
        self.assertIs(data is not None, True)

    def test_print(self):
        updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )

        match = updater.find_match('IBM')
        rec = Stocks.print_results(match)
        self.assertIs(bool(rec), True)
        print rec

    def test_df2im(self):
        updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )

        match = updater.find_match('Microsoft')
        res = Stocks.data_frame2png(match[:19], os.path.join(ROOT, 'workspace/stocks/table.html'))
        self.assertIs(res, True)

    def test_plot(self):
        updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )

        data = updater.get_stock_data('IBM')

        self.assertIs(
            updater.plot_data(data, 'IBM', os.path.join(ROOT, 'workspace/stocks/stocks.png')), True
        )


class DictTest(unittest.TestCase):

    def test_search(self):
        dictionary = Dictionary(os.path.join(ROOT, 'data/dicts/MullerDict.dz'))
        ans = dictionary.search_word('dog')
        print ans
        self.assertEqual(bool(ans), True)

    def test_get(self):
        dictionary = Dictionary(os.path.join(ROOT, 'data/dicts/MullerDict.dz'))
        ans = dictionary.get_translate(dictionary.indexes['dog'])
        print ans
        self.assertEqual(bool(ans), True)