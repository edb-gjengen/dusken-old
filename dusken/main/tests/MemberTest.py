import logging

from support.test import ResourceTestCase
from main.models import Member

class MemberTest(ResourceTestCase):
    fixtures = [ 'testdata.json' ]

    def assertValidMemberData(self, member):
        self.assertEquals(type(member), dict)
        self.assertKeys(member, [ 
            u'id', 
            u'email', 
            u'username', 
            u'password',
            u'phone_number', 
            u'first_name', 
            u'last_name',
            u'date_of_birth',
            u'legacy_id',
            u'created',
            u'updated',
            u'resource_uri' 
            ])
        self.assertNotEquals(None,member['id'])
        self.assertNotEquals(None,member['email'])
        self.assertNotEquals(None,member['created'])
        self.assertNotEquals(None,member['updated'])
        self.assertNotEquals(None,member['resource_uri'])

    def setUp(self):
        super(MemberTest, self).setUp()

        # Get the preloaded member, which will be used for 
        # comparison with fetched object.
        self.member = Member.objects.get(username='robertko')

        # URI to get the existing member. We'll probably 
        # need it at one point or another.
        self.all_members_url = '/api/v1/member/'
        self.member_url = self.all_members_url + '{}/'.format(self.member.pk)

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


    def test_get_member(self):
        """
        Tests that we can get a premade user correctly.
        """
        resp = self.api_client.get(self.member_url, format='json')
        self.assertValidJSONResponse(resp)

        # Check if the returned data is correct:
        member = self.deserialize(resp)
        self.assertValidMemberData(member)

    def test_get_all_members(self):
        """
        Tests that we can get all users from the api.
        """
        resp = self.api_client.get(self.all_members_url, format='json')
        self.assertValidJSONResponse(resp)

        # Check if the returned data is correct:
        all_members = self.deserialize(resp)['objects']
        self.assertEqual(len(all_members), 2)

        for index in range(len(all_members)):
            self.assertValidMemberData(all_members[index])

    def test_get_filtered_members(self):
        """
        Tests that we can get a filtered list from the api.
        """
        data = { 
            "username" : "robertko"
        }

        resp = self.api_client.get(self.all_members_url, format='json', data=data)
        self.assertValidJSONResponse(resp)

        # Check if the returned data is correct:
        all_members = self.deserialize(resp)['objects']
        self.assertEqual(len(all_members), 1)

        member = all_members[0]
        self.assertValidMemberData(member)

