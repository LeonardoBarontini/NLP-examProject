#from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
bad_words = ['1','2','3','4','5','6','7','8','9','0',
             ':','!','?',';','.',',','(',')',"/",'\\','-','+',
             'and','with','without']
for el in bad_words:
    stop_words.add(el)
taboo_words = stop_words


def words_in_set(list_of_words, sset, stemmed=False):
    """
    look for how many of the words are present in the set and
    gives a positive score if more than one are present
    if the list_of_words is composed by only one word,
    it ignores the single word match penalization
    """
    score = 0
    matches = 0
    for word in list_of_words:
        temp = 0
        if stemmed:
            for element in sset:
                if word in element:
                    temp += 1
        else:
            if word.lower() in sset:
                temp += 1
        if temp != 0:
            matches += 1
            score += temp
    if len(list_of_words) != 1:    #for multiple word checkings, excludes the single word matches found
        if matches == 1:
            score = -score
    return score

def matched_entries2(list_of_word, dict_of_sets, stemmed=False):
    """
    returns a dictionary with: {'database disease name key': score}
    for a multiple word entry
    """
    elenco = {}
    for name, entry in dict_of_sets.items():
        exam = words_in_set(list_of_word, entry, stemmed=stemmed)
        if exam != 0:
            elenco[name]=exam
    return elenco

def best_match(list_of_word, dict_of_sets, stemmed=False):
    """lis_of_word already tokenized"""
    
    # if len(lis_of_word) == 1:
    #     elenco = matched_entries(lis_of_word, dict_of_sets, stemmed=stemmed)
    # else:
    elenco = matched_entries2(list_of_word, dict_of_sets, stemmed=stemmed)
    best_count=0
    best_entry=''
    best_list = []
    for entry, count in elenco.items():
        if count == best_count:
            best_list.append(entry)
        elif count > best_count:
            best_count = count
            best_entry = entry
            best_list = []
    best_list.append(best_entry)
    return best_list







#@not implemented yet
# def swap_typo():
# 	#check for word permutations


#@not implemented yet
# def proximity_typo():
# 	#check for proximity missclicks


    




    