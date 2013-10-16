#!/bin/bash

if [ -f dusken.db ]; then
    echo 'Removing existing database...'
    rm dusken.db
fi

echo 'Synchronizing database...'
python manage.py syncdb --noinput > /dev/null
echo 'Migrating database...'
python manage.py migrate > /dev/null

echo ''
echo 'Loading fixtures...'
echo '  - Auth'
python manage.py loaddata dusken/fixtures/auth.json > /dev/null
echo '  - Country'
python manage.py loaddata dusken/fixtures/country.json > /dev/null
echo '  - Address'
python manage.py loaddata dusken/fixtures/address.json > /dev/null
echo '  - Institution'
python manage.py loaddata dusken/fixtures/institution.json > /dev/null
echo '  - Group'
python manage.py loaddata dusken/fixtures/group.json

echo ''
echo 'Done.'
echo ''
