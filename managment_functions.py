import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words.add(':')
from statistics import mean, stdev


def is_disease(string):
    """
    Returns weather the passed string is a disease or not based on the disease_recognition_string
    """
    if type(string) is not str: raise TypeError
    ###
    disease_recognition_string = '_symptoms_and_signs'
    ###
    return disease_recognition_string in string


def format_string(string):
    """
    tries to format the passed string to a "standard" (all lowercase, no trailing and leading witespaces, no '_' but spaces, no "'s") then returns it.
    """
    ###
    disease_recognition_string = '_symptoms_and_signs'
    ###
    step1 = string.split(disease_recognition_string)[0]    #if not a disease this does nothing
    step2 = step1.lower()
    step3 = step2.strip()
    step4 = step3.replace('_', ' ')
    step5 = step4.replace("'s", '')

    return step5


def substring_in_elements(lis, substring):
    """
    inspects the passed list of strings and returns a list with all the elements that contains the passed substring
    """
    element_list = []
    for el in lis:
        if el.find(substring)!=(-1):
            element_list.append(el)
    return element_list



def create_main_lists(dictionary, disease_racognition_string):
    """
    passing the keys of the main object of the database (supposing they are diseases and symptoms),
    this funcion returns a tuple with the list of, respectively, the diseases and the symptoms,
    where the diseases are identified by the disease_racognition_string.
    """
    symptoms_diseases_list = list(dictionary.keys())
    diseases_list=[]
    symptoms_list=[]
    for element in symptoms_diseases_list:
        formatted_element = format_string(element)
        
        if disease_racognition_string in element:
            diseases_list.append(formatted_element)
        else:
            symptoms_list.append(formatted_element)
            
        for sym in dictionary[element]['Related']:
            symptom = format_string(sym)
            if symptom not in symptoms_list: symptoms_list.append(symptom)
            
        for dis in dictionary[element]['Causes']:
            disease = format_string(dis)
            if disease not in diseases_list: diseases_list.append(disease)
        
            
    return diseases_list, symptoms_list


def add_unique_disease_id(lis):
    """
    warning: assuming lis has unique elements
    returns a dictionary with {id:disease}
    """
    id_diseases_dict = {}
    base = 'dis'
    for index in range(len(lis)):
        id_string = base + str(index+1).zfill(5)   #having more than 99999 diseases could be a problem. In that case change the 5 to how much more you need.
        id_diseases_dict[id_string] = lis[index]

    return id_diseases_dict

def add_unique_symptom_id(lis):
    """
    warning: assuming lis has unique elements
    returns a dictionary with {id:symptom}
    """
    id_symptoms_dict = {}
    base = 'sym'
    for index in range(len(lis)):
        id_string = base + str(index+1).zfill(5)   #having more than 99999 symptoms could be a problem. In that case change the 5 to how much more you need.
        id_symptoms_dict[id_string] = lis[index]

    return id_symptoms_dict

def create_drug_list(dictionary):
    """
    
    """
    drug_list = []
    for key in dictionary.keys():
        data_drug_list = dictionary[key]['Drugs']
        for drg in data_drug_list:
            drug = format_string(drg)
            if drug in drug_list: pass
            else:
                drug_list.append(drug)
            
    return drug_list

def add_unique_drug_id(lis):
    """
    warning: assuming lis has unique elements
    returns a dictionary with {id:drug}
    """
    id_drugs_dict = {}
    base = 'drg'
    for index in range(len(lis)):
        id_string = base + str(index+1).zfill(5)   #having more than 99999 drugs could be a problem. In that case change the 5 to how much more you need.
        id_drugs_dict[id_string] = lis[index]

    return id_drugs_dict


def get_id_of_string(dictionary, string):
    """
    return the id(key) of the passed string(data)
    """
    for searched_id in dictionary.keys():
        if dictionary[searched_id] == string:
            return searched_id 

    
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

            

def lenghts_mean_and_stdev(lis):
    lenghts = []
    for el in lis:
        lenghts.append(len(el))
    m = mean(lenghts)
    std = stdev(lenghts)
    return m, std

def suspiciously_long_entry(lis, lenght):
    warnings = []
    for el in lis:
        if len(el)>lenght:
            warnings.append(el)
    return warnings

def suspiciously_written_entry(lis):
    warnings = []
    bad_symbols = ['1','2','3','4','5','6','7','8','9','0',':','!','?',';','.',',','(',')',"/",'\\','-','+']
    for el in lis:
        for symb in bad_symbols:
            if symb in el:
                warnings.append(el)
                break
    return warnings

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
    creates a dictionary with every element of the passed list as a key and his frequency inside the list as data
    """
    dictionary = {}
    for el in lis:
        dictionary[el] = lis.count(el)
    return dictionary

word_list = []
stem_list = []
def create_word_stem_lists(word_list):
    for element in symptoms_diseases_list:
        formatted_element = format_string(element)
        # if len(formatted_element)>2*mean_lenght()
        tokenized_element = word_tokenize(formatted_element)
        tokenized_and_stopped_element = [w for w in tokenized_element if w not in stop_words]
        #stemmed_element = [ps.stem(w) for w in tokenized_and_stopped_element]
        word_list = word_list + tokenized_and_stopped_element
        #stem_list.append(stemmed_element)
    return word_list



