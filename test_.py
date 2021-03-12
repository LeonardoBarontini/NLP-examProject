import pytest
from managment_functions import is_disease

from hypothesis import given
import hypothesis.strategies as st

@given(inp = st.text())   #is this useful?????????
def test_given(inp):
    assert is_disease(inp)==False

# %% tests
def test_is_disease_input_type_int():
    inp = 1
    with pytest.raises(TypeError):
        is_disease(inp)
    
def test_is_disease_input_type_list():
    inp = [1]
    with pytest.raises(TypeError):
        is_disease(inp)
    
def test_is_disease_input_type_tuple():
    inp = (1)
    with pytest.raises(TypeError):
        is_disease(inp)
        
def test_is_disease_input_type_dictionary_1():
    inp = {'1':1}
    with pytest.raises(TypeError):
        is_disease(inp)
    
def test_is_disease_input_type_dictionary_2():############################failing
    inp = {'_symptoms_and_signs':1}
    with pytest.raises(TypeError):
        is_disease(inp)
        
def test_is_disease_input_type_none():
    inp = None
    with pytest.raises(TypeError):
        is_disease(inp)
    
def test_is_disease_input_empty_string():
    inp = ''
    assert is_disease(inp)==False
    
def test_is_disease_output_correct_1():
    inp = 'this is not a disease'
    assert is_disease(inp)==False
    
def test_is_disease_output_correct_2():
    inp = 'this is a disease_symptoms_and_signs'
    assert is_disease(inp)==True
    
def test_is_disease_output_correct_3():
    inp = '_symptoms_this is a typo_and_signs'
    assert is_disease(inp)==False
