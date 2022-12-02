import creds
import telebot
from telebot import types
import os
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

# db config

# engine = create_engine(os.getenv('APP_DATABASE_URL'))
# conn = engine.connect()
# Session = sessionmaker(engine)
# s = Session()

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


def main():
    # APP_TOKEN = os.getenv('APP_TOKEN')
    bot.infinity_polling()  


if __name__ == '__main__':
    main()