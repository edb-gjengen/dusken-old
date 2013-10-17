import logging
import django

from dusken.models import Address, Country, Member, ApiKey
from support.test import ResourceTestCase
from utils.tests import load_test_fixtures_for_membership, test_fixtures_membership

class MembershipTest(ResourceTestCase):

    membership_url = '/api/v1/membership/'
    membership_url_single = '/api/v1/membership/{}/'

    fixtures = test_fixtures_membership()


    def setUp(self):
        #load_test_fixtures_for_membership() # FIXME use fixtures above

        self.creds = self.create_apikey(
                username=Member.objects.get(id=2).username, 
                api_key=ApiKey.objects.get(user=Member.objects.get(id=2)).key)

        super(MembershipTest, self).setUp()

    ####################################################################
    ### Helper Functions
    def member_url(self, member_id):
        return self.membership_url_single.format(member_id)

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
    ### Tests
    def test_get_memberships(self):
        resp = self.do_get_request(self.membership_url)

        self.assertValidJSONResponse(resp)
        self.assertEqual(self.expected_memberships(), self.deserialize(resp)['objects'])

    def test_get_membership(self):
        resp = self.do_get_request(self.member_url(1))

        self.assertValidJSONResponse(resp)
        self.assertEqual(self.expected_membership(), self.deserialize(resp))

    def test_get_membership_with_payment(self):
        resp = self.do_get_request(self.member_url(3))

        self.assertValidJSONResponse(resp)

    def test_post_membership(self):
        data = {
                u'member': 2,
                u'membership_type': 1,
                u'start_date': u'2013-09-11',
            }

        resp = self.do_post_request(self.membership_url, data)

        self.assertValidJSONResponse(resp)

    def test_patch_membership(self):
        data = {
                #u'member': 2,
                #u'membership_type': 1,
                u'start_date': u'2013-09-11',
            }

        resp = self.api_client.patch(self.member_url(1), 
            format='json', 
            data=data,
            authentication=self.creds)

        self.assertValidJSONResponse(resp)

    ####################################################################
    ### JSON Responses
    def expected_memberships(self):
        return [{
                u'created': u'2013-09-11T20:45:13.341000',
                u'expires': u'2013-09-11',
                u'id': 1,
                u'member': 2,
                u'membership_type': 1,
                u'payment': None,
                u'resource_uri': u'/api/v1/membership/1/',
                u'start_date': u'2013-09-11',
                u'updated': u'2013-09-11T20:45:13.341000'
            },
            {
                u'membership_type': 1, 
                u'updated': u'2013-09-11T20:45:30.084000', 
                u'created': u'2013-09-11T20:45:30.084000', 
                u'expires': u'2013-09-11', 
                u'id': 2, u'member': 2, 
                u'start_date': u'2013-09-15', 
                u'payment': None, 
                u'resource_uri': u'/api/v1/membership/2/'
            },
            {
                u'membership_type': 2, 
                u'updated': u'2013-09-11T20:45:53.522000', 
                u'created': u'2013-09-11T20:45:53.522000', 
                u'expires': u'2013-09-11', 
                u'id': 3, 
                u'member': 2, 
                u'start_date': u'2013-09-11', 
                u'payment': None, 
                u'resource_uri': u'/api/v1/membership/3/'
            }]

    def expected_membership(self):
        return {
                u'created': u'2013-09-11T20:45:13.341000',
                u'expires': u'2013-09-11',
                u'id': 1,
                u'member': 2,
                u'membership_type': 1,
                u'payment': None,
                u'resource_uri': u'/api/v1/membership/1/',
                u'start_date': u'2013-09-11',
                u'updated': u'2013-09-11T20:45:13.341000'
            }

    def expected_membership_with_payment(self):
        return {
            # TODO add membership with payment
        }
