"""
Main module from where the global execution starts and is handeled.
"""

from time import time
from datetime import datetime

from RX_database_class import RX_instance
from disgenet_database_class import Disgenet_instance
from stargate import Stargate_to_SNAP_diseases




print(
      """
      #########   Processing SNAP data   #########
      """
      )
start = time()
print(datetime.fromtimestamp(start).time())


stargateD = Stargate_to_SNAP_diseases()


end = time()
print('\rfinished loading in '+str(end-start)+' seconds')
###################### RX-SNAP overlapping
print(
      """
      #########   Processing RX data   #########
      """
      )
print("""\n---> start loading RX-data""")
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

print("""\n---> starting RX-SNAP disease overlapping""")
start = time()
print(datetime.fromtimestamp(start).time())


RX_to_SNAP_disease_links, check_dict = stargateD.disease_stargate_link_with_check(RXdata.id_diseases_dict, progress=True)


end = time()
print('\rfinished loading in '+str(end-start)+' seconds')

count=0
for key, el in RX_to_SNAP_disease_links.items():
    if el == ['']:
        pass
    else:
        count+=1
total = len(RXdata.id_diseases_dict)
over = (count/total)*100
overlap = int((count/total)*100)
print('overlap between RXdata and SNAPdata diseases: '+str(overlap)+'%')
print(over)

lisa1=[]     #the ones left unlinked
for key, el in check_dict.items():
    if el == ['']:
        lisa1.append(key)

print("""\n---> starting RX-SNAP symptom overlapping""")
start = time()
print(datetime.fromtimestamp(start).time())


RX_to_SNAP_symptom_links, check_dict = stargateD.disease_stargate_link_with_check(RXdata.id_symptoms_dict, progress=True)


end = time()
print('\rfinished loading in '+str(end-start)+' seconds')

count=0
for key, el in RX_to_SNAP_symptom_links.items():
    if el == ['']:
        pass
    else:
        count+=1
total = len(RXdata.id_symptoms_dict)
over = (count/total)*100
overlap = int((count/total)*100)
print('overlap between RXdata and SNAPdata symptom: '+str(overlap)+'%')
print(over)

lisa1=[]     #the ones left unlinked
for key, el in check_dict.items():
    if el == ['']:
        lisa1.append(key)


############################## disgenet-SNAP overlapping
# print(
#       """
#       #########   Processing disgenet data   #########
#       """
#       )
# print("""\n---> start loading DisgenetData""")
# start = time()
# print(datetime.fromtimestamp(start).time())


# DisgenetData = Disgenet_instance('disgenet_2020.db')
# DisgenetData.create_disease_dict()

# end = time()
# print('\rfinished loading in '+str(end-start)+' seconds')
# print("""\n---> starting disgenet-SNAP disease overlapping""")
# start = time()
# print(datetime.fromtimestamp(start).time())


# disgenet_to_SNAP_links, check_dict = stargateD.disease_stargate_link_with_check(DisgenetData.disease_dictionary, progress=True)


# end = time()
# print('\rfinished loading in '+str(end-start)+' seconds')


# count=0
# for key, el in disgenet_to_SNAP_links.items():
#     if el == ['']:
#         pass
#     else:
#         count+=1
# total = len(DisgenetData.disease_dictionary)
# over = (count/total)*100
# overlap = int((count/total)*100)
# print('overlap between disgenetData and SNAPdata diseases: '+str(overlap)+'%')
# print(over)

# lisa2=[]     #the ones left unlinked
# for key, el in check_dict.items():
#     if el == ['']:
#         lisa2.append(key)




# tsv_file = open('nomedelfile.tsv', 'w')
# tsv_file.truncate()
# tsv_file.write('# ID_start\tID_end\n')
# for id_start, list_id_end in check_dict.items():
#     for id_end in list_id_end:
#         tsv_file.write(id_start+'\t'+id_end+'\n')
# tsv_file.close()







