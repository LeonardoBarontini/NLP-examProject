--- Documentation and tests 3 ---
improved comunicability of Tutorial
improved comunicability of Explanation
improved name comunicability of some functions
improved boosted format_string function: now actually removes punctuation (also 'and', 'with', 'without', and single digit numbers)
added more tests for format_string function
corrected stop_words / taboo_words distinction
added reference and docstrings for format_string function
added reference and docstrings for add_unique_disease_id function
added reference and docstrings for add_unique_symptom_id function
added reference and docstrings for add_unique_drug_id function
added reference and docstrings for get_id_of_string function
added tests for add_relation_to_dict function
added reference and docstrings for add_relation_to_dict function
added reference and docstrings for start_timer_at function
added reference and docstrings for stop_timer_at function
added reference and docstrings for check_overlap_percentage function
added reference and docstrings for check_unlinked function
added tests for check_overlap_percentage function
added tests for check_unlinked function
added reference and docstrings for count_elements function
added reference and docstrings for frequency_dictionary function
added tests for count_elements function
added tests for frequency_dictionary function
improved docstrings and reference for Disgenet_instance class and relative methods
added tests for start_timer_at function
added tests for stop_timer_at function
added tests for create_tsv_table_file function
added reference and docstrings for create_tsv_table_file function
added tests for create_stargate_network_table function
added reference and docstrings for create_stargate_network_table function
added docstring for snap_database_classes module
added reference and docstrings for D_MeshMiner_miner_disease_instance class and relative methods
added tests for D_MeshMiner_miner_disease_instance class and relative methods
added reference and docstrings for G_SynMiner_miner_geneHUGO_instance class and relative methods
added tests for G_SynMiner_miner_geneHUGO_instance class and relative methods
added reference and docstrings for RX_instance class and relative methods
added tests for RX_instance class and relative methods
added reference and docstrings for Stargate_to_SNAP_diseases class and relative methods
added tests for Stargate_to_SNAP_diseases class and relative methods
added reference and docstrings for Stargate_to_SNAP_gene class and relative methods
added tests for Stargate_to_SNAP_gene class and relative methods

--- Documentation and tests 2 ---
slightly improved link quality in disease links, introducing word stopping
added tutorial for base use of the project
completed first version of project explanation
added docstrings for Disgenet_instance class and relative methods
added reference for Disgenet_instance class and relative methods
added tests for Disgenet_instance class and relative methods

--- Documentation and tests 1 ---
added docstring and tests for words_in_set
added docstring and tests for matched_entries
added docstring and tests for best_match
added NLP functions Explanation and Reference

--- Stargate big database ---
updated disease_stargate_link to match disease_stargate_link_with_check
D_MeshMiner_miner_disease_instance class now has a create_SNAP_disease_table function
added create_stargate_network_table calls to main module to populate Stargate_big_database.db
completed G_SynMiner_miner_geneHUGO_instance also with create_SNAP_gene_table
created Stargate_to_SNAP_gene class
now every function that creates a relational table, first drops it to prevent data doubling (or more)
added create_gene_dict function to Disgenet_instance class
updated main module to process Disgenet-SNAP gene linking

--- adding score and verification to network table ---
now best_match returns the score with the best list in tuple form
stargate methods modified to handle new best_match output
> now stargate outputs a dictionary in the form {'initial id': ([list of best ids], score, 'unchecked')}
> reordered search steps to match score "weighting"
> added score differentiation between different matching criteria
main module modified to manage new outputs   
some main module processes have been moved to managment_functions module and became:
> start_timer_at, stop_timer_at, check_overlap_percentage
> check_unlinked, create_tsv_table_file
added create_stargate_network_table for next patch
added process wrapping method to RX_database_class

--- documentation try # ---
added .tsv output file in main module for every network table created
readme file now has something on it
created explanation, tutorial, reference, and how-to documentation files

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
