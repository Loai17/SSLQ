from random import *
from os import listdir, path
from dateutil.relativedelta import relativedelta

from model import *

# LOCAL
engine = create_engine('sqlite:///database.db')
is_postgres = False

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

# Reset the database
print ('\nDeleted:')
for tablename in Base.metadata.tables.keys():
    print ('    - ' + str(session.query(eval(tablename)).delete()) + ' ' + tablename + '.')

if is_postgres:
    session.execute("ALTER SEQUENCE business_id_seq RESTART WITH 1;")
    session.execute("ALTER SEQUENCE question_id_seq RESTART WITH 1;")

#Add all manual/tester database objects

session.commit()


print ('\nCreated:')
for tablename in Base.metadata.tables.keys():
    print ('    - ' + str(len(session.query(eval(tablename)).all())) + ' ' + tablename + '.')

print ('\n\t===\tDatabase initialized.\t===\n')
