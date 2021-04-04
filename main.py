"""
Main module from where the global execution starts and is handeled.
"""

from time import time

from managment_functions import start_timer_at, stop_timer_at, check_overlap_percentage
from managment_functions import check_unlinked, create_tsv_table_file, create_stargate_network_table
from RX_database_class import RX_instance
from disgenet_database_class import Disgenet_instance
from stargate import Stargate_to_SNAP_diseases
from stargate import Stargate_to_SNAP_gene




print(
      """
      #########   Processing SNAP data   #########
      """
      )
start = start_timer_at(time())


stargateD = Stargate_to_SNAP_diseases()
stargateD.SNAP_data.create_SNAP_disease_table('Stargate_big_database.db')

stargateG = Stargate_to_SNAP_gene()
stargateG.SNAP_data.create_SNAP_gene_table('Stargate_big_database.db')


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
create_stargate_network_table('Stargate_big_database.db', RX_to_SNAP_disease_links, 'RX_disease_to_SNAP_disease', 'disease(serial)', 'D_MeshMiner_miner_disease(MESH_ID)')


end = stop_timer_at(time(),start)
check_overlap_percentage(RXdata.id_diseases_dict, 'RXdata', RX_to_SNAP_disease_links, 'SNAPdata diseases', precise=True)
lisa1 = check_unlinked(check_dict)
create_tsv_table_file('RXdis-links.tsv', check_dict)


print("""\n---> starting RX-SNAP symptom overlapping""")
start = start_timer_at(time())


RX_to_SNAP_symptom_links, check_dict = stargateD.disease_stargate_link_with_check(RXdata.id_symptoms_dict, progress=True)
create_stargate_network_table('Stargate_big_database.db', RX_to_SNAP_symptom_links, 'RX_symptom_to_SNAP_disease', 'symptom(serial)', 'D_MeshMiner_miner_disease(MESH_ID)')


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
create_stargate_network_table('Stargate_big_database.db', disgenet_to_SNAP_links, 'Disgenet_disease_to_SNAP_disease', 'diseaseAttributes(diseaseNID)', 'D_MeshMiner_miner_disease(MESH_ID)')


end = stop_timer_at(time(),start)
check_overlap_percentage(DisgenetData.disease_dictionary, 'disgenetData', disgenet_to_SNAP_links, 'SNAPdata diseases')
lisa3 = check_unlinked(check_dict)
create_tsv_table_file('disgenet-disease-links.tsv', check_dict)



DisgenetData.unload_diseaseAttributes_table()
DisgenetData.load_geneAttributes_table()
DisgenetData.create_gene_dict()

end = stop_timer_at(time(),start)
print("""\n---> starting disgenet-SNAP gene overlapping""")
start = start_timer_at(time())


disgenet_to_SNAP_links, check_dict = stargateG.gene_stargate_link_with_check(DisgenetData.gene_dictionary, progress=True)
create_stargate_network_table('Stargate_big_database.db', disgenet_to_SNAP_links, 'Disgenet_gene_to_SNAP_gene', 'geneAttributes(geneNID)', 'G_SynMiner_miner_geneHUGO(ensembl_gene_id)')


end = stop_timer_at(time(),start)
check_overlap_percentage(DisgenetData.gene_dictionary, 'disgenetData', disgenet_to_SNAP_links, 'SNAPdata gene')
lisa4 = check_unlinked(check_dict)
create_tsv_table_file('disgenet-gene-links.tsv', check_dict)




