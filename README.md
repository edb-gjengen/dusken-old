D.U.S.K.E.N
===========
Dårlig Utrustet Studentsystem som Kommer til å Endre Norge.

You can find the documentation at [http://dusken.readthedocs.org/]().


[![Build Status](https://api.travis-ci.org/neuf/dusken.png)](https://travis-ci.org/neuf/dusken)


Installation
------------
See http://edb.neuf.no/wiki/index.php/DUSKEN for installation

**TODO installation:**

Download latest version of Vagrant from [http://downloads.vagrantup.com/]() and then do:

    vagrant plugin install vagrant-salt
    vagrant up
    vagrant ssh


Database Diagram Generation
---------------------------
    sudo apt-get install graphviz libgraphviz-dev 
    pip install pygraphviz django-extensions
    python manage.py graph_models -o diagramfile.png main


Generate Fixtures for Test
--------------------------
`python manage.py dumpdata --all -n > main/fixtures/new-testdata.json`


Design References
-----------------

* Database model: [http://www.databaseanswers.org/data_models/generic_foundation/index.htm]()
* Database model: [http://www.databaseanswers.org/data_models/organisations_and_people_and_transactions/index.htm]()
* Database model: [http://www.databaseanswers.org/data_models/organisations_and_people/index.htm]()

Developer References
--------------------
* Tastypie: [https://django-tastypie.readthedocs.org/en/latest/]()

