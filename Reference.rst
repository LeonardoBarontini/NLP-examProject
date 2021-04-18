============
Reference
============


.. contents:: Reference table of contents
	:local:

disgenet_database_class module
******************************
Module containing the ``Disgenet_instance`` class wich handles the disgenet database.

Disgenet_instance
-----------------
Disgenet database handling class.

Acquires data from the database in the working directory, the database name is passed
as parameter in the ``__init__`` method.

By default only the ``diseaseAttributes`` table is loaded, the other tables are managed
using the ``load`` and ``unload`` methods. This is to not overload memory as data are stored
in the class instance for quick access.

A loaded table is saved as a ``pandas.read_sql_query`` dataframe in the respective
``self.table_name`` attribute. An unloaded table has the respective attribute set to ``None``.

For computation processes, disease and gene dictionaries are created respectively
with ``create_disease_dict`` and ``create_gene_dict`` methods.

__init__
^^^^^^^^
.. code-block:: python

    def __init__(self, database_name):
        self.database = sqlite3.connect(database_name)
        self.disease2class = None
        self.diseaseAttributes = pandas.read_sql_query("SELECT * FROM diseaseAttributes", self.database)
        self.diseaseClass = None
        self.geneAttributes = None
        self.geneDiseaseNetwork = None
        self.variantAttributes = None
        self.variantDiseaseNetwork = None
        self.variantGene = None

Initializer method.

>>> instance = Disgenet_instance("disgenet_2020.db")
>>> instance
<disgenet_database_class.Disgenet_instance at 0x7f279a3a12b0>

First estabilishes the connection with the database using the ``database_name``
passed as argument.
Then creates all the attributes where the database tables will be loaded.
Finally only the ``diseaseAttributes`` table is loaded, for memory sake.

load_****_table
^^^^^^^^^^^^^^^
.. code-block:: python

    def load_****_table(self):
        self.**** = pandas.read_sql_query("SELECT * FROM ****", self.database)

Loader method for the specified table.

It reads from the database and save the table in the respective class attribute.

unload_****_table
^^^^^^^^^^^^^^^^^
.. code-block:: python

    def unload_****_table(self):
        self.**** = None

Unloader method for the specified table.

Sets the respective class attribute to None.

create_disease_list
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_disease_list(self):
        target = self.diseaseAttributes['diseaseName']
        self.disease_list = list(target)

Creates a list of diseases from the diseaseAttributes table of the database.
Then creates the class attribute disease_list and saves there the list.

>>> instance.create_disease_list()
>>> instance.disease_list
['disease1', 'disease2', 'disease_n']

Note that before calling this method, the attribute does not exists.

>>> instance = Disgenet_instance("disgenet.db")
>>> instance.disease_list
AttributeError: 'Disgenet_instance' object has no attribute 'disease_list'

create_disease_dict
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_disease_dict(self):
        self.disease_dictionary = {}
        for index, row in self.diseaseAttributes.iterrows():
            self.disease_dictionary[row['diseaseNID']]=row['diseaseName']

Creates a dictionary of diseasesNID:diseaseName from the diseaseAttributes table
of the database, saving it in the class attribute disease_dictionary.

>>> instance.create_disease_dict()
>>> instance.disease_dictionary
{'1':'disease1', '2':'disease2', 'n':'disease_n'}

Note that before calling this method, the attribute does not exists.

>>> instance = Disgenet_instance("disgenet.db")
>>> instance.disease_dictionary
AttributeError: 'Disgenet_instance' object has no attribute 'disease_dictionary'

create_gene_dict
^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_gene_dict(self):
        self.gene_dictionary = {}
        for index, row in self.geneAttributes.iterrows():
            self.gene_dictionary[row['geneNID']]=(row['geneName'], row['geneDescription'])

Creates a dictionary of geneNID:(geneName, geneDescription) from the diseaseAttributes
table of the database, saving it in the class attribute gene_dictionary.

>>> instance.create_gene_dict()
>>> instance.gene_dictionary
{'1':('gene1', 'desc1'), '2':('gene2', 'desc2'), 'n':('geneN', 'descN')}

Note that before calling this method, the attribute does not exists.

>>> instance = Disgenet_instance("disgenet.db")
>>> instance.gene_dictionary
AttributeError: 'Disgenet_instance' object has no attribute 'gene_dictionary'


nlp module
**********
Module containing general Natural Language Processing (NLP) functions.

Defines the ``words_in_set``, ``matched_entries``, ``best_match`` functions.

Imports english ``stop_words`` and expands them with ``bad_words`` creating ``taboo_words``.

.. code-block:: python

    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    bad_words = ['1','2','3','4','5','6','7','8','9','0',
                 ':','!','?',';','.',',','(',')',"/",'\\','-','+',
                 'and','with','without']
    for el in bad_words:
        stop_words.add(el)
    taboo_words = stop_words

words_in_set
------------

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
---------------

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

>>> matched_entries(
                    ['hello', 'world'],
                    {
                    'hello':{'hello', 'ciao', 'salut'},
                    'hello world':{'hello', 'world', 'python'}
                        }
                    )
{'hello': -1, 'hello world': 2}

The ``stemmed`` option is just passed to the words_in_set function.

The ``mono`` option is used to recover single word matches when we have a
**single word** `set` to match to. In these cases the score is set to 1.

>>> matched_entries(
                    ['hello', 'world'],
                    {
                    'hello':{'hello'},
                    'hello world':{'hello', 'hi', 'python'}
                        },
                    mono=True
                    )
{'hello': 1, 'hello world': -1}

best_match
----------

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

>>> best_match(
                ['hello', 'world', 'python'],
                {
                'hello':{'hello', 'ciao', 'salut'},
                'hello world':{'hello', 'world'},
                'hello python':{'hello', 'world', 'python'},
                'ciao python':{'ciao', 'hello', 'world', 'python'}
                    }
                )
(3, ['ciao python', 'hello python'])

Note that the first entry with the best score found, is last in the list.