"""
Module containing general Natural Language Processing (NLP) functions.
Defines the words_in_set, matched_entries, best_match functions.
Imports english stop_words and expands them with bad_words creating taboo_words.
"""

#from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
bad_words = ['1','2','3','4','5','6','7','8','9','0',
             ':','!','?',';','.',',','(',')',"/",'\\','-','+',
             'and','with','without']
taboo_words = stop_words
for el in bad_words:
    taboo_words.add(el)


def words_in_set(list_of_words, sset, stemmed=False):
    """Gives a score to state how well list_of_words and sset match.

    It looks for how many of the words in list_of_words are present in the set
    and gives a positive score if more than one are present.

    >>> words_in_set(['hello', 'world', 'Italy'], {"hello", 'world'})
    2

    If only one is present, the match is penalized transforming the score from
    positive to negative. This is to avoid matches given by common words.

    >>> words_in_set(['hello', 'world'], {"hello"})
    -1

    If list_of_words is composed by only one word, it ignores the single word
    match penalization.

    >>> words_in_set(['hello'], {"hello", 'world'})
    1

    The stemmed flag allows for a proper checking in the set, iterating for
    every set item so the 'in' statement checks for the word inside a single
    string and not in the hole set, where it would search for the exact same
    word wich, beeing stemmed, will not be present.

    >>> words_in_set(['hel', 'worl', 'Ital'], {"hello", 'world'}, stemmed=True)
    2
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
    if len(list_of_words) != 1:    #penalization for single match in multiple word checkings
        if matches == 1:
            score = -score
    return score

def matched_entries(list_of_word, dict_of_sets, stemmed=False, mono=False):
    """Returns a dictionary in the form: {'database name key': score}

    It creates a dictionary using the name keys of dict_of_sets as keys and
    associates to them the matching score given by the words_in_set function
    between list_of_word and the item set of the key it is examining. It adds
    the key to the dictionary only if the score is not zero.

    >>> matched_entries(['hello', 'world'],
                        {
                        'hello':{'hello', 'ciao', 'salut'},
                        'hello world':{'hello', 'world', 'python'}
                            })
    {'hello': -1, 'hello world': 2}

    The 'stemmed' option is just passed to the words_in_set function.

    The 'mono' option is used to recover single word matches when we have a
    single word set to match to. In these cases the score is set to 1.

    >>> matched_entries(['hello', 'world'],
                        {
                        'hello':{'hello'},
                        'hello world':{'hello', 'hi', 'python'}
                            },
                        mono=True)
    {'hello': 1, 'hello world': -1}
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

def best_match(list_of_words, dict_of_sets, stemmed=False, mono=False):
    """Returns a tuple containing (the best_score, the best_list) among all
    the scores and lists given by the matched_entries function.

    To spot the best matches among the obtained ones, it iterates over the
    returned dictionary checking the score of the item against the best_score.
    If it finds a better score, it saves score and entry as bests. If the score
    equals the best_score it appends the entry to the best_list. Otherwise
    does nothing.

    The 'mono' and 'stemmed' options are passed to the matched_entries function.

    >>> best_match(['hello', 'world', 'python'],
                    {
                    'hello':{'hello', 'ciao', 'salut'},
                    'hello world':{'hello', 'world'},
                    'hello python':{'hello', 'world', 'python'},
                    'ciao python':{'ciao', 'hello', 'world', 'python'}
                        })
    (3, ['ciao python', 'hello python'])

    Note that the first entry with the best score found, is last in the list.
    """
    dictionary = matched_entries(list_of_words, dict_of_sets, stemmed=stemmed, mono=mono)
    best_score = 0
    best_entry = ''
    best_list = []
    for entry, score in dictionary.items():
        if score == best_score:
            best_list.append(entry)
        elif score > best_score:
            best_score = score
            best_entry = entry
            best_list = []
    best_list.append(best_entry)
    return (best_score, best_list)
