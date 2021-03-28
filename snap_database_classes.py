from nltk.tokenize import word_tokenize
import pandas
from managment_functions import format_string
from nlp import taboo_words


class D_MeshMiner_miner_disease_instance:
    """
    data loader for 'D-MeshMiner_miner-disease.tsv' SNAP table
    """
    #placeholder_general_variable = True

    def __init__(self):#, tsv_table):
        """
        loads the table in a pandas dataframe
        """
        self.dataframe = pandas.read_table('D-MeshMiner_miner-disease.tsv')

    def create_disease_name_synonyms_dicts(self):
        """
        return a dictionary in the form {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'and', 'synonyms'}}
        """
        dict_of_sets = {}
        for index, row in self.dataframe.iterrows():
            entry_set = set()
            synonyms_list = []
            name = row['Name']
            name_word_list = word_tokenize(format_string(name, boosted=True))
            for x in name_word_list:
                entry_set.add(x)
            if type(row['Synonyms']) is str:
                synonyms_list = row['Synonyms'].split('|')
                word_list=[]
                for string in synonyms_list:
                    formatted = format_string(string, boosted=True)
                    word_list.extend(word_tokenize(formatted))
                for x in word_list:
                    entry_set.add(x)
            entry_set.difference_update(taboo_words)
            dict_of_sets[name] = entry_set
        return dict_of_sets
    
    def create_disease_name_description_dicts(self):
        """
        return a dictionary in the form {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'and', 'definition'}}
        """
        dict_of_sets = {}
        for index, row in self.dataframe.iterrows():
            entry_set = set()
            description_list = []
            name = row['Name']
            name_word_list = word_tokenize(format_string(name, boosted=True))
            for x in name_word_list:
                entry_set.add(x)
            if type(row['Definitions']) is str:
                description_list = word_tokenize(format_string(row['Definitions'], boosted=True))
                for x in description_list:
                    entry_set.add(x)
            entry_set.difference_update(taboo_words)
            dict_of_sets[name] = entry_set
        return dict_of_sets









