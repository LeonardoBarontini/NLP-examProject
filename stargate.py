import sys
import datetime
from nlp import best_match
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()

from snap_database_classes import D_MeshMiner_miner_disease_instance


class Stargate_to_SNAP_diseases:
    """
    Stargate class that handles the creation of connections with the SNAP table(s)
    """
    def __init__(self):#, SNAP_tsv_file):
        self.SNAP_data = D_MeshMiner_miner_disease_instance()#'D-MeshMiner_miner-disease.tsv')
        self.dis_synon_dicts = self.SNAP_data.create_disease_name_synonyms_dicts()
        self.dis_desc_dicts = self.SNAP_data.create_disease_name_description_dicts()
        self.dis_name_only_dict = self.SNAP_data.create_disease_name_only_dicts()

    def disease_stargate_link_with_check(self, start_link_dict, progress=False):
        """
        connects disease_id with the SNAP disease_id (MESH_ID)
        returns it in the form {'starting_disease_id': ['list_of', 'SNAP_MESH_ID']}
        start_link_dict is a dictionary in the form {'id': 'name_string'}
        the method uses the dictionaries of sets created by the SNAP_data_instance
        also with check dictionary {'disease_name': ['list_of_dis_names']} and optional progress percentage
        """
        check_dict={}
        stargate_link_to_SNAP = {}
        start_link = start_link_dict.items()
        end_link = self.dis_synon_dicts
        end_link2 = self.dis_desc_dicts
        end_link3 = self.dis_name_only_dict
        if progress:
            count=0
            total=len(start_link)
            perc= int(total/100)
        
        for ID, disease in start_link:
            disease_word_list = word_tokenize(disease)
            best_list = best_match(disease_word_list, end_link)
            if best_list == ['']:      #no match? try this please [this increases overlapping by 16% in RX->SNAP]
                best_list = best_match(disease_word_list, end_link2)
            if best_list == ['']:      #still no match? what abount this?!  [+0.5%_RX-SNAP]
                stemmed_disease_list = []
                for word in disease_word_list:
                    stemmed_disease_list.append(ps.stem(word))
                best_list = best_match(stemmed_disease_list, end_link2, stemmed=True)
            if best_list == ['']:      #yet no match? what abount this!!!  [+8%_RX-SNAP]
                stemmed_disease_list = []
                for word in disease_word_list:
                    stemmed_disease_list.append(ls.stem(word))
                best_list = best_match(stemmed_disease_list, end_link2, stemmed=True)
            if best_list == ['']:      #you refuse match?! then get this!!!  [+0.3%_RX-SNAP]
                stemmed_disease_list = []
                for word in disease_word_list:
                    stemmed_disease_list.append(ls.stem(word))
                best_list = best_match(stemmed_disease_list, end_link, stemmed=True)
            if best_list == ['']:      #let's get back the mono named diseases  [+2%_RX-SNAP]
                best_list = best_match(disease_word_list, end_link3, mono=True)
            if best_list == ['']:      #I sed let's get them back!      [+2%_RX-SNAP]
                stemmed_disease_list = []
                for word in disease_word_list:
                    stemmed_disease_list.append(ls.stem(word))
                best_list = best_match(stemmed_disease_list, end_link3, stemmed=True, mono=True)
            
            if best_list == ['']:      #ok i give up.... no match for you
                    check_dict[disease]=['']
                    stargate_link_to_SNAP[ID]=['']
            else:
                id_list_of_best = []
                for bst in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['Name'] == bst]['# MESH_ID'].values[0])
                check_dict[disease]=best_list
                stargate_link_to_SNAP[ID]=id_list_of_best
            if progress:
                count+=1
                if count%perc==0: sys.stdout.write('\r'+str(count)+'/'+str(total)+': '+str(int((count/total)*100))+'% at '+str(datetime.datetime.now().time()))

        return stargate_link_to_SNAP, check_dict


    def disease_stargate_link(self, start_link_dict):
        """
        connects disease_id with the SNAP disease_id (MESH_ID)
        returns it in the form {'starting_disease_id': ['list_of', 'SNAP_MESH_ID']}
        start_link_dict is a dictionary in the form {'id': 'name_string'}
        the method uses the dictionaries of sets created by the SNAP_data_instance
        """
        stargate_link_to_SNAP = {}
        start_link = start_link_dict.items()
        end_link = self.dis_synon_dicts
        end_link2 = self.dis_desc_dicts
        
        for ID, disease in start_link:
            best_list = []
            disease_word_list = word_tokenize(disease)
            best = best_match(disease_word_list, end_link)
            if best == '':      #no match? try this please [this increases overlapping by 16% in RX->SNAP]
                best = best_match(disease_word_list, end_link2)
            if best == '':      #still no match? what abount this?!  [+0.5%_RX-SNAP]
                stemmed_disease_list = []
                for word in disease_word_list:
                    stemmed_disease_list.append(ps.stem(word))
                best = best_match(stemmed_disease_list, end_link2, stemmed=True)
            if best == '':      #yet no match? what abount this!!!  [+8%_RX-SNAP]
                stemmed_disease_list = []
                for word in disease_word_list:
                    stemmed_disease_list.append(ls.stem(word))
                best = best_match(stemmed_disease_list, end_link2, stemmed=True)
            if best == '':      #you refuse match?! then get this!!!  [+0.3%_RX-SNAP]
                stemmed_disease_list = []
                for word in disease_word_list:
                    stemmed_disease_list.append(ls.stem(word))
                best = best_match(stemmed_disease_list, end_link, stemmed=True)
            
            if best == '':      #ok i give up.... no match for you
                    stargate_link_to_SNAP[ID]=['']
            else:
                if type(best)==str:
                    best_list.append(best)
                else:
                    best_list.extend(best)
                id_list_of_best = []
                for bst in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['Name'] == bst]['# MESH_ID'].values[0])
                stargate_link_to_SNAP[ID]=id_list_of_best

        return stargate_link_to_SNAP   
            
            
            
            
            
            
            
            
            
            
            