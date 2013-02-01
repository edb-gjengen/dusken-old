D.U.S.K.E.N
===========
Dårlig Utrustet Studentsystem som Kommer til å Endre Norge.

Installation
============
* sudo apt-get install python-dev postgresql-server-dev libmysqlclient-dev python-virtualenv python-pip
* virtualenv --distribute --no-site-packages venv
* . venv/bin/activate
* pip install -r requirements.txt

Database Diagram Generation
===========================
* sudo apt-get install graphviz libgraphviz-dev 
* pip install pygraphviz django-extensions
* python manage.py graph_models -o diagramfile.png main
