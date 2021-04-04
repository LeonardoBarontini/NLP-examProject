from nltk.tokenize import word_tokenize
import pandas
import sqlite3
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
        
    def create_SNAP_disease_table(self, database_name):
        self.database = sqlite3.connect(database_name)
        self.c = self.database.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS D_MeshMiner_miner_disease(MESH_ID TEXT PRIMARY KEY NOT NULL, Name TEXT, Definitions TEXT, Synonyms TEXT);")
        for index, row in self.dataframe.iterrows():
            self.c.execute("INSERT OR IGNORE INTO D_MeshMiner_miner_disease (MESH_ID, Name, Definitions, Synonyms) VALUES(?,?,?,?);",(row['# MESH_ID'], row['Name'], row['Definitions'], row['Synonyms']))
        self.database.commit()
        self.database.close()
        return 'Done'

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

    def create_disease_name_only_dicts(self):
        """
        return a dictionary in the form {'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'only'}}
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
    data loader for 'G-SynMiner_miner-geneHUGO.tsv' SNAP table
    """
    #placeholder_general_variable = True

    def __init__(self):#, tsv_table):
        """
        loads the table in a pandas dataframe
        """
        self.dataframe = pandas.read_table('G-SynMiner_miner-geneHUGO.tsv')

    def create_SNAP_gene_table(self, database_name):
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
        dictionary = {}
        for index, row in self.dataframe.iterrows():
            dictionary[row['symbol']] = row['name']
        return dictionary















