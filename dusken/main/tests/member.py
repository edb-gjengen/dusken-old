import logging

from support.test import ResourceTestCase
from main.models import Member

class MemberTest(ResourceTestCase):
    fixtures = [ 'testdata.json' ]
    standard_username = 'robert'

    def assertValidMemberData(self, member):
        self.assertEquals(type(member), dict)
        self.assertKeys(member, [ 
            u'id', 
            u'email', 
            u'username', 
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
        self.member = Member.objects.get(username=self.standard_username)

        # URI to get the existing member. We'll probably 
        # need it at one point or another.
        self.all_members_url = '/api/v1/member/'
        self.member_url = self.all_members_url + '{}/'.format(self.member.pk)

    def test_check_request_types(self):
        """
        Tests that the endpoint responds to correct types of requests.
        """
        # /api/v1/member/
        self.assertHttpOK(self.api_client.get(self.all_members_url))
        self.assertHttpCreated(self.api_client.post(self.all_members_url))
        self.assertHttpMethodNotAllowed(self.api_client.patch(self.all_members_url, data={}))
        self.assertHttpMethodNotAllowed(self.api_client.put(self.all_members_url))
        self.assertHttpMethodNotAllowed(self.api_client.delete(self.all_members_url))

        # /api/v1/member/<pk>/
        self.assertHttpOK(self.api_client.get(self.member_url))
        self.assertHttpMethodNotAllowed(self.api_client.post(self.member_url))
        self.assertHttpAccepted(self.api_client.patch(self.member_url, data={}))
        self.assertHttpMethodNotAllowed(self.api_client.put(self.member_url))
        self.assertHttpMethodNotAllowed(self.api_client.delete(self.member_url))

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
            "username" : self.member.username,
            "email" : self.member.email,
            "phone_number" : self.member.phone_number
        }

        for key, value in data.items():
            resp = self.api_client.get(self.all_members_url, format='json', data={ key : value })
            self.assertValidJSONResponse(resp)

            # Check if the returned data is correct:
            all_members = self.deserialize(resp)['objects']
            self.assertEqual(len(all_members), 1, "Wrong amount of returned members for ({},{}): {} ".format(key,value,len(all_members)))

            member = all_members[0]
            self.assertValidMemberData(member)

    def test_post_new_member(self):
        """
        Tests that we can correctly put in new users.
        """
        data = {
            'username' : 'testmemberUno',
            'password' : 'unodostres',
            'email' : 'kak-edb@studentersamfundet.no',
            'phone_number' : 90567260
        }

        resp = self.api_client.post(self.all_members_url, 
            format='json', 
            data=data)
        self.assertHttpCreated(resp)

        # Check if user was actually put into database:
        try:
            user = Member.objects.get(username=data['username'])
        except Member.DoesNotExist:
            self.fail("Inserted user does not exist.")
        self.assertNotEquals(None, user)
        self.assertEquals(user.email, data['email'])

        self.assertEquals(user.phone_number, data['phone_number'])

    def test_patch_change_member(self):
        """
        Tests that we can correctly change data of existing members.
        """
        data = {
            'password' : 'unodostres',
            'email' : 'kak-edb@studentersamfundet.no',
            'phone_number' : 90541242
        }

        resp = self.api_client.patch(self.member_url, 
            format='json', 
            data=data)
        self.assertHttpAccepted(resp)

        # Check if user was actually updated:
        user = Member.objects.get(username=self.standard_username)
        self.assertNotEquals(user.password, data['password']) # just to ensure that it's encrypted
        self.assertEquals(user.email, data['email'])
        self.assertEquals(user.phone_number, data['phone_number'])

    def test_patch_invalid_change_member(self):
        """
        Tests that we can't change fields that shouldn't be possible to be changed.
        """
        oldusername = self.member.username
        newusername = oldusername + 'lolzorz'

        data = { 'username' : newusername }
        resp = self.api_client.patch(self.member_url, format='json', data=data)
        self.assertHttpForbidden(resp)
        
        try:
            Member.objects.get(username=oldusername)
        except Member.DoesNotExist:
            self.fail("Username was changed. It is not supposed to.")

        try:
            Member.objects.get(username=newusername)
            self.fail("You will never see this message. If you do, call +7 331 24 337 for further instructions.")
        except Member.DoesNotExist:
            pass # ...the test.

