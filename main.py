"""
Main module from where the global execution starts and is handeled.
"""

from time import time
from datetime import datetime

from RX_database_class import RX_instance
from disgenet_database_class import Disgenet_instance
from stargate import Stargate_to_SNAP




print(
      """
      #########   Loading SNAP data   #########
      """
      )
start = time()
print(datetime.fromtimestamp(start).time())


stargate = Stargate_to_SNAP()


end = time()
print('\rfinished loading in '+str(end-start)+' seconds')
###################### RX-SNAP overlapping
print(
      """
      #########   Loading RX data   #########
      """
      )
start = time()
print(datetime.fromtimestamp(start).time())


RXdata = RX_instance('RXlist_data.json')
RXdata.create_main_lists()
RXdata.create_main_dicts()
RXdata.create_drug_list()
RXdata.create_drug_dict()
RXdata.create_relation_dicts()
RXdata.create_RX_database('RXdata.db')
RXdata.populate()


end = time()
print('\rfinished loading in '+str(end-start)+' seconds')
print("""\n---> starting RX-SNAP overlapping""")
start = time()
print(datetime.fromtimestamp(start).time())


RX_to_SNAP_links, check_dict = stargate.disease_stargate_link_with_check(RXdata.id_diseases_dict, progress=True)


end = time()
print('\rfinished loading in '+str(end-start)+' seconds')
print("""\n---> finished RX-SNAP overlapping""")

count=0
for key, el in RX_to_SNAP_links.items():
    if el == ['']:
        pass
    else:
        count+=1
total = len(RXdata.id_diseases_dict)
over = (count/total)*100
overlap = int((count/total)*100)
print('overlap between RXdata and SNAPdata: '+str(overlap)+'%')
print(over)

lisa1=[]     #the ones left unlinked
for key, el in check_dict.items():
    if el == ['']:
        lisa1.append(key)

############################## disgenet-SNAP overlapping
print(
      """
      #########   Loading disgenet data   #########
      """
      )
start = time()
print(datetime.fromtimestamp(start).time())


DisgenetData = Disgenet_instance('disgenet_2020.db')
DisgenetData.create_disease_dict()

end = time()
print('\rfinished loading in '+str(end-start)+' seconds')
print("""\n---> starting disgenet-SNAP overlapping""")
start = time()
print(datetime.fromtimestamp(start).time())


disgenet_to_SNAP_links, check_dict = stargate.disease_stargate_link_with_check(DisgenetData.disease_dictionary, progress=True)


end = time()
print('\rfinished loading in '+str(end-start)+' seconds')
print("""\n---> finished disgenet-SNAP overlapping""")


count=0
for key, el in disgenet_to_SNAP_links.items():
    if el == ['']:
        pass
    else:
        count+=1
total = len(DisgenetData.disease_dictionary)
over = (count/total)*100
overlap = int((count/total)*100)
print('overlap between disgenetData and SNAPdata: '+str(overlap)+'%')
print(over)

lisa2=[]     #the ones left unlinked
for key, el in check_dict.items():
    if el == ['']:
        lisa2.append(key)


