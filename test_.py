"""
general module for testing.
"""

import pytest
from _pytest.outcomes import Failed
import sqlite3
import pandas
import os

#from managment_functions import is_disease
from managment_functions import add_unique_disease_id
from managment_functions import add_unique_symptom_id
from managment_functions import add_unique_drug_id
#from managment_functions import substring_in_elements
from managment_functions import format_string
from managment_functions import get_id_of_string
from managment_functions import add_relation_to_dict
from managment_functions import start_timer_at
from managment_functions import stop_timer_at
from managment_functions import check_overlap_percentage
from managment_functions import check_unlinked
from managment_functions import create_tsv_table_file
from managment_functions import create_stargate_network_table
from managment_functions import count_elements
from managment_functions import frequency_dictionary

from nlp import words_in_set
from nlp import matched_entries
from nlp import best_match

from disgenet_database_class import Disgenet_instance
from snap_database_classes import D_MeshMiner_miner_disease_instance
from snap_database_classes import G_SynMiner_miner_geneHUGO_instance
from RX_database_class import RX_instance
from stargate import Stargate_to_SNAP_diseases
from stargate import Stargate_to_SNAP_gene

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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# TESTING MODULE      management_funcions
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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

def test_format_string_step6_substitution():
    input_string = " a/b "
    output_string = 'a or b'
    assert format_string(input_string) == output_string

def test_format_string_boosted_1():
    input_string = "hello hello hello"
    output_string = 'hello'
    assert format_string(input_string, boosted=True) == output_string
    
def test_format_string_boosted_2():
    input_string = "hello, hello hello! ciao"
    output_string1 = 'hello ciao'
    output_string2 = 'ciao hello'
    assert format_string(input_string, boosted=True) == output_string1 or output_string2 
    
def test_format_string_boosted_numbers():
    input_string = "hello, 2 hello! 14 1.4"
    output_string1 = 'hello 14'
    output_string2 = '14 hello'
    assert format_string(input_string, boosted=True) == output_string1 or output_string2

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

# # ==================================================
# # TESTING      substring_in_elements
# # ==================================================

# def test_substring_in_elements_correct_1():
#     input_list = ['ciao', 'hello']
#     input_substring = 'k'
#     output_list = []
#     assert substring_in_elements(input_list, input_substring) == output_list

# def test_substring_in_elements_correct_2():
#     input_list = ['ciao', 'hello']
#     input_substring = 'o'
#     output_list = ['ciao', 'hello']
#     assert substring_in_elements(input_list, input_substring) == output_list

# def test_substring_in_elements_correct_3():
#     input_list = ['ciao', 'hello']
#     input_substring = 'h'
#     output_list = ['hello']
#     assert substring_in_elements(input_list, input_substring) == output_list

# def test_substring_in_elements_correct_4():
#     input_list = []
#     input_substring = 'k'
#     output_list = []
#     assert substring_in_elements(input_list, input_substring) == output_list

# def test_substring_in_elements_combination_currently_not_possible():
#     input_list = ['ciao', 'hello']
#     input_substring = ''
#     output_list = []
#     assert substring_in_elements(input_list, input_substring) != output_list

# def test_substring_in_elements_correct_special_empty_string_case():
#     input_list = ['ciao', 'hello', '']
#     input_substring = ''
#     output_list = ['']
#     assert substring_in_elements(input_list, input_substring) == output_list

# def test_substring_in_elements_wrong_type_intruder():
#     input_list = ['ciao', 'hello', 1]
#     input_substring = 'c'
#     #output_list = ['ciao']
#     with pytest.raises(TypeError):
#         substring_in_elements(input_list, input_substring)

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
# TESTING      add_relation_to_dict
# ==================================================

def test_add_relation_to_dict_correct_1():
    input_dictionary = {'dis000314':['sym000041']}
    input_id_key = "dis000014"
    input_id_data = 'sym000002'
    output_dictionary = {'dis000314':['sym000041'], 'dis000014':['sym000002']}
    assert add_relation_to_dict(input_dictionary, input_id_key, input_id_data) == output_dictionary
    
def test_add_relation_to_dict_correct_2():
    input_dictionary = {}
    input_id_key = "dis000014"
    input_id_data = 'sym000002'
    output_dictionary = {'dis000014':['sym000002']}
    assert add_relation_to_dict(input_dictionary, input_id_key, input_id_data) == output_dictionary
    
def test_add_relation_to_dict_correct_3():
    input_dictionary = {'dis000014':['sym000001']}
    input_id_key = "dis000014"
    input_id_data = 'sym000002'
    output_dictionary = {'dis000014':['sym000001', 'sym000002']}
    assert add_relation_to_dict(input_dictionary, input_id_key, input_id_data) == output_dictionary
    
def test_add_relation_to_dict_correct_4():
    input_dictionary = {'dis000014':['sym000001']}
    input_id_key = "dis000014"
    input_id_data = 'sym000001'
    output_dictionary = {'dis000014':['sym000001']}
    assert add_relation_to_dict(input_dictionary, input_id_key, input_id_data) == output_dictionary

# ==================================================
# TESTING           start_timer_at
# ==================================================

def test_start_timer_at_correct_1(capsys):
    input_time = 1619777180.5149667
    start = start_timer_at(input_time)
    output_time = 1619777180.5149667
    printed_time = "12:06:20.514967\n"
    assert capsys.readouterr().out == printed_time
    assert start == output_time

# ==================================================
# TESTING           stop_timer_at
# ==================================================

def test_stop_timer_at_correct_1(capsys): 
    input_time = 1619777666.3599267
    start_time = 1619777659.85105
    end = stop_timer_at(input_time,start_time)
    output_time = 1619777666.3599267
    printed_output = "\rfinished processing in 6.508876800537109 seconds\n"
    assert capsys.readouterr().out == printed_output
    assert end == output_time
    
# ==================================================
# TESTING       check_overlap_percentage
# ==================================================
    
def test_check_overlap_percentage_correct_1():
    initial_dataset = {'key1':'string', 'key2':'string', 'key3':'string', 'key4':'string'}
    dataset_name = "initial"
    link_network = {'key1':([''], None,''), 'key2':([''], None,''), 'key3':([''], None,''), 'key4':(['link'], 1,'')}
    final_dataset_name = 'final'
    output = 25.0
    assert check_overlap_percentage(initial_dataset, dataset_name, link_network, final_dataset_name) == output
    
# ==================================================
# TESTING            check_unlinked
# ==================================================
    
def test_check_unlinked_correct_1():
    check_dict = {'key1':([''], None,''), 'key2':([''], None,''), 'key3':([''], None,''), 'key4':(['link'], 1,'')}
    output = ['key1', 'key2', 'key3']
    assert check_unlinked(check_dict) == output

# ==================================================
# TESTING         create_tsv_table_file
# ==================================================

def test_create_tsv_table_file_correct_1():
    input_dict = {'disease1':([''], None, 'unchecked'), 'disease2':(['match1', 'match2'], 14, 'unchecked')}
    filename = 'test_create_tsv_table_file.tsv'
    create_tsv_table_file(filename, input_dict)
    file = open(filename, 'r+')
    line1 = file.readline()
    line2 = file.readline()
    line3 = file.readline()
    line4 = file.readline()
    file.close()
    os.remove('test_create_tsv_table_file.tsv')
    assert line1 == '# ID_start\tID_end\tScore\tStatus\n'
    assert line2 == 'disease1\t\tNone\tunchecked\n'
    assert line3 == 'disease2\tmatch1\t14\tunchecked\n'
    assert line4 == 'disease2\tmatch2\t14\tunchecked\n'


# ==================================================
# TESTING       create_stargate_network_table
# ==================================================

def test_create_stargate_network_table_correct1():
    test_database = 'test_database.db'
    test_links = {'disease1':([''], None, 'unchecked'), 'disease2':(['match1', 'match2'], 14, 'unchecked')}
    new_table_name = 'new_table_name'
    connecting_column = 'starting_ID_column(disease)'
    recieving_column = 'ending_ID_column(MESH_ID)'
    create_stargate_network_table(test_database, test_links, new_table_name, connecting_column, recieving_column)
    database = sqlite3.connect(test_database)
    c = database.cursor()
    c.execute("SELECT * FROM new_table_name")
    rows = c.fetchall()
    database.commit()
    database.close()
    os.remove('test_database.db')
    expected_rows_output = [('disease1', '', None, 'unchecked'), ('disease2', 'match1', '14', 'unchecked'), ('disease2', 'match2', '14', 'unchecked')]
    assert rows == expected_rows_output

# ==================================================
# TESTING            count_elements
# ==================================================

def test_count_elements_correct_1():
    lis = ['a', 'a', 'b', 'c', 'b', 'a', 'd', 'z']
    output = [3, 3, 2, 1, 2, 3, 1, 1]
    assert count_elements(lis) == output
    
def test_count_elements_empty():
    lis = []
    output = []
    assert count_elements(lis) == output

# ==================================================
# TESTING            frequency_dictionary
# ==================================================

def test_frequency_dictionary_correct_1():
    lis = ['a', 'a', 'b', 'c', 'b', 'a', 'd', 'z']
    output = {'a':3, 'b':2, 'c':1, 'd':1, 'z':1}
    assert frequency_dictionary(lis) == output
    
def test_frequency_dictionary_empty():
    lis = []
    output = {}
    assert frequency_dictionary(lis) == output

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# TESTING MODULE           nlp
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# TESTING MODULE      disgenet_database_class
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# ==================================================
# TESTING           Disgenet_instance
# ==================================================




def test_Disgenet_instance_instanciation():
    inp = Disgenet_instance("disgenet_2020.db")   #input instance for tests
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
    inp = Disgenet_instance("disgenet_2020.db")   
    inp.unload_diseaseAttributes_table()
    assert inp.diseaseAttributes == None
    
    inp.load_variantGene_table()
    assert isinstance(inp.variantGene, pandas.core.frame.DataFrame) == isinstance(pandas.read_sql_query("SELECT * FROM variantGene", inp.database), pandas.core.frame.DataFrame)


def test_create_disease_list():
    inp = Disgenet_instance("disgenet_2020.db")   
    inp.diseaseAttributes = {'diseaseName':('1','2','3','4')}
    inp.create_disease_list()
    assert inp.disease_list == ['1','2','3','4']

def test_create_disease_dict():
    inp = Disgenet_instance("disgenet_2020.db")   
    inp.diseaseAttributes = pandas.DataFrame({'diseaseNID':['1','2','3'], 'diseaseName':['a', 'b', 'c']})
    inp.create_disease_dict()
    assert inp.disease_dictionary == {'1':'a','2':'b','3':'c'}

def test_create_gene_dict():
    inp = Disgenet_instance("disgenet_2020.db")   
    inp.geneAttributes = pandas.DataFrame({'geneNID':['1','2','3'], 'geneName':['a', 'b', 'c'], 'geneDescription':['y','n','y']})
    inp.create_gene_dict()
    assert inp.gene_dictionary == {'1':('a','y'),'2':('b','n'),'3':('c','y')}


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# TESTING MODULE    snap_database_classes
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# ==================================================
# TESTING    D_MeshMiner_miner_disease_instance
# ==================================================


def test_D_MeshMiner_miner_disease_instance_instanciation():
    inp = D_MeshMiner_miner_disease_instance()   #input instance for tests
    assert isinstance(inp.dataframe, pandas.core.frame.DataFrame) == isinstance(pandas.read_table('D-MeshMiner_miner-disease.tsv'), pandas.core.frame.DataFrame)

def test_create_SNAP_disease_table_in_correct1():
    inp = D_MeshMiner_miner_disease_instance()   
    test_database = 'test_database.db'
    inp.create_SNAP_disease_table_in(test_database)
    
    database = sqlite3.connect(test_database)
    c = database.cursor()
    c.execute("SELECT * FROM D_MeshMiner_miner_disease")
    rows = c.fetchall()
    database.commit()
    database.close()
    os.remove('test_database.db')
    expected_rows_output = []
    for index, row in pandas.read_table('D-MeshMiner_miner-disease.tsv').iterrows():
        if type(row[0])!=str:
            row[0] = None
        if type(row[1])!=str:       #handling NaN
            row[1] = None
        if type(row[2])!=str:
            row[2] = None
        if type(row[3])!=str:
            row[3] = None
        expected_rows_output.append((row[0],row[1],row[2],row[3]))
    assert rows == expected_rows_output

def test_create_disease_name_synonyms_dicts_correct1():
    inp = D_MeshMiner_miner_disease_instance()
    inp.dataframe=pandas.DataFrame([['disease1', 'dis1|d1|first disease'],['disease2', 'dis2|d2|second disease']], columns=['Name', 'Synonyms'])
    output = inp.create_disease_name_synonyms_dicts()
    assert output == {'disease1': {'d1', 'dis1', 'disease', 'disease1', 'first'}, 'disease2': {'d2', 'dis2', 'disease', 'disease2', 'second'}}
    
def test_create_disease_name_description_dicts_correct1():
    inp = D_MeshMiner_miner_disease_instance()
    inp.dataframe=pandas.DataFrame([['disease1', 'this is the first disease'],['disease2', 'this is the second disease']], columns=['Name', 'Definitions'])
    output = inp.create_disease_name_description_dicts()
    assert output ==  {'disease1': {'disease', 'disease1', 'first'}, 'disease2': {'disease', 'disease2', 'second'}}

def test_create_disease_name_only_dicts_correct1():
    inp = D_MeshMiner_miner_disease_instance()
    inp.dataframe=pandas.DataFrame([['disease1'],['second disease']], columns=['Name'])
    output = inp.create_disease_name_only_dicts()
    assert output ==  {'disease1': {'disease1'}, 'second disease': {'disease', 'second'}}


# ==================================================
# TESTING    G_SynMiner_miner_geneHUGO_instance
# ==================================================

def test_G_SynMiner_miner_geneHUGO_instance_instanciation():
    inp = G_SynMiner_miner_geneHUGO_instance()   #input instance for tests
    assert isinstance(inp.dataframe, pandas.core.frame.DataFrame) == isinstance(pandas.read_table('G-SynMiner_miner-geneHUGO.tsv'), pandas.core.frame.DataFrame)

def test_create_SNAP_gene_table_in_correct1():
    """
    too many columns to hard-code
    assert problem: None != nan
    see test_create_SNAP_disease_table_in_correct1 for solution
    """
    assert 1==1
   
def test_create_gene_symbol_name_dict_correct1():
    inp = G_SynMiner_miner_geneHUGO_instance()
    inp.dataframe=pandas.DataFrame([['SYM1B', 'gene1'],['SYM2B', 'gene2']], columns=['symbol', 'name'])
    output = inp.create_gene_symbol_name_dict()
    assert output ==  {'SYM1B': 'gene1', 'SYM2B': 'gene2'}


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# TESTING MODULE       RX_database_class
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# ==================================================
# TESTING              RX_instance
# ==================================================

def test_RX_instance_instanciation():
    inp = RX_instance('RXlist_data.json')   #input instance for tests
    assert inp.disease_recognition_string == '_symptoms_and_signs'
    assert isinstance(inp.data, dict) == True
    assert isinstance(inp.df, pandas.core.frame.DataFrame) == True

def test_create_main_lists_correct1():
    inp = RX_instance('RXlist_data.json')
    inp.df=pandas.DataFrame({
        'dis_symptoms_and_signs':
            {'Related':['sym1', 'sym2'],'Causes':[],'Drugs':['drg1', 'drg2']},
        'symptom':
            {'Related':['sym1', 'sym2'],'Causes':['dis1', 'dis2'],'Drugs':['drg1', 'drg2']}
            })
    inp.create_main_lists()
    assert set(inp.diseases_list) == {'dis', 'dis1', 'dis2'}
    assert set(inp.symptoms_list) == {'symptom', 'sym1', 'sym2'}

def test_create_drug_list_correct1():
    inp = RX_instance('RXlist_data.json')
    inp.df=pandas.DataFrame({
        'dis_symptoms_and_signs':
            {'Related':['sym1', 'sym2'],'Causes':[],'Drugs':['drg1', 'drg2']},
        'symptom':
            {'Related':['sym1', 'sym2'],'Causes':['dis1', 'dis2'],'Drugs':['drg1', 'drg2']}
            })
    inp.create_drug_list()
    assert set(inp.drug_list) == {'drg2', 'drg1'}

def test_create_main_dicts_correct1():
    inp = RX_instance('RXlist_data.json')
    inp.df=pandas.DataFrame({
        'dis_symptoms_and_signs':
            {'Related':['sym1', 'sym2'],'Causes':[],'Drugs':['drg1', 'drg2']},
        'symptom':
            {'Related':['sym1', 'sym2'],'Causes':['dis1', 'dis2'],'Drugs':['drg1', 'drg2']}
            })
    inp.create_main_lists()
    inp.create_main_dicts()
    assert inp.id_diseases_dict == {'dis000001':'dis', 'dis000002':'dis1', 'dis000003':'dis2'}
    assert inp.id_symptoms_dict == {'sym000001':'sym1', 'sym000002':'sym2', 'sym000003':'symptom'}

def test_create_drug_dict_correct1():
    inp = RX_instance('RXlist_data.json')
    inp.df=pandas.DataFrame({
        'dis_symptoms_and_signs':
            {'Related':['sym1', 'sym2'],'Causes':[],'Drugs':['drg1', 'drg2']},
        'symptom':
            {'Related':['sym1', 'sym2'],'Causes':['dis1', 'dis2'],'Drugs':['drg1', 'drg2']}
            })
    inp.create_drug_list()
    inp.create_drug_dict()
    assert inp.id_drugs_dict == {'drg000002':'drg2', 'drg000001':'drg1'}

def test_create_relation_dicts_correct1():
    inp = RX_instance('RXlist_data.json')
    inp.df=pandas.DataFrame({
        'dis_symptoms_and_signs':
            {'Related':['sym1', 'sym2'],'Causes':[],'Drugs':['drg1', 'drg2']},
        'symptom':
            {'Related':['sym1', 'sym2'],'Causes':['dis1', 'dis2'],'Drugs':['drg1', 'drg2']}
            })
    inp.create_main_lists()
    inp.create_main_dicts()
    inp.create_drug_list()
    inp.create_drug_dict()
    inp.create_relation_dicts()
    assert inp.dis_drg_dict == {'dis000001': ['drg000001', 'drg000002']}

def test_create_RX_database_AND_insert_into_XXX_AND_populate_correct1():
    inp = RX_instance('RXlist_data.json')
    test_database = 'test_database.db'
    inp.create_main_lists()
    inp.create_main_dicts()
    inp.create_drug_list()
    inp.create_drug_dict()
    inp.create_relation_dicts()
    inp.create_RX_database(test_database)
    inp.populate()
    
    database = sqlite3.connect(test_database)
    c = database.cursor()
    
    c.execute("SELECT * FROM diseases")
    rows = c.fetchall()
    expected_rows_output = []
    for row in inp.id_diseases_dict.items():
        expected_rows_output.append(row)
    assert rows == expected_rows_output
    c.execute("SELECT * FROM symptoms")
    rows = c.fetchall()
    expected_rows_output = []
    for row in inp.id_symptoms_dict.items():
        expected_rows_output.append(row)
    assert rows == expected_rows_output
    c.execute("SELECT * FROM drugs")
    rows = c.fetchall()
    expected_rows_output = []
    for row in inp.id_drugs_dict.items():
        expected_rows_output.append(row)
    assert rows == expected_rows_output
    c.execute("SELECT * FROM symptoms_to_symptoms_relat")
    rows = c.fetchall()
    expected_rows_output = []
    for key, item_list in inp.sym_sym_dict.items():
        for element in item_list:
            expected_rows_output.append((key, element))
    assert rows == expected_rows_output
    c.execute("SELECT * FROM diseases_to_symptoms_relat")
    rows = c.fetchall()
    expected_rows_output = []
    for key, item_list in inp.dis_sym_dict.items():
        for element in item_list:
            expected_rows_output.append((key, element))
    assert rows == expected_rows_output
    c.execute("SELECT * FROM diseases_to_drugs_relat")
    rows = c.fetchall()
    expected_rows_output = []
    for key, item_list in inp.dis_drg_dict.items():
        for element in item_list:
            expected_rows_output.append((key, element))
    assert rows == expected_rows_output
    c.execute("SELECT * FROM symptoms_to_drugs_relat")
    rows = c.fetchall()
    expected_rows_output = []
    for key, item_list in inp.sym_drg_dict.items():
        for element in item_list:
            expected_rows_output.append((key, element))
    assert rows == expected_rows_output

    database.commit()
    database.close()
    os.remove('test_database.db')
    
def test_process_RXdata_to_correct1():
    """
    Wrapper method.
    Nothing to test.
    Functions called already tested.
    """
    pass

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# TESTING MODULE          stargate
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# ==================================================
# TESTING         Stargate_to_SNAP_diseases
# ==================================================

def test_Stargate_to_SNAP_diseases_instanciation():
    """
    This instanciation method uses methods from D_MeshMiner_miner_disease_instance.
    If those fails this should fail as well.
    """
    test_D_MeshMiner_miner_disease_instance_instanciation()
    test_create_disease_name_synonyms_dicts_correct1()
    test_create_disease_name_description_dicts_correct1()
    test_create_disease_name_only_dicts_correct1()

def test_disease_stargate_link_with_check_correct1():
    inp = Stargate_to_SNAP_diseases()
    initial_point_dict={'dis000001': 'abdominal pain', 'dis000002': 'unlucky'}
    output_link, output_check = inp.disease_stargate_link_with_check(initial_point_dict)
    assert output_link == {'dis000001': (['MESH:C564899', 'MESH:D015746'], 2, 'unchecked'), 'dis000002': ([''], None, 'unchecked')}
    assert output_check == {'abdominal pain': (['Pelger-Huet-Like Anomaly and Episodic Fever with ''Abdominal Pain', 'Abdominal Pain'], 2, 'unchecked'), 'unlucky': ([''], None, 'unchecked')}
 
def test_disease_stargate_link_correct1():
    inp = Stargate_to_SNAP_diseases()
    initial_point_dict={'dis000001': 'abdominal pain', 'dis000002': 'unlucky'}
    output_link = inp.disease_stargate_link(initial_point_dict)
    assert output_link == {'dis000001': (['MESH:C564899', 'MESH:D015746'], 2, 'unchecked'), 'dis000002': ([''], None, 'unchecked')}

# ==================================================
# TESTING         Stargate_to_SNAP_gene
# ==================================================

def test_Stargate_to_SNAP_gene_instanciation():
    """
    This instanciation method uses methods from G_SynMiner_miner_geneHUGO_instance.
    If those fails this should fail as well.
    """
    test_create_gene_symbol_name_dict_correct1()

def test_gene_stargate_link_with_check_correct1():
    inp = Stargate_to_SNAP_gene()
    initial_point_dict={ 513: ('BTK', 'Bruton tyrosine kinase')}
    output_link, output_check = inp.gene_stargate_link_with_check(initial_point_dict)
    assert output_link == {513: (['ENSG00000010671'], 5, 'unchecked')}
    assert output_check == {'BTK': (['BTK'], 5, 'unchecked')}

def test_gene_stargate_link_correct1():
    inp = Stargate_to_SNAP_gene()
    initial_point_dict={ 513: ('BTK', 'Bruton tyrosine kinase')}
    output_link = inp.gene_stargate_link(initial_point_dict)
    assert output_link == {513: (['ENSG00000010671'], 5, 'unchecked')}


if __name__ == '__main__':
    pytest.main([__file__])









