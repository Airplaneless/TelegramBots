import logging
import datetime
from pandas_datareader._utils import RemoteDataError
from commands import Stocks, Quotes
from config import *


def usr2str(usr):
    return "{} {} ({}, {})".format(
        usr['first_name'],
        usr['last_name'],
        usr['username'],
        usr['id']
    )


class Interface:

    def __init__(self):
        time = datetime.datetime.now()
        log_file = os.path.join(ROOT, 'logs/{0}_{1}_{2}.log'.format(time.year, time.month, time.day))

        if not os.path.exists(log_file):
            os.mknod(log_file)

        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s %(message)s'
        )

        self.stock_updater = Stocks(os.path.join(ROOT, 'data/yahoo'))
        self.quoter = Quotes(os.path.join(ROOT, 'data/Havamal.csv'))

    @staticmethod
    def start(bot, update):
        user = update.message.from_user
        logging.debug('Saying hi to {}'.format(usr2str(user)))
        bot.send_message(chat_id=update.message.chat_id, text="Send stock name, which you wish find")

    @staticmethod
    def echo(bot, update):
        user = update.message.from_user
        logging.debug("Repeat after user {}, text: u'{}'".format(usr2str(user), update.message.text))
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def rand_quote(self, bot, update):
        user = update.message.from_user
        logging.debug('Sending quotation for {}'.format(usr2str(user)))
        bot.send_message(chat_id=update.message.chat_id, text=self.quoter.random_quote())

    def search_stock(self, bot, update):
        user = update.message.from_user
        request = update.message.text
        logging.debug('{} request search'.format(usr2str(user)))
        logging.debug('Searching for {} stock info'.format(request))
        match = self.stock_updater.find_match(request)
        if match is None:
            logging.debug("Couldn't  find {} stock info".format(request))
            bot.send_message(chat_id=update.message.chat_id, text="Can't find that")
        else:
            logging.debug("{} stock info founded".format(request))
            #Stocks.data_frame2png(match[:19], os.path.join(ROOT, 'workspace/stocks/table.html'))
            bot.send_message(chat_id=update.message.chat_id, text="For your request I found:")
            bot.send_message(
                chat_id=update.message.chat_id,
                text=Stocks.print_results(match[:19])
            )

    def get_stock(self, bot, update):
        user = update.message.from_user
        request = int(update.message.text.split('_')[-1])
        ticker = self.stock_updater.stock_list.iloc[request]['Ticker']
        logging.debug("{} request load data".format(usr2str(user)))
        bot.send_message(chat_id=update.message.chat_id, text="Loading data, wait a minute")
        logging.debug("Loading stock data for {}".format(ticker))
        try:
            data = self.stock_updater.get_stock_data(ticker)
            logging.debug("Got {} stock data, plotting...".format(ticker))
            self.stock_updater.plot_data(data, ticker, os.path.join(ROOT, 'workspace/stocks/stocks.png'))
            logging.debug("Finish plotting, sending photo")
            bot.send_photo(
                chat_id=update.message.chat_id,
                photo=open(os.path.join(ROOT, 'workspace/stocks/stocks.png'), 'rb')
            )
        except RemoteDataError:
            logging.debug("Error: Can't load data for {}".format(ticker))
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Error: Unable get data from finance.yahoo.com for {}".format(ticker)
            )
