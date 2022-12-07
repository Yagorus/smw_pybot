from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, update
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os
from dotenv import load_dotenv

# load_dotenv()

Base = declarative_base()

# Data for local db 
postgresql = {
    'pguser' : 'postgres', # user name of db
    'pgpassword' : '12345', # password for postgres db
    'pghost' : 'localhost', # ip addres db
    'pgport' : '5432', # db port 
    'pgdb' : 'db_bot' # name of db
}

# method for local test to create engine
def get_engine(user, passwd, host, port, db):
    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine

#method for apply engine (also for local db)
def get_engine_from_settings():
    keys = ['pguser', 'pgpassword', 'pghost', 'pgport', 'pgdb']

    if not all(key in keys for key in postgresql.keys()):
        raise Exception("Bad config file")
    return get_engine(
            postgresql['pguser'],
            postgresql['pgpassword'],
            postgresql['pghost'],
            postgresql['pgport'],
            postgresql['pgdb']
            )



class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index = True)
    count = Column(Integer())       # id in accaunt in Telegram
    name = Column(String(60))       # username in Telegram (@username)
    
    def __init__(self, name, count):
        # self.id = id
        self.name = name
        self.count = count

    def __repr__(self):
        return f"<User(id='{self.id}', name='{self.name}', city='{self.count}')>"

    
    
class City(Base):
    __tablename__  = 'city'
    id = Column(Integer, primary_key=True)
    lon = Column(String(16))                # Longitude
    lat = Column(String(16))                # Latitude 
    city = Column(String(64))               # City name
    pop = Column(Integer)                   # City Population
    country_id = Column(Integer, ForeignKey("country.id"))           # City Population
   
    
    country = relationship('Country')



    def __init__(self, lon, lat, city, pop, country_id):
        # self.id = id
        self.lon = lon
        self.lat = lat
        self.city = city
        self.pop = pop
        self.country_id = country_id

    def __repr__(self):
        return f"<City(id='{self.id}', city='{self.city}', pop='{self.pop}', country_id = '{self.country_id}', lon = '{self.lon}', lat = '{self.lat}')>"

class Country(Base):
    __tablename__  = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(16))

    def __init__(self, name):
        # self.id = id
        self.name = name

    def __repr__(self):
        return f"<Country(id='{self.id}' , country='{self.name}')>"


class Info(Base):
    __tablename__  = 'info'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    city_id = Column(Integer, ForeignKey("city.id"))

    user = relationship('User')
    country = relationship('City')

    def __repr__(self):
        return f"<Info(id='{self.id}' ,user_id='{self.user_id}', city_id='{self.city_id}')>"
    

Base.metadata.create_all(get_engine_from_settings())
