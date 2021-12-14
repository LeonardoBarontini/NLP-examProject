"""
Module containing the Stargate_to_SNAP_diseases class and
Stargate_to_SNAP_gene class wich handles the Stargate-to-SNAP relation connections.
"""

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
    Stargate class that handles the creation of relations with the SNAP disease tables.
    Creates a D_MeshMiner_miner_disease_instance in self.SNAP_data to work with,
    and uses its methods to ready data for computation.
    The disease_stargate_link (also available _with_check) represents the main
    computation: given a dictionary originated from a database, connects it to
    the SNAP_disease table, going through various levels of refinement.
    
    Methods defined here:
        
        __init__(self)
            Initialize self.
        
        disease_stargate_link_with_check(self, initial_point_dict, progress=False)
            Returns a dictionary with network connections to the SNAP's
            D-MeshMiner_miner-disease table.
            Also returns a check_dict as tracking of unconnected entries.
        
        disease_stargate_link(self, initial_point_dict)
            Returns a dictionary with network connections to the SNAP's
            D-MeshMiner_miner-disease table.
    """
    def __init__(self):
        """
        Initializer method.
        
        >>> instance = Stargate_to_SNAP_diseases()
        >>> instance
        <stargate.Stargate_to_SNAP_diseases at 0x7fb0fc625fd0>
        
        Instanciates a D_MeshMiner_miner_disease_instance into self.SNAP_data.
        Uses the SNAP_data to save the computation dictionaries in the
        respective attributes:
            dictionary with name and synonims in self.dis_synon_dicts
            dictionary with name and description in self.dis_desc_dicts
            dictionary with name only in self.dis_name_only_dict
        """
        self.SNAP_data = D_MeshMiner_miner_disease_instance()
        self.dis_synon_dicts = self.SNAP_data.create_disease_name_synonyms_dicts()
        self.dis_desc_dicts = self.SNAP_data.create_disease_name_description_dicts()
        self.dis_name_only_dict = self.SNAP_data.create_disease_name_only_dicts()

    def disease_stargate_link_with_check(self, initial_point_dict, progress=False):
        """
        Method that connects a disease_id with the SNAP disease_id (MESH_ID).
        It returns a dictionary in the form:
            {'starting_disease_id': (['list','of','connected','SNAP_MESH_ID'], score, 'unchecked')}
        initial_point_dict represents the connecting database and must be
        a dictionary in the form {'id': 'name_string'}.
        The method uses the dictionaries of sets created by the SNAP_data_instance:
        for every connecting disease, first it tokenize the disease_name, then calls
        the best_match function with the tokenized name on the destination1, wich
        is the SANP's disease_name_synonyms_dict.
        After that, the method procedes to refine the computation via increasingly
        specific iterations: it starts using the EnglishStemmer and the LancasterStemmer 
        checking on destination1, then creates a stopped_word_list, checks it on destination2,
        applies the EnglishStemmer and the LancasterStemmer still checking on
        destination2, then as last hope, checks on destination3 with the mono
        option enabled, respectively with raw names, with englishStemmed-words and
        with lancasterStemmed-wors. If none of theese results in a connection,
        the entry remains unconnected (it will have an empty connection list).
        Either way, the entry is added to the stargate_link_to_SNAP output dictionary.
        The score feature keeps track of how many connections were detected and
        at wich iteration the connection was made, adding a letter at the end.
        The 'unchecked' tag symbolizes the automation process of connection and
        allows to track for human-verified connections inside the database.
        The _with_check version also returns a similar dictionary of diseases but as:
            {'disease_name': (['list','of','connected','disease','names'], score, 'unchecked')}
        Enableing the optional progress flag will print out the completion percentage
        along with the time of rilevation, for computation tracking pourpouses.
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
        
        for ID, name_string in initial_point:
            disease_word_list = word_tokenize(name_string)
            
            score, best_list = best_match(disease_word_list, destination1)
            #in the RX-to-SNAP network case this gives overlaps for: diseases=65%, symptoms=31%
            #the results are similar for the Disgenet-to-SNAP network
                #the following results are obtained with progressive addition to the search
                #the work is done targeting the entries that didn't found a match.
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
                    check_dict[name_string]=([''], None,'unchecked')
                    stargate_link_to_SNAP[ID]=([''], None,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['Name'] == best]['# MESH_ID'].values[0])
                check_dict[name_string]=(best_list, score,'unchecked')
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')
            if progress:
                count+=1
                if count%perc==0: sys.stdout.write('\r'+str(count)+'/'+str(total)+': '+str(int((count/total)*100))+'% at '+str(datetime.datetime.now().time()))

        return stargate_link_to_SNAP, check_dict


    def disease_stargate_link(self, initial_point_dict):
        """
        Method that connects a disease_id with the SNAP disease_id (MESH_ID).
        It returns a dictionary in the form:
            {'starting_disease_id': (['list','of','connected','SNAP_MESH_ID'], score, 'unchecked')}
        initial_point_dict represents the connecting database and must be
        a dictionary in the form {'id': 'name_string'}.
        The method uses the dictionaries of sets created by the SNAP_data_instance:
        for every connecting disease, first it tokenize the disease_name, then calls
        the best_match function with the tokenized name on the destination1, wich
        is the SANP's disease_name_synonyms_dict.
        After that, the method procedes to refine the computation via increasingly
        specific iterations: it starts using the EnglishStemmer and the LancasterStemmer 
        checking on destination1, then creates a stopped_word_list, checks it on destination2,
        applies the EnglishStemmer and the LancasterStemmer still checking on
        destination2, then as last hope, checks on destination3 with the mono
        option enabled, respectively with raw names, with englishStemmed-words and
        with lancasterStemmed-wors. If none of theese results in a connection,
        the entry remains unconnected (it will have an empty connection list).
        Either way, the entry is added to the stargate_link_to_SNAP output dictionary.
        The score feature keeps track of how many connections were detected and
        at wich iteration the connection was made, adding a letter at the end.
        The 'unchecked' tag symbolizes the automation process of connection and
        allows to track for human-verified connections inside the database.
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
    Stargate class that handles the creation of relations with the SNAP gene tables.
    Creates a G_SynMiner_miner_geneHUGO_instance in self.SNAP_data to work with,
    and uses its methods to ready data for computation.
    The gene_stargate_link (also available _with_check) represents the main
    computation: given a dictionary originated from a database, connects it to
    the SNAP_gene table, going through various levels of refinement.
    
    Methods defined here:
        
        __init__(self)
            Initialize self.
        
        gene_stargate_link_with_check(self, initial_point_dict, progress=False)
            Returns a dictionary with network connections to the SNAP's
            G-SynMiner_miner-geneHUGO table.
            Also returns a check_dict as tracking of unconnected entries.
        
        gene_stargate_link(self, initial_point_dict)
            Returns a dictionary with network connections to the SNAP's
            G-SynMiner_miner-geneHUGO table.
    """
    def __init__(self):
        """
        Initializer method.
        
        >>> instance = Stargate_to_SNAP_gene()
        >>> instance
        <stargate.Stargate_to_SNAP_gene at 0x7fb0fc5f5eb0>
        
        Instanciates a G_SynMiner_miner_geneHUGO_instance into self.SNAP_data.
        Uses the SNAP_data to save the computation dictionaries in the
        respective attributes:
            dictionary with name and symbol in self.gene_sym_name_dict
        """
        self.SNAP_data = G_SynMiner_miner_geneHUGO_instance()
        self.gene_sym_name_dict = self.SNAP_data.create_gene_symbol_name_dict()       
            
    def gene_stargate_link_with_check(self, initial_point_dict, progress=False):
        """        
        Method that connects a gene_id with the SNAP gene_id (ensembl_gene_id).
        It returns a dictionary in the form:
            {'starting_gene_id': (['list','of','connected','SNAP_ensembl_gene_id'], score, 'unchecked')}
        initial_point_dict represents the connecting database and must be
        a dictionary in the form {'id': ('name_string', 'desc_string')}.
        The method uses the dictionaries of sets created by the SNAP_data_instance:
        for every connecting gene, it checks the name_string and desc_string in
        the dictionary, first matching the name with the SNAP_symbol string, then
        matching the decstiption with the SNAP_name string.
        Theese string are mostly name codes, much like the database ids, so they are
        unique and do not need to be stemmed. If both name and symbol matches the
        score gets boosted. If none of theese results in a connection,
        the entry remains unconnected (it will have an empty connection list).
        Either way, the entry is added to the stargate_link_to_SNAP output dictionary.
        The score feature keeps track of how many connections were detected.        
        The 'unchecked' tag symbolizes the automation process of connection and
        allows to track for human-verified connections inside the database.
        The _with_check verion also returns a similar dictionary of genes but as:
            {'gene_name': (['list','of','connected','gene','names'], score, 'unchecked')}
        Enableing the optional progress flag will print out the completion percentage
        along with the time of rilevation, for computation tracking pourpouses.
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
        Method that connects a gene_id with the SNAP gene_id (ensembl_gene_id).
        It returns a dictionary in the form:
            {'starting_gene_id': (['list','of','connected','SNAP_ensembl_gene_id'], score, 'unchecked')}
        initial_point_dict represents the connecting database and must be
        a dictionary in the form {'id': ('name_string', 'desc_string')}.
        The method uses the dictionaries of sets created by the SNAP_data_instance:
        for every connecting gene, it checks the name_string and desc_string in
        the dictionary, first matching the name with the SNAP_symbol string, then
        matching the decstiption with the SNAP_name string.
        Theese string are mostly name codes, much like the database ids, so they are
        unique and do not need to be stemmed. If both name and symbol matches the
        score gets boosted. If none of theese results in a connection,
        the entry remains unconnected (it will have an empty connection list).
        Either way, the entry is added to the output dictionary.
        The score feature keeps track of how many connections were detected.        
        The 'unchecked' tag symbolizes the automation process of connection and
        allows to track for human-verified connections inside the database.
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
            
            
            