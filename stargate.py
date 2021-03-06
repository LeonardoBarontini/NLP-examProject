import sys
import datetime
from nlp import best_match
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()
from nltk.stem.snowball import EnglishStemmer
es = EnglishStemmer()
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

from snap_database_classes import D_MeshMiner_miner_disease_instance
from snap_database_classes import G_SynMiner_miner_geneHUGO_instance


class Stargate_to_SNAP_diseases:
    """
    Stargate class that handles the creation of connections with the SNAP table(s)
    """
    def __init__(self):
        self.SNAP_data = D_MeshMiner_miner_disease_instance()
        self.dis_synon_dicts = self.SNAP_data.create_disease_name_synonyms_dicts()
        self.dis_desc_dicts = self.SNAP_data.create_disease_name_description_dicts()
        self.dis_name_only_dict = self.SNAP_data.create_disease_name_only_dicts()

    def disease_stargate_link_with_check(self, initial_point_dict, progress=False):
        """
        connects disease_id with the SNAP disease_id (MESH_ID)
        returns it in the form {'starting_disease_id': (['list_of_SNAP_MESH_ID'], score, 'unchecked')}
        initial_point_dict must be a dictionary in the form {'id': 'name_string'}
        the method uses the dictionaries of sets created by the SNAP_data_instance
        also with check dictionary {'disease_name': ['list_of_dis_names']} and optional progress percentage
        """
        check_dict={}
        stargate_link_to_SNAP = {}
        initial_point = initial_point_dict.items()
        destination1 = self.dis_synon_dicts
        destination2 = self.dis_desc_dicts
        destination3 = self.dis_name_only_dict
        if progress:
            count=0
            total=len(initial_point)
            perc= int(total/100)
        
        for ID, disease in initial_point:
            disease_word_list = word_tokenize(disease)
            
            score, best_list = best_match(disease_word_list, destination1)
            #in the RX-SNAP network this gives overlaps for: diseases=65%, symptoms=31%
                #the following results are obtained with progressive addition to the search
                    #no match? first try this [RX-SNAP overlaps: diseases=79%(+14%), symptoms=58%(+27%)]
            if best_list == ['']:      
                stemmed_disease_list_es = []
                for word in disease_word_list:
                    stemmed_disease_list_es.append(es.stem(word))
                score, best_list = best_match(stemmed_disease_list_es, destination1, stemmed=True)
                score = str(score)+'a'
                    #and then this please [RX-SNAP overlaps: diseases=81%(+2%), symptoms=63%(+5%)]
            if best_list == ['']:      
                stemmed_disease_list_ls = []
                for word in disease_word_list:
                    stemmed_disease_list_ls.append(ls.stem(word))
                score, best_list = best_match(stemmed_disease_list_ls, destination1, stemmed=True)
                score = str(score)+'b'
                    #yet no match? what abount this!!!  [RX-SNAP overlaps: diseases=87%(+6%), symptoms=63%(+13%)]
            if best_list == ['']:
                stopped_word_list = [w for w in disease_word_list if w not in stop_words]
                score, best_list = best_match(stopped_word_list, destination2)
                score = str(score)+'c'
                    #nothing yet? what abount this one?!  [RX-SNAP overlaps: diseases=90%(+3%), symptoms=82%(+19%)]
            if best_list == ['']:      
                stopped_stemmed_disease_list_es = []
                for word in stopped_word_list:
                    stopped_stemmed_disease_list_es.append(es.stem(word))
                score, best_list = best_match(stopped_stemmed_disease_list_es, destination2, stemmed=True)
                score = str(score)+'d'
                    #And this one!!!  [RX-SNAP overlaps: diseases=91%(+1%), symptoms=85%(+3%)]
            if best_list == ['']:      
                stopped_stemmed_disease_list_ls = []
                for word in stopped_word_list:
                    stopped_stemmed_disease_list_ls.append(ls.stem(word))
                score, best_list = best_match(stopped_stemmed_disease_list_ls, destination2, stemmed=True)
                score = str(score)+'e'
                    #you refuse to match?!  [RX-SNAP overlaps: diseases=93%(+2%), symptoms=85%(+0.6%)]
            if best_list == ['']:      
                score, best_list = best_match(disease_word_list, destination3, mono=True)
                score = str(score)+'f'
                    #Let's get back the mono word ones!      [RX-SNAP overlaps: diseases=94%(+1%), symptoms=89%(+4%)]
            if best_list == ['']:
                score, best_list = best_match(stemmed_disease_list_es, destination3, stemmed=True, mono=True)
                score = str(score)+'g'
                    #I sed let's get them back!      [RX-SNAP overlaps: diseases=94%(+0.5%), symptoms=91%(+2%)]
            if best_list == ['']:
                score, best_list = best_match(stemmed_disease_list_ls, destination3, stemmed=True, mono=True)
                score = str(score)+'h'
                    #ok i give up.... no match for you
            if best_list == ['']:      
                    check_dict[disease]=([''], None,'unchecked')
                    stargate_link_to_SNAP[ID]=([''], None,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['Name'] == best]['# MESH_ID'].values[0])
                check_dict[disease]=(best_list, score,'unchecked')
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')
            if progress:
                count+=1
                if count%perc==0: sys.stdout.write('\r'+str(count)+'/'+str(total)+': '+str(int((count/total)*100))+'% at '+str(datetime.datetime.now().time()))

        return stargate_link_to_SNAP, check_dict


    def disease_stargate_link(self, initial_point_dict):
        """
        connects disease_id with the SNAP disease_id (MESH_ID)
        returns it in the form {'starting_disease_id': (['list_of_SNAP_MESH_ID'], score, 'unchecked')}
        initial_point_dict must be a dictionary in the form {'id': 'name_string'}
        the method uses the dictionaries of sets created by the SNAP_data_instance
        """
        stargate_link_to_SNAP = {}
        initial_point = initial_point_dict.items()
        destination1 = self.dis_synon_dicts
        destination2 = self.dis_desc_dicts
        destination3 = self.dis_name_only_dict
        
        for ID, disease in initial_point:
            disease_word_list = word_tokenize(disease)
            
            score, best_list = best_match(disease_word_list, destination1)
            #in the RX-SNAP network this gives overlaps for: diseases=65%, symptoms=31%
                #the following results are obtained with progressive addition to the search
                    #no match? first try this [RX-SNAP overlaps: diseases=79%(+14%), symptoms=58%(+27%)]
            if best_list == ['']:      
                stemmed_disease_list_es = []
                for word in disease_word_list:
                    stemmed_disease_list_es.append(es.stem(word))
                score, best_list = best_match(stemmed_disease_list_es, destination1, stemmed=True)
                score = str(score)+'a'
                    #and then this please [RX-SNAP overlaps: diseases=81%(+2%), symptoms=63%(+5%)]
            if best_list == ['']:      
                stemmed_disease_list_ls = []
                for word in disease_word_list:
                    stemmed_disease_list_ls.append(ls.stem(word))
                score, best_list = best_match(stemmed_disease_list_ls, destination1, stemmed=True)
                score = str(score)+'b'
                    #yet no match? what abount this!!!  [RX-SNAP overlaps: diseases=87%(+6%), symptoms=63%(+13%)]
            if best_list == ['']:
                stopped_word_list = [w for w in disease_word_list if w not in stop_words]
                score, best_list = best_match(stopped_word_list, destination2)
                score = str(score)+'c'
                    #nothing yet? what abount this one?!  [RX-SNAP overlaps: diseases=90%(+3%), symptoms=82%(+19%)]
            if best_list == ['']:      
                stopped_stemmed_disease_list_es = []
                for word in stopped_word_list:
                    stopped_stemmed_disease_list_es.append(es.stem(word))
                score, best_list = best_match(stopped_stemmed_disease_list_es, destination2, stemmed=True)
                score = str(score)+'d'
                    #And this one!!!  [RX-SNAP overlaps: diseases=91%(+1%), symptoms=85%(+3%)]
            if best_list == ['']:      
                stopped_stemmed_disease_list_ls = []
                for word in stopped_word_list:
                    stopped_stemmed_disease_list_ls.append(ls.stem(word))
                score, best_list = best_match(stopped_stemmed_disease_list_ls, destination2, stemmed=True)
                score = str(score)+'e'
                    #you refuse to match?!  [RX-SNAP overlaps: diseases=93%(+2%), symptoms=85%(+0.6%)]
            if best_list == ['']:      
                score, best_list = best_match(disease_word_list, destination3, mono=True)
                score = str(score)+'f'
                    #Let's get back the mono word ones!      [RX-SNAP overlaps: diseases=94%(+1%), symptoms=89%(+4%)]
            if best_list == ['']:
                score, best_list = best_match(stemmed_disease_list_es, destination3, stemmed=True, mono=True)
                score = str(score)+'g'
                    #I sed let's get them back!      [RX-SNAP overlaps: diseases=94%(+0.5%), symptoms=91%(+2%)]
            if best_list == ['']:
                score, best_list = best_match(stemmed_disease_list_ls, destination3, stemmed=True, mono=True)
                score = str(score)+'h'
                    #ok i give up.... no match for you
            if best_list == ['']:
                    stargate_link_to_SNAP[ID]=([''], None,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['Name'] == best]['# MESH_ID'].values[0])
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')

        return stargate_link_to_SNAP
            
            
            
class Stargate_to_SNAP_gene:
    """
    Stargate class that handles the creation of connections with the SNAP table(s)
    """
    def __init__(self):
        self.SNAP_data = G_SynMiner_miner_geneHUGO_instance()
        self.gene_sym_name_dict = self.SNAP_data.create_gene_symbol_name_dict()       
            
    def gene_stargate_link_with_check(self, initial_point_dict, progress=False):
        """
        connects gene_id with the SNAP gene_id (ensembl_gene_id)
        returns it in the form {'starting_gene_id': (['list_of_SNAP_ensembl_gene_id'], score, 'unchecked')}
        initial_point_dict must be a dictionary in the form {'id': ('name_string', 'desc_string')}
        also with check dictionary {'gene_name': ['list_of_gene_names']} and optional progress percentage
        """
        check_dict={}
        stargate_link_to_SNAP = {}
        initial_point = initial_point_dict.items()
        destination1 = self.gene_sym_name_dict
        if progress:
            count=0
            total=len(initial_point)
            perc= int(total/100)
        
        for ID, (name, desc) in initial_point:
            best_list=[]
            score = 0
            for SNAP_symbol, SNAP_name in destination1.items():
                if name==SNAP_symbol:
                    score+=1
                    if desc==SNAP_name:
                        score+=4
                        best_list.append(SNAP_symbol)
                    else:
                        best_list.append(SNAP_symbol)
                        
            if best_list == []:      
                    check_dict[name]=([''], score,'unchecked')
                    stargate_link_to_SNAP[ID]=([''], score,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['symbol'] == best]['# ensembl_gene_id'].values[0])
                check_dict[name]=(best_list, score,'unchecked')
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')
            if progress:
                count+=1
                if count%perc==0: sys.stdout.write('\r'+str(count)+'/'+str(total)+': '+str(int((count/total)*100))+'% at '+str(datetime.datetime.now().time()))

        return stargate_link_to_SNAP, check_dict


    def gene_stargate_link(self, initial_point_dict):
        """
        connects gene_id with the SNAP gene_id (ensembl_gene_id)
        returns it in the form {'starting_gene_id': (['list_of_SNAP_ensembl_gene_id'], score, 'unchecked')}
        initial_point_dict must be a dictionary in the form {'id': ('name_string', 'desc_string')}
        """
        stargate_link_to_SNAP = {}
        initial_point = initial_point_dict.items()
        destination1 = self.gene_sym_name_dict
        
        for ID, (name, desc) in initial_point:
            best_list=[]
            score = 0
            for SNAP_symbol, SNAP_name in destination1.items():
                if name==SNAP_symbol:
                    score+=1
                    if desc==SNAP_name:
                        score+=4
                        best_list.append(SNAP_symbol)
                    else:
                        best_list.append(SNAP_symbol)
                        
            if best_list == []:      
                    stargate_link_to_SNAP[ID]=([''], score,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['symbol'] == best]['# ensembl_gene_id'].values[0])
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')
           
        return stargate_link_to_SNAP
            
            
            