"""
colection of functions for general management
"""

import sqlite3
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
ps = PorterStemmer()


# @deprecated
# def is_disease(string):
#     """
#     Returns weather the passed string is a disease or not based on the disease_recognition_string
#     """
#     if type(string) is not str: raise TypeError(str(string)+' is not a string.\n')
#     ###
#     disease_recognition_string = '_symptoms_and_signs'
#     ###
#     return disease_recognition_string in string


def format_string(string, boosted=False):
    """
    tries to format the passed string to a "standard":
        all lowercase,
        no trailing and leading witespaces,
        no '_' but spaces,
        no "'s"
        no "/" but " or "
        if boosted:
            no duplicate words
    then returns it.
    """
    ###
    disease_recognition_string = '_symptoms_and_signs'
    ###
    step1 = string.split(disease_recognition_string)[0]    #if not a rx-disease this does nothing
    step2 = step1.lower()
    step3 = step2.strip()
    step4 = step3.replace('_', ' ')
    step5 = step4.replace("'s", '')
    step6 = step5.replace("/", ' or ')
    if boosted:
        step7 = word_tokenize(step6) #add if stemmed after this?
        step8 = set(step7)      #this is the no duplicate words part
        step9 = ' '.join(word for word in step8)
        return step9

    return step6


def substring_in_elements(lis, substring):
    """
    inspects the passed list of strings and returns a list containing all the strings
    that contains the passed substring.
    returns [''] if an empty substring is given.
    """
    if substring == '':
        return ['']
    element_list = []
    for element in lis:
        if not isinstance(element, str): raise TypeError("An element of the list is not a string.\nSearch for: "+str(element)+'\nIt is a '+str(type(element)))
        if element.find(substring)!=(-1):
            element_list.append(element)
    return element_list


def add_unique_disease_id(lis, digits=6):
    """
    warning: assuming lis has unique elements
    returns a dictionary with {id:disease}
    """
    #having more than 999999 diseases will be a problem. In that case change the digits to how much more you need.
    if len(lis) > ((10**digits)-1):
        raise ValueError('input list is too long, the resulting ids will be wrongly sorted!\nChange the digits input value so you can handle more entries.')
    id_diseases_dict = {}
    base = 'dis'
    for index, value in enumerate(lis):
        id_string = base + str(index+1).zfill(digits)
        id_diseases_dict[id_string] = value

    return id_diseases_dict

def add_unique_symptom_id(lis, digits=6):
    """
    warning: assuming lis has unique elements
    returns a dictionary with {id:symptom}
    """
    #having more than 999999 symptoms will be a problem. In that case change the digits to how much more you need.
    if len(lis) > ((10**digits)-1):
        raise ValueError('input list is too long, the resulting ids will be wrongly sorted!\nChange the digits input value so you can handle more entries.')
    id_symptoms_dict = {}
    base = 'sym'
    for index, value in enumerate(lis):
        id_string = base + str(index+1).zfill(digits)
        id_symptoms_dict[id_string] = value

    return id_symptoms_dict


def add_unique_drug_id(lis, digits=6):
    """
    warning: assuming lis has unique elements
    returns a dictionary with {id:drug}
    """
    #having more than 999999 drugs will be a problem. In that case change the digits to how much more you need.
    if len(lis) > ((10**digits)-1):
        raise ValueError('input list is too long, the resulting ids will be wrongly sorted!\nChange the digits input value so you can handle more entries.')
    id_drugs_dict = {}
    base = 'drg'
    for index, value in enumerate(lis):
        id_string = base + str(index+1).zfill(digits)
        id_drugs_dict[id_string] = value

    return id_drugs_dict


def get_id_of_string(dictionary, string):
    """
    gets in input a dictionary and an input string.
    the dictionary contains unique ids as keys and strings as data.
    the function returns the id of the input string if present.
    IMPORTANT: it's supposed that a string can be related to only one id.
    """
    for searched_id in dictionary.keys():
        if dictionary[searched_id] == string:
            return searched_id
    return None


def add_relation_to_dict(dictionary, id_key, id_data):
    """
    return a dictionary integrated with the new id-id relation
    """
    if id_key not in dictionary:
        dictionary[id_key] = [id_data]
    elif id_data in dictionary[id_key]:
        pass
    else:
        dictionary[id_key].append(id_data)
    return dictionary


def start_timer_at(time):
    print(datetime.fromtimestamp(time).time())
    return time

def stop_timer_at(time, start):
    print('\rfinished processing in '+str(time-start)+' seconds')
    return time

def check_overlap_percentage(initial_dataset, dataset_name, link_network, final_dataset_name, precise=False):
    count=0
    for key, (lis, score, chek) in link_network.items():
        if lis == ['']:
            pass
        else:
            count+=1
    total = len(initial_dataset)
    over = (count/total)*100
    overlap = int((count/total)*100)
    print('overlap between '+dataset_name+' and '+final_dataset_name+' : '+str(overlap)+'%')
    if precise:
        print(over)
    return overlap

def check_unlinked(check_dict):
    lisa=[]     
    for key, (lis, score, chek) in check_dict.items():
        if lis == ['']:
            lisa.append(key)
    return lisa

def create_tsv_table_file(filename, output_dict):
    tsv_file = open(filename, 'w')
    tsv_file.truncate()
    tsv_file.write('# ID_start\tID_end\tScore\tStatus\n')
    for id_start, (lis, score, chek) in output_dict.items():
        for id_end in lis:
            tsv_file.write(id_start+'\t'+id_end+'\t'+str(score)+'\t'+chek+'\n')
    tsv_file.close()
    return 'Done'

def create_stargate_network_table(database_name, output_dict, table_name, initial_ID_table_column_ref, final_ID_table_column_ref):
    database = sqlite3.connect(database_name)
    c = database.cursor()
    initial_column = initial_ID_table_column_ref.split('(')[1].split(')')[0]
    final_column = final_ID_table_column_ref.split('(')[1].split(')')[0]
    c.execute("DROP TABLE IF EXISTS "+table_name+";")
    c.execute("CREATE TABLE IF NOT EXISTS "+table_name+"("+initial_column+" TEXT NOT NULL, "+final_column+" TEXT, Score TEXT, Status TEXT, FOREIGN KEY("+initial_column+") REFERENCES "+initial_ID_table_column_ref+" ON DELETE CASCADE, FOREIGN KEY("+final_column+") REFERENCES "+final_ID_table_column_ref+" ON DELETE CASCADE);")
    for id_start, (lis, score, chek) in output_dict.items():
        for id_end in lis:
            c.execute("INSERT OR IGNORE INTO "+table_name+" ("+initial_column+", "+final_column+", Score, Status) VALUES(?,?,?,?);",(id_start, id_end, score, chek))
    database.commit()
    database.close()
    return 'Done'

def count_elements(lis):
    """
    returns a list with the respective frequencies of every element of the list
    """
    counts = []
    for el in lis:
        counts.append(lis.count(el))
    return counts

def frequency_dictionary(lis):
    """
    creates a dictionary with every element of the passed list as a key
    and his frequency inside the list as data
    """
    dictionary = {}
    for el in lis:
        dictionary[el] = lis.count(el)
    return dictionary





