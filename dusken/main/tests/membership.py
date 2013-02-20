import logging

from support.test import ResourceTestCase
from main.models import Membership

class MembershipTest(ResourceTestCase):
    fixtures = [ 'testdata.json' ]

    def assertValidMembershipData(self, membership):
        self.assertEquals(type(membership), dict)
        self.assertKeys(membership, [ 
            u'id', 
			u'start_date',
			u'expires',
			u'mtype',
			u'payment',
			u'member',
            u'created',
            u'updated',
            u'resource_uri' 
            ])
        self.assertNotEquals(None,membership['id'])
        self.assertNotEquals(None,membership['start_date'])
        self.assertNotEquals(None,membership['expires'])
        self.assertNotEquals(None,membership['mtype'])
        self.assertNotEquals(None,membership['member'])
        self.assertNotEquals(None,membership['created'])
        self.assertNotEquals(None,membership['updated'])
        self.assertNotEquals(None,membership['resource_uri'])

    def setUp(self):
        super(MembershipTest, self).setUp()

        # URI to get the existing member. We'll probably 
        # need it at one point or another.
        self.membership_url = '/api/v1/membership/'


    def test_check_request_types(self):
        """
        Tests that the endpoint responds to correct types of requests.
        """
        resp = self.api_client.get(self.membership_url, format='json')
        self.assertNotEquals(resp.status_code, 405)

        resp = self.api_client.post(self.membership_url)
        self.assertNotEquals(resp.status_code, 405)

        resp = self.api_client.put(self.membership_url)
        self.assertHttpMethodNotAllowed(resp)

        resp = self.api_client.delete(self.membership_url)
        self.assertHttpMethodNotAllowed(resp)

    def test_get_memberships(self):
        """
        Tests that we can get a premade user correctly.
        """
        resp = self.api_client.get(self.membership_url +'1/', format='json')
        self.assertValidJSONResponse(resp)

        # Check if the returned data is correct:
        membership = self.deserialize(resp)
        self.assertValidMembershipData(membership)


