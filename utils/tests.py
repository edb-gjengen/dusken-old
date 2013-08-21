import os.path
from django.core.management import call_command

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_fixtures():
    ''' Returns a list with the locations of all defined fixtures. '''
    return [os.path.join('dusken', 'fixtures', 'address.json'),
            os.path.join('dusken', 'fixtures', 'country.json'),
            os.path.join('dusken', 'fixtures', 'institution.json'),
           ]

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def load_test_fixtures():
    ''' Explicitly load all defined fixtures. This can be useful when
    you only want to load the fixtures for some testcases, but not
    for all tests in a test class.'''
    for f in test_fixtures():
        call_command('loaddata', f, verbosity=0)
