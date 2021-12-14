"""
Module containing the RX_instance class wich handles the RX-database
"""

import sqlite3
import json
import pandas

from managment_functions import format_string, add_unique_disease_id, add_unique_symptom_id
from managment_functions import add_unique_drug_id, get_id_of_string, add_relation_to_dict


class RX_instance:
    """
    RX-database class: takes the json csv and manages it to create a database.
    The file name is passed as argument in the instanciation.
    The instanciation loads the file as a pandas dataframe, keeping it loaded.
    The data distincion between disease and symptom is held by the
    disease_recognition_string attribute.
    Various methods manage data formatting and database populating. 
    
    Methods defined here:
        
        __init__(self, json_data):
            Initialize self.
        
        create_main_lists(self):
            Method that creates the self.diseases_list and self.symptom_list.
            
        create_main_dicts(self):
            Method that creates disease and symptom id based dictionaries
            
        create_drug_list(self):
            Method that creates the self.drug_list.
            
        create_drug_dict(self):
            Method that creates drug id based dictionary.
            
        create_relation_dicts(self):
            Method that creates relational dictionaries in the form of
            {entry:[list, of, related]}.
            
        create_RX_database(self, database_name):
            Method that creates the SQL database for the class data.
            
        insert_into_diseases(self, serial, disease):
            inserts an entry into disease table

        insert_into_symptoms(self, serial, symptom):
            inserts an entry into symptoms table

        insert_into_drugs(self, serial, drug):
            inserts an entry into drugs table

        insert_into_sym_sym_relation(self, symptom1, symptom2):
            inserts an entry into symptoms_to_symptoms_relat table

        insert_into_dis_sym_relation(self, disease, symptom):
            inserts an entry into diseases_to_symptoms_relat table

        insert_into_dis_drug_relation(self, disease, drug):
            inserts an entry into diseases_to_drugs_relat table

        insert_into_sym_drug_relation(self, symptom, drug):
            inserts an entry into symptoms_to_drugs_relat table
        
        populate(self):
            method that populate an already existing database with data,
            using the insert_into_* methods
        
        process_RXdata_to(self, database_name):
            Wrapper method for processing
    """
    #placeholder_general_variable = True

    def __init__(self, json_data):
        """
        Initialization method that takes the json csv file as a string argument.
    
        >>> instance = RX_instance("RXlist_data.json")
        >>> instance
        <RX_database_class.RX_instance at 0x7fb31c120670>
        
        The file is loaded via the json module and saved in the data attribute.
        The data attribute is converted to a pandas dataframe, then is stored
        in the df attribute for further computations.
        The entries are composed of diseases and symptoms.
        The distincion between disease and symptom is held by the
        disease_recognition_string attribute.
        """
        self.data = json.load(open(json_data))
        self.df = pandas.DataFrame(data=self.data)
        self.disease_recognition_string = '_symptoms_and_signs'


    def create_main_lists(self):
        """
        Method that processes raw data creating two lists needed for further
        computation: self.diseases_list and self.symptom_list.
        It reads the self.df pandas dataframe, iterating over the entries
        divided between former keys and items of the json dictionary.
        When iterating over the keys it divedes them between the two lists
        based on the self.disease_recognition_string.
        Then it searches inside the Related and Causes lists to catch possible
        diseases or symptoms not listed in the main object.
        """
        self.diseases_list=[]
        self.symptoms_list=[]
        for key, items in self.df.iteritems():
            formatted_key = format_string(key)

            if self.disease_recognition_string in key:
                if formatted_key not in self.diseases_list:
                    self.diseases_list.append(formatted_key)
            else:
                if formatted_key not in self.symptoms_list:
                    self.symptoms_list.append(formatted_key)

            for sym in items[0]:   #['Related']
                symptom = format_string(sym)
                if symptom not in self.symptoms_list:
                    self.symptoms_list.append(symptom)

            for dis in items[1]:   #['Causes']
                disease = format_string(dis)
                if disease not in self.diseases_list:
                    self.diseases_list.append(disease)

        return 'created main lists\n'


    def create_main_dicts(self):
        """
        Method that creates diseases and symptoms id based dictionaries in the
        form: {'unique_id': 'entry_name'}.
        It passes the self.*_list to the management function add_unique_*_id,
        then stores the resulting dicionaries in the self.id_*_dict
        """
        self.id_diseases_dict = add_unique_disease_id(self.diseases_list)
        self.id_symptoms_dict = add_unique_symptom_id(self.symptoms_list)
        
        return 'created main dicts\n'


    def create_drug_list(self):
        """
        Method that process raw data creating a list needed for further
        computation: self.drug_list.
        It iterates the self.df dataframe and collects all the 'Drugs' found
        in the former items of the json dictionary.
        """
        self.drug_list = []
        for key, items in self.df.iteritems():
            data_drug_list = items[2]   #['Drugs']
            for drg in data_drug_list:
                drug = format_string(drg)
                if drug in self.drug_list: pass
                else:
                    self.drug_list.append(drug)

        return 'created drug list\n'


    def create_drug_dict(self):
        """
        Method that creates drug id based dictionary in the form:
            {'unique_id': 'entry_name'}.
        It passes the self.drug_list to the management function 
        add_unique_drug_id, then stores the resulting dicionary in
        the self.id_drugs_dict.
        """
        self.id_drugs_dict = add_unique_drug_id(self.drug_list)

        return 'created drug dict\n'


    def create_relation_dicts(self):
        """
        Method that uses the self.id_*_dict and the self.df dataframe to create
        relational dictionaries in the form:
            {'entry_id':['list', 'of', 'related', 'ids']}.
        It uses the get_id_of_string management function to fetch the ids from
        the self.id_*_dict.
        The dictionaries created are saved in self.dis_sym_dict, self.sym_sym_dict,
        self.dis_drg_dict, self.sym_drg_dict.
        It uses the add_relation_to_dict management function to populate the
        self.*_*_dict with relations.
        To create a relation, first it iterates the self.df dataframe identifying
        the former key as a disease or as a symptom; then, in the disease case,
        it associates its id to a list af related symptoms, for the dis_sym_dict,
        and to a list of related drugs, for the dis_drg_dict; otherwise, in the
        stmptom case, it associates its id to a list af related symptoms, 
        for the sym_sym_dict, and to a list of related drugs, for the sym_drg_dict,
        also checking for previouselty unrelated diseases to add to the dis_sym_dict.
        As a sanity chech, raises ValueError if a disease has a cause.
        """
        self.dis_sym_dict={}
        self.sym_sym_dict={}
        self.dis_drg_dict={}
        self.sym_drg_dict={}
        for key, items in self.df.iteritems():

            if self.disease_recognition_string in key:
                disease = format_string(key)
                dis_id = get_id_of_string(self.id_diseases_dict, disease)

                for sym in items[0]:   #['Related']
                    symptom = format_string(sym)
                    sym_id = get_id_of_string(self.id_symptoms_dict, symptom)
                    self.dis_sym_dict = add_relation_to_dict(self.dis_sym_dict, dis_id, sym_id)

                if items[1] != []:   #['Causes']
                    print(''.zfill(42))
                    print("This disease has a cause!!! What's going on???")
                    print(key)
                    raise ValueError

                for drg in items[2]:   #['Drugs']
                    drug = format_string(drg)
                    drg_id = get_id_of_string(self.id_drugs_dict, drug)
                    self.dis_drg_dict = add_relation_to_dict(self.dis_drg_dict, dis_id, drg_id)
            else:
                symptom = format_string(key)
                sym_id = get_id_of_string(self.id_symptoms_dict, symptom)

                for sym2 in items[0]:   #['Related']
                    symptom2 = format_string(sym2)
                    sym2_id = get_id_of_string(self.id_symptoms_dict, symptom2)
                    self.sym_sym_dict = add_relation_to_dict(self.sym_sym_dict, sym_id, sym2_id)

                for dis in items[1]:   #['Causes']
                    disease = format_string(dis)
                    dis_id = get_id_of_string(self.id_diseases_dict, disease)
                    self.dis_sym_dict = add_relation_to_dict(self.dis_sym_dict, dis_id, sym_id)

                for drg in items[2]:   #['Drugs']
                    drug = format_string(drg)
                    drg_id = get_id_of_string(self.id_drugs_dict, drug)
                    self.sym_drg_dict = add_relation_to_dict(self.sym_drg_dict, sym_id, drg_id)

        return 'created relational dictionaries\n'


    def create_RX_database(self, database_name):
        """
        Method that creates a SQL database for the class data using the database_name
        passed as argument and instanciate the self.c cursor wich operates over it.
        The database connection is saved in self.database and is left open after
        the function's operations for further computation.
        """
        self.database = sqlite3.connect(database_name)
        self.c = self.database.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS drugs(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("DROP TABLE IF EXISTS diseases_to_symptoms_relat;")
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases_to_symptoms_relat(disease_id TEXT ,symptom_id TEXT,FOREIGN KEY(disease_id) REFERENCES diseases(serial) ON DELETE CASCADE,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE);")
        self.c.execute("DROP TABLE IF EXISTS symptoms_to_symptoms_relat;")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms_to_symptoms_relat(symptom_id TEXT ,related_symptom_id TEXT,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE,FOREIGN KEY(related_symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE);")
        self.c.execute("DROP TABLE IF EXISTS diseases_to_drugs_relat;")
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases_to_drugs_relat(disease_id TEXT ,drug_id TEXT,FOREIGN KEY(disease_id) REFERENCES diseases(serial) ON DELETE CASCADE,FOREIGN KEY(drug_id) REFERENCES drugs(serial) ON DELETE CASCADE);")
        self.c.execute("DROP TABLE IF EXISTS symptoms_to_drugs_relat;")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms_to_drugs_relat(symptom_id TEXT ,drug_id TEXT,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE,FOREIGN KEY(drug_id) REFERENCES drugs(serial) ON DELETE CASCADE);")

        return 'created database\n'


    def insert_into_diseases(self, serial, disease):
        """
        Helper method that inserts an entry: (id, name) of a disease in the diseases table.
        """
        self.c.execute("INSERT OR IGNORE INTO diseases (serial, name) VALUES(?,?);",(serial, disease))

    def insert_into_symptoms(self, serial, symptom):
        """
        Helper method that inserts an entry: (id, name) of a symptom in the symptoms table.
        """
        self.c.execute("INSERT OR IGNORE INTO symptoms (serial, name) VALUES(?,?);",(serial, symptom))

    def insert_into_drugs(self, serial, drug):
        """
        Helper method that inserts an entry: (id, name) of a drug in the drugs table.
        """
        self.c.execute("INSERT OR IGNORE INTO drugs (serial, name) VALUES(?,?);",(serial, drug))

    def insert_into_sym_sym_relation(self, symptom1, symptom2):
        """
        Helper method that inserts an entry: (id1, id2) of two symptoms in the 
        symptom-to-symptom relation table.
        """
        self.c.execute("INSERT OR IGNORE INTO symptoms_to_symptoms_relat (symptom_id, related_symptom_id) VALUES(?,?);",(symptom1,symptom2))

    def insert_into_dis_sym_relation(self, disease, symptom):
        """
        Helper method that inserts an entry: (id1, id2) of a disease and a symptom
        in the disease-to-symptom relation table.
        """
        self.c.execute("INSERT OR IGNORE INTO diseases_to_symptoms_relat (disease_id, symptom_id) VALUES(?,?);",(disease,symptom))

    def insert_into_dis_drug_relation(self, disease, drug):
        """
        Helper method that inserts an entry: (id1, id2) of a disease and a drug
        in the disease-to-drug relation table.
        """
        self.c.execute("INSERT OR IGNORE INTO diseases_to_drugs_relat (disease_id, drug_id) VALUES(?,?);",(disease, drug))

    def insert_into_sym_drug_relation(self, symptom, drug):
        """
        Helper method that inserts an entry: (id1, id2) of a symptom and a drug
        in the symptom-to-drug relation table.
        """
        self.c.execute("INSERT OR IGNORE INTO symptoms_to_drugs_relat (symptom_id, drug_id) VALUES(?,?);",(symptom, drug))


    def populate(self):
        """
        Method that populate an already existing database with data.
        It uses the insert_into_* helper methods wich uses the self.c cursor
        created with the create_RX_database method that has to be active.
        At the end the method commits and closes the database.
        """
        for ID, disease in self.id_diseases_dict.items():
            self.insert_into_diseases(ID, disease)

        for ID, symptom in self.id_symptoms_dict.items():
            self.insert_into_symptoms(ID, symptom)

        for ID, drug in self.id_drugs_dict.items():
            self.insert_into_drugs(ID, drug)

        for ID, lis_of_sym in self.dis_sym_dict.items():
            for sym in lis_of_sym:
                self.insert_into_dis_sym_relation(ID, sym)

        for ID, lis_of_sym in self.sym_sym_dict.items():
            for sym in lis_of_sym:
                self.insert_into_sym_sym_relation(ID, sym)

        for ID, lis_of_drg in self.dis_drg_dict.items():
            for drg in lis_of_drg:
                self.insert_into_dis_drug_relation(ID, drg)

        for ID, lis_of_drg in self.sym_drg_dict.items():
            for drg in lis_of_drg:
                self.insert_into_sym_drug_relation(ID, drg)

        self.database.commit()
        self.database.close()

    def process_RXdata_to(self, database_name):
        """
        Wrapper method for processing, it packs all the calls to methods
        needed for the various RX-related tasks.
        Calling this method means:
            create disease, symptoms and drug lists
            create disease, symptoms and drug id dictionaryes
            create relational dictionaries between diseases, dymptoms and drugs
            create the database for the class data
            pupulate the database with the class data
        """
        self.create_main_lists()
        self.create_main_dicts()
        self.create_drug_list()
        self.create_drug_dict()
        self.create_relation_dicts()
        self.create_RX_database(database_name)
        self.populate()