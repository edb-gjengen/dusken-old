from dusken.authentication import create_access_token
from dusken.models import Member
from dusken.utils.tests import test_fixtures_membership, do_get_request, do_post_request

from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase

class MembershipTest(ResourceTestCase):
    fixtures = test_fixtures_membership()

    #TODO Perhaps a subclass is better suited for these
    do_get_request = do_get_request
    do_post_request = do_post_request

    membership_url = '/api/v1/membership/'
    membership_url_single = '/api/v1/membership/{}/'

    def setUp(self):
        self.member = Member.objects.get(pk=2)

        self.creds = create_access_token(self.member)

        super(MembershipTest, self).setUp()

    ####################################################################
    ### Helper Functions
    def member_url(self, member_id):
        return self.membership_url_single.format(member_id)


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

        self.assertHttpCreated(resp)

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
        
        self.assertHttpAccepted(resp) # Note: Patch requests should return HTTP 202 Accepted

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
