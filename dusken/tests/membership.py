import logging

from dusken.models import Address, Country, Member
from support.test import ResourceTestCase
from tastypie.models import ApiKey
from utils.tests import load_test_fixtures_for_membership

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class MembershipTest(ResourceTestCase):

    membership_url = '/api/v1/membership/'
    membership_url_single = '/api/v1/membership/{}/'.format(1)

    def setUp(self):
        load_test_fixtures_for_membership()

        self.creds = self.create_apikey(
                username=Member.objects.get(user_ptr_id=2).username, 
                api_key=ApiKey.objects.get(user=Member.objects.get(user_ptr_id=2)).key)

        super(MembershipTest, self).setUp()

    def test_get_memberships(self):
        resp = self.api_client.get(
                self.membership_url, 
                format='json', 
                authentication=self.creds
        )

        self.assertValidJSONResponse(resp)

    def test_get_single_membership(self):
        resp = self.api_client.get(
                self.membership_url_single,
                format='json',
                authentication=self.creds
        )

        self.assertValidJSONResponse(resp)
