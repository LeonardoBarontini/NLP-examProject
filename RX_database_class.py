"""
module containing the RXinstance class wich handles the RX-database
"""

import sqlite3
import json
import pandas

from managment_functions import format_string, add_unique_disease_id, add_unique_symptom_id
from managment_functions import add_unique_drug_id, get_id_of_string, add_relation_to_dict


class RXinstance:
    """
    RX-database class
    takes the json csv and manages it to create a database.
    also keeps the data in the instance of the object.
    """
    #placeholder_general_variable = True

    def __init__(self, json_data):

        self.data = json.load(open(json_data))
        self.df = pandas.DataFrame(data=self.data)
        self.disease_recognition_string = '_symptoms_and_signs'


    def create_main_lists(self):
        """
        method that creates the self.diseases_list and self.symptom_list.
        it reads the self.df pandas dataframe and divides between the two lists
        based and the self.disease_recognition_string.
        it checks both the main objects and the Related and Causes lists.
        """
        self.diseases_list=[]
        self.symptoms_list=[]
        for element, lists in self.df.iteritems():
            formatted_element = format_string(element)

            if self.disease_recognition_string in element:
                self.diseases_list.append(formatted_element)
            else:
                self.symptoms_list.append(formatted_element)

            for sym in lists[0]:   #['Related']
                symptom = format_string(sym)
                if symptom not in self.symptoms_list:
                    self.symptoms_list.append(symptom)

            for dis in lists[1]:   #['Causes']
                disease = format_string(dis)
                if disease not in self.diseases_list:
                    self.diseases_list.append(disease)

        return 'created main lists\n'


    def create_main_dicts(self):
        """
        method that creates disease and symptom id based dictionaries.
        it uses the self.*_list with the add_unique_*_id and stores the resulting
        dicionaries in the self.id_*_dict
        """
        self.id_diseases_dict = add_unique_disease_id(self.diseases_list)
        self.id_symptoms_dict = add_unique_symptom_id(self.symptoms_list)
        
        return 'created main dicts\n'


    def create_drug_list(self):
        """
        method that iterates the self.df dataframe and collects all the 'Drugs' found in there.
        le drug list created is stored in the self.drug_list
        """
        self.drug_list = []
        for element, lists in self.df.iteritems():
            data_drug_list = lists[2]   #['Drugs']
            for drg in data_drug_list:
                drug = format_string(drg)
                if drug in self.drug_list: pass
                else:
                    self.drug_list.append(drug)

        return 'created drug list\n'


    def create_drug_dict(self):
        """
        method that creates drug id based dictionary.
        it uses the self.drug_list with the add_unique_drug_id and stores the resulting
        dicionary in the self.id_drugs_dict
        """
        self.id_drugs_dict = add_unique_drug_id(self.drug_list)

        return 'created drug dict\n'


    def create_relation_dicts(self):
        """
        Method that uses the self.id_*_dict and the self.df dataframe to create
        relational dictionaries in the form of entry:list of related.
        The dictionaries created are saved in self.*_*_dict
        Raises ValueError if a disease has a cause.
        """
        self.dis_sym_dict={}
        self.sym_sym_dict={}
        self.dis_drg_dict={}
        self.sym_drg_dict={}
        for element, lists in self.df.iteritems():

            if self.disease_recognition_string in element:
                disease = format_string(element)
                dis_id = get_id_of_string(self.id_diseases_dict, disease)

                for sym in lists[0]:   #['Related']
                    symptom = format_string(sym)
                    sym_id = get_id_of_string(self.id_symptoms_dict, symptom)
                    self.dis_sym_dict = add_relation_to_dict(self.dis_sym_dict, dis_id, sym_id)

                if lists[1] != []:   #['Causes']
                    print(''.zfill(42))
                    print("This disease has a cause!!! What's going on???")
                    print(element)
                    raise ValueError

                for drg in lists[2]:   #['Drugs']
                    drug = format_string(drg)
                    drg_id = get_id_of_string(self.id_drugs_dict, drug)
                    self.dis_drg_dict = add_relation_to_dict(self.dis_drg_dict, dis_id, drg_id)
            else:
                symptom = format_string(element)
                sym_id = get_id_of_string(self.id_symptoms_dict, symptom)

                for sym2 in lists[0]:   #['Related']
                    symptom2 = format_string(sym2)
                    sym2_id = get_id_of_string(self.id_symptoms_dict, symptom2)
                    self.sym_sym_dict = add_relation_to_dict(self.sym_sym_dict, sym_id, sym2_id)

                for dis in lists[1]:   #['Causes']
                    disease = format_string(dis)
                    dis_id = get_id_of_string(self.id_diseases_dict, disease)
                    self.dis_sym_dict = add_relation_to_dict(self.dis_sym_dict, dis_id, sym_id)

                for drg in lists[2]:   #['Drugs']
                    drug = format_string(drg)
                    drg_id = get_id_of_string(self.id_drugs_dict, drug)
                    self.sym_drg_dict = add_relation_to_dict(self.sym_drg_dict, sym_id, drg_id)

        return 'created relational dictionaries\n'


    def create_RXdatabase(self, database_name):
        """
        method that creates the SQL database for the class data and
        instanciate the self.c cursor wich operates over it.
        the database connection is saved in self.database
        """
        self.database = sqlite3.connect(database_name)
        self.c = self.database.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS drugs(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases_to_symptoms_relat(disease_id TEXT ,symptom_id TEXT,FOREIGN KEY(disease_id) REFERENCES diseases(serial) ON DELETE CASCADE,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms_to_symptoms_relat(symptom_id TEXT ,related_symptom_id TEXT,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE,FOREIGN KEY(related_symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases_to_drugs_relat(disease_id TEXT ,drug_id TEXT,FOREIGN KEY(disease_id) REFERENCES diseases(serial) ON DELETE CASCADE,FOREIGN KEY(drug_id) REFERENCES drugs(serial) ON DELETE CASCADE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms_to_drugs_relat(symptom_id TEXT ,drug_id TEXT,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE,FOREIGN KEY(drug_id) REFERENCES drugs(serial) ON DELETE CASCADE);")

        return 'created database\n'


    def insert_into_diseases(self, serial, disease):
        self.c.execute("INSERT OR IGNORE INTO diseases (serial, name) VALUES(?,?);",(serial, disease))

    def insert_into_symptoms(self, serial, symptom):
        self.c.execute("INSERT OR IGNORE INTO symptoms (serial, name) VALUES(?,?);",(serial, symptom))

    def insert_into_drugs(self, serial, drug):
        self.c.execute("INSERT OR IGNORE INTO drugs (serial, name) VALUES(?,?);",(serial, drug))

    def insert_into_sym_sym_relation(self, symptom1, symptom2):
        self.c.execute("INSERT OR IGNORE INTO symptoms_to_symptoms_relat (symptom_id, related_symptom_id) VALUES(?,?);",(symptom1,symptom2))

    def insert_into_dis_sym_relation(self, disease, symptom):
        self.c.execute("INSERT OR IGNORE INTO diseases_to_symptoms_relat (disease_id, symptom_id) VALUES(?,?);",(disease,symptom))

    def insert_into_dis_drug_relation(self, disease, drug):
        self.c.execute("INSERT OR IGNORE INTO diseases_to_drugs_relat (disease_id, drug_id) VALUES(?,?);",(disease, drug))

    def insert_into_sym_drug_relation(self, symptom, drug):
        self.c.execute("INSERT OR IGNORE INTO symptoms_to_drugs_relat (symptom_id, drug_id) VALUES(?,?);",(symptom, drug))


    def populate(self):
        """
        method that populate an already existing database with data.
        it uses the self.c cursor wich has to be active.
        at the end the method commits and closes the database.
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

