"""
Main module from where the global execution starts and is handeled.
"""

from time import time

from managment_functions import start_timer_at, stop_timer_at, check_overlap_percentage
from managment_functions import check_unlinked, create_tsv_table_file
from RX_database_class import RX_instance
from disgenet_database_class import Disgenet_instance
from stargate import Stargate_to_SNAP_diseases




print(
      """
      #########   Processing SNAP data   #########
      """
      )
start = start_timer_at(time())


stargateD = Stargate_to_SNAP_diseases()


end = stop_timer_at(time(),start)
###################### RX-SNAP overlapping
print(
      """
      #########   Processing RX data   #########
      """
      )
print("""\n---> start loading RX-data""")
start = start_timer_at(time())


RXdata = RX_instance('RXlist_data.json')
RXdata.process('Stargate_big_database.db')


end = stop_timer_at(time(),start)
print("""\n---> starting RX-SNAP disease overlapping""")
start = start_timer_at(time())


RX_to_SNAP_disease_links, check_dict = stargateD.disease_stargate_link_with_check(RXdata.id_diseases_dict, progress=True)


end = stop_timer_at(time(),start)
check_overlap_percentage(RXdata.id_diseases_dict, 'RXdata', RX_to_SNAP_disease_links, 'SNAPdata diseases', precise=True)
lisa1 = check_unlinked(check_dict)
create_tsv_table_file('RXdis-links.tsv', check_dict)


print("""\n---> starting RX-SNAP symptom overlapping""")
start = start_timer_at(time())


RX_to_SNAP_symptom_links, check_dict = stargateD.disease_stargate_link_with_check(RXdata.id_symptoms_dict, progress=True)


end = stop_timer_at(time(),start)
check_overlap_percentage(RXdata.id_symptoms_dict, 'RXdata', RX_to_SNAP_symptom_links, 'SNAPdata symptom', precise=True)
lisa2 = check_unlinked(check_dict)
create_tsv_table_file('RXsym-links.tsv', check_dict)



############################## disgenet-SNAP overlapping
print(
      """
      #########   Processing disgenet data   #########
      """
      )
print("""\n---> start loading DisgenetData""")
start = start_timer_at(time())


DisgenetData = Disgenet_instance('disgenet_2020.db')
DisgenetData.create_disease_dict()

end = stop_timer_at(time(),start)
print("""\n---> starting disgenet-SNAP disease overlapping""")
start = start_timer_at(time())


disgenet_to_SNAP_links, check_dict = stargateD.disease_stargate_link_with_check(DisgenetData.disease_dictionary, progress=True)


end = stop_timer_at(time(),start)
check_overlap_percentage(DisgenetData.disease_dictionary, 'disgenetData', disgenet_to_SNAP_links, 'SNAPdata diseases')
lisa3 = check_unlinked(check_dict)
create_tsv_table_file('disgenet-links.tsv', check_dict)








