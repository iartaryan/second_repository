from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import token
import ephem
import datetime

import logging
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('planet', check_constellation, pass_args=True))
    dp.add_handler(CommandHandler('wordcount', wordcount_f, pass_args=True))
    
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    updater.start_polling()
    updater.idle()

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)
        
def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def check_constellation(bot, update, args):
    print(args[0])
    update.message.reply_text(constellation_f(args[0]))


def wordcount_f(bot, update, args):
    print(args)
    word = args[0]
    update.message.reply_text(word.split(' '))


def constellation_f(user_planet):
    planet_list = []
    for name in ephem._libastro.builtin_planets():
        planet_list.append(name[2])

    if user_planet in planet_list:
        pl = getattr(ephem, user_planet)
        print(user_planet, ' in ', ephem.constellation(pl(datetime.datetime.now()))[1])
        constel = ephem.constellation(pl(datetime.datetime.now()))[1]
    else:
        constel = 'I have no answer('
    return constel


main()


