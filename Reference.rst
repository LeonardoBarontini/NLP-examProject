============
Reference
============


.. contents:: Reference table of contents
	:local:

management_functions module
***************************
Collection module of various functions for general processing or management

format_string
-------------
.. code-block:: python

    format_string(string, boosted=False):
        [...]
        return 'formatted string'

Tries to format the passed string to a "standard".

``string`` is the `string` that the function will format.

``boosted`` is a `boolean` value.

The first step the function takes is to remove the RX-``disease_recognition_string`` if present.

.. code-block:: python

    step1 = string.split(disease_recognition_string)[0] 

so you'll have::

    'fever_symptoms_and_signs'  --->  'fever'

The second and third steps make the string all lowercase and remove leading and triling whitespaces.

.. code-block:: python

    step2 = step1.lower()
    step3 = step2.strip()

so you'll have::

    ' Fever '  --->  ' fever '  --->   'fever'

The fourth step replaces '_' with a withespace.

.. code-block:: python

    step4 = step3.replace('_', ' ')

so you'll have::

    'abdominal_pain'  --->  'abdominal pain'

The fifth step removes saxson's genitives.

.. code-block:: python

    step5 = step4.replace("'s", '')

so you'll have::

    'alzheimer's disease'  --->  'alzheimer disease'

The sixth step replaces '/' with ' or '.

.. code-block:: python

    step6 = step5.replace("/", ' or ')

so you'll have::

    'internal/external'  --->  'internal or external'

By default formattation ends here and the function returns the obtained string.

The ``boosted`` flag allows for a more powerful but more compute consuming formattation using standard nlp procedures:

The seventh step tokenizes the string by word, using the ``nltk.tokenize.word_tokenize`` function and so creating a list of words contained in the string.

.. code-block:: python

    step7 = word_tokenize(step6)

so you'll have::

    'low blood pressure'  --->  ['low', 'blood', 'pressure']

The eigth step removes from the list the ``bad_words``.

.. code-block:: python

    step8 = [w for w in step7 if w not in bad_words]

so you'll have::

    ['pneumonia', '3', 'with', 'sepsis']  --->  ['pneumonia', 'sepsis']

The nineth step makes the list a set to remove duplicates word.

.. code-block:: python

    step9 = set(step8)

so you'll have::

    ['abdominal', 'pain', 'pain', 'guts']  --->  {'abdominal', 'pain', 'guts'}

The tenth and last step recreates a string from the set.

.. code-block:: python

    step10 = ' '.join(word for word in step9)

so you'll have::

    {'abdominal', 'pain', 'guts'}   --->   'abdominal pain guts'

then the function returns the string.

add_unique_disease_id
---------------------

.. code-block:: python

    add_unique_disease_id(lis, digits=6):
        [...]
        return id_diseases_dict

Given a list of diseases returns a dictionary in the form ``{id:disease}``.

``lis`` is a `list` containing one or more `strings`.

``digits`` is an `int` value wich defines the lenght of the numeral part of the id.

The id construction is based on the disease's index in the list, wich is
filled with zeros to the left, to reach the lenght fixed by the ``digits`` value,
the resulting string is appended to the ``base`` string, giving the id.
For example:
    if at index 114 we have 'Fever'

    the default dictionary output will be >> ``dis000114:'Fever'``
If the passed list il longer than how much the digits can handle, a warning
message is displayed while raising ``ValueError``.
Warning: ``lis`` is assumed to have unique elements. 

add_unique_symptom_id
---------------------

.. code-block:: python

    add_unique_symptom_id(lis, digits=6):
        [...]
        return id_symptoms_dict

Given a list of symptoms returns a dictionary in the form ``{id:symptom}``.

``lis`` is a `list` containing one or more `strings`.

``digits`` is an `int` value wich defines the lenght of the numeral part of the id.

The id construction is based on the symptom's index in the list, wich is
filled with zeros to the left, to reach the lenght fixed by the ``digits`` value,
the resulting string is appended to the ``base`` string, giving the id.
For example:
    if at index 214 we have 'Chills'

    the default dictionary output will be >> ``sym000214:'Chills'``
If the passed list il longer than how much the digits can handle, a warning
message is displayed while raising ``ValueError``.
Warning: ``lis`` is assumed to have unique elements. 

add_unique_drug_id
------------------

.. code-block:: python

    add_unique_drug_id(lis, digits=6):
        [...]
        return id_drugs_dict

Given a list of drugs returns a dictionary in the form ``{id:drug}``.

``lis`` is a `list` containing one or more `strings`.

``digits`` is an `int` value wich defines the lenght of the numeral part of the id.

The id construction is based on the drug's index in the list, wich is
filled with zeros to the left, to reach the lenght fixed by the ``digits`` value,
the resulting string is appended to the ``base`` string, giving the id.
For example:
    if at index 314 we have 'Aspirin'

    the default dictionary output will be >> ``drg000314:'Aspirin'``
If the passed list il longer than how much the digits can handle, a warning
message is displayed while raising ``ValueError``.
Warning: ``lis`` is assumed to have unique elements. 

get_id_of_string
----------------

.. code-block:: python

    get_id_of_string(dictionary, string):
        [...]
            if found:
                return searched_id
        return None

``dictionary`` is a `dictionary` in the form ``{id:string}``.

``string`` is a `string` which is searched among the ``dictionary``'s items.

Given a ``dictionary`` and a ``string``, searches for the string inside the
dictionary's items and, if it founds it, returns the associated key.

>>> get_id_of_string({'id1': 'hello', 'id2':'ciao'}, "ciao")
'id2'

The passed dictionary is supposed to contain unique ids, wich are strings,
as keys and strings as items.
So function returns the id of the passed string if it's present.

Warning: it's supposed that a string can be related to only one id. Every
subsequent match will be ignored as only the first is returned.

add_relation_to_dict
--------------------

.. code-block:: python

    add_relation_to_dict(dictionary, id_key, id_data):
        [...]
        return dictionary

``dictionary`` is a `dictionary` in the form ``{id_string:[id_string, id_string]}``.

``id_key`` is a `string` wich will be a key in the ``dictionary``.

``id_data`` is a `string` wich will be part of the list, item of ``id_key`` in the ``dictionary``.

Given a ``dictionary``, an id wich will be a key and an id wich will be an
item, the function adds the ``id_data`` to the list item of the ``id_key`` of the
``dictionary`` if that ``id_data`` isn't altready present, otherwise does nothing
and then returns the updated ``dictionary``.

The keys' items are lists of ids.

>>> add_relation_to_dict({'dis000314':['sym000041']}, 'dis000014', 'sym000002')
{'dis000314':['sym000041'], 'dis000014':['sym000002']}

start_timer_at & stop_timer_at
------------------------------
These functions are intended to work together as one relies on the saved output of the other.

.. code-block:: python

    start_timer_at(time):
        print(datetime.fromtimestamp(time).time())
        return time

``time`` is a `float` given by the time() function of the time library.

Prints information about the time obtained from the time library.
Returns the passed time for storing purpouses.
    
    >>> start = start_timer_at(time())
    12:06:20.514967
    >>> start
    1619777180.5149667

.. code-block:: python

    stop_timer_at(stop, start):
        print('\rfinished processing in '+str(stop-start)+' seconds')
        return stop

``start`` and ``stop`` are `float` given by the time() function of the time library.

Prints information about the elapsed processing time, calculating from
the start time, to the stop time, both of wich are passed as inputs.
    
    >>> end = stop_timer_at(time(),start)
    finished processing in 6.508876800537109 seconds
    >>> end
    1619777666.3599267

check_overlap_percentage
------------------------

.. code-block:: python

    check_overlap_percentage(initial_dataset, dataset_name, link_network, final_dataset_name, precise=False):
        [...]
        over = (count/total)*100
        [...]
        return over

``initial_dataset`` is a `dictionary` in the form ``{id:string}``.

``dataset_name`` is a `string` representing the name of the initial dataset.

``link_network`` is a `dictionary` in the form ``{id:([id_list], score, 'unchecked')}``.

``final_dataset_name`` is a `string` representing the name of the final dataset.

``precise`` is a `boolean` flag wich enables printing of the overlapping float value.

``over`` is the `float` value resulting from the computation of the overlapping.

Given an ``initial_dataset`` and a ``link_network``, checks for how many items
of the ``link_network`` have a connection, wich means a "non empty" list, then
calculates the percentage of connections with respect to the total entries of
the ``initial_dataset``.
Prints out the result using the linked dataset names for better comprehention.
If ``precise`` is set to ``True``, also prints the float value of the percentage,
wich could be useful to spot subtle changes in the linking outcome.
Returns ``over`` for eventual computations.
    
    >>> check_overlap_percentage(RXdata.id_diseases_dict, 'RXdata', RX_to_SNAP_disease_links, 'SNAPdata diseases', precise=True)
    overlap between RXdata and SNAPdata diseases : 94%
    94.98480243161094

check_unlinked
--------------

.. code-block:: python

    check_unlinked(check_dict):
        lista = []
        [...]
        return lista

``check_dict`` is a `dictionary` in the form ``{id:([name_list], score, 'unchecked')}``.

``lista`` is a `list` where the unlinked entries are appended.

Checks for how many items of the ``check_dict``
don't have a connection, wich means an "empty" list, then appends the
respective key to a list wich will be returned at the end.
    
    >>> check_unlinked({'fever':(['some connection'], 2, 'unchecked'), 'nausea':([''], 0, 'unchecked')})
    ['nausea']

create_tsv_table_file
---------------------

.. code-block:: python

    create_tsv_table_file(filename, output_dict):
        [...]
        tsv_file.write('# ID_start\tID_end\tScore\tStatus\n')
        [...]
            tsv_file.write(id_start+'\t'+id_end+'\t'+str(score)+'\t'+chek+'\n')
        [...]
        return 'Done'

``filename`` is a `string` in the form ``'filename.tsv'``.

``output_dict`` is a `dictionary` in the form ``{id:([name_list], score, 'unchecked')}``.

Given a dictionary of ID conncetions, with score and status, and
a 'filename.tsv', creates a tsv file containing the dictionary informations.
The columns names are: ID_start - ID_end - Score - Status

create_stargate_network_table
---------------------

.. code-block:: python

    create_tsv_table_file(database_name, output_dict, table_name, initial_ID_table_column_ref, final_ID_table_column_ref):
        database = sqlite3.connect(database_name)
        c = database.cursor()
        [...]
        c.execute("DROP TABLE IF EXISTS "+table_name+";")
        c.execute("CREATE TABLE IF NOT EXISTS "+table_name+"("+initial_column+" TEXT NOT NULL, "+final_column+" TEXT, Score TEXT, Status TEXT, FOREIGN KEY("+initial_column+") REFERENCES "+initial_ID_table_column_ref+" ON DELETE CASCADE, FOREIGN KEY("+final_column+") REFERENCES "+final_ID_table_column_ref+" ON DELETE CASCADE);")    
        [...]
                c.execute("INSERT OR IGNORE INTO "+table_name+" ("+initial_column+", "+final_column+", Score, Status) VALUES(?,?,?,?);",(id_start, id_end, score, chek))
        [...]
        return 'Done'

``database_name`` is a `string` in the form ``'database.db'``.

``output_dict`` is a `dictionary` in the form ``{id:([name_list], score, 'unchecked')}``.

``table_name`` is a `string` in the form ``'new_table_name'``.

``initial_ID_table_column_ref`` is a `string` in the form ``'tableName(referenceColumn)``.

``final_ID_table_column_ref`` is a `string` in the form ``'tableName(referenceColumn)``.

Creates a new table (or updates the existing one) in the passed database,
populating it with the output_dict dictionary informations.

The table is composed of four columns: 

* column 1: the ID reference of the connecting table
* column 2: the ID reference of the recieving table
* column 3: the score of the connection
* column 4: the status of the connection

count_elements
--------------

.. code-block:: python

    count_elements(lis):
        [...]
        return counts

Given a list, returns another list with the same lenght, wich has 
in place of every element of the passed list, its frequency in that list.
    
    >>> count_elements(['a', 'a', 'b', 'c', 'b', 'a', 'd', 'z'])
    [3, 3, 2, 1, 2, 3, 1, 1]

frequency_dictionary
--------------------

.. code-block:: python

    frequency_dictionary(lis):
        [...]
        return dictionary

Given a list, returns a dictionary that has every element of the
passed list as key and his frequency inside that list as item.
    
    >>> frequency_dictionary(['a', 'a', 'b', 'c', 'b', 'a', 'd', 'z'])
    {'a':3, 'b':2, 'c':1, 'd':1, 'z':1}

snap_database_classes module
******************************
Module containing the ``D_MeshMiner_miner_disease_instance`` class and
``G_SynMiner_miner_geneHUGO_instance`` class wich handles the SNAP-database's tables.

D_MeshMiner_miner_disease_instance
------------------------------
*'D-MeshMiner_miner-disease.tsv'* SNAP table handling class.

Acquires data from the .tsv file in the working directory, the filename is 
supposed to be static and is hardcoded in the ``__init__`` method.

The loaded table is saved as a ``pandas.read_table`` dataframe in the respective
``self.dataframe`` attribute.

The ``create_SNAP_disease_table_in`` method gives you the possibility to add the
SNAP table to an existing database.

For computation processes, dictionaries of sets of words related to a specific
*disease_name*, are created with ``create_disease_name_synonyms_dicts`` method
from the *Name* and *Synonyms* columns, with ``create_disease_name_description_dicts``
method from the *Name* and *Definitions* columns and with ``create_disease_name_only_dicts``
method from the *Name* column only.

__init__
^^^^^^^^

.. code-block:: python

    def __init__(self):
        self.dataframe = pandas.read_table('D-MeshMiner_miner-disease.tsv')

Initializer method.

>>> instance = D_MeshMiner_miner_disease_instance()
>>> instance
<snap_database_classes.D_MeshMiner_miner_disease_instance at 0x7ff40822e250>

Loads the *'D-MeshMiner_miner-disease.tsv'*  table in a pandas dataframe
wich is stored in the ``self.dataframe`` attribute.

The table is composed of four columns: 

- column 1: the ID reference of the disease
- column 2: the Name of the disease
- column 3: the Definitions, characterizing the disease
- column 4: the Synonyms, other known names of the disease

create_SNAP_disease_table_in
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    create_SNAP_disease_table_in(self, database_name):
        self.database = sqlite3.connect(database_name)
        self.c = self.database.cursor()
        self.c.execute("DROP TABLE IF EXISTS D_MeshMiner_miner_disease;")
        self.c.execute("CREATE TABLE IF NOT EXISTS D_MeshMiner_miner_disease(MESH_ID TEXT PRIMARY KEY NOT NULL, Name TEXT, Definitions TEXT, Synonyms TEXT);")
        for index, row in self.dataframe.iterrows():
            self.c.execute("INSERT OR IGNORE INTO D_MeshMiner_miner_disease (MESH_ID, Name, Definitions, Synonyms) VALUES(?,?,?,?);",(row['# MESH_ID'], row['Name'], row['Definitions'], row['Synonyms']))
        [...]
        return 'Done'

``database_name`` is a `string` in the form ``'database.db'``.

Creates a new table (or updates the existing one) in the passed database,
populating it with the 'D-MeshMiner_miner-disease.tsv' informations.
The created table in the database will have the name *D_MeshMiner_miner_disease*.

The table is composed of four columns: 

- column 1: the ID reference of the disease
- column 2: the Name of the disease
- column 3: the Definitions, characterizing the disease
- column 4: the Synonyms, other known names of the disease

create_disease_name_synonyms_dicts
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    create_disease_name_synonyms_dicts(self):
        dict_of_sets = {}
        for index, row in self.dataframe.iterrows():
            entry_set = set()
            synonyms_list = []
            name = row['Name']
            name_word_list = word_tokenize(format_string(name, boosted=True))
            for x in name_word_list:
                entry_set.add(x)
            if type(row['Synonyms']) is str:
                synonyms_list = row['Synonyms'].split('|')
                word_list=[]
                for string in synonyms_list:
                    formatted = format_string(string, boosted=True)
                    word_list.extend(word_tokenize(formatted))
                for x in word_list:
                    entry_set.add(x)
            entry_set.difference_update(taboo_words)
            dict_of_sets[name] = entry_set
        return dict_of_sets

Returns a dictionary in the form
{'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'and', 'synonyms'}}

The set is populated with words from the 'Name' and 'Synonyms' columns;
it is accessed by the corresponding disease_name.

Given
:: 
               Name                Synonyms
        0  disease1   dis1|d1|first disease
        1  disease2  dis2|d2|second disease


We have

>>> instance.create_disease_name_synonyms_dicts()
{'disease1': {'d1', 'dis1', 'disease', 'disease1', 'first'},
 'disease2': {'d2', 'dis2', 'disease', 'disease2', 'second'}}


create_disease_name_description_dicts
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    create_disease_name_description_dicts(self):
        dict_of_sets = {}
        for index, row in self.dataframe.iterrows():
            entry_set = set()
            description_list = []
            name = row['Name']
            name_word_list = word_tokenize(format_string(name, boosted=True))
            for x in name_word_list:
                entry_set.add(x)
            if type(row['Definitions']) is str:
                description_list = word_tokenize(format_string(row['Definitions'], boosted=True))
                for x in description_list:
                    entry_set.add(x)
            entry_set.difference_update(taboo_words)
            dict_of_sets[name] = entry_set
        return dict_of_sets

Return a dictionary in the form
{'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'and', 'definition'}}

The set is populated with words from the 'Name' and 'Definitions' columns;
it is accessed by the corresponding disease_name.

Given
:: 
               Name                Definitions
        0  disease1   this is the first disease
        1  disease2  this is the second disease


We have

>>> instance.create_disease_name_description_dicts()
{'disease1': {'disease', 'disease1', 'first'},
 'disease2': {'disease', 'disease2', 'second'}}

create_disease_name_only_dicts
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    create_disease_name_only_dicts(self):
        dict_of_sets = {}
        for index, row in self.dataframe.iterrows():
            entry_set = set()
            name = row['Name']
            name_word_list = word_tokenize(format_string(name, boosted=True))
            for x in name_word_list:
                entry_set.add(x)
            entry_set.difference_update(taboo_words)
            dict_of_sets[name] = entry_set
        return dict_of_sets

Return a dictionary in the form
{'disease_name_string': {'set', 'of', 'word', 'in', 'name', 'only'}}

The set is populated with words from the 'Name' column only;
it is accessed by the corresponding disease_name.

Given
:: 
                     Name
        0        disease1
        1  second disease


We have

>>> instance.create_disease_name_description_dicts()
{'disease1': {'disease1'},
 'second disease': {'disease', 'second'}}

G_SynMiner_miner_geneHUGO_instance
------------------------------
*'G-SynMiner_miner-geneHUGO.tsv'* SNAP table handling class.

Acquires data from the .tsv file in the working directory, the filename is 
supposed to be static and is hardcoded in the ``__init__`` method.

The loaded table is saved as a ``pandas.read_table`` dataframe in the respective
``self.dataframe`` attribute.

The ``create_SNAP_gene_table_in`` method gives you the possibility to add the
SNAP table to an existing database.

For computation processes, a dictionary relating a specific gene code to its
name is created with ``create_gene_symbol_name_dict method``.

__init__
^^^^^^^^

.. code-block:: python

    def __init__(self):
        self.dataframe = pandas.read_table('G-SynMiner_miner-geneHUGO.tsv')

Initializer method.

>>> instance = G_SynMiner_miner_geneHUGO_instance()
>>> instance
<snap_database_classes.G_SynMiner_miner_geneHUGO_instance at 0x7f9fc8081100>

Loads the *'G-SynMiner_miner-geneHUGO.tsv'* table in a pandas dataframe
wich is stored in the self.dataframe attribute.

The table is composed of 48 columns but the program uses only two of them: 

- column 3: 'symbol', a specific gene identification code
- column 4: 'name', common name of the gene

create_SNAP_gene_table_in
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_SNAP_gene_table_in(self, database_name):
        self.database = sqlite3.connect(database_name)
        self.c = self.database.cursor()
        #mamit-trnadb and pseudogene.org have been reformatted to pseudogene_org and mamit_trnadb to allow execution
        string1 = "ensembl_gene_id TEXT PRIMARY KEY NOT NULL, hgnc_id TEXT, symbol TEXT, name TEXT, locus_group TEXT, locus_type TEXT, status TEXT, location TEXT, location_sortable TEXT, alias_symbol TEXT, alias_name TEXT, prev_symbol TEXT, prev_name TEXT, gene_family TEXT, gene_family_id TEXT, date_approved_reserved TEXT, date_symbol_changed TEXT, date_name_changed TEXT, date_modified TEXT, entrez_id TEXT, vega_id TEXT, ucsc_id TEXT, ena TEXT, refseq_accession TEXT, ccds_id TEXT, uniprot_ids TEXT, pubmed_id TEXT, mgd_id TEXT, rgd_id TEXT, lsdb TEXT, cosmic TEXT, omim_id TEXT, mirbase TEXT, homeodb TEXT, snornabase TEXT, bioparadigms_slc TEXT, orphanet TEXT, pseudogene_org TEXT, horde_id TEXT, merops TEXT, imgt TEXT, iuphar TEXT, kznf_gene_catalog TEXT, mamit_trnadb TEXT, cd TEXT, lncrnadb TEXT, enzyme_id TEXT, intermediate_filament_db TEXT"
        self.c.execute("CREATE TABLE IF NOT EXISTS G_SynMiner_miner_geneHUGO("+string1+");")
        string2 = 'ensembl_gene_id, hgnc_id, symbol, name, locus_group, locus_type, status, location, location_sortable, alias_symbol, alias_name, prev_symbol, prev_name, gene_family, gene_family_id, date_approved_reserved, date_symbol_changed, date_name_changed, date_modified, entrez_id, vega_id, ucsc_id, ena, refseq_accession, ccds_id, uniprot_ids, pubmed_id, mgd_id, rgd_id, lsdb, cosmic, omim_id, mirbase, homeodb, snornabase, bioparadigms_slc, orphanet, pseudogene_org, horde_id, merops, imgt, iuphar, kznf_gene_catalog, mamit_trnadb, cd, lncrnadb, enzyme_id, intermediate_filament_db'
        for index, row in self.dataframe.iterrows():
            self.c.execute("INSERT OR IGNORE INTO G_SynMiner_miner_geneHUGO ("+string2+") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(row['# ensembl_gene_id'], row['hgnc_id'], row['symbol'], row['name'], row['locus_group'], row['locus_type'], row['status'], row['location'], row['location_sortable'], row['alias_symbol'], row['alias_name'], row['prev_symbol'], row['prev_name'], row['gene_family'], row['gene_family_id'], row['date_approved_reserved'], row['date_symbol_changed'], row['date_name_changed'], row['date_modified'], row['entrez_id'], row['vega_id'], row['ucsc_id'], row['ena'], row['refseq_accession'], row['ccds_id'], row['uniprot_ids'], row['pubmed_id'], row['mgd_id'], row['rgd_id'], row['lsdb'], row['cosmic'], row['omim_id'], row['mirbase'], row['homeodb'], row['snornabase'], row['bioparadigms_slc'], row['orphanet'], row['pseudogene.org'], row['horde_id'], row['merops'], row['imgt'], row['iuphar'], row['kznf_gene_catalog'], row['mamit-trnadb'], row['cd'], row['lncrnadb'], row['enzyme_id'], row['intermediate_filament_db']))
        self.database.commit()
        self.database.close()
        return 'Done'

``database_name`` is a `string` in the form ``'database.db'``.

Creates a new table (or updates the existing one) in the passed database,
populating it with the 'G-SynMiner_miner-geneHUGO.tsv' informations.
The created table in the database will have the name *G_SynMiner_miner_geneHUGO*.

create_gene_symbol_name_dict
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    dictionary = {}
        for index, row in self.dataframe.iterrows():
            dictionary[row['symbol']] = row['name']
        return dictionary

Return a dictionary in the form {'gene_symbol': 'gene_name'}

The dictionary is populated with the 'symbol' and 'name' entries of
the table's rows.

Given
::
      symbol   name
    0  SYM1B  gene1
    1  SYM2B  gene2

We have

>>> instance.create_disease_name_description_dicts()
{'SYM1B': 'gene1', 'SYM2B': 'gene2'}

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

Loader method for the named table.

It reads from the database and save the table in the respective class attribute.

unload_****_table
^^^^^^^^^^^^^^^^^
.. code-block:: python

    def unload_****_table(self):
        self.**** = None

Unloader method for the named table.

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

RX_database_class module
******************************
Module containing the ``RX_instance`` class wich handles the RX-database.

RX_instance
-----------------
RX-database class: takes the *json* *csv* and manages it to create a database.

The file name is passed as argument in the instanciation.
The instanciation loads the file as a *pandas dataframe*, keeping it loaded.

The data distincion between disease and symptom is held by the
``disease_recognition_string`` attribute.

Various methods manage data formatting and database populating. 

__init__
^^^^^^^^
.. code-block:: python

    def __init__(self, json_data):
        self.data = json.load(open(json_data))
        self.df = pandas.DataFrame(data=self.data)
        self.disease_recognition_string = '_symptoms_and_signs'

Initializer method.

>>> instance = RX_instance("RXlist_data.json")
>>> instance
<RX_database_class.RX_instance at 0x7fb31c120670>

The file is loaded via the *json* module and saved in the ``data`` attribute.
The data attribute is converted to a *pandas dataframe*, then is stored
in the ``df`` attribute for further computations.

The entries are composed of *diseases* and *symptoms*.
The distincion between disease and symptom is held by the
``disease_recognition_string`` attribute.

create_main_lists
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_main_lists(self):
        self.diseases_list=[]
        self.symptoms_list=[]
        for key, items in self.df.iteritems():
            formatted_key = format_string(key)

            if self.disease_recognition_string in key:
                if formatted_key not in self.diseases_list:
                    self.diseases_list.append(formatted_key)
            else:
                if formatted_key not in self.symptoms_list:
                    self.symptoms_list.append(formatted_key)

            for sym in items[0]:   #['Related']
                symptom = format_string(sym)
                if symptom not in self.symptoms_list:
                    self.symptoms_list.append(symptom)

            for dis in items[1]:   #['Causes']
                disease = format_string(dis)
                if disease not in self.diseases_list:
                    self.diseases_list.append(disease)

        return 'created main lists\n'

Method that processes raw data creating two lists needed for further
computation: ``self.diseases_list`` and ``self.symptom_list``.

It reads the ``self.df`` *pandas dataframe*, iterating over the entries
divided between former keys and items of the json dictionary.

When iterating over the keys it divedes them between the two lists
based on the ``self.disease_recognition_string``.
Then it searches inside the *Related* and *Causes* lists to catch possible
diseases or symptoms not listed in the main object.

create_main_dicts
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_main_dicts(self):
        self.id_diseases_dict = add_unique_disease_id(self.diseases_list)
        self.id_symptoms_dict = add_unique_symptom_id(self.symptoms_list)
        
        return 'created main dicts\n'

Method that creates diseases and symptoms *id based dictionaries* in the
form: ``{'unique_id': 'entry_name'}``.

It passes the ``self.*_list`` to the *management function* ``add_unique_*_id``,
then stores the resulting dicionaries in the ``self.id_*_dict``.

create_drug_list
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_drug_list(self):
        self.drug_list = []
        for key, items in self.df.iteritems():
            data_drug_list = items[2]   #['Drugs']
            for drg in data_drug_list:
                drug = format_string(drg)
                if drug in self.drug_list: pass
                else:
                    self.drug_list.append(drug)

        return 'created drug list\n'

Method that process raw data creating a list needed for further
computation: ``self.drug_list``.

It iterates the ``self.df`` dataframe and collects all the *'Drugs'*  found
in the former items of the json dictionary.

create_drug_dict
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_drug_dict(self):
        self.id_drugs_dict = add_unique_drug_id(self.drug_list)

        return 'created drug dict\n'

Method that creates drug *id based dictionary* in the form:
    ``{'unique_id': 'entry_name'}``.
It passes the ``self.drug_list`` to the *management function* 
``add_unique_drug_id``, then stores the resulting dicionary in
the ``self.id_drugs_dict``.

create_relation_dicts
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_relation_dicts(self):
        self.dis_sym_dict={}
        self.sym_sym_dict={}
        self.dis_drg_dict={}
        self.sym_drg_dict={}
        for key, items in self.df.iteritems():

            if self.disease_recognition_string in key:
                disease = format_string(key)
                dis_id = get_id_of_string(self.id_diseases_dict, disease)

                for sym in items[0]:   #['Related']
                    symptom = format_string(sym)
                    sym_id = get_id_of_string(self.id_symptoms_dict, symptom)
                    self.dis_sym_dict = add_relation_to_dict(self.dis_sym_dict, dis_id, sym_id)

                if items[1] != []:   #['Causes']
                    print(''.zfill(42))
                    print("This disease has a cause!!! What's going on???")
                    print(key)
                    raise ValueError

                for drg in items[2]:   #['Drugs']
                    drug = format_string(drg)
                    drg_id = get_id_of_string(self.id_drugs_dict, drug)
                    self.dis_drg_dict = add_relation_to_dict(self.dis_drg_dict, dis_id, drg_id)
            else:
                symptom = format_string(key)
                sym_id = get_id_of_string(self.id_symptoms_dict, symptom)

                for sym2 in items[0]:   #['Related']
                    symptom2 = format_string(sym2)
                    sym2_id = get_id_of_string(self.id_symptoms_dict, symptom2)
                    self.sym_sym_dict = add_relation_to_dict(self.sym_sym_dict, sym_id, sym2_id)

                for dis in items[1]:   #['Causes']
                    disease = format_string(dis)
                    dis_id = get_id_of_string(self.id_diseases_dict, disease)
                    self.dis_sym_dict = add_relation_to_dict(self.dis_sym_dict, dis_id, sym_id)

                for drg in items[2]:   #['Drugs']
                    drug = format_string(drg)
                    drg_id = get_id_of_string(self.id_drugs_dict, drug)
                    self.sym_drg_dict = add_relation_to_dict(self.sym_drg_dict, sym_id, drg_id)

        return 'created relational dictionaries\n'

Method that uses the ``self.id_*_dict`` and the ``self.df`` dataframe to create
relational dictionaries in the form:
    ``{'entry_id':['list', 'of', 'related', 'ids']}``.

It uses the ``get_id_of_string`` *management function* to fetch the ids from
the ``self.id_*_dict``.

The dictionaries created are saved in ``self.dis_sym_dict``, ``self.sym_sym_dict``,
``self.dis_drg_dict``, ``self.sym_drg_dict``.

It uses the ``add_relation_to_dict`` *management function* to populate the
``self.*_*_dict`` with relations.

To create a relation, first it iterates the ``self.df`` dataframe identifying
the former key as a disease or as a symptom; then, in the disease case,
it associates its id to a list af related symptoms, for the ``dis_sym_dict``,
and to a list of related drugs, for the ``dis_drg_dict``; otherwise, in the
stmptom case, it associates its id to a list af related symptoms, 
for the ``sym_sym_dict``, and to a list of related drugs, for the ``sym_drg_dict``,
also checking for previouselty unrelated diseases to add to the ``dis_sym_dict``.

As a sanity chech, raises *ValueError* if a disease has a cause.

create_RX_database
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def create_RX_database(self, database_name):
        self.database = sqlite3.connect(database_name)
        self.c = self.database.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("CREATE TABLE IF NOT EXISTS drugs(serial TEXT PRIMARY KEY NOT NULL, name TEXT UNIQUE);")
        self.c.execute("DROP TABLE IF EXISTS diseases_to_symptoms_relat;")
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases_to_symptoms_relat(disease_id TEXT ,symptom_id TEXT,FOREIGN KEY(disease_id) REFERENCES diseases(serial) ON DELETE CASCADE,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE);")
        self.c.execute("DROP TABLE IF EXISTS symptoms_to_symptoms_relat;")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms_to_symptoms_relat(symptom_id TEXT ,related_symptom_id TEXT,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE,FOREIGN KEY(related_symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE);")
        self.c.execute("DROP TABLE IF EXISTS diseases_to_drugs_relat;")
        self.c.execute("CREATE TABLE IF NOT EXISTS diseases_to_drugs_relat(disease_id TEXT ,drug_id TEXT,FOREIGN KEY(disease_id) REFERENCES diseases(serial) ON DELETE CASCADE,FOREIGN KEY(drug_id) REFERENCES drugs(serial) ON DELETE CASCADE);")
        self.c.execute("DROP TABLE IF EXISTS symptoms_to_drugs_relat;")
        self.c.execute("CREATE TABLE IF NOT EXISTS symptoms_to_drugs_relat(symptom_id TEXT ,drug_id TEXT,FOREIGN KEY(symptom_id) REFERENCES symptoms(serial) ON DELETE CASCADE,FOREIGN KEY(drug_id) REFERENCES drugs(serial) ON DELETE CASCADE);")

        return 'created database\n'

Method that creates a SQL database for the class data using the ``database_name``
passed as argument and instanciate the ``self.c`` cursor wich operates over it.

The database connection is saved in ``self.database`` and is left open after
the function's operations for further computation.

insert_into_**
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def insert_into_**(self, **, **):
        self.c.execute("INSERT OR IGNORE INTO ** (**, **) VALUES(?,?);",(**, **))

Helper method that inserts an entry of the passed type in the relative table.

populate
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def populate(self):
        for ID, disease in self.id_diseases_dict.items():
            self.insert_into_diseases(ID, disease)

        for ID, symptom in self.id_symptoms_dict.items():
            self.insert_into_symptoms(ID, symptom)

        for ID, drug in self.id_drugs_dict.items():
            self.insert_into_drugs(ID, drug)

        for ID, lis_of_sym in self.dis_sym_dict.items():
            for sym in lis_of_sym:
                self.insert_into_dis_sym_relation(ID, sym)

        for ID, lis_of_sym in self.sym_sym_dict.items():
            for sym in lis_of_sym:
                self.insert_into_sym_sym_relation(ID, sym)

        for ID, lis_of_drg in self.dis_drg_dict.items():
            for drg in lis_of_drg:
                self.insert_into_dis_drug_relation(ID, drg)

        for ID, lis_of_drg in self.sym_drg_dict.items():
            for drg in lis_of_drg:
                self.insert_into_sym_drug_relation(ID, drg)

        self.database.commit()
        self.database.close()

Method that populate an already existing database with data.

It uses the ``insert_into_*`` helper methods wich uses the ``self.c`` cursor
created with the ``create_RX_database method`` that has to be active.

At the end the method commits and closes the database.

process_RXdata_to
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def process_RXdata_to(self, database_name):
        self.create_main_lists()
        self.create_main_dicts()
        self.create_drug_list()
        self.create_drug_dict()
        self.create_relation_dicts()
        self.create_RX_database(database_name)
        self.populate()

Wrapper method for processing, it packs all the calls to methods
needed for the various RX-related tasks.

Calling this method means:

- create disease, symptoms and drug lists
- create disease, symptoms and drug id dictionaryes
- create relational dictionaries between diseases, dymptoms and drugs
- create the database for the class data
- pupulate the database with the class data

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
    taboo_words = stop_words
    for el in bad_words:
        taboo_words.add(el)

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

stargate module
******************************
Module containing the ``Stargate_to_SNAP_diseases`` class and
``Stargate_to_SNAP_gene`` class wich handles the *Stargate-to-SNAP* relation connections.

Stargate_to_SNAP_diseases
-----------------
Stargate class that handles the creation of relations with the SNAP disease tables.

Creates a ``D_MeshMiner_miner_disease_instance`` in ``self.SNAP_data`` to work with,
and uses its methods to ready data for computation.

The ``disease_stargate_link`` (also available ``_with_check``) represents the main
computation: given a dictionary originated from a database, connects it to
the ``SNAP_disease`` table, going through various levels of refinement.

__init__
^^^^^^^^
.. code-block:: python

    def __init__(self):
        self.SNAP_data = D_MeshMiner_miner_disease_instance()
        self.dis_synon_dicts = self.SNAP_data.create_disease_name_synonyms_dicts()
        self.dis_desc_dicts = self.SNAP_data.create_disease_name_description_dicts()
        self.dis_name_only_dict = self.SNAP_data.create_disease_name_only_dicts()

Initializer method.
        
>>> instance = Stargate_to_SNAP_diseases()
>>> instance
<stargate.Stargate_to_SNAP_diseases at 0x7fb0fc625fd0>

Instanciates a ``D_MeshMiner_miner_disease_instance`` into ``self.SNAP_data``.
Uses the ``SNAP_data`` to save the computation dictionaries in the
respective attributes:

- dictionary with name and synonims in ``self.dis_synon_dicts``
- dictionary with name and description in ``self.dis_desc_dicts``
- dictionary with name only in ``self.dis_name_only_dict``

disease_stargate_link_with_check
^^^^^^^^
.. code-block:: python

    def disease_stargate_link_with_check(self, initial_point_dict, progress=False):
        check_dict={}
        stargate_link_to_SNAP = {}
        initial_point = initial_point_dict.items()
        destination1 = self.dis_synon_dicts
        destination2 = self.dis_desc_dicts
        destination3 = self.dis_name_only_dict
        if progress:
            count=0
            total=len(initial_point)
            perc= int(total/100)
        
        for ID, disease in initial_point:
            disease_word_list = word_tokenize(disease)
            
            score, best_list = best_match(disease_word_list, destination1)
            #in the RX-to-SNAP network case this gives overlaps for: diseases=65%, symptoms=31%
            #the results are similar for the Disgenet-to-SNAP network
                #the following results are obtained with progressive addition to the search
                #the work is done targeting the entries that didn't found a match.
                    #no match? first try this [RX-SNAP overlaps: diseases=79%(+14%), symptoms=58%(+27%)]
            if best_list == ['']:      
                stemmed_disease_list_es = []
                for word in disease_word_list:
                    stemmed_disease_list_es.append(es.stem(word))
                score, best_list = best_match(stemmed_disease_list_es, destination1, stemmed=True)
                score = str(score)+'a'
                    #and then this please [RX-SNAP overlaps: diseases=81%(+2%), symptoms=63%(+5%)]
            if best_list == ['']:      
                stemmed_disease_list_ls = []
                for word in disease_word_list:
                    stemmed_disease_list_ls.append(ls.stem(word))
                score, best_list = best_match(stemmed_disease_list_ls, destination1, stemmed=True)
                score = str(score)+'b'
                    #yet no match? what abount this!!!  [RX-SNAP overlaps: diseases=87%(+6%), symptoms=63%(+13%)]
            if best_list == ['']:
                stopped_word_list = [w for w in disease_word_list if w not in stop_words]
                score, best_list = best_match(stopped_word_list, destination2)
                score = str(score)+'c'
                    #nothing yet? what abount this one?!  [RX-SNAP overlaps: diseases=90%(+3%), symptoms=82%(+19%)]
            if best_list == ['']:      
                stopped_stemmed_disease_list_es = []
                for word in stopped_word_list:
                    stopped_stemmed_disease_list_es.append(es.stem(word))
                score, best_list = best_match(stopped_stemmed_disease_list_es, destination2, stemmed=True)
                score = str(score)+'d'
                    #And this one!!!  [RX-SNAP overlaps: diseases=91%(+1%), symptoms=85%(+3%)]
            if best_list == ['']:      
                stopped_stemmed_disease_list_ls = []
                for word in stopped_word_list:
                    stopped_stemmed_disease_list_ls.append(ls.stem(word))
                score, best_list = best_match(stopped_stemmed_disease_list_ls, destination2, stemmed=True)
                score = str(score)+'e'
                    #you refuse to match?!  [RX-SNAP overlaps: diseases=93%(+2%), symptoms=85%(+0.6%)]
            if best_list == ['']:      
                score, best_list = best_match(disease_word_list, destination3, mono=True)
                score = str(score)+'f'
                    #Let's get back the mono word ones!      [RX-SNAP overlaps: diseases=94%(+1%), symptoms=89%(+4%)]
            if best_list == ['']:
                score, best_list = best_match(stemmed_disease_list_es, destination3, stemmed=True, mono=True)
                score = str(score)+'g'
                    #I sed let's get them back!      [RX-SNAP overlaps: diseases=94%(+0.5%), symptoms=91%(+2%)]
            if best_list == ['']:
                score, best_list = best_match(stemmed_disease_list_ls, destination3, stemmed=True, mono=True)
                score = str(score)+'h'
                    #ok i give up.... no match for you
            if best_list == ['']:      
                    check_dict[disease]=([''], None,'unchecked')
                    stargate_link_to_SNAP[ID]=([''], None,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['Name'] == best]['# MESH_ID'].values[0])
                check_dict[disease]=(best_list, score,'unchecked')
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')
            if progress:
                count+=1
                if count%perc==0: sys.stdout.write('\r'+str(count)+'/'+str(total)+': '+str(int((count/total)*100))+'% at '+str(datetime.datetime.now().time()))

        return stargate_link_to_SNAP, check_dict

Method that connects a disease ``ID`` with the SNAP disease id (``MESH_ID``).
It returns a dictionary in the form:
    ``{'starting_disease_id': (['list','of','connected','SNAP_MESH_ID'], score, 'unchecked')}``

``initial_point_dict`` represents the connecting database and must be
a dictionary in the form ``{'id': 'name_string'}``.

The method uses the dictionaries of sets created by the ``SNAP_data`` instance:
for every connecting disease, first it tokenize the ``name_string``, then calls
the ``best_match`` function with the tokenized name on the destination1, wich
is the SANP's ``disease_name_synonyms_dict``.

After that, the method procedes to refine the computation via increasingly
specific iterations: it starts using the ``EnglishStemmer`` and the ``LancasterStemmer``
checking on destination1, then creates a ``stopped_word_list``, checks it on destination2,
applies the ``EnglishStemmer`` and the ``LancasterStemmer`` still checking on
destination2, then as last hope, checks on destination3 with the ``mono``
option enabled, respectively with raw names, with englishStemmed-words and
with lancasterStemmed-wors. If none of theese results in a connection,
the entry remains unconnected (it will have an empty connection list).
Either way, the entry is added to the ``stargate_link_to_SNAP`` output dictionary.

The ``score`` feature keeps track of how many connections were detected and
at wich iteration the connection was made, adding a letter at the end.

The ``'unchecked'`` tag symbolizes the automation process of connection and
allows to track for human-verified connections inside the database.

The ``_with_check`` version also returns a similar dictionary of diseases but as:
    ``{'disease_name': (['list','of','connected','disease','names'], score, 'unchecked')}``

Enableing the optional ``progress`` flag will print out the completion percentage
along with the time of rilevation, for computation tracking pourpouses.

disease_stargate_link
^^^^^^^^
.. code-block:: python

    def disease_stargate_link(self, initial_point_dict):
        stargate_link_to_SNAP = {}
        initial_point = initial_point_dict.items()
        destination1 = self.dis_synon_dicts
        destination2 = self.dis_desc_dicts
        destination3 = self.dis_name_only_dict
        
        for ID, disease in initial_point:
            disease_word_list = word_tokenize(disease)
            
            score, best_list = best_match(disease_word_list, destination1)
            #in the RX-SNAP network this gives overlaps for: diseases=65%, symptoms=31%
                #the following results are obtained with progressive addition to the search
                    #no match? first try this [RX-SNAP overlaps: diseases=79%(+14%), symptoms=58%(+27%)]
            if best_list == ['']:      
                stemmed_disease_list_es = []
                for word in disease_word_list:
                    stemmed_disease_list_es.append(es.stem(word))
                score, best_list = best_match(stemmed_disease_list_es, destination1, stemmed=True)
                score = str(score)+'a'
                    #and then this please [RX-SNAP overlaps: diseases=81%(+2%), symptoms=63%(+5%)]
            if best_list == ['']:      
                stemmed_disease_list_ls = []
                for word in disease_word_list:
                    stemmed_disease_list_ls.append(ls.stem(word))
                score, best_list = best_match(stemmed_disease_list_ls, destination1, stemmed=True)
                score = str(score)+'b'
                    #yet no match? what abount this!!!  [RX-SNAP overlaps: diseases=87%(+6%), symptoms=63%(+13%)]
            if best_list == ['']:
                stopped_word_list = [w for w in disease_word_list if w not in stop_words]
                score, best_list = best_match(stopped_word_list, destination2)
                score = str(score)+'c'
                    #nothing yet? what abount this one?!  [RX-SNAP overlaps: diseases=90%(+3%), symptoms=82%(+19%)]
            if best_list == ['']:      
                stopped_stemmed_disease_list_es = []
                for word in stopped_word_list:
                    stopped_stemmed_disease_list_es.append(es.stem(word))
                score, best_list = best_match(stopped_stemmed_disease_list_es, destination2, stemmed=True)
                score = str(score)+'d'
                    #And this one!!!  [RX-SNAP overlaps: diseases=91%(+1%), symptoms=85%(+3%)]
            if best_list == ['']:      
                stopped_stemmed_disease_list_ls = []
                for word in stopped_word_list:
                    stopped_stemmed_disease_list_ls.append(ls.stem(word))
                score, best_list = best_match(stopped_stemmed_disease_list_ls, destination2, stemmed=True)
                score = str(score)+'e'
                    #you refuse to match?!  [RX-SNAP overlaps: diseases=93%(+2%), symptoms=85%(+0.6%)]
            if best_list == ['']:      
                score, best_list = best_match(disease_word_list, destination3, mono=True)
                score = str(score)+'f'
                    #Let's get back the mono word ones!      [RX-SNAP overlaps: diseases=94%(+1%), symptoms=89%(+4%)]
            if best_list == ['']:
                score, best_list = best_match(stemmed_disease_list_es, destination3, stemmed=True, mono=True)
                score = str(score)+'g'
                    #I sed let's get them back!      [RX-SNAP overlaps: diseases=94%(+0.5%), symptoms=91%(+2%)]
            if best_list == ['']:
                score, best_list = best_match(stemmed_disease_list_ls, destination3, stemmed=True, mono=True)
                score = str(score)+'h'
                    #ok i give up.... no match for you
            if best_list == ['']:
                    stargate_link_to_SNAP[ID]=([''], None,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['Name'] == best]['# MESH_ID'].values[0])
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')

        return stargate_link_to_SNAP

Method that connects a disease ``ID`` with the SNAP disease id (``MESH_ID``).
It returns a dictionary in the form:
    ``{'starting_disease_id': (['list','of','connected','SNAP_MESH_ID'], score, 'unchecked')}``

``initial_point_dict`` represents the connecting database and must be
a dictionary in the form ``{'id': 'name_string'}``.

The method uses the dictionaries of sets created by the ``SNAP_data`` instance:
for every connecting disease, first it tokenize the ``name_string``, then calls
the ``best_match`` function with the tokenized name on the destination1, wich
is the SANP's ``disease_name_synonyms_dict``.

After that, the method procedes to refine the computation via increasingly
specific iterations: it starts using the ``EnglishStemmer`` and the ``LancasterStemmer``
checking on destination1, then creates a ``stopped_word_list``, checks it on destination2,
applies the ``EnglishStemmer`` and the ``LancasterStemmer`` still checking on
destination2, then as last hope, checks on destination3 with the ``mono``
option enabled, respectively with raw names, with englishStemmed-words and
with lancasterStemmed-wors. If none of theese results in a connection,
the entry remains unconnected (it will have an empty connection list).
Either way, the entry is added to the ``stargate_link_to_SNAP`` output dictionary.

The ``score`` feature keeps track of how many connections were detected and
at wich iteration the connection was made, adding a letter at the end.

The ``'unchecked'`` tag symbolizes the automation process of connection and
allows to track for human-verified connections inside the database.

Stargate_to_SNAP_gene
-----------------
Stargate class that handles the creation of relations with the SNAP gene tables.
Creates a ``G_SynMiner_miner_geneHUGO_instance`` in ``self.SNAP_data`` to work with,
and uses its methods to ready data for computation.

The ``gene_stargate_link`` (also available ``_with_check``) represents the main
computation: given a dictionary originated from a database, connects it to
the ``SNAP_gene`` table, going through various levels of refinement.

__init__
^^^^^^^^
.. code-block:: python

    def __init__(self):
        self.SNAP_data = G_SynMiner_miner_geneHUGO_instance()
        self.gene_sym_name_dict = self.SNAP_data.create_gene_symbol_name_dict()

Initializer method.
        
>>> instance = Stargate_to_SNAP_gene()
>>> instance
<stargate.Stargate_to_SNAP_gene at 0x7fb0fc5f5eb0>

Instanciates a ``G_SynMiner_miner_geneHUGO_instance`` into ``self.SNAP_data``.

Uses the ``SNAP_data`` to save the computation dictionaries in the
respective attributes:

- dictionary with name and symbol in ``self.gene_sym_name_dict``.

gene_stargate_link_with_check
^^^^^^^^
.. code-block:: python

    def gene_stargate_link_with_check(self, initial_point_dict, progress=False):
        check_dict={}
        stargate_link_to_SNAP = {}
        initial_point = initial_point_dict.items()
        destination1 = self.gene_sym_name_dict
        if progress:
            count=0
            total=len(initial_point)
            perc= int(total/100)
        
        for ID, (name, desc) in initial_point:
            best_list=[]
            score = 0
            for SNAP_symbol, SNAP_name in destination1.items():
                if name==SNAP_symbol:
                    score+=1
                    if desc==SNAP_name:
                        score+=4
                        best_list.append(SNAP_symbol)
                    else:
                        best_list.append(SNAP_symbol)
                        
            if best_list == []:      
                    check_dict[name]=([''], score,'unchecked')
                    stargate_link_to_SNAP[ID]=([''], score,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['symbol'] == best]['# ensembl_gene_id'].values[0])
                check_dict[name]=(best_list, score,'unchecked')
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')
            if progress:
                count+=1
                if count%perc==0: sys.stdout.write('\r'+str(count)+'/'+str(total)+': '+str(int((count/total)*100))+'% at '+str(datetime.datetime.now().time()))

        return stargate_link_to_SNAP, check_dict

Method that connects a gene ``ID`` with the SNAP gene_id (``ensembl_gene_id``).
It returns a dictionary in the form:
    ``{'starting_gene_id': (['list','of','connected','SNAP_ensembl_gene_id'], score, 'unchecked')}``

``initial_point_dict`` represents the connecting database and must be
a dictionary in the form ``{'id': ('name_string', 'desc_string')}``.

The method uses the dictionaries of sets created by the ``SNAP_data`` instance:
for every connecting gene, it checks the ``name_string`` and ``desc_string`` in
the dictionary, first matching the *name* with the ``SNAP_symbol`` string, then
matching the *decstiption* with the ``SNAP_name`` string.

Theese string are mostly name codes, much like the database ids, so they are
unique and do not need to be stemmed. If both name and symbol matches the
score gets boosted. If none of theese results in a connection,
the entry remains unconnected (it will have an empty connection list).
Either way, the entry is added to the ``stargate_link_to_SNAP`` output dictionary.

The ``score`` feature keeps track of how many connections were detected. 

The ``'unchecked'`` tag symbolizes the automation process of connection and
allows to track for human-verified connections inside the database.

The _with_check verion also returns a similar dictionary of genes but as:
    ``{'gene_name': (['list','of','connected','gene','names'], score, 'unchecked')}``

Enableing the optional ``progress`` flag will print out the completion percentage
along with the time of rilevation, for computation tracking pourpouses.

gene_stargate_link
^^^^^^^^
.. code-block:: python

    def gene_stargate_link(self, initial_point_dict):
        stargate_link_to_SNAP = {}
        initial_point = initial_point_dict.items()
        destination1 = self.gene_sym_name_dict
        
        for ID, (name, desc) in initial_point:
            best_list=[]
            score = 0
            for SNAP_symbol, SNAP_name in destination1.items():
                if name==SNAP_symbol:
                    score+=1
                    if desc==SNAP_name:
                        score+=4
                        best_list.append(SNAP_symbol)
                    else:
                        best_list.append(SNAP_symbol)
                        
            if best_list == []:      
                    stargate_link_to_SNAP[ID]=([''], score,'unchecked')
                    
            else:
                id_list_of_best = []
                for best in best_list:
                    id_list_of_best.append(self.SNAP_data.dataframe[self.SNAP_data.dataframe['symbol'] == best]['# ensembl_gene_id'].values[0])
                stargate_link_to_SNAP[ID]=(id_list_of_best, score, 'unchecked')
           
        return stargate_link_to_SNAP

Method that connects a gene ``ID`` with the SNAP gene_id (``ensembl_gene_id``).
It returns a dictionary in the form:
    ``{'starting_gene_id': (['list','of','connected','SNAP_ensembl_gene_id'], score, 'unchecked')}``

``initial_point_dict`` represents the connecting database and must be
a dictionary in the form ``{'id': ('name_string', 'desc_string')}``.

The method uses the dictionaries of sets created by the ``SNAP_data`` instance:
for every connecting gene, it checks the ``name_string`` and ``desc_string`` in
the dictionary, first matching the *name* with the ``SNAP_symbol`` string, then
matching the *decstiption* with the ``SNAP_name`` string.

Theese string are mostly name codes, much like the database ids, so they are
unique and do not need to be stemmed. If both name and symbol matches the
score gets boosted. If none of theese results in a connection,
the entry remains unconnected (it will have an empty connection list).
Either way, the entry is added to the ``stargate_link_to_SNAP`` output dictionary.

The ``score`` feature keeps track of how many connections were detected. 

The ``'unchecked'`` tag symbolizes the automation process of connection and
allows to track for human-verified connections inside the database.