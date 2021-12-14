"""
Module containing the D_MeshMiner_miner_disease_instance class and
G_SynMiner_miner_geneHUGO_instance class wich handles the SNAP-database's tables.
"""

import sqlite3
from nltk.tokenize import word_tokenize
import pandas
from managment_functions import format_string
from nlp import taboo_words


class D_MeshMiner_miner_disease_instance:
    """    
    'D-MeshMiner_miner-disease.tsv' SNAP table handling class.
    Acquires data from the .tsv file in the working directory, the filename is 
    supposed to be static and is hardcoded in the __init__ method.
    The loaded table is saved as a pandas.read_table dataframe in the respective
    self.dataframe attribute.
    The create_SNAP_disease_table_in method gives you the possibility to add the
    SNAP table to an existing database.
    For computation processes, dictionaries of sets of words related to a specific
    disease_name, are created with create_disease_name_synonyms_dicts method
    from the Name and Synonyms columns, with create_disease_name_description_dicts
    method from the Name and Definitions columns and with create_disease_name_only_dicts
    method from the Name column only.
    
    Methods defined here:
        
        __init__(self)
            Initialize self.
        
        create_SNAP_disease_table_in(self, database_name)
            add the SNAP table to an existing database.
        
        create_disease_name_synonyms_dicts(self)
            return a dictionary in the form
            {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'and', 'synonyms'}}
        
        create_disease_name_description_dicts(self)
            return a dictionary in the form
            {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'and', 'definition'}}
        
        create_disease_name_only_dicts(self)
            return a dictionary in the form
            {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'only'}}
    """
    #placeholder_general_variable = True

    def __init__(self):#, tsv_table):
        """
        Initializer method.
        
        >>> instance = D_MeshMiner_miner_disease_instance()
        >>> instance
        <snap_database_classes.D_MeshMiner_miner_disease_instance at 0x7ff40822e250>
        
        Loads the 'D-MeshMiner_miner-disease.tsv' table in a pandas dataframe
        wich is stored in the self.dataframe attribute.
        The table is composed of four columns: 
            column 1: the ID reference of the disease
            column 2: the Name of the disease
            column 3: the Definitions, characterizing the disease
            column 4: the Synonyms, other known names of the disease
        """
        self.dataframe = pandas.read_table('D-MeshMiner_miner-disease.tsv')
        
    def create_SNAP_disease_table_in(self, database_name):
        """
        Creates a new table (or updates the existing one) in the passed database,
        populating it with the 'D-MeshMiner_miner-disease.tsv' informations.
        The created table in the database will have the name D_MeshMiner_miner_disease.
        The table is composed of four columns: 
            column 1: the ID reference of the disease
            column 2: the Name of the disease
            column 3: the Definitions, characterizing the disease
            column 4: the Synonyms, other known names of the disease
        """
        self.database = sqlite3.connect(database_name)
        self.c = self.database.cursor()
        self.c.execute("DROP TABLE IF EXISTS D_MeshMiner_miner_disease;")
        self.c.execute("CREATE TABLE IF NOT EXISTS D_MeshMiner_miner_disease(MESH_ID TEXT PRIMARY KEY NOT NULL, Name TEXT, Definitions TEXT, Synonyms TEXT);")
        for index, row in self.dataframe.iterrows():
            self.c.execute("INSERT OR IGNORE INTO D_MeshMiner_miner_disease (MESH_ID, Name, Definitions, Synonyms) VALUES(?,?,?,?);",(row['# MESH_ID'], row['Name'], row['Definitions'], row['Synonyms']))
        self.database.commit()
        self.database.close()
        return 'Done'

    def create_disease_name_synonyms_dicts(self):
        """
        Returns a dictionary in the form
        {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'and', 'synonyms'}}
        
        The set is populated with words from the 'Name' and 'Synonyms' columns;
        it is accessed by the corresponding disease_name.
        
        Given
               Name                Synonyms
        0  disease1   dis1|d1|first disease
        1  disease2  dis2|d2|second disease
        
        We have
        >>> instance.create_disease_name_synonyms_dicts()
        {'disease1': {'d1', 'dis1', 'disease', 'disease1', 'first'},
         'disease2': {'d2', 'dis2', 'disease', 'disease2', 'second'}}
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
        Return a dictionary in the form
        {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'and', 'definition'}}
        
        The set is populated with words from the 'Name' and 'Definitions' columns;
        it is accessed by the corresponding disease_name.
        
        Given
               Name                Definitions
        0  disease1   this is the first disease
        1  disease2  this is the second disease
        
        We have
        >>> instance.create_disease_name_description_dicts()
        {'disease1': {'disease', 'disease1', 'first'},
         'disease2': {'disease', 'disease2', 'second'}}
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

    def create_disease_name_only_dicts(self):
        """
        Return a dictionary in the form
        {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'only'}}
        
        The set is populated with words from the 'Name' column only;
        it is accessed by the corresponding disease_name.
        
        Given
                     Name
        0        disease1
        1  second disease
        
        We have
        >>> instance.create_disease_name_description_dicts()
        {'disease1': {'disease1'},
         'second disease': {'disease', 'second'}}
        """
        dict_of_sets = {}
        for index, row in self.dataframe.iterrows():
            entry_set = set()
            name = row['Name']
            name_word_list = word_tokenize(format_string(name, boosted=True))
            for x in name_word_list:
                entry_set.add(x)
            entry_set.difference_update(taboo_words)
            dict_of_sets[name] = entry_set
        return dict_of_sets


class G_SynMiner_miner_geneHUGO_instance:
    """
    'G-SynMiner_miner-geneHUGO.tsv' SNAP table handling class.
    Acquires data from the .tsv file in the working directory, the filename is 
    supposed to be static and is hardcoded in the __init__ method.
    The loaded table is saved as a pandas.read_table dataframe in the respective
    self.dataframe attribute.
    The create_SNAP_gene_table_in method gives you the possibility to add the
    SNAP table to an existing database.
    For computation processes, a dictionary relating a specific gene code to its
    gene_name is created with create_gene_symbol_name_dict method.
    
    Methods defined here:
        
        __init__(self)
            Initialize self.
        
        create_SNAP_gene_table_in(self, database_name)
            add the SNAP table to an existing database.
        
        create_gene_symbol_name_dict(self)
            return a dictionary in the form {'gene_symbol': 'gene_name'}
    """
    #placeholder_general_variable = True

    def __init__(self):
        """
        Initializer method.
        
        >>> instance = G_SynMiner_miner_geneHUGO_instance()
        >>> instance
        <snap_database_classes.G_SynMiner_miner_geneHUGO_instance at 0x7f9fc8081100>
        
        Loads the 'G-SynMiner_miner-geneHUGO.tsv' table in a pandas dataframe
        wich is stored in the self.dataframe attribute.
        The table is composed of 48 columns but the program uses only two of them: 
            column 3: 'symbol', a specific gene identification code
            column 4: 'name', common name of the gene
        """
        self.dataframe = pandas.read_table('G-SynMiner_miner-geneHUGO.tsv')

    def create_SNAP_gene_table_in(self, database_name):
        """
        Creates a new table (or updates the existing one) in the passed database,
        populating it with the 'G-SynMiner_miner-geneHUGO.tsv' informations.
        The created table in the database will have the name G_SynMiner_miner_geneHUGO.
        """
        self.database = sqlite3.connect(database_name)
        self.c = self.database.cursor()
        #mamit-trnadb and pseudogene.org have been reformatted to pseudogene_org and mamit_trnadb to allow execution
        string1 = "ensembl_gene_id TEXT PRIMARY KEY NOT NULL, hgnc_id TEXT, symbol TEXT, name TEXT, locus_group TEXT, locus_type TEXT, status TEXT, location TEXT, location_sortable TEXT, alias_symbol TEXT, alias_name TEXT, prev_symbol TEXT, prev_name TEXT, gene_family TEXT, gene_family_id TEXT, date_approved_reserved TEXT, date_symbol_changed TEXT, date_name_changed TEXT, date_modified TEXT, entrez_id TEXT, vega_id TEXT, ucsc_id TEXT, ena TEXT, refseq_accession TEXT, ccds_id TEXT, uniprot_ids TEXT, pubmed_id TEXT, mgd_id TEXT, rgd_id TEXT, lsdb TEXT, cosmic TEXT, omim_id TEXT, mirbase TEXT, homeodb TEXT, snornabase TEXT, bioparadigms_slc TEXT, orphanet TEXT, pseudogene_org TEXT, horde_id TEXT, merops TEXT, imgt TEXT, iuphar TEXT, kznf_gene_catalog TEXT, mamit_trnadb TEXT, cd TEXT, lncrnadb TEXT, enzyme_id TEXT, intermediate_filament_db TEXT"
        self.c.execute("CREATE TABLE IF NOT EXISTS G_SynMiner_miner_geneHUGO("+string1+");")
        string2 = 'ensembl_gene_id, hgnc_id, symbol, name, locus_group, locus_type, status, location, location_sortable, alias_symbol, alias_name, prev_symbol, prev_name, gene_family, gene_family_id, date_approved_reserved, date_symbol_changed, date_name_changed, date_modified, entrez_id, vega_id, ucsc_id, ena, refseq_accession, ccds_id, uniprot_ids, pubmed_id, mgd_id, rgd_id, lsdb, cosmic, omim_id, mirbase, homeodb, snornabase, bioparadigms_slc, orphanet, pseudogene_org, horde_id, merops, imgt, iuphar, kznf_gene_catalog, mamit_trnadb, cd, lncrnadb, enzyme_id, intermediate_filament_db'
        for index, row in self.dataframe.iterrows():
            self.c.execute("INSERT OR IGNORE INTO G_SynMiner_miner_geneHUGO ("+string2+") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(row['# ensembl_gene_id'], row['hgnc_id'], row['symbol'], row['name'], row['locus_group'], row['locus_type'], row['status'], row['location'], row['location_sortable'], row['alias_symbol'], row['alias_name'], row['prev_symbol'], row['prev_name'], row['gene_family'], row['gene_family_id'], row['date_approved_reserved'], row['date_symbol_changed'], row['date_name_changed'], row['date_modified'], row['entrez_id'], row['vega_id'], row['ucsc_id'], row['ena'], row['refseq_accession'], row['ccds_id'], row['uniprot_ids'], row['pubmed_id'], row['mgd_id'], row['rgd_id'], row['lsdb'], row['cosmic'], row['omim_id'], row['mirbase'], row['homeodb'], row['snornabase'], row['bioparadigms_slc'], row['orphanet'], row['pseudogene.org'], row['horde_id'], row['merops'], row['imgt'], row['iuphar'], row['kznf_gene_catalog'], row['mamit-trnadb'], row['cd'], row['lncrnadb'], row['enzyme_id'], row['intermediate_filament_db']))
        self.database.commit()
        self.database.close()
        return 'Done'

    def create_gene_symbol_name_dict(self):
        """
        Return a dictionary in the form {'gene_symbol': 'gene_name'}
        
        The dictionary is populated with the 'symbol' and 'name' entries of
        the table's rows.
        
        Given
          symbol   name
        0  SYM1B  gene1
        1  SYM2B  gene2
        
        We have
        >>> instance.create_disease_name_description_dicts()
        {'SYM1B': 'gene1', 'SYM2B': 'gene2'}
        """
        dictionary = {}
        for index, row in self.dataframe.iterrows():
            dictionary[row['symbol']] = row['name']
        return dictionary















