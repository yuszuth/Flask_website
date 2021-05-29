from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://rszaqswymijvpw:49dbb8a47c368b728a671b75b12570db0fb577b94fe09e5a451e7287b5080a40@ec2-52-50-171-4.eu-west-1.compute.amazonaws.com:5432/db51je8rirvdo3'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Session = sessionmaker()
Session.configure(bind=engine)

Base = declarative_base()
