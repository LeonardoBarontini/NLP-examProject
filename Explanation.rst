============
Explanation
============


.. contents:: Explanation table of contents
	:local:

NLP functions
**********************
The heart of the project are the ``words_in_set``, ``matched_entries`` and ``best_match`` functions. They provide the natural language processing of the data, matching words and giving the match a score.

words_in_set
------------------------------
At the baseline, the ``words_in_set`` function takes a ``list_of_words`` and a ``sset``. For each word, it checks if that word is in the set and, if succesfull, it raises the score by one and counts a match found.

Now, the ``list_of_words`` could contain one or more descriptive words, wich appears in many set, even in ones that are uncorrelated. We can not discard them, but we have to take into account this phenomena.
Take for example *['abdominal', 'pain']*: discarding the word *'pain'* would result in a possible correlation with an ipotetical *'abdominal fat deposits'* entry, wich would be wrong. At the same time, taking into account every possible *'pain'* correlation could give birth to strange couples like *'abdominal pain'->'fingers pain'*, wich is also wrong.
For these reasons, when we have a ``list_of_words`` composed by two ore more words, every single word match is saved with a negative score. In this way we can preserve the matching score result (as absolute value) but we penalize it in further computations as, beeing negative, it's smaller then other scores.

We also have to address the word stemming: when ``stemmed``, a word could be changed either losing a piece or beeing modified. In this way when checking inside the set with the ``in`` statement, we will never find any corrispondence as the set's words are not stemmed.
Therefore we need to check for the stemmed word, not in the *set*, but in *every word of the set*, as the stemming process is built to preserve the root of the word and we aim to match that.

matched_entries
------------------------------
We now step up a level, the ``matched_entries`` function manages the ``dict_of_sets`` taken in input, passing one set at a time to the ``words_in_set`` function.
When the ``words_in_set`` function returns a score, if it's not zero, wich means that at least one match has been found, the ``matched_entries`` function adds to the dictionary it is building, the ``name`` of the matched set, as the key, together with its ``score``, as value.

We have seen that single word matches are problematic, but what to do when the set we are looking at has only one word?
That's why we can enable checking for ``mono`` word sets. In these cases, when there's a match the score will be negative for sure. Checking for the set to contain only one word, will let us set the ``score`` to an arbitrary '1', therefore recovering the match for further computations.

best_match
------------------------------
Lastly, the ``best_match`` function checks all the ``matched_entries`` picking the best one(s).
Iterating over the obtained dictionary, the function initially saves the first positive non-zero ``entry``: ``score`` pair that it founds, then updates it whenever a higher ``score`` appears.
Allowing for multiple best matches, every time a ``score`` equal to the best one is found, the ``entry`` is appended to the ``best_list``. The first ``best_entry`` found is appended last to dodge possible swapping mistakes.

When are these functions used?
------------------------------
To check the words of the connecting database to the receiving one's words, Stargate uses the NLP functions described above, calling the ``best_match`` functions with the appropriate parameters.

Stargate classes
**********************
This is a database linking project so it's normal to use databases, but the way the task is handled is worth some explanation.

As you can see the `stargate module <https://github.com/LeonardoBarontini/NLP-examProject/blob/main/stargate.py>`_ has more than one ``Stargate_*_`` class. That's because every receiving database needs its own procedure to be handled. In the same way, every connecting database needs to properly try to connect, depending on wich database it is trying to reach.

Stargate_to_SNAP_diseases
------------------------------
To handle connections to the ``SNAP_D_MeshMiner_miner_disease`` database, first of all the data has to be loaded, so we don't need to load again everything every time we try to connect a new database, we just use the same ``database_class_instance``. Then the data needs to be prepared for computation, this is because using raw database data accessed directly and processed during runtime, would result in aeons long computations.

The reasoning behind these preparation, both for the connecting and the receiving databases, is that we are trying to match entries between two different formatted databases, so we need to identify a common value type that allow for unique, easy and significant enough connections, and they have to be correct (as much as possible).

So after we identified the discriminant value we will try to match with, we need to develop these preparations. In this case, matchings are based on disease names. The receiving database is the one most work is done upon, here it's the SNAP database because of its ``synonims`` values that enlarge the word pool for every disease name and for its ``description`` values, both of wich highten the chanches of a successfull link.

For both databases, disease names, synonims and descriptions are divided by word (tokenized) and, for every word in the connecting disease name, the program checks if that word is present in the set of the receiving disease name, synonims and description.

Stargate_to_SNAP_genes
------------------------------
Handling connections to the ``G_SynMiner_miner_geneHUGO`` is easier because we can rely on genes codes (``symbol``) wich are unique and we can directly compare the values between databases.

Not having to process the data means a faster computation and the lack of need of checking functions.

Database classes
**********************
The database modules: `disgenet_database_class <https://github.com/LeonardoBarontini/NLP-examProject/blob/main/disgenet_database_class.py>`_, `RX_database_class <https://github.com/LeonardoBarontini/NLP-examProject/blob/main/RX_database_class.py>`_ and `snap_database_classes <https://github.com/LeonardoBarontini/NLP-examProject/blob/main/snap_database_classes.py>`_, contains the class instances that handle the various database used.

D_MeshMiner_miner_disease_instance
------------------------------
This class reads the respective ``.tsv`` file and loads the table into a ``pandas`` dataframe. A method for inserting the table into a database is the ``create_SNAP_disease_table`` method, that takes as input the name of the target database.

The other methods are used to prepare the data for the computations: the ``create_disease_name_synonyms_dicts`` creates a collection of set of words from names and synonims, the ``create_disease_name_description_dicts`` creates a collection of set of words from names and descriptions and the ``create_disease_name_only_dicts`` creates a collection of set of words from names only.

G_SynMiner_miner_geneHUGO_instance
------------------------------
This class reads the respective ``.tsv`` file and loads tha table into a pandas dataframe. A method for inserting the table into a database is the ``create_SNAP_gene_table`` method, that takes as input the name of the target database.

The ``create_gene_symbol_name_dict`` creates a dictionary of ``symbols:names`` wich will be used in the data computations.

Disgenet_instance
------------------------------
This class reads the ``disgenet.db`` database and, by default, loads the ``diseaseAttributes`` table. Loading and unloading methods are available for every table of the database.

The ``create_disease_dict`` and the ``create_gene_dict`` are the ones used to generate the ``ID:name`` dictionary of the data used in the computations.

RX_instance
------------------------------
This class reads the respective ``.json`` file and loads it in a pandas dataframe. These data still needs to be processed.

The ``create_main_lists`` and ``create_main_dicts`` functions process the data to get a ``ID:name`` dictionary for diseases and symptoms.

The ``create_drug_list`` and ``create_drug_dict`` functions process the data to get an ``ID:name`` dictionary for drugs.

The ``create_relation_dicts`` function produces four dictionaries in the form of ``ID:ID`` and will be the relational tables of the RX database.

The ``create_RX_database`` creates the database and the functions ``insert_into_*`` and ``populate``, respectively operates and manages the population of the database. 


Some management functions
**********************
In the `management_functions <https://github.com/LeonardoBarontini/NLP-examProject/blob/main/management_functions.py>`_ module are grouped some general pourpouse functions used in various places of the project.

format_string
-------------
This function is used to have a processing standard when dealing with strings. Formatting a to be used string, means that we know what to expect (almost) about the composition of that string, this facilitates processing as we don't need to check all the possible cases.

add_unique_*_id
---------------
These are functions, mainly used by the ``RX-class``, used to assign an unique id to lists of * when creating a database in case it didn't already exist. Those ids are used to prevent problems in case a modification of the single data entry is needed, basically the ids are invariants of the data entries.

check_overlap_percentage
------------------------
This function is used to see in percentage how many entries have been linked with at least one connection. It does not assess on the validity of the connection, it only checks how many entries are connected, giving an hint on the coverage of the connection process and not on its goodness. It's usefull to understand the linking performance of the algorithm.

check_unlinked
--------------
This function returns a list of the entries that did not get a connection. It's intended to be used when the ``Stargate`` methods are called using the ``*_with_check`` variant, as it takes in input the ``check_dict`` outputted by those variants. Its use is to show wich entries have failed to get a link, hoping that this could give some hints on how to boost the matching algorithm. It can also be used to inspect the list of missing entries in the receiving database, for eventual integrations.

The main function
**********************
The main pourpouse of this module is to wrap all the processes in one, easely executable, point. The base idea is that the user, `wich has the data files in the same folder of the project`, can just execute the main and have a cup of tea while the program does everything.

Some print statements should help in following the ongoing process, wich starts by processing SNAP data, than RX data, than start the connection process between RX and SNAP, then loads disgenet data and finally connects disgenet to SNAP.

Usefull informations are provided by the ``stop`` and ``start`` ``timer`` functions and the ``check_overlap_percentage`` functions, while the ``create_tsv_table_file`` and ``create_stargate_network_table`` functions respectively, produces a ``.tsv`` file with the single network data and adds the corresponding network table to the ``Stargate_big_database.db``
