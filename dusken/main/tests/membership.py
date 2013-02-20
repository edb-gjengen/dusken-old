import logging

from support.test import ResourceTestCase
from main.models import Membership

class MembershipTest(ResourceTestCase):
    fixtures = [ 'testdata.json' ]

    def assertValidMembershipData(self, membership):
        self.assertEquals(type(membership), dict)
        self.assertKeys(member, [ 
            u'id', 
			u'start_date',
			u'mtype',
			u'payment',
			u'member',
            u'created',
            u'updated',
            u'resource_uri' 
            ])
        self.assertNotEquals(None,member['id'])
        self.assertNotEquals(None,member['start_type'])
        self.assertNotEquals(None,member['mtype'])
        self.assertNotEquals(None,member['member'])
        self.assertNotEquals(None,member['created'])
        self.assertNotEquals(None,member['updated'])
        self.assertNotEquals(None,member['resource_uri'])

    def setUp(self):
        super(MembershipTest, self).setUp()

        # URI to get the existing member. We'll probably 
        # need it at one point or another.
        self.all_membership_url = '/api/v1/membership/'


    def test_check_request_types(self):
        """
        Tests that the endpoint responds to correct types of requests.
        """
        resp = self.api_client.get(self.all_members_url, format='json')
        self.assertNotEquals(resp.status_code, 405)

        resp = self.api_client.post(self.all_members_url)
        self.assertNotEquals(resp.status_code, 405)

        resp = self.api_client.put(self.all_members_url)
        self.assertHttpMethodNotAllowed(resp)

        resp = self.api_client.delete(self.all_members_url)
        self.assertHttpMethodNotAllowed(resp)

    def test_get_memberships(self):
        """
        Tests that we can get a premade user correctly.
        """
        resp = self.api_client.get(self.membership_url, format='json')
        self.assertValidJSONResponse(resp)

        # Check if the returned data is correct:
        member = self.deserialize(resp)
        self.assertValidMembershipData(member)


