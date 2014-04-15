from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from getdata import Edmunds

apiKey = 'changeme'
edmunds_debug = True
make_list = []
model_year_list = []
model_styles_list = []

metadata = MetaData()
makes = Table('makes', metadata,
              Column('id', Integer, primary_key=True),
              Column('edmunds_id', Integer),
              Column('name', String)
              )

models = Table('models', metadata,
               Column('id', Integer, primary_key=True),
               Column('edmunds_id', Integer),
               Column('name', String),
               Column('make_id', None, ForeignKey('makes.id')),
               Column('year', String)
               )
trims = Table('trims', metadata,
              Column('id', Integer, primary_key=True),
              Column('edmunds_id', Integer),
              Column('name', String),
              Column('year', String),
              Column('trim', String),
              Column('model_name', String),
              Column('model_id', None, ForeignKey('models.id'))
              )

engine = create_engine('sqlite:///testdb.db', echo=True)
metadata.create_all(engine)

endpoint = '/api/vehicle/v2/makes'

api = Edmunds(apiKey, edmunds_debug)

response = api.make_call(endpoint)

for make in response['makes']:
    make_list.append(dict(edmunds_id=make['id'], name=make['name']))

for make in response['makes']:
    for model in make['models']:
        for year in model['years']:
            model_year_list.append(dict(year=year['year'], edmunds_id=year['id'], name=model['name'], make_id=make['id']))
print make_list
print model_year_list

for tmodel in make_list:
    endpoint = '/api/vehicle/v2/%s/models'%tmodel['name']
    response = api.make_call(endpoint)
    for row in response['models']:
        for year in row['years']:
            for trim in year['styles']:
                model_styles_list.append(dict(edmunds_id=trim['id'], name=trim['name'], \
                                              trim=trim['trim'],model_id=year['id'], \
                                              year=year['year'], model_name=trim['submodel']['modelName']))

for trim in model_styles_list:
    print trim

conn = engine.connect()
make_ins = makes.insert()
conn.execute(make_ins, make_list)

model_ins = models.insert()
conn.execute(model_ins, model_year_list)

trim_ins = trims.insert()
conn.execute(trim_ins, model_styles_list)

s = select([makes])
result = conn.execute(s)
for row in result:
    print row
s = select([models])
result = conn.execute(s)
for row in result:
    print '----- \n'
    print row
s = select([trims])
result = conn.execute(s)
for row in result:
    print '****** \n'
    print row
