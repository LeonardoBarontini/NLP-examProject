"""
Main module from where the global execution starts and is handeled.
"""

from RX_database_class import RXinstance


RXdata = RXinstance('RXlist_data.json')
RXdata.create_main_lists()
RXdata.create_main_dicts()
RXdata.create_drug_list()
RXdata.create_drug_dict()
RXdata.create_relation_dicts()
RXdata.create_RXdatabase('RXdata.db')
RXdata.populate()



