import os
import telebot
from telebot import types

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db import City, User, Country, Info

import logging
from dotenv import load_dotenv
import API_json as API_json

load_dotenv()
# make bot
bot = telebot.TeleBot(os.getenv("BOT_TOKEN")) 
engine = create_engine(os.getenv('APP_DATABASE_URL'))

#for local start db
# engine = get_engine_from_settings()

# config for local db
Base = declarative_base()
engine = create_engine(os.getenv('APP_DATABASE_URL'))
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
        '/forecast - get forecast for 5 days',
        '/check - get forecast for all saved ',
        '/list - check all cites saved for user ',
    ])
    bot.send_message(message.chat.id,txt)

@bot.message_handler(commands=["commit"])
def commit_db(message):
    bot.send_message(message.chat.id, "Input city for commit")
    bot.register_next_step_handler(message, commit_city)

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
            city_id = get_city_id(cityname)
            user_id = get_user_id(message.from_user.id)
            commit_info_to_db(user_id, city_id)
            session.close()
            list_db(message)
    
def get_country_id(city):
    country = API_json.get_country_name(city)
    qr = session.query(exists().where(Country.name == country)).scalar()
    if commit_country_to_db(country) is True:
        result = session.query(Country.id).filter_by(name=country).first()
        return result[0]
    else:
        return session.query(Country.id).filter_by(name=country).first()[0]

def get_city_id(city):
    return session.query(City.id).filter_by(city=city).first()[0]

def get_user_id(Telegram_count_id):
    return session.query(User.id).filter_by(count=Telegram_count_id).first()[0]

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

def commit_info_to_db(user_id, city_id):
    info_db = Info(user_id= user_id, city_id=city_id)
    qr = session.query(exists().where(Info.user_id == user_id, Info.city_id == city_id)).scalar()
    try:
        if qr is False:
            session.add(info_db)
            session.commit()
    finally:
        pass
        
@bot.message_handler(commands=['check'])
def get_weather_from_db(message):
    try:
        user_id=get_user_id_from_db(message)
        result = session.query(Info.city_id).filter_by(user_id=user_id).all()
        user_id_lst = [i[0] for i in result]
        for i in user_id_lst:
            result = session.query(City.city).filter_by(id=i).first()
            get_city_db(message, result[0])
    except TypeError:
        bot.send_message(message.chat.id, "No elements in db")

def get_city_db(message, cityname):
    txt=API_json.get_weather_city(cityname)
    bot.send_message(message.chat.id, txt)

def get_user_id_from_db(Telegram_message):
    return session.query(User.id).filter_by(count=Telegram_message.from_user.id).first()[0]

@bot.message_handler(commands=["list"])
def list_db(message):
    try:
        user_id=get_user_id_from_db(message)
        result = session.query(Info.city_id).filter_by(user_id=user_id).all()
        user_id_lst = [i[0] for i in result]
        print_lst = []
        txt = '\n\t-'
        for i in user_id_lst:
            result = session.query(City.city).filter_by(id=i).first()
            print_lst.append(result[0])
        bot.send_message(message.chat.id,"Saved cytes:\n\t-"+txt.join(print_lst))
    except TypeError:
        bot.send_message(message.chat.id, "No elements in db")

@bot.message_handler(commands=['delete'])
def delete_city_from_db(message):
    bot.send_message(message.chat.id, "Input city name, thay you want to delete")
    bot.register_next_step_handler(message, delete_city_from_db_hdlr)

def delete_city_from_db_hdlr(message):
    try:
        city_id=get_city_id(message.text)
        session.query(Info).filter_by(city_id=city_id).delete()
        session.commit()
        print(message.text + "\tDeleted from list")
    except TypeError:
        bot.send_message(message.chat.id, "There is no such elemet")

def main():
    # APP_TOKEN = os.getenv('APP_TOKEN')
    bot.infinity_polling()
    

if __name__ == '__main__':
    main()

