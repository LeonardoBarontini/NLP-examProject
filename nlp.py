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

def matched_entries(list_of_word, dict_of_sets, stemmed=False, mono=False):
    """
    returns a dictionary with: {'database disease name key': score}
    for a multiple word entry
    """
    dictionary = {}
    for name, entry in dict_of_sets.items():
        score = words_in_set(list_of_word, entry, stemmed=stemmed)
        if mono:
            if score<0:
                if len(entry)==1:
                    score=1
        if score != 0:
            dictionary[name]=score
    return dictionary

def best_match(list_of_word, dict_of_sets, stemmed=False, mono=False):
    """lis_of_word already tokenized"""

    dictionary = matched_entries(list_of_word, dict_of_sets, stemmed=stemmed, mono=mono)
    best_count=0
    best_entry=''
    best_list = []
    for entry, count in dictionary.items():
        if count == best_count:
            best_list.append(entry)
        elif count > best_count:
            best_count = count
            best_entry = entry
            best_list = []
    best_list.append(best_entry)
    return best_list







#########################
##  TO BE IMPLEMENTED  ##
#########################
# def swap_typo():
# 	#check for word permutations

# def proximity_typo():
# 	#check for proximity missclicks

# def suspiciously_long_entry(lis, lenght):
#     warnings = []
#     for el in lis:
#         if len(el)>lenght:
#             warnings.append(el)
#     return warnings

# def suspiciously_written_entry(lis):
#     warnings = []
#     bad_symbols = ['1','2','3','4','5','6','7','8','9','0',':','!','?',';','.',',','(',')',"/",'\\','-','+']
#     for el in lis:
#         for symb in bad_symbols:
#             if symb in el:
#                 warnings.append(el)
#                 break
#     return warnings
    




    