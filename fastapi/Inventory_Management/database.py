from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory_management.db" # in this directory create the db
engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})#One thread at a time

SessionLocal = sessionmaker(autocommit=False,bind=engine,autoflush=False)

base = declarative_base()