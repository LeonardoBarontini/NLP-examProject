"""
Module containing the Disgenet_instance class wich handles the disgenet-database.
"""

import sqlite3
import pandas


class Disgenet_instance:
    """
    Disgenet-database handling class.
    Acquires data from the database in the working directory, the database name is passed
    as parameter in the __init__ method.
    By default only the diseaseAttributes table is loaded, the other tables are managed
    using the load and unload methods. This is to not overload memory as data are stored
    in the class instance for quick access.
    A loaded table is saved as a pandas.read_sql_query dataframe in the respective
    self.table_name attribute. An unloaded table has the respective attribute set to None.
    For computation processes, disease and gene dictionaries are created respectively
    with create_disease_dict and create_gene_dict methods.
    
    Methods defined here:
        
        __init__(self, database_name)
            Initialize self.
            
        load_disease2class_table(self)
            loads the disease2class table.
            
        unload_disease2class_table(self)
            unloads the disease2class table.
            
        load_diseaseAttributes_table(self)
            loads the diseaseAttributes table.
            
        unload_diseaseAttributes_table(self)
            unloads the diseaseAttributes table.
            
        load_diseaseClass_table(self)
            loads the diseaseClass table.
            
        unload_diseaseClass_table(self)
            unloads the diseaseClass table.
            
        load_geneAttributes_table(self)
            loads the geneAttributes table.
            
        unload_geneAttributes_table(self)
            unloads the geneAttributes table.
            
        load_geneDiseaseNetwork_table(self)
            loads the geneDiseaseNetwork table.
            
        unload_geneDiseaseNetwork_table(self)
            unloads the geneDiseaseNetwork table.
            
        load_variantAttributes_table(self)
            loads the variantAttributes table.
            
        unload_variantAttributes_table(self)
            unloads the variantAttributes table.
            
        load_variantDiseaseNetwork_table(self)
            loads the variantDiseaseNetwork table.
            
        unload_variantDiseaseNetwork_table(self)
            unloads the variantDiseaseNetwork table.
            
        load_variantGene_table(self)
            loads the variantGene table.
            
        unload_variantGene_table(self)
            unloads the variantGene table.
            
        create_disease_list(self)
            creates a list af diseases from self.diseaseAttributes
            
        create_disease_dict(self)
            creates a {'diseaseNID':'diseaseName'} dictionary from self.diseaseAttributes
            
        create_gene_dict(self)
            creates a {'geneNID':('geneName', 'geneDescription')} dictionary from self.geneAttributes
    """
    #placeholder_general_variable = True

    def __init__(self, database_name):
        """
        Initializer method.
        
        >>> instance = Disgenet_instance("disgenet_2020.db")
        >>> instance
        <disgenet_database_class.Disgenet_instance at 0x7f279a3a12b0>
        
        First estabilishes the connection with the database using the database_name
        passed as argument.
        Then creates all the attributes where the database tables will be loaded.
        Finally only the diseaseAttributes table is loaded, for memory sake.
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
        """
        Loader method for the named table.
        It reads from the database and save the table in the respective class attribute.
        """
        self.disease2class = pandas.read_sql_query("SELECT * FROM disease2class", self.database)

    def unload_disease2class_table(self):
        """
        Unloader method for the named table.
        Sets the respective class attribute to None.
        """
        self.disease2class = None

    def load_diseaseAttributes_table(self):
        """
        Loader method for the named table.
        It reads from the database and save the table in the respective class attribute.
        """
        self.diseaseAttributes = pandas.read_sql_query("SELECT * FROM diseaseAttributes", self.database)

    def unload_diseaseAttributes_table(self):
        """
        Unloader method for the named table.
        Sets the respective class attribute to None.
        """
        self.diseaseAttributes = None

    def load_diseaseClass_table(self):
        """
        Loader method for the named table.
        It reads from the database and save the table in the respective class attribute.
        """
        self.diseaseClass = pandas.read_sql_query("SELECT * FROM diseaseClass", self.database)

    def unload_diseaseClass_table(self):
        """
        Unloader method for the named table.
        Sets the respective class attribute to None.
        """
        self.diseaseClass = None

    def load_geneAttributes_table(self):
        """
        Loader method for the named table.
        It reads from the database and save the table in the respective class attribute.
        """
        self.geneAttributes = pandas.read_sql_query("SELECT * FROM geneAttributes", self.database)

    def unload_geneAttributes_table(self):
        """
        Unloader method for the named table.
        Sets the respective class attribute to None.
        """
        self.geneAttributes = None

    def load_geneDiseaseNetwork_table(self):
        """
        Loader method for the named table.
        It reads from the database and save the table in the respective class attribute.
        """
        self.geneDiseaseNetwork = pandas.read_sql_query("SELECT * FROM geneDiseaseNetwork", self.database)

    def unload_geneDiseaseNetwork_table(self):
        """
        Unloader method for the named table.
        Sets the respective class attribute to None.
        """
        self.geneDiseaseNetwork = None

    def load_variantAttributes_table(self):
        """
        Loader method for the named table.
        It reads from the database and save the table in the respective class attribute.
        """
        self.variantAttributes = pandas.read_sql_query("SELECT * FROM variantAttributes", self.database)

    def unload_variantAttributes_table(self):
        """
        Unloader method for the named table.
        Sets the respective class attribute to None.
        """
        self.variantAttributes = None

    def load_variantDiseaseNetwork_table(self):
        """
        Loader method for the named table.
        It reads from the database and save the table in the respective class attribute.
        """
        self.variantDiseaseNetwork = pandas.read_sql_query("SELECT * FROM variantDiseaseNetwork", self.database)

    def unload_variantDiseaseNetwork_table(self):
        """
        Unloader method for the named table.
        Sets the respective class attribute to None.
        """
        self.variantDiseaseNetwork = None

    def load_variantGene_table(self):
        """
        Loader method for the named table.
        It reads from the database and save the table in the respective class attribute.
        """
        self.variantGene = pandas.read_sql_query("SELECT * FROM variantGene", self.database)

    def unload_variantGene_table(self):
        """
        Unloader method for the named table.
        Sets the respective class attribute to None.
        """
        self.variantGene = None


    def create_disease_list(self):
        """
        Creates a list of diseases from the diseaseAttributes table of the database.
        Then creates the class attribute disease_list and saves there the list.
        
        >>> instance.create_disease_list()
        >>> instance.disease_list
        ['disease1', 'disease2', 'disease_n']
        
        Note that before calling this method, the attribute does not exists.
        
        >>> instance = Disgenet_instance("disgenet.db")
        >>> instance.disease_list
        AttributeError: 'Disgenet_instance' object has no attribute 'disease_list'
        """
        self.disease_list = []
        target = self.diseaseAttributes['diseaseName']
        self.disease_list = list(target)

    def create_disease_dict(self):
        """
        Creates a dictionary of diseasesNID:diseaseName from the diseaseAttributes table
        of the database, saving it in the class attribute disease_dictionary.
        
        >>> instance.create_disease_dict()
        >>> instance.disease_dictionary
        {'1':'disease1', '2':'disease2', 'n':'disease_n'}
        
        Note that before calling this method, the attribute does not exists.
        
        >>> instance = Disgenet_instance("disgenet.db")
        >>> instance.disease_dictionary
        AttributeError: 'Disgenet_instance' object has no attribute 'disease_dictionary'
        """
        self.disease_dictionary = {}
        for index, row in self.diseaseAttributes.iterrows():
            self.disease_dictionary[row['diseaseNID']]=row['diseaseName']
    
    def create_gene_dict(self):
        """
        Creates a dictionary of geneNID:(geneName, geneDescription) from the diseaseAttributes
        table of the database, saving it in the class attribute gene_dictionary.
        
        >>> instance.create_gene_dict()
        >>> instance.gene_dictionary
        {'1':('gene1', 'desc1'), '2':('gene2', 'desc2'), 'n':('geneN', 'descN')}
        
        Note that before calling this method, the attribute does not exists.
        
        >>> instance = Disgenet_instance("disgenet.db")
        >>> instance.gene_dictionary
        AttributeError: 'Disgenet_instance' object has no attribute 'gene_dictionary'
        """
        self.gene_dictionary = {}
        for index, row in self.geneAttributes.iterrows():
            self.gene_dictionary[row['geneNID']]=(row['geneName'], row['geneDescription'])
    
    
    
    
    
    
    