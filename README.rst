###################################################
Stargate: a database linking / network creator.
###################################################

.. contents:: Quick access links
	:local:
	:depth: 1

***********
Description
***********
Stargate is a project wich aims to link diverse databases of the same topic, in this case medical databases, without altering their database structure. In this way it is possible to have network tables linking precedently unlinked databases, maintaining already existing tables and structure, hence without loosing any of the already estabilished data process.

The job is done by creating network tables that relationate unique ids, around wich the single databases are structured. This allows users to query in multiple databases levereging the network tables, hence accessing external-no-more databases, linking the structure they are used to, with new data via the stargate-created network tables.

The relations between ids are obtained with a Natural Language Processing (NLP) algorithm inspecting the data. Chosen an initial and a final databases, the algorithm uses a characteristic column from the initial databases wich contains valuable information, to search in the final database for the best match for every entry, then gets their ids and matches them.

***********
Python version(s)
***********
Project developed in python 3.9.5

Project tested in python 3.9.5

***********
Documentation links
***********
`Tutorial <https://github.com/LeonardoBarontini/NLP-examProject/blob/main/Tutorial.rst>`_

`Explanation <https://github.com/LeonardoBarontini/NLP-examProject/blob/main/Explanation.rst>`_

`Reference <https://github.com/LeonardoBarontini/NLP-examProject/blob/main/Reference.rst>`_
