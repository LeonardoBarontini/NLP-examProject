.. _tutorial:

=========
Tutorial
=========

Stargate  "pre biult" for its designed use case, `having the database files`, you just have to git clone, cd to the project directory, `where you'll also put your databases`, check for filenames correspondence and run the main.py file.

Let us first explore what to expect from the program execution.

main.py execution
=================

Let's do this step by step:

after hitting run, you'll see the program notifies you with what is going on printing on your terminal::

      		#########   Processing SNAP data   #########

	10:17:08.848666
	finished processing in 31.42429208755493 seconds

this block refers to the first instruction of the main file where the program loads the ``D-MeshMiner_miner-disease.tsv`` data with the ``Stargate_to_SNAP_diseases`` class in the ``stargateD`` instance, and the ``G-SynMiner_miner-geneHUGO.tsv`` data with the ``Stargate_to_SNAP_gene`` class in the ``stargateG`` instance.

.. code-block:: python

	print(
	      """
	      #########   Processing SNAP data   #########
	      """
	      )
	start = start_timer_at(time())

	stargateD = Stargate_to_SNAP_diseases()
	stargateD.SNAP_data.create_SNAP_disease_table('Stargate_big_database.db')

	stargateG = Stargate_to_SNAP_gene()
	stargateG.SNAP_data.create_SNAP_gene_table('Stargate_big_database.db')

	end = stop_timer_at(time(),start)


Then the first database to link will begin to load, as you can see you'll be notified with the starting time of the computation and the time elapsed when it finishes::

	      #########   Processing RX data   #########
      
	---> start loading RX-data
	10:17:40.273026
	finished processing in 2.6576101779937744 seconds

This corresponds to the lines

.. code-block:: python

	print(
	      """
	      #########   Processing RX data   #########
	      """
	      )
	print("""\n---> start loading RX-data""")
	start = start_timer_at(time())

	RXdata = RX_instance('RXlist_data.json')
	RXdata.process('Stargate_big_database.db')

	end = stop_timer_at(time(),start)

When database loading is done, the linking procedure will begin::

	---> starting RX-SNAP disease overlapping
	10:17:42.930860

Wich corresponds to the instructions

.. code-block:: python

	print("""\n---> starting RX-SNAP disease overlapping""")
	start = start_timer_at(time())

	RX_to_SNAP_disease_links, check_dict = stargateD.disease_stargate_link_with_check(RXdata.id_diseases_dict, progress=True)

When finished you'll be notified with the elapsed time and the overlapping percentage::

	finished processing in 34.64814519882202 seconds
	overlap between RXdata and SNAPdata diseases : 94%
	94.98480243161094

As you can see in the code, the program also creates a list and a .tsv file of unlinked entries, in case they are needed.

.. code-block:: python

	end = stop_timer_at(time(),start)
	check_overlap_percentage(RXdata.id_diseases_dict, 'RXdata', RX_to_SNAP_disease_links, 'SNAPdata diseases', precise=True)
	unlinked_list1 = check_unlinked(check_dict)
	create_tsv_table_file('RXdis-links.tsv', check_dict)

The program then goes on processing and repeats these same operations for every step of the computation.

This is a brief explanation of what happens when you run the main file and everything is set up correctly, so this is what you will expect from the program execution. 

Now we have to check if we have what it takes to properly run the program as it was designed to.


Filenames
=========

Now let's say you have the database files but they have different names or are scattered accross your system.

First of all you will have to move or copy them into the directory where the project is saved. 

Then let's check that the program is loading your ``SNAP`` files and not the default ones. 

Open the ``snap_database_classes.py`` file and check, for every snap file you have, in the corresponding class ``__init__`` method for the ``self.dataframe`` variable. 

This variable contains the filename string of the file to load, wich by default is ``'D-MeshMiner_miner-disease.tsv'`` for the disease table and ``'G-SynMiner_miner-geneHUGO.tsv'`` for the gene table. 

.. code-block:: python

	def __init__(self):
	    self.dataframe = pandas.read_table('D-MeshMiner_miner-disease.tsv')

.. code-block:: python

    def __init__(self):
    	self.dataframe = pandas.read_table('G-SynMiner_miner-geneHUGO.tsv')

Of course it must equals the filename you want to load so, if this is not the case, you will either change the string in the code, or change the name of the file so that it matches the string.

For RXlist and disgenet the name of the corresponding file is passed as argument at initializzation time so you'll check the main.py where the initializzation is done.

.. code-block:: python

	RXdata = RX_instance('RXlist_data.json')

	DisgenetData = Disgenet_instance('disgenet_2020.db')

Databases 
==========

SNAP
****
The expected SNAP tables are: ``'D-MeshMiner_miner-disease.tsv'`` and ``'G-SynMiner_miner-geneHUGO.tsv'``.
These are ``.tsv`` files that ``pandas`` handles easly using ``pandas.read_table('table_name')``.

In the disease table, the ``'# MESH_ID'``, ``'Name'``, ``'Definitions'`` and ``'Synonyms'`` columns are used, wich are all the columns in the table.

In the gene table, the ``'symbol'`` and ``'name'`` columns are used, but the table consists of 48 columns wich are needed if you want to integrate the table in your 'big_database'.

RXlist
******
RXlist is a ``.json`` file from wich the RX-database is constructed.

It is structured as a python dictionary: its primary key consists of symptoms and diseases, the last of wich are identified by a ``disease_recognition_string``; these keys have a dictionary as item, wich has three keys: ``'Related'``, ``'Causes'`` and ``'Drugs'``, every one of them with a list as item, for the first one we have a list of symptoms, for the second of diseases and for the third of drugs.

disgenet
********
Disgenet comes as a database already biult. Stargate uses the ``diseaseAttributes`` and ``geneAttributes`` tables.

In the ``diseaseAttributes`` table, the ``'diseaseNID'`` and ``'diseaseName'`` columns are used.

In the ``geneAttributes`` table, the ``'geneNID'``, ``'geneName'`` and ``'geneDescription'`` columns are used.

Going beyond
============

Now let's say you want to add another database the the stargate network...

Well, unless that database has the same structure of one of the already used databases, you will have to biuld your own class to handle that database....

Otherwise, let's say you have a disgenet-like database, you can just copy the corresponding part of the main.py module and paste it at the end of the module, then change all the name strings needed and you're done. Beware tho that beeing database-like means, not only having the same form or the same number of tables, but also the same table and column names, written in the same exact way or you'll have to modify the program if you don't want it to brake. 








