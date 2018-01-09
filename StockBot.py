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

    interface = Interface()
    ls = ['load_' + str(i) for i in range(len(interface.stock_updater.stock_list)+1)]

    start_handler = CommandHandler('start', interface.start)
    find_stocks = MessageHandler(Filters.text, interface.search_stock)
    load_stocks = CommandHandler(ls, interface.get_stock)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(load_stocks)
    dispatcher.add_handler(find_stocks)

    updater.start_polling()
    updater.idle()