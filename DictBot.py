#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BotTools import Interface
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

if __name__ == '__main__':

    with open('token_DictBot', mode='r') as f:
        __token__ = f.readline()

    updater = Updater(__token__)
    dispatcher = updater.dispatcher

    interface = Interface('DictBot')

    ls = ['get_' + str(i) for i in interface.dictionary.indexes.values()]

    start_handler = CommandHandler('start', interface.start_dictbot)
    print_translate = CommandHandler(ls, interface.translate)
    about = CommandHandler('about', interface.about_dict)
    find_word = MessageHandler(Filters.text, interface.search_in_dict)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(print_translate)
    dispatcher.add_handler(about)
    dispatcher.add_handler(find_word)

    updater.start_polling()
    updater.idle()
