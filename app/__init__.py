import os
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import DevelopmentConfig, ProductionConfig, TestingConfig

my_app = Flask("property_manaager")
Base = declarative_base()
env = os.environ.get("FLASK_ENV", default=None)
if env == "production":
    my_app.config.from_object(ProductionConfig)
elif env == "testing":
    my_app.config.from_object(TestingConfig)
else:
    my_app.config.from_object(DevelopmentConfig)

engine = create_engine(
    my_app.config["DATABASE_URI"], connect_args={"check_same_thread": False}
)
Session = sessionmaker(bind=engine)
config = os.environ.get("TESTING", default=None)
db = Session()


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


import app.views
