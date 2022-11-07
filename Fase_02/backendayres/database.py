from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv('db_access.env')

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
CONECTION = os.getenv('CONECTION')
DATABASE = os.getenv('DB')

SQLALCHEMY_DATABASE_URL = "mysql://{0}:{1}@{2}/{3}".format(USER, PASSWORD, CONECTION, DATABASE)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()