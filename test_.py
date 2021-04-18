"""
general module for testing.
"""

import pytest
from _pytest.outcomes import Failed
import sqlite3
import pandas

#from managment_functions import is_disease
from managment_functions import add_unique_disease_id
from managment_functions import add_unique_symptom_id
from managment_functions import add_unique_drug_id
from managment_functions import substring_in_elements
from managment_functions import format_string
from managment_functions import get_id_of_string

from nlp import words_in_set
from nlp import matched_entries
from nlp import best_match

from disgenet_database_class import Disgenet_instance

######  placeholder test
# from hypothesis import given
# import hypothesis.strategies as st
# @given(inp = st.text())
# def test_given(inp):
#     assert is_disease(inp)==False
######

def manual_test_input_type(function):
    """Helper function for manual input type testing.
    
    ___not for automate testing___
    
    Checks for TypeError raising in the passed function.
    At least one test should fail unless the passed function
    takes in input a "non standard type".
    """
    types = [1, [1], (1), {'1':1}, '1', None]
    for typ in types:
        try:
            pytest.raises(TypeError, function, typ)
        except Failed:
            print(
                "\nDoesn't raise exceptions for input " + str(type(typ)) +
                ", is this the intended input type?"
                )
            #pytest.raises(TypeError, function, typ)   #uncomment to get traceback



# @deprecated
# # ==================================================
# # TESTING          is_disease
# # ==================================================

# def test_is_disease__input_empty_string():
#     inp = ''
#     assert is_disease(inp) is False

# def test_is_disease__output_correct_1():
#     inp = 'this is not a disease'
#     assert is_disease(inp) is False

# def test_is_disease__output_correct_2():
#     inp = 'this is a disease_symptoms_and_signs'
#     assert is_disease(inp) is True

# def test_is_disease__output_correct_3():
#     inp = '_symptoms_this is a typo_and_signs'
#     assert is_disease(inp) is False

# # def test_is_disease_output_incorrect():
# #     inp = """_symptoms_and_signs_this is not a disease.
# #               the output is True but it is wrong.
# #               --->knownIssue<---
# #               this is intended to fail"""
# #     assert is_disease(inp)==False

# ==================================================
# TESTING      add_unique_disease_id
# ==================================================

def test_add_unique_disease_id__correct_1():
    input_list = ['correct']
    assert add_unique_disease_id(input_list, digits=6) == {'dis000001':input_list[0]}

def test_add_unique_disease_id__correct_2():
    input_list = []
    assert add_unique_disease_id(input_list, digits=6) == {}

def test_add_unique_disease_id__digits_works_as_intended():
    input_list = ['correct']
    assert add_unique_disease_id(input_list, digits=1) == {'dis1':input_list[0]}

def test_add_unique_disease_id__too_many_entryes_1():
    input_list = ['correct', 1,2,3,4,5,6,7,8,'too long']
    with pytest.raises(ValueError):
        add_unique_disease_id(input_list, digits=1)

def test_add_unique_disease_id__too_many_entryes_2():
    input_list = range(100)
    with pytest.raises(ValueError):
        add_unique_disease_id(input_list, digits=2)

def test_add_unique_disease_id__checking_len_of_dict_is_correct():
    input_list = [0,1]
    output_dict = add_unique_disease_id(input_list, digits=1)
    assert len(output_dict) == 2

def test_add_unique_disease_id__checking_len_vs_digits():
    input_list = range(999)
    output_dict = add_unique_disease_id(input_list, digits=3)
    assert len(output_dict) == 999

# ==================================================
# TESTING      add_unique_symptom_id
# ==================================================

def test_add_unique_symptom_id__correct_1():
    input_list = ['correct']
    assert add_unique_symptom_id(input_list, digits=6) == {'sym000001':input_list[0]}

def test_add_unique_symptom_id__correct_2():
    input_list = []
    assert add_unique_symptom_id(input_list, digits=6) == {}

def test_add_unique_symptom_id__digits_works_as_intended():
    input_list = ['correct']
    assert add_unique_symptom_id(input_list, digits=1) == {'sym1':input_list[0]}

def test_add_unique_symptom_id__too_many_entryes_1():
    input_list = ['correct', 1,2,3,4,5,6,7,8,'too long']
    with pytest.raises(ValueError):
        add_unique_symptom_id(input_list, digits=1)

def test_add_unique_symptom_id__too_many_entryes_2():
    input_list = range(100)
    with pytest.raises(ValueError):
        add_unique_symptom_id(input_list, digits=2)

def test_add_unique_symptom_id__checking_len_of_dict_is_correct():
    input_list = [0,1]
    output_dict = add_unique_symptom_id(input_list, digits=1)
    assert len(output_dict) == 2

def test_add_unique_symptom_id__checking_len_vs_digits():
    input_list = range(999)
    output_dict = add_unique_symptom_id(input_list, digits=3)
    assert len(output_dict) == 999

# ==================================================
# TESTING      add_unique_drug_id
# ==================================================

def test_add_unique_drug_id__correct_1():
    input_list = ['correct']
    assert add_unique_drug_id(input_list, digits=6) == {'drg000001':input_list[0]}

def test_add_unique_drug_id__correct_2():
    input_list = []
    assert add_unique_drug_id(input_list, digits=6) == {}

def test_add_unique_drug_id__digits_works_as_intended():
    input_list = ['correct']
    assert add_unique_drug_id(input_list, digits=1) == {'drg1':input_list[0]}

def test_add_unique_drug_id__too_many_entryes_1():
    input_list = ['correct', 1,2,3,4,5,6,7,8,'too long']
    with pytest.raises(ValueError):
        add_unique_drug_id(input_list, digits=1)

def test_add_unique_drug_id__too_many_entryes_2():
    input_list = range(100)
    with pytest.raises(ValueError):
        add_unique_drug_id(input_list, digits=2)

def test_add_unique_drug_id__checking_len_of_dict_is_correct():
    input_list = [0,1]
    output_dict = add_unique_drug_id(input_list, digits=1)
    assert len(output_dict) == 2

def test_add_unique_drug_id__checking_len_vs_digits():
    input_list = range(999)
    output_dict = add_unique_drug_id(input_list, digits=3)
    assert len(output_dict) == 999

# ==================================================
# TESTING      substring_in_elements
# ==================================================

def test_substring_in_elements_correct_1():
    input_list = ['ciao', 'hello']
    input_substring = 'k'
    output_list = []
    assert substring_in_elements(input_list, input_substring) == output_list

def test_substring_in_elements_correct_2():
    input_list = ['ciao', 'hello']
    input_substring = 'o'
    output_list = ['ciao', 'hello']
    assert substring_in_elements(input_list, input_substring) == output_list

def test_substring_in_elements_correct_3():
    input_list = ['ciao', 'hello']
    input_substring = 'h'
    output_list = ['hello']
    assert substring_in_elements(input_list, input_substring) == output_list

def test_substring_in_elements_correct_4():
    input_list = []
    input_substring = 'k'
    output_list = []
    assert substring_in_elements(input_list, input_substring) == output_list

def test_substring_in_elements_combination_currently_not_possible():
    input_list = ['ciao', 'hello']
    input_substring = ''
    output_list = []
    assert substring_in_elements(input_list, input_substring) != output_list

def test_substring_in_elements_correct_special_empty_string_case():
    input_list = ['ciao', 'hello', '']
    input_substring = ''
    output_list = ['']
    assert substring_in_elements(input_list, input_substring) == output_list

def test_substring_in_elements_wrong_type_intruder():
    input_list = ['ciao', 'hello', 1]
    input_substring = 'c'
    #output_list = ['ciao']
    with pytest.raises(TypeError):
        substring_in_elements(input_list, input_substring)

# ==================================================
# TESTING      format_string
# ==================================================

def test_format_string_step1_does_nothing():
    input_string = 'ciao'
    output_string = 'ciao'
    assert format_string(input_string) == output_string

def test_format_string_step1_remove_desiese_identification():
    input_string = 'ciao_symptoms_and_signs'
    output_string = 'ciao'
    assert format_string(input_string) == output_string

def test_format_string_step2_does_lower():
    input_string = 'ciAo'
    output_string = 'ciao'
    assert format_string(input_string) == output_string

def test_format_string_step3_does_strip():
    input_string = ' ciao '
    output_string = 'ciao'
    assert format_string(input_string) == output_string

def test_format_string_step4_does_replace_underscores():
    input_string = 'ciao_hello_yo'
    output_string = 'ciao hello yo'
    assert format_string(input_string) == output_string

def test_format_string_step5_does_kill_genitive():
    input_string = "ciao's_revenge"
    output_string = 'ciao revenge'
    assert format_string(input_string) == output_string

def test_format_string_empty_input():
    input_string = ''
    output_string = ''
    assert format_string(input_string) == output_string

def test_format_string_deadstring_input():
    input_string = " _'s_ "
    output_string = '  '
    assert format_string(input_string) == output_string

# ==================================================
# TESTING      get_id_of_string
# ==================================================

def test_get_id_of_string_correct_1():
    input_dictionary = {'ciao': 'hello'}
    input_string = "hello"
    output_string = 'ciao'
    assert get_id_of_string(input_dictionary, input_string) == output_string

def test_get_id_of_string_correct_2():
    input_dictionary = {'id1': 'hello', 'id2':'ciao'}
    input_string = "ciao"
    output_string = 'id2'
    assert get_id_of_string(input_dictionary, input_string) == output_string

def test_get_id_of_string_key_is_strange():
    input_dictionary = {1: 'hello'}
    input_string = "hello"
    output_string = 1
    assert get_id_of_string(input_dictionary, input_string) == output_string

def test_get_id_of_string_correct_but_not_completely():
    input_dictionary = {'ciao': 'hello', 'world': 'hello'} #second finding is ignored
    input_string = "hello"
    output_string = 'ciao'
    assert get_id_of_string(input_dictionary, input_string) == output_string

def test_get_id_of_string_key_not_found():
    input_dictionary = {'ciao': 'hello'}
    input_string = "world"
    output_string = None
    assert get_id_of_string(input_dictionary, input_string) == output_string

# ==================================================
# TESTING           words_in_set
# ==================================================

def test_words_in_set_correct_1():
    input_list_of_words = ['hello', 'world']
    input_sset = {"hello"}
    output_score = -1
    assert words_in_set(input_list_of_words, input_sset) == output_score

def test_words_in_set_correct_2():
    input_list_of_words = ['hello', 'world', 'Italy']
    input_sset = {"hello", 'world'}
    output_score = 2
    assert words_in_set(input_list_of_words, input_sset) == output_score

def test_words_in_set_mono_word_list():
    input_list_of_words = ['hello']
    input_sset = {"hello", 'world'}
    output_score = 1
    assert words_in_set(input_list_of_words, input_sset) == output_score

def test_words_in_set_empty_set():
    input_list_of_words = ['hello']
    input_sset = set()
    output_score = 0
    assert words_in_set(input_list_of_words, input_sset) == output_score

def test_words_in_set_empty_list():
    input_list_of_words = []
    input_sset = {"hello", 'world'}
    output_score = 0
    assert words_in_set(input_list_of_words, input_sset) == output_score

def test_words_in_set_no_match():
    input_list_of_words = ['what?']
    input_sset = {"hello", 'world'}
    output_score = 0
    assert words_in_set(input_list_of_words, input_sset) == output_score

def test_words_in_set_stemmed():
    input_list_of_words = ['hel', 'worl', 'Ital']
    input_sset = {"hello", 'world'}
    output_score = 2
    assert words_in_set(input_list_of_words, input_sset, stemmed=True) == output_score
    
# ==================================================
# TESTING           matched_entries
# ==================================================

def test_matched_entries_correct_1():
    input_list_of_words = ['hello', 'world']
    input_dict_of_sets = {
                        'hello':{'hello', 'ciao', 'salut'},
                        'hello world':{'hello', 'world', 'python'}
                            }
    output_dictionary = {'hello': -1, 'hello world': 2}
    assert matched_entries(input_list_of_words, input_dict_of_sets) == output_dictionary
    
def test_matched_entries_mono():
    input_list_of_words = ['hello', 'world']
    input_dict_of_sets = {
                        'hello':{'hello'},
                        'hello world':{'hello', 'hi', 'python'}
                            }
    output_dictionary = {'hello': 1, 'hello world': -1}
    assert matched_entries(input_list_of_words, input_dict_of_sets, mono=True) == output_dictionary

def test_matched_entries_empty_word_list():
    input_list_of_words = []
    input_dict_of_sets = {'hello':{'hello'}}
    output_dictionary = {}
    assert matched_entries(input_list_of_words, input_dict_of_sets) == output_dictionary

def test_matched_entries_empty_dictionary_of_sets():
    input_list_of_words = ['hello', 'world']
    input_dict_of_sets = {}
    output_dictionary = {}
    assert matched_entries(input_list_of_words, input_dict_of_sets) == output_dictionary

# ==================================================
# TESTING           best_match
# ==================================================

def test_best_match_corresct_1():
    input_list_of_words = ['hello', 'world', 'python']
    input_dict_of_sets = {
                    'hello':{'hello', 'ciao', 'salut'},
                    'hello world':{'hello', 'world'},
                    'hello python':{'hello', 'world', 'python'},
                    'ciao python':{'ciao', 'hello', 'world', 'python'}
                        }
    output_tuple = (3, ['ciao python', 'hello python'])
    assert best_match(input_list_of_words, input_dict_of_sets) == output_tuple

def test_best_match_empty_word_list():
    input_list_of_words = []
    input_dict_of_sets = {'hello':{'hello'}}
    output_tuple = (0, [''])
    assert best_match(input_list_of_words, input_dict_of_sets) == output_tuple

def test_best_match_empty_dictionary_of_sets():
    input_list_of_words = ['hello', 'world']
    input_dict_of_sets = {}
    output_tuple = (0, [''])
    assert best_match(input_list_of_words, input_dict_of_sets) == output_tuple   

# ==================================================
# TESTING           Disgenet_instance
# ==================================================

inp = Disgenet_instance("disgenet_2020.db")


def test_class_instanciation():
    assert isinstance(inp.database, sqlite3.Connection) == isinstance(sqlite3.connect("disgenet_2020.db"), sqlite3.Connection) 
    assert inp.disease2class == None
    assert isinstance(inp.diseaseAttributes, pandas.core.frame.DataFrame) == isinstance(pandas.read_sql_query("SELECT * FROM diseaseAttributes", inp.database), pandas.core.frame.DataFrame)
    assert inp.diseaseClass == None
    assert inp.geneAttributes == None
    assert inp.geneDiseaseNetwork == None
    assert inp.variantAttributes == None
    assert inp.variantDiseaseNetwork == None
    assert inp.variantGene == None


def test_table_unload_and_load():
    inp.unload_diseaseAttributes_table()
    assert inp.diseaseAttributes == None
    
    inp.load_variantGene_table()
    assert isinstance(inp.variantGene, pandas.core.frame.DataFrame) == isinstance(pandas.read_sql_query("SELECT * FROM variantGene", inp.database), pandas.core.frame.DataFrame)


def test_create_disease_list():
    inp.diseaseAttributes = {'diseaseName':('1','2','3','4')}
    inp.create_disease_list()
    assert inp.disease_list == ['1','2','3','4']

def test_create_disease_dict():
    inp.diseaseAttributes = pandas.DataFrame({'diseaseNID':['1','2','3'], 'diseaseName':['a', 'b', 'c']})
    inp.create_disease_dict()
    assert inp.disease_dictionary == {'1':'a','2':'b','3':'c'}

def test_create_gene_dict():
    inp.geneAttributes = pandas.DataFrame({'geneNID':['1','2','3'], 'geneName':['a', 'b', 'c'], 'geneDescription':['y','n','y']})
    inp.create_gene_dict()
    assert inp.gene_dictionary == {'1':('a','y'),'2':('b','n'),'3':('c','y')}


# to be implemented?
# def test_for_double_dict_entries():
#     lisa=[]
#     for key, dis in RXdata.id_diseases_dict.items():
#         if dis not in lisa:
#             lisa.append(dis)
#         else:
#             print(key, dis)
#             print(lisa.index(dis))












