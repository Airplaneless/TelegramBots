import logging
import datetime
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
            level=logging.INFO,
            format='%(asctime)s %(message)s'
        )

        self.stock_updater = Stocks(os.path.join(ROOT, 'data/yahoo'))
        self.quoter = Quotes(os.path.join(ROOT, 'data/Havamal.csv'))

    @staticmethod
    def start(bot, update):
        user = update.message.from_user
        logging.info('Saying hi to {}'.format(usr2str(user)))
        bot.send_message(chat_id=update.message.chat_id, text="Send stock index, which you wish find")

    @staticmethod
    def echo(bot, update):
        user = update.message.from_user
        logging.info("Repeat after user {}, text: u'{}'".format(usr2str(user), update.message.text))
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def rand_quote(self, bot, update):
        user = update.message.from_user
        logging.info('Sending quotation for {}'.format(usr2str(user)))
        bot.send_message(chat_id=update.message.chat_id, text=self.quoter.random_quote())

    def search_stock(self, bot, update):
        user = update.message.from_user
        request = update.message.text
        logging.info('{} request search'.format(usr2str(user)))
        logging.info('Searching for {} stock info'.format(request))
        match = self.stock_updater.find_match(request)
        if match is None:
            logging.warning("Couldn't  find {} stock info".format(request))
            bot.send_message(chat_id=update.message.chat_id, text="Can't find that")
        else:
            logging.info("{} stock info founded".format(request))
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
        logging.info("{} request load data".format(usr2str(user)))
        bot.send_message(chat_id=update.message.chat_id, text="Loading data, wait a minute")
        logging.info("Loading stock data for {}".format(ticker))
        data = self.stock_updater.get_stock_data(ticker)
        if data is None:
            logging.warning("Couldn't  load {} stock data".format(ticker))
            bot.send_message(chat_id=update.message.chat_id, text="There is no {} index".format(ticker))
        else:
            logging.info("Got {} stock data, plotting...".format(ticker))
            self.stock_updater.plot_data(data, ticker, os.path.join(ROOT, 'workspace/stocks/stocks.png'))
            logging.info("Finish plotting, sending photo")
            bot.send_photo(
                chat_id=update.message.chat_id,
                photo=open(os.path.join(ROOT, 'workspace/stocks/stocks.png'), 'rb')
            )

    @staticmethod
    def func_builder(f, args):
        return f(args=args)