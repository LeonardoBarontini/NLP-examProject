"""
Main module from where the global execution starts and is handeled.
"""

import datetime

from RX_database_class import RX_instance
from disgenet_database_class import Disgenet_instance
from snap_database_classes import D_MeshMiner_miner_disease_instance


RXdata = RX_instance('RXlist_data.json')
RXdata.create_main_lists()
RXdata.create_main_dicts()
RXdata.create_drug_list()
RXdata.create_drug_dict()
RXdata.create_relation_dicts()
RXdata.create_RX_database('RXdata.db')
RXdata.populate()



DisgenetData = Disgenet_instance('disgenet_2020.db')
DisgenetData.create_disease_list()



SnapData = D_MeshMiner_miner_disease_instance('D-MeshMiner_miner-disease.tsv')
Dis_synon_lists = SnapData.create_disease_name_synonyms_list()

print(datetime.datetime.now().time())