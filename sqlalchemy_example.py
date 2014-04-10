from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlite_ex import Makes, Models, Base

engine = create_engine('sqlite:///sqlalchemy_example.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

new_make = Makes(name='TEST')
session.add(new_make)
session.commit()

new_model = Models(name='this', year='2013', make=new_make)
session.add(new_model)
session.commit()
