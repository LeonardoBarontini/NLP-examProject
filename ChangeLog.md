--- unlimited powerrr ---
enhanced stargate matching function, now with 91%+ coverage
upgraded main module, now with more processing and better process monitoring
added G_SynMiner_miner_geneHUGO_instance class for future gene-linking

--- time to travel between databases ---
new functions for data handling given to Disgenet_instance and D_MeshMiner_miner_disease_instance 
the D_MeshMiner_miner_disease_instance class now auto loads the corresponding .tsv table
format_string function is now boostable
added module nlp wich contains scoring functions for match analysis and a list of "taboo_words"
added module stargate wich contains the Stargate_to_* classes
added Stargate_to_SNAP class wich handles the linking process to the SNAP database
expanded main file to handle the operations


--- pre-link adjustments ---
fixed a bug in RX_instance.create_main_lists wich led to 5 double records in disease list and prehemptively fixed even for symptoms

--- disgenet class and snap first class ---
added Disgenet_instance class wich reads from the disgenet database
given load and unload methods to disgenet class for mamory management
added D_MeshMiner_miner_disease_instance class wich reads from the corrispondent snap tsv table file
given prototype function for databases linking to D_MeshMiner_miner_disease_instance class

--- here comes the pandas ---
little code cleaning and modularity improvements to RX class
@deprecated the management moved functions and others no more usefull (and the corresponding tests)
moved some RX-exclusive functions from management file to the RX class
RX-database class revamped now with pandas

--- testing and fixing ---
some code analysis and cleaning
added test_get_id_of_string_*_()       
various docstrings power up
added test_format_string_*_()
fixed substring_in_elements raising AttributeError if an element of the input list was not a string Type; now raises TypeError
fixed substring_in_elements returning the input list if an ampty string is given as substring to find
added test_substring_in_elements_*_()
now add_unique_drug_id() raises ValueError if input list is longer than the default value
now the numbering of the ids in add_unique_drug_id() has a default input value: digits = 6
added test_add_unique_drug_id_*_()
now add_unique_symptom_id() raises ValueError if input list is longer than the default value
now the numbering of the ids in add_unique_symptom_id() has a default input value: digits = 6
added test_add_unique_symptom_id_*_()
now add_unique_disease_id() raises ValueError if input list is longer than the default value
now the numbering of the ids in add_unique_disease_id() has a default input value: digits = 6
added test_add_unique_disease_id_*_()
renamed class Instanciator to RX_instance
renamed sqlite_database_populator.py  to  RX_database_class.py
added manualTest_input_type()


--- added test and changelog ---
added test_is_disease_*_()
created ChangeLog.md
created test.py


--- pre alpha-1 ---
start of the project
