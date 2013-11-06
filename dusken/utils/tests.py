import os.path
from django.core.management import call_command
import django
from dusken.models import *

####################################################################
### Request helper functions
def do_get_request(self, url):
    return self.api_client.get(
            url, 
            format='json', 
            authentication=self.creds
    )

def do_post_request(self, url, data):
    return self.api_client.post(
            url,
            format='json',
            data=data,
            authentication=self.creds
    )

####################################################################
### Fixture helper functions
def test_fixtures():
    ''' Returns a list with the locations of all defined fixtures. '''
    return [os.path.join('dusken', 'fixtures', 'country.json'),
            os.path.join('dusken', 'fixtures', 'address.json'),
            os.path.join('dusken', 'fixtures', 'institution.json'),
        ]

def test_fixtures_member():
    ''' Returns a list with the locations of all defined fixtures. '''
    return [os.path.join('dusken', 'fixtures', 'member.json'),
            os.path.join('dusken', 'fixtures', 'country.json'),
            os.path.join('dusken', 'fixtures', 'address.json'),
            os.path.join('dusken', 'fixtures', 'institution.json'),
           ]

def test_fixtures_membership():
    return test_fixtures() + [
            os.path.join('dusken', 'fixtures', 'member.json'),
            os.path.join('dusken', 'fixtures', 'membershiptype.json'),
            os.path.join('dusken', 'fixtures', 'membership.json'),
        ]

def test_fixtures_group():
    return test_fixtures_member() + [
        os.path.join('dusken', 'fixtures', 'group.json'),
    ]