from sqlite_database_populator import *


database = Instanciator('RXdata.db', 'RXlist_data.json', '_symptoms_and_signs')

database.populate()







