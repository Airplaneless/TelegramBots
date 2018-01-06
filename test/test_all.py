import unittest
import os
from BotTools import Quotes, Stocks

ROOT = os.path.abspath("../")


class RandomQuoteTest(unittest.TestCase):

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
        rec = Stocks.print_series(match)
        self.assertIs(bool(rec), True)
        print rec

    def test_df2im(self):
        updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )

        match = updater.find_match('Microsoft')
        res = Stocks.data_frame2png(match[:9], os.path.join(ROOT, 'workspace/stocks/test.html'))
        self.assertIs(res, True)

    def test_plot(self):
        updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )

        data = updater.get_stock_data('IBM')

        self.assertIs(
            Stocks.plot_data(data, 'IBM', os.path.join(ROOT, 'workspace/stocks/stocks.png')), True
        )
