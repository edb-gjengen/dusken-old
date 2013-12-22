#D.U.S.K.E.N

Dårlig Utrustet Studentsystem som Kommer til å Endre Norge.

[![Build Status](https://api.travis-ci.org/neuf/dusken.png)](https://travis-ci.org/neuf/dusken)

You can find the documentation at [dusken.readthedocs.org](http://dusken.readthedocs.org/).

## Installation

    sudo apt-get install python-virtualenv python-dev postgresql libpq-dev pgadmin3
    cd dusken
    virtualenv --distribute venv
    . venv/bin/activate
    pip install -r requirements.txt
    cd dusken
    cp settings-sample.py settings.py
    # Edit database settings (sqlite3 is easiest to setup, but postgresql is recommended. See discussion below.)
    cd ..
    ./manage.py syncdb --all
    ./manage.py runserver

See [the EDB wiki](http://edb.neuf.no/wiki/index.php/DUSKEN) for more info.
 
## Development tasks
    # Reset DB
    python manage.py reset_db --router=default && python manage.py syncdb --all

    # Generate Fixtures for Test
    python manage.py dumpdata dusken.<model> -n --indent=4 > dusken/fixtures/<model>.json

    # Database Diagram Generation
    sudo apt-get install graphviz libgraphviz-dev # system requirements
    pip install pygraphviz django-extensions # python requirements
    python manage.py graph_models -o diagramfile.png dusken auth

## Development references

* [Tastypie](https://django-tastypie.readthedocs.org/)

## Database

### Design references
A similar data model might allready [exist](http://www.databaseanswers.org/data_models/generic_foundation/index.htm) [out](http://www.databaseanswers.org/data_models/organisations_and_people_and_transactions/index.htm) [there](http://www.databaseanswers.org/data_models/organisations_and_people/index.htm), [somewhere](http://www.databaseanswers.org/data_models/magazine_subscriptions/index.htm).


### SQLite3 vs PostgreSQL
* SQLite runs tests much faster
* SQLite does not check foreign key constraints out of the box [[1]](http://stackoverflow.com/questions/6745763/enable-integrity-checking-with-sqlite-in-django) [FIXED].
* SQLite is easier to set up.
* SQLite does not provide environment parity between development and production [[2]](http://12factor.net/dev-prod-parity).

