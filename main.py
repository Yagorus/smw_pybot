import creds
import telebot
from telebot import types

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db import get_engine_from_settings, City, User, Country, Info

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
    print(message)

@bot.message_handler(commands=["commit"])
def commit_db(message):
    bot.send_message(message.chat.id, "Input city for commit")
    bot.register_next_step_handler(message, commit_city)

#testing
def commit_city(message):
    commit_user_to_db(message)
    if not (API_json.get_coords_city(message.text) == None):
        coords=API_json.get_coords_city(message.text)
        cityname = message.text
        country_id = get_country_id(cityname)
        pop = API_json.population(coords['lon'], coords["lat"])

        city = City(
            lon=str(coords['lon']),
            lat=str(coords['lat']),
            city=cityname,
            pop=pop['population'],
            country_id = country_id
        )
        qr = session.query(exists().
        where(  City.lon==str(coords['lon']),
                City.lat==str(coords['lat']),
                City.city==cityname,
                City.pop==pop['population'],
                City.country_id == country_id)).scalar()
        try:
            if qr is False:
                session.add(city)
                session.commit()
        finally:
            commit_info_to_db(message.from_user.id, country_id)
            session.close()
    
#testing
def get_country_id(city):
    country = API_json.get_country_name(city)
    qr = session.query(exists().where(Country.name == country)).scalar()
    if commit_country_to_db(country) is True:
        result = session.query(Country.id).filter_by(name=country).first()
        return result[0]
    else:
        return session.query(Country.id).filter_by(name=country).first()[0]

def commit_country_to_db(country):
    qr = session.query(exists().where(Country.name == country)).scalar()
    if qr is False:
        country=Country(name=country)
        session.add(country)
        session.commit()
        return True
    else:
        return False
    
def commit_user_to_db(TelegramMessage):
    count = TelegramMessage.from_user.id
    name = TelegramMessage.from_user.username
    user_db = User(count= count, name=name)
    qr = session.query(exists().where(User.name == name, User.count == count)).scalar()
    try:
        if qr is False:
            session.add(user_db)
            session.commit()
    finally:
        session.close()

def commit_info_to_db(user, city):
    pass

def main():
    # APP_TOKEN = os.getenv('APP_TOKEN')
    bot.infinity_polling() 
    

if __name__ == '__main__':
    main()

