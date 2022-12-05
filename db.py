from sqlalchemy import Column, Integer, String, create_engine
import sqlalchemy 
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


class UserCoord(Base):  
    __tablename__  = 'usercoord'
    id = Column(Integer, primary_key=True)
    u_id = Column(Integer(), index=True)
    name = Column(String(60))
    lat = Column(String(16))
    lon = Column(String(16))
    city = Column(String(64))
    country = Column(String(16))
    pop = Column(Integer)

    def __init__(self, id, u_id, name, lat,lon,city,country, pop):
        self.id = id
        self.u_id = u_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.city = city
        self.country = country
        self.pop = pop

    def __repr__(self):
        return "<Coordinates(name='{}', lat='{}', lon='{}', u_id='{}', city='{}')>".format(self.name,
                                                                                           self.lat, self.lon,
                                                                                           self.u_id, self.city)
