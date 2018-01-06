import sys
from BotTools import Interface
from key import TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    Interface()

    start_handler = CommandHandler('start', Interface.start)
    quote_handler = CommandHandler('wisdom', Interface.rand_quote)
    find_stocks = CommandHandler('find', Interface.search_stock, pass_args=True)
    load_stocks = CommandHandler('get', Interface.get_stock, pass_args=True)
    echo_handler = MessageHandler(Filters.text, Interface.echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(quote_handler)
    dispatcher.add_handler(find_stocks)
    dispatcher.add_handler(load_stocks)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()
