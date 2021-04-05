============
Reference
============


.. contents:: Reference table of contents
	:local:

nlp module
----------

words_in_set
************

.. code-block:: python

	words_in_set(list_of_words, sset, stemmed=False):
		[...]
		return score

Gives a score to state how well ``list_of_words`` and ``sset`` match.

``list_of_words`` is a `list` containing one or more `strings`, wich are **single word** `strings`.

``sset`` is a `set` cointaining one or more `strings`, wich are **single word** `strings`.

``stemmed`` is a `boolean` value.
    
It looks for how many of the words in ``list_of_words`` are present in the `set`
and gives a positive score if more than one are present.

>>> words_in_set(['hello', 'world', 'Italy'], {"hello", 'world'})
2

If only one is present, the match is penalized transforming the score from
positive to negative. This is to avoid matches given by common words.

>>> words_in_set(['hello', 'world'], {"hello"})
-1

If ``list_of_words`` is composed by *only one* word, it ignores the single word
match penalization.

>>> words_in_set(['hello'], {"hello", 'world'})
1

The ``stemmed`` flag allows for a proper checking in the `set`, iterating for
every `set` `item` so the ``in`` statement checks for the word inside a single
`string` and not in the hole `set`, where it would search for the exact same
word wich, beeing stemmed, will not be present.

>>> words_in_set(['hel', 'worl', 'Ital'], {"hello", 'world'}, stemmed=True)
2							

matched_entries
***************

.. code-block:: python

	matched_entries(list_of_word, dict_of_sets, stemmed=False, mono=False):
		[...]
		return dictionary

Returns a `dictionary` in the form: ``{'database name key': score}``

``list_of_words`` is a `list` containing one or more `strings`, wich are **single word** `strings`.

``dict_of_sets`` is a `dictionary` containing as `keys` the 'name' of the items and as `items` a `set` cointaining one or more `strings`, wich are **single word** `strings`.

``stemmed`` and ``mono`` are `boolean` values.
    
It creates a `dictionary` using the name keys of ``dict_of_sets`` as `keys` and
associates to them the matching score given by the ``words_in_set`` function
between ``list_of_word`` and the item set of the key it is examining. It adds
the `key` to the `dictionary` only if the score is not zero.

>>> matched_entries(['hello', 'world'],
                    {
                    'hello':{'hello', 'ciao', 'salut'},
                    'hello world':{'hello', 'world', 'python'}
                        }
                    )
{'hello': -1, 'hello world': 2}

The ``stemmed`` option is just passed to the words_in_set function.

The ``mono`` option is used to recover single word matches when we have a
**single word** `set` to match to. In these cases the score is set to 1.

>>> matched_entries(['hello', 'world'],
                    {
                    'hello':{'hello'},
                    'hello world':{'hello', 'hi', 'python'}
                        },
                    mono=True
                    )
{'hello': 1, 'hello world': -1}

best_match
**********

.. code-block:: python
	
	best_match(list_of_words, dict_of_sets, stemmed=False, mono=False):
		[...]
		return (best_score, best_list)

Returns a `tuple` containing (the ``best_score``, the ``best_list``) among all
the ``scores`` and lists given by the ``matched_entries`` function.

``list_of_words`` is a `list` containing one or more `strings`, wich are **single word** `strings`.

``dict_of_sets`` is a `dictionary` containing as `keys` the 'name' of the items and as `items` a `set` cointaining one or more `strings`, wich are **single word** `strings`.

``stemmed`` and ``mono`` are `boolean` values.

To spot the best matches among the obtained ones, it iterates over the
returned `dictionary` checking the ``score`` of the item against the ``best_score``.
If it finds a better score, it saves ``score`` and ``entry`` as bests. If the score
equals the ``best_score`` it appends the ``entry`` to the ``best_list``. Otherwise
does nothing.

The ``mono`` and ``stemmed`` options are passed to the ``matched_entries`` function.

>>> best_match(['hello', 'world', 'python'],
                {
                'hello':{'hello', 'ciao', 'salut'},
                'hello world':{'hello', 'world'},
                'hello python':{'hello', 'world', 'python'},
                'ciao python':{'ciao', 'hello', 'world', 'python'}
                    }
                )
(3, ['ciao python', 'hello python'])

Note that the first entry with the best score found, is last in the list.