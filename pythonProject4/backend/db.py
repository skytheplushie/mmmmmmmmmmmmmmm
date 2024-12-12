from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('sqlite:///app/taskmanager.db')
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass