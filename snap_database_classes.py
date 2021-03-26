
import pandas


class D_MeshMiner_miner_disease_instance:
    """
    """
    #placeholder_general_variable = True

    def __init__(self, tsv_table):
        self.dataframe = pandas.read_table('D-MeshMiner_miner-disease.tsv')

    def create_disease_name_synonyms_list(self):
        list_of_lists = []
        for row in self.dataframe.iterrows():
            entry_list = []
            synonyms_list = []
            entry_list.append(row[1][1])
            if type(row[1][3]) is str:
                synonyms_list = row[1][3].split('|')
            entry_list.extend(synonyms_list)
            list_of_lists.append(entry_list)
        return list_of_lists

