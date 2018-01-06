import sys
from BotTools import Interface
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')

    with open('token_StockBot', mode='r') as f:
        __token__ = f.readline()

    updater = Updater(__token__)
    dispatcher = updater.dispatcher

    Interface()

    start_handler = CommandHandler('start', Interface.start)
    find_stocks = MessageHandler(Filters.text, Interface.search_stock)
    load_stocks = CommandHandler('get', Interface.get_stock, pass_args=True)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(load_stocks)
    dispatcher.add_handler(find_stocks)

    updater.start_polling()
    updater.idle()