D.U.S.K.E.N
===========
Dårlig Utrustet Studentsystem som Kommer til å Endre Norge.

Installation
------------
See http://edb.neuf.no/wiki/index.php/DUSKEN

`sudo apt-get install python-dev libmysqlclient-dev python-virtualenv python-pip
sudo apt-get install postgresql-server-dev-9.1  # for postgres client lib
virtualenv --distribute --no-site-packages venv  # create a project specific python environment
. venv/bin/activate  # active the environment
pip install -U distribute  # upgrade distribute
pip install -r requirements.txt  # install all requirements`

Database Diagram Generation
---------------------------
`sudo apt-get install graphviz libgraphviz-dev 
pip install pygraphviz django-extensions
python manage.py graph_models -o diagramfile.png main`


Generate Fixtures for Test
--------------------------
`python manage.py dumpdata --all -n > main/fixtures/new-testdata.json`
