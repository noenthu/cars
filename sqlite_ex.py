import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Makes(Base):
    __tablename__ = 'makes'
    # Here we define columns for the table make
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

class Models(Base):
    __tablename__ = 'models'
    # Here we define the columns for table models
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    make_id = Column(Integer, ForeignKey('makes.id'))
    make = relationship(Makes)
    year = Column(String(30), nullable=False)

engine = create_engine('sqlite:///sqlalchemy_example.db')

Base.metadata.create_all(engine)
