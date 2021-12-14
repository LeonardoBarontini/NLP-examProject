"""
collection of functions for general management
"""

import sqlite3
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nlp import bad_words



def format_string(string, boosted=False):
    """
    tries to format the passed string to a "standard":
        all lowercase,
        no trailing and leading witespaces,
        no '_' but spaces,
        no "'s"
        no "/" but " or "
        if boosted:
            no punctuation
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
        step7 = word_tokenize(step6)
        step8 = [w for w in step7 if w not in bad_words]
        step9 = set(step8)      #this is the no duplicate words part
        step10 = ' '.join(word for word in step9)
        return step10

    return step6


def add_unique_disease_id(lis, digits=6):
    """Given a list of diseases returns a dictionary in the form {id:disease}.
    The id construction is based on the disease's index in the list, wich is
    filled with zeros to the left, to reach the lenght fixed by the digits value,
    the resulting string is appended to the base string, giving the id.
    For example:
        if at index 114 we have 'Fever'
        the default dictionary output will be >> dis000114:'Fever'
    If the passed list il longer than how much the digits can handle, a warning
    message is displayed while raising ValueError.
    Warning: lis is assumed to have unique elements.    
    """
    #if you have more than 999999 diseases it'll be a problem. In that case change the digits to how much more you need.
    if len(lis) > ((10**digits)-1):
        raise ValueError('Input list is too long, the resulting ids will be wrongly sorted!\n'+
                         'Change the digits input value so you can handle more entries.')
    id_diseases_dict = {}
    base = 'dis'
    for index, value in enumerate(lis):
        id_string = base + str(index+1).zfill(digits)
        id_diseases_dict[id_string] = value

    return id_diseases_dict

def add_unique_symptom_id(lis, digits=6):
    """Given a list of symptoms returns a dictionary in the form {id:symptom}.
    The id construction is based on the symptom's index in the list, wich is
    filled with zeros to the left, to reach the lenght fixed by the digits value,
    the resulting string is appended to the base string, giving the id.
    For example:
        if at index 214 we have 'Chills'
        the default dictionary output will be >> sym000214:'Chills'
    If the passed list il longer than how much the digits can handle, a warning
    message is displayed while raising ValueError.
    Warning: lis is assumed to have unique elements. 
    """
    #if you have more than 999999 diseases it'll be a problem. In that case change the digits to how much more you need.
    if len(lis) > ((10**digits)-1):
        raise ValueError('Input list is too long, the resulting ids will be wrongly sorted!\n'+
                         'Change the digits input value so you can handle more entries.')
    id_symptoms_dict = {}
    base = 'sym'
    for index, value in enumerate(lis):
        id_string = base + str(index+1).zfill(digits)
        id_symptoms_dict[id_string] = value

    return id_symptoms_dict


def add_unique_drug_id(lis, digits=6):
    """Given a list of drugs returns a dictionary in the form {id:drug}.
    The id construction is based on the drug's index in the list, wich is
    filled with zeros to the left, to reach the lenght fixed by the digits value,
    the resulting string is appended to the base string, giving the id.
    For example:
        if at index 314 we have 'Aspirin'
        the default dictionary output will be >> drg000314:'Aspirin'
    If the passed list il longer than how much the digits can handle, a warning
    message is displayed while raising ValueError.
    Warning: lis is assumed to have unique elements.
    """
    #if you have more than 999999 diseases it'll be a problem. In that case change the digits to how much more you need.
    if len(lis) > ((10**digits)-1):
        raise ValueError('Input list is too long, the resulting ids will be wrongly sorted!\n'+
                         'Change the digits input value so you can handle more entries.')
    id_drugs_dict = {}
    base = 'drg'
    for index, value in enumerate(lis):
        id_string = base + str(index+1).zfill(digits)
        id_drugs_dict[id_string] = value

    return id_drugs_dict


def get_id_of_string(dictionary, string):
    """Given a dictionary and a string, searches for the string inside the
    dictionary's items and, if it founds it, returns the associated key.
    
    >>> get_id_of_string({'id1': 'hello', 'id2':'ciao'}, "ciao")
    'id2'
    
    The passed dictionary is supposed to contain unique ids, wich are strings,
    as keys and strings as items.
    So function returns the id of the passed string if it's present.
    Warning: it's supposed that a string can be related to only one id. Every
    subsequent match will be ignored as only the first is returned.
    """
    for searched_id in dictionary.keys():
        if dictionary[searched_id] == string:
            return searched_id
    return None


def add_relation_to_dict(dictionary, id_key, id_data):
    """Given a dictionary, an id wich will be a key and an id wich will be an
    item, the function adds the id_data to the item list of the id_key of the
    dictionary if that id_data isn't altready present, otherwise does nothing
    and then returns the updated dictionary.
    The keys' items are lists of ids.
    
    >>>add_relation_to_dict({'dis000314':['sym000041']}, 'dis000014', 'sym000002')
    {'dis000314':['sym000041'], 'dis000014':['sym000002']}
    """
    if id_key not in dictionary:
        dictionary[id_key] = [id_data]
    elif id_data in dictionary[id_key]:
        pass
    else:
        dictionary[id_key].append(id_data)
    return dictionary


def start_timer_at(time):
    """Prints information about the time obtained from the time library.
    Returns the passed time for storing purpouses.
    
    >>> start = start_timer_at(time())
    12:06:20.514967
    >>> start
    1619777180.5149667
    """
    print(datetime.fromtimestamp(time).time())
    return time

def stop_timer_at(stop, start):
    """Prints information about the elapsed processing time, calculating from
    the start time, to the stop time, both of wich are passed as inputs.
    
    >>> end = stop_timer_at(time(),start)
    finished processing in 6.508876800537109 seconds
    >>> end
    1619777666.3599267
    """
    print('\rfinished processing in '+str(stop-start)+' seconds')
    return stop

def check_overlap_percentage(initial_dataset, dataset_name, link_network, final_dataset_name, precise=False):
    """Given an initial_dataset and a link_network, checks for how many items
    of the link_network have a connection, wich means a "non empty" list, then
    calculates the percentage of connections with respect to the total entries of
    the initial_dataset.
    Prints out the result using the linked dataset names for better comprehention.
    If precise is set to True, also prints the float value of the percentage,
    wich could be useful to spot subtle changes in the linking outcome.
    Returns over for eventual computations.
    
    >>> check_overlap_percentage(RXdata.id_diseases_dict, 'RXdata', RX_to_SNAP_disease_links, 'SNAPdata diseases', precise=True)
    overlap between RXdata and SNAPdata diseases : 94%
    94.98480243161094
    """
    count=0
    for key, (lis, score, chek) in link_network.items():
        if lis == ['']:
            pass
        else:
            count+=1
    total = len(initial_dataset)
    over = (count/total)*100
    overlap = int(over)
    print('overlap between '+dataset_name+' and '+final_dataset_name+' : '+str(overlap)+'%')
    if precise:
        print(over)
    return over

def check_unlinked(check_dict):
    """Checks for how many items of the check_dict don't have a connection,
    wich means an "empty" list, then appends the respective key to a list
    wich will be returned at the end.
    
    >>> check_unlinked({'fever':(['some connection'], 2, 'unchecked'), 'nausea':([''], None, 'unchecked')})
    ['nausea']
    """
    lista=[]     
    for key, (lis, score, chek) in check_dict.items():
        if lis == ['']:
            lista.append(key)
    return lista

def create_tsv_table_file(filename, output_dict):
    """
    Given a dictionary of ID conncetions, with score and status, and
    a 'filename.tsv', creates a tsv file containing the dictionary informations.
    The coloumns names are: ID_start - ID_end - Score - Status
    """
    tsv_file = open(filename, 'w')
    tsv_file.truncate()
    tsv_file.write('# ID_start\tID_end\tScore\tStatus\n')
    for id_start, (lis, score, chek) in output_dict.items():
        for id_end in lis:
            tsv_file.write(id_start+'\t'+id_end+'\t'+str(score)+'\t'+chek+'\n')
    tsv_file.close()
    return 'Done'

def create_stargate_network_table(database_name, output_dict, table_name, initial_ID_table_column_ref, final_ID_table_column_ref):
    """
    Creates a new table (or updates the existing one) in the passed database,
    populating it with the output_dict dictionary informations.
    The table is composed of four columns: 
        column 1: the ID reference of the connecting table
        column 2: the ID reference of the recieving table
        column 3: the score of the connection
        column 4: the status of the connection
    """
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
    """Given a list, returns another list with the same lenght, wich has 
    in place of every element of the passed list, its frequency in that list.
    
    >>> count_elements(['a', 'a', 'b', 'c', 'b', 'a', 'd', 'z'])
    [3, 3, 2, 1, 2, 3, 1, 1]
    """
    counts = []
    for el in lis:
        counts.append(lis.count(el))
    return counts

def frequency_dictionary(lis):
    """Given a list, returns a dictionary that has every element of the
    passed list as key and his frequency inside that list as item.
    
    >>> frequency_dictionary(['a', 'a', 'b', 'c', 'b', 'a', 'd', 'z'])
    {'a':3, 'b':2, 'c':1, 'd':1, 'z':1}
    """
    dictionary = {}
    for el in lis:
        dictionary[el] = lis.count(el)
    return dictionary