from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import Date
from database import Base
from datetime import datatime


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    secret_link = Column(String)
    verification_status = Column(String)


class Ip(Base):
    __tablename__ = 'Ips'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    email = Column(String)
    time = Column(DateTime)

class Worker(Base):
    __tablename__ = 'Workers'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    time = Column(DateTime, datetime.now().strftime("%H:%M:%S"))
    N = Column(Integer)
    p = Column(Integer)
    q = Column(Integer)
    status = Column(String)
    time_start = Column(String)
    time_end = Column(String )