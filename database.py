import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

SQLALCHEMY_DATABASE_URL = environ['postgres_url']

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Session = sessionmaker()
Session.configure(bind=engine)

Base = declarative_base()
