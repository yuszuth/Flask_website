from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import Date
from database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    secret_link = Column(String)
    verification_status = Column(String)

class Ips(Base):
    __tablename__ = 'Ips'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    email = Column(String)
    time = Column(DateTime)

class Workers(Base):
    __tablename__ = 'Workers'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    time = Column(DateTime, default=datetime.now().strftime("%H:%M:%S.%f"))
    n = Column(Integer)
    p = Column(Integer)
    q = Column(Integer)
    status = Column(String)
    time_start = Column(String)
    time_end = Column(String )