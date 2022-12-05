import creds
import telebot
from telebot import types

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db import get_engine_from_settings

import logging
from dotenv import load_dotenv
import creds
import API_json

# Get all hidden vars from file creds.env 
load_dotenv()
# make bot
bot = telebot.TeleBot(creds.BOT_TOKEN) 
# loggin into API service

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# # db config for AWS that take db url from local vars in conteiner
# engine = create_engine(os.getenv('APP_DATABASE_URL'))


# config for local db
Base = declarative_base()
engine = get_engine_from_settings()
Base.metadata.create_all(bind = engine)
session = sessionmaker(bind = engine)()


def start_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('/city')
    btn2 = types.KeyboardButton('Get Weather place')
    markup.add(btn1,btn2)
    return markup

@bot.message_handler(commands=['start'])
def startBot(message):
   bot.reply_to(message, "options : ",reply_markup=start_markup())


@bot.message_handler(commands=['city'])
def get_weather(message):
    bot.send_message(message.chat.id, API_json.geo_weather(39.099724,39.099724))



@bot.message_handler(commands=["find"])
def get_weather(message):
    bot.send_message(message.chat.id, "Input city name")
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    txt=API_json.get_weather_city(message.text)
    bot.send_message(message.chat.id, txt)

@bot.message_handler(commands=["forecast"])
def get_weather_5(message):
    bot.send_message(message.chat.id, "Input city name")
    bot.register_next_step_handler(message, get_city_5)

def get_city_5(message):
    txt=API_json.get_weather_city_5(message.text)
    bot.send_message(message.chat.id, txt)
    
@bot.message_handler(commands=["help"])
def help_msg(message):
    txt = "\n".join([
        '/start - run bot',
        '/help - output this help message',
        '/find - get info about weather in city via coords',
        '/forecast - get forecast for 5 days'
    ])
    bot.send_message(message.chat.id,txt)


def main():
    # APP_TOKEN = os.getenv('APP_TOKEN')
    bot.infinity_polling() 
    

if __name__ == '__main__':
    main()

