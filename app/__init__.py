from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


my_app = Flask(__name__)
my_app.secret_key='56hh67bnn'
Base = declarative_base()

engine = create_engine('sqlite:///app.db', echo=True, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
db = Session()
def create_db():
    Base.metadata.create_all(engine)
def drop_db():
    Base.metadata.drop_all(engine)

import app.views
