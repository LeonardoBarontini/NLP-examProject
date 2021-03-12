import sqlite3
import json

from managment_functions import *


class Instanciator:
    dummy_general_variable = True

    def createRelationDICTs(self):
        """
        Method that uses the self.id_dictionaries and the self.data to create relational dictionaries in the form of entry:list of related.
        _returns a tuple of 4 dictionaries: (dis_sym_dict, sym_sym_dict, dis_drg_dict, sym_drg_dict)
        _raises ValueError if a disease has a cause.
        """
        dis_sym_dict={}   
        sym_sym_dict={}
        dis_drg_dict={}
        sym_drg_dict={}
        for main_entry in self.data.keys():
            
            if is_disease(main_entry):
                
                disease = format_string(main_entry)
                dis_id = get_id_of_string(self.id_diseases_dict, disease)
                
                related = self.data[main_entry]['Related']
                for sym in related:
                    symptom = format_string(sym)
                    sym_id = get_id_of_string(self.id_symptoms_dict, symptom)
                    dis_sym_dict = add_relation_to_dict(dis_sym_dict, dis_id, sym_id)

                if self.data[main_entry]['Causes'] != []:
                    print(''.zfill(42))
                    print("This disease has a cause!!! What's going on???")
                    print(main_entry)
                    raise ValueError
                
                drugs = self.data[main_entry]['Drugs']
                for drg in drugs:
                    drug = format_string(drg)
                    drg_id = get_id_of_string(self.id_drugs_dict, drug)
                    dis_drg_dict = add_relation_to_dict(dis_drg_dict, dis_id, drg_id)
                    
            else:
                
                symptom = format_string(main_entry)
                sym_id = get_id_of_string(self.id_symptoms_dict, symptom)
                
                related = self.data[main_entry]['Related']
                for sym2 in related:
                    symptom2 = format_string(sym2)
                    sym2_id = get_id_of_string(self.id_symptoms_dict, symptom2)
                    sym_sym_dict = add_relation_to_dict(sym_sym_dict, sym_id, sym2_id)
                    
                causes = self.data[main_entry]['Causes']
                for dis in causes:
                    disease = format_string(dis)
                    dis_id = get_id_of_string(self.id_diseases_dict, disease)
                    dis_sym_dict = add_relation_to_dict(dis_sym_dict, dis_id, sym_id)
                    
                drugs = self.data[main_entry]['Drugs']
                for drg in drugs:
                    drug = format_string(drg)
                    drg_id = get_id_of_string(self.id_drugs_dict, drug)
                    sym_drg_dict = add_relation_to_dict(sym_drg_dict, sym_id, drg_id)
                    
        return (dis_sym_dict, sym_sym_dict, dis_drg_dict, sym_drg_dict)
    

    def __init__(self, database, data, disease_racognition_string):
        
        self.database = sqlite3.connect(database)

        self.c = self.database.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS drugs(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases_to_symptoms_relat(disease_id TEXT ,symptom_id TEXT,FOREIGN KEY(disease_id) REFERENCES diseases(serial) ON DELETE CASCADE,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms_to_symptoms_relat(symptom_id TEXT ,related_symptom_id TEXT,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE,FOREIGN KEY(related_symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases_to_drugs_relat(disease_id TEXT ,drug_id TEXT,FOREIGN KEY(disease_id) REFERENCES diseases(serial) ON DELETE CASCADE,FOREIGN KEY(drug_id) REFERENCES drugs(serial) ON DELETE CASCADE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms_to_drugs_relat(symptom_id TEXT ,drug_id TEXT,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE,FOREIGN KEY(drug_id) REFERENCES drugs(serial) ON DELETE CASCADE);")


        self.data = json.load(open(data))                       #creates a dictionary based on the json file
        self.main_object_keys = self.data.keys()                #creates a list of diseases and symptoms from the main object keys

        self.disease_racognition_string = disease_racognition_string

        self.diseases_list, self.symptoms_list = create_main_lists(self.data, self.disease_racognition_string)
        self.id_diseases_dict = add_unique_disease_id(self.diseases_list)
        self.id_symptoms_dict = add_unique_symptom_id(self.symptoms_list)

        self.drug_list = create_drug_list(self.data)
        self.id_drugs_dict = add_unique_drug_id(self.drug_list)

        self.dis_sym_dict, self.sym_sym_dict, self.dis_drg_dict, self.sym_drg_dict = self.createRelationDICTs()


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
        
        for ID in self.id_diseases_dict:
            dis = self.id_diseases_dict[ID]
            self.insert_into_diseases(ID, dis)
            
        for ID in self.id_symptoms_dict:
            sym = self.id_symptoms_dict[ID]
            self.insert_into_symptoms(ID, sym)
            
        for ID in self.id_drugs_dict:
            drg = self.id_drugs_dict[ID]
            self.insert_into_drugs(ID, drg)
            
        for ID in self.dis_sym_dict:
            lis_of_sym = self.dis_sym_dict[ID]
            for sym in lis_of_sym:
                self.insert_into_dis_sym_relation(ID, sym)
            
        for ID in self.sym_sym_dict:
            lis_of_sym = self.sym_sym_dict[ID]
            for sym in lis_of_sym:
                self.insert_into_sym_sym_relation(ID, sym)
            
        for ID in self.dis_drg_dict:
            lis_of_drg = self.dis_drg_dict[ID]
            for drg in lis_of_drg:
                self.insert_into_dis_drug_relation(ID, drg)
            
        for ID in self.sym_drg_dict:
            lis_of_drg = self.sym_drg_dict[ID]
            for drg in lis_of_drg:
                self.insert_into_sym_drug_relation(ID, drg)
                
        self.database.commit()
        self.database.close()


#first the program iterates over the main keys, dividing them between diseases and symptoms and adding them, if not already present, to their respective tables
##
##
##for main_entry in main_object_keys:
##    if disease_racognition_string in main_entry:
##        main_entry_type = 'disease'
##        disease_name = format_string(main_entry)
##        insert_into_diseases(serial, disease_name)
##    else:
##        main_entry_type = 'symptom'
##        symptom_name = main_entry
##        insert_into_symptoms(serial, symptom_name)
##        
###then for every entry, it iterates in the Related, Causes and Drugs lists, adding every element to the appropriate table if it's not already present and recording the relation between the main entry and the element in the appropriate table
##    subkeys = data[main_entry].keys()
##    for sub_key in subkeys:
##        element_list = data[main_entry][sub_key]
##        if sub_key == 'Related':
##            for element in element_list:
##                insert_into_symptoms(element)
##                if main_entry_type == 'symptom':
##                    insert_into_sym_sym_relation(symptom_name, element)
##                elif main_entry_type == 'disease':
##                    insert_into_dis_sym_relation(disease_name, element)
##        elif sub_key == 'Causes':
##            for element in element_list:
##                insert_into_diseases(element)
##                if main_entry_type == 'symptom':
##                    insert_into_dis_sym_relation(element, symptom_name)
##                elif main_entry_type == 'disease':
##                    raise ValueError   #I think this would go against the disease definition (a disease is the cause, it is not caused by)
##        elif sub_key == 'Drugs':
##            for element in element_list:
##                insert_into_drugs(serial, element)
##                if main_entry_type == 'symptom':
##                    insert_into_sym_drug_relation(symptom_name, element)
##                elif main_entry_type == 'disease':
##                    insert_into_dis_drug_relation(disease_name, element)
##





