import logging
import datetime
from commands import Stocks, Quotes
from config import *


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

    @staticmethod
    def start(bot, update):
        user = update.message.from_user
        logging.info('Saying hi to {}'.format(user))
        bot.send_message(chat_id=update.message.chat_id, text="Chat with me!")

    @staticmethod
    def echo(bot, update):
        user = update.message.from_user
        logging.info("Repeat after user {}, text: u'{}'".format(user, update.message.text))
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    @staticmethod
    def rand_quote(bot, update):
        user = update.message.from_user
        quoter = Quotes(
            os.path.join(ROOT, 'data/Havamal_quotes.csv')
        )
        logging.info('Sending quotation for {}'.format(user))
        bot.send_message(chat_id=update.message.chat_id, text=quoter.random_quote())

    @staticmethod
    def search_stock(bot, update, args):
        user = update.message.from_user
        stack_updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )
        request = " ".join(args)
        logging.info('{} request search'.format(user))
        logging.info('Searching for {} stock info'.format(request))
        match = stack_updater.find_match(request)
        if match is None:
            logging.warning("Couldn't  find {} stock info".format(request))
            bot.send_message(chat_id=update.message.chat_id, text="Can't find it")
        else:
            logging.info("{} stock info founded".format(request))
            Stocks.data_frame2png(match[:19], os.path.join(ROOT, 'workspace/stocks/table.html'))
            #bot.send_message(chat_id=update.message.chat_id, text=ans)
            bot.send_message(chat_id=update.message.chat_id, text="For your request I found:")
            bot.send_photo(
                chat_id=update.message.chat_id,
                photo=open(os.path.join(ROOT, 'workspace/stocks/table.png'), 'rb')
            )

    @staticmethod
    def get_stock(bot, update, args):
        user = update.message.from_user
        stock_updater = Stocks(
            os.path.join(ROOT, 'data/yahoo')
        )
        request = " ".join(args)
        logging.info("{} request load data".format(user))
        bot.send_message(chat_id=update.message.chat_id, text="Loading stock data, wait a minute...")
        logging.info("Loading stock data for {}".format(request))
        data = stock_updater.get_stock_data(request)
        if data is None:
            logging.warning("Couldn't  load {} stock data".format(request))
            bot.send_message(chat_id=update.message.chat_id, text="I can't find that")
        else:
            logging.info("Got {} stock data, plotting...".format(request))
            Stocks.plot_data(data, request, os.path.join(ROOT, 'workspace/stocks/stocks.png'))
            logging.info("Finish plotting, sending photo")
            bot.send_photo(
                chat_id=update.message.chat_id,
                photo=open(os.path.join(ROOT, 'workspace/stocks/stocks.png'), 'rb')
            )