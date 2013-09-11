import os.path
from django.core.management import call_command
import django
from dusken.models import Member
from tastypie.models import create_api_key

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_fixtures():
    ''' Returns a list with the locations of all defined fixtures. '''
    return [os.path.join('dusken', 'fixtures', 'country.json'),
            os.path.join('dusken', 'fixtures', 'address.json'),
            os.path.join('dusken', 'fixtures', 'institution.json'),
        ]

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def load_test_fixtures():
    ''' Explicitly load all defined fixtures. This can be useful when
    you only want to load the fixtures for some testcases, but not
    for all tests in a test class.'''
    for f in test_fixtures():
        call_command('loaddata', f, verbosity=0)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def test_fixtures_member():
    ''' Returns a list with the locations of all defined fixtures. '''
    return [os.path.join('dusken', 'fixtures', 'address.json'),
            os.path.join('dusken', 'fixtures', 'country.json'),
            os.path.join('dusken', 'fixtures', 'institution.json'),
           ]

def test_fixtures_membership():
    return test_fixtures() + [
            os.path.join('dusken', 'fixtures', 'users.json'),
            os.path.join('dusken', 'fixtures', 'apikey.json'),
            os.path.join('dusken', 'fixtures', 'member.json'),
            os.path.join('dusken', 'fixtures', 'membershiptype.json'),
            os.path.join('dusken', 'fixtures', 'membership.json'),
        ]
def load_test_fixtures_for_membership():
    django.db.models.signals.post_save.disconnect(create_api_key, sender=Member)
    for f in test_fixtures_membership():
        call_command('loaddata', f, verbosity=0)