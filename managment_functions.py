"""
colection of functions for general management
"""

#import nltk
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


# @deprecated
# def create_main_lists(dictionary, disease_racognition_string):
#     """
#     passing the keys of the main object of the database (supposing they are diseases and symptoms),
#     this funcion returns a tuple with the list of, respectively, the diseases and the symptoms,
#     where the diseases are identified by the disease_racognition_string.
#     """
#     symptoms_diseases_list = list(dictionary.keys())
#     diseases_list=[]
#     symptoms_list=[]
#     for element in symptoms_diseases_list:
#         formatted_element = format_string(element)

#         if disease_racognition_string in element:
#             diseases_list.append(formatted_element)
#         else:
#             symptoms_list.append(formatted_element)

#         for sym in dictionary[element]['Related']:
#             symptom = format_string(sym)
#             if symptom not in symptoms_list: symptoms_list.append(symptom)

#         for dis in dictionary[element]['Causes']:
#             disease = format_string(dis)
#             if disease not in diseases_list: diseases_list.append(disease)


#     return diseases_list, symptoms_list


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

# @deprecated
# def create_drug_list(dictionary):
#     """
#     takes the json data dictionary and collects all the 'Drugs' found in there.
#     return a unique list with all the drugs entries.
#     """
#     drug_list = []
#     for key in dictionary.keys():
#         data_drug_list = dictionary[key]['Drugs']
#         for drg in data_drug_list:
#             drug = format_string(drg)
#             if drug in drug_list: pass
#             else:
#                 drug_list.append(drug)

#     return drug_list

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





