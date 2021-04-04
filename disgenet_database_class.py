"""
module containing the Disgenet_instance class wich handles the disgenet-database
"""

import pandas
import sqlite3
from nltk.stem import PorterStemmer
ps = PorterStemmer()

class Disgenet_instance:
    """
    disgenet-database class
    acquires data from the digenet_current.db in the working directory.
    also keeps the data in the instance of the object.
    """
    #placeholder_general_variable = True

    def __init__(self, database_name):
        """
        by default, after estabilishing the connection, only the diseaseAttributes table is loaded, for memory sake.
        """
        self.database = sqlite3.connect(database_name)
        self.disease2class = None
        self.diseaseAttributes = pandas.read_sql_query("SELECT * FROM diseaseAttributes", self.database)
        self.diseaseClass = None
        self.geneAttributes = None
        self.geneDiseaseNetwork = None
        self.variantAttributes = None
        self.variantDiseaseNetwork = None
        self.variantGene = None
        
    def load_disease2class_table(self):
        self.disease2class = pandas.read_sql_query("SELECT * FROM disease2class", self.database)

    def unload_disease2class_table(self):
        self.disease2class = None

    def load_diseaseAttributes_table(self):
        self.diseaseAttributes = pandas.read_sql_query("SELECT * FROM diseaseAttributes", self.database)

    def unload_diseaseAttributes_table(self):
        self.diseaseAttributes = None

    def load_diseaseClass_table(self):
        self.diseaseClass = pandas.read_sql_query("SELECT * FROM diseaseClass", self.database)

    def unload_diseaseClass_table(self):
        self.diseaseClass = None

    def load_geneAttributes_table(self):
        self.geneAttributes = pandas.read_sql_query("SELECT * FROM geneAttributes", self.database)

    def unload_geneAttributes_table(self):
        self.geneAttributes = None

    def load_geneDiseaseNetwork_table(self):
        self.geneDiseaseNetwork = pandas.read_sql_query("SELECT * FROM geneDiseaseNetwork", self.database)

    def unload_geneDiseaseNetwork_table(self):
        self.geneDiseaseNetwork = None

    def load_variantAttributes_table(self):
        self.variantAttributes = pandas.read_sql_query("SELECT * FROM variantAttributes", self.database)

    def unload_variantAttributes_table(self):
        self.variantAttributes = None

    def load_variantDiseaseNetwork_table(self):
        self.variantDiseaseNetwork = pandas.read_sql_query("SELECT * FROM variantDiseaseNetwork", self.database)

    def unload_variantDiseaseNetwork_table(self):
        self.variantDiseaseNetwork = None

    def load_variantGene_table(self):
        self.variantGene = pandas.read_sql_query("SELECT * FROM variantGene", self.database)

    def unload_variantGene_table(self):
        self.variantGene = None


    def create_disease_list(self):
        target = self.diseaseAttributes['diseaseName']
        self.disease_list = list(target)

    def create_disease_dict(self):
        self.disease_dictionary = {}
        for index, row in self.diseaseAttributes.iterrows():
            self.disease_dictionary[row['diseaseNID']]=row['diseaseName']
    
    def create_gene_dict(self):
        self.gene_dictionary = {}
        for index, row in self.geneAttributes.iterrows():
            self.gene_dictionary[row['geneNID']]=(row['geneName'], row['geneDescription'])
    
    
    
    
    
    
    