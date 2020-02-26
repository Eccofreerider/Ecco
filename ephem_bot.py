"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход 
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите 
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите 
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import datetime
import ephem
from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings
import smiles

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


def body(bot, update, user_data):

    text = update.message.text
    body_name = text.split()[-1]
    current_date = datetime.date.today().strftime("%Y/%m/%d")
    calc_data = getattr(ephem, body_name)(current_date)
    try:
        final = ephem.constellation(calc_data)
        update.message.reply_text(f"Планета находится в созвездии {final[1]}")
    except AttributeError:
        update.message.reply_text("Повторите название планеты.")


def greet_user(bot, update, user_data):
    emo = emojize(choice(smiles.smile), use_aliases = True)
    user_data['emo'] = emo
    text = f'Привет {emo}'
    contacts_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать геолокацию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup(
                                        [
                                            ['Прислать котика', 'Сменить аватарку'],
                                            [contacts_button, location_button]
                                        ]
                                        )
    print(update.message.chat.first_name, ':', text)
    update.message.reply_text(text, reply_markup = my_keyboard)


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = f'Привет, {update.message.chat.first_name} {emo}! Ты написал: {update.message.text}'
    print(update.message.chat.first_name, ": ", user_text)
    update.message.reply_text(user_text)
 
def send_cat_picture(bot, update, user_data):
    source = glob('images/cat*.png')
    rand = choice(source)
    bot.send_photo(chat_id = update.message.chat.id, photo = open(rand,'rb'))

def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text(f'Готово: {emo}')

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(smiles.smile), use_aliases = True)
        return user_data['emo']

def get_contact(bot,update,user_data):
    print(update.message.contact)
    update.message.reply_text(f'Готово: {emo}')

def get_location(bot,update,user_data):
    print(update.message.location)
    update.message.reply_text(f'Готово: {emo}')

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", body, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()
