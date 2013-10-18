import logging
from tastypie.models import ApiKey

from dusken.models import Address, Country, Member
from tastypie.test import ResourceTestCase
from utils.tests import test_fixtures_member

class MemberTestBase(ResourceTestCase):
    
    # Ref: https://docs.djangoproject.com/en/dev/topics/testing/overview/#django.test.TransactionTestCase.fixtures 
    fixtures = test_fixtures_member()

    def setUp(self):
        super(MemberTestBase, self).setUp()

        # TODO use fixtures for this
        # Get the preloaded member, which will be used for 
        # comparison with fetched object.
        self.member = Member.objects.get(pk=2)
        ## create credentials
        self.creds = self.create_apikey(username=self.member.username, api_key=ApiKey.objects.get(user=self.member).key)

        # URIs to the member api
        self.all_members_url = '/api/v1/member/'
        self.member_url = self.all_members_url + '{}/'

class MemberTest(MemberTestBase):
    def assertValidMemberData(self, member):
        self.assertEquals(type(member), dict)
        self.assertKeys(member, [ 
            u'id',
            u'address',
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

    def test_get_member_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.member_url.format(self.member.pk), format='json'))

    def test_get_member(self):
        """
        Tests that we can get a premade user correctly.
        """
        resp = self.api_client.get(self.member_url.format(self.member.pk), format='json', authentication=self.creds)
        self.assertValidJSONResponse(resp)

        # Check if the returned data is correct:
        member = self.deserialize(resp)
        self.assertValidMemberData(member)

    def test_get_all_members_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.all_members_url, format='json'))

    def test_get_all_members(self):
        """
        Tests that we can get all users from the api.
        """
        resp = self.api_client.get(self.all_members_url, format='json', authentication=self.creds)
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
            "phone_number" : self.member.phone_number
        }

        for key, value in data.items():
            resp = self.api_client.get(self.all_members_url, format='json', data={ key : value }, authentication=self.creds)
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
            'phone_number' : "+4790567260"
        }

        resp = self.api_client.post(self.all_members_url, 
            format='json', 
            data=data,
            authentication=self.creds)
        self.assertHttpCreated(resp)

        # Check if user was actually put into database:
        try:
            user = Member.objects.get(username=data['username'])
        except Member.DoesNotExist:
            self.fail("Inserted user does not exist.")
        self.assertNotEquals(None, user)
        self.assertEquals(user.email, data['email'])

        self.assertEquals(user.phone_number, data['phone_number'])

    def test_post_existing_member(self):
        """
        Tests that we can't create users with duplicate username
        """
        data = {
            'username' : self.member.username,
            'password' : 'asdf',
            'email' : self.member.email,
            'phone_number' : self.member.phone_number
        }

        resp = self.api_client.post(self.all_members_url,
            format = 'json',
            data = data,
            authentication=self.creds)
        self.assertHttpForbidden(resp)

    def test_patch_change_member(self):
        """
        Tests that we can correctly change data of existing members.
        """
        data = {
            'password' : 'unodostres',
            'email' : 'kak-edb@studentersamfundet.no',
            'phone_number' : "+4790541242"
        }

        resp = self.api_client.patch(self.member_url.format(self.member.pk), 
            format='json', 
            data=data,
            authentication=self.creds)
        self.assertHttpAccepted(resp)

        # Check if user was actually updated:
        user = Member.objects.get(username=self.member.username)
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
        resp = self.api_client.patch(self.member_url.format(self.member.pk), format='json', data=data, authentication=self.creds)
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

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class MemberAddressTest(MemberTestBase):

    def setUp(self):
        super(MemberAddressTest, self).setUp()

    def test_member_address_update_street(self):
        data = {
                "address": {
                    "street_address" : "somestreet 2",
                }
        }

        response = self.api_client.patch(
                self.member_url.format(self.member.id), 
                format='json', 
                data=data,
                authentication=self.creds)

        self.assertHttpAccepted(response)
        self.assertEquals('somestreet 2', Member.objects.get(id=self.member.id).address.street_address)

    def test_member_address_update_city(self):
        data = {
                "address": {
                    "city": "Amsterdam"
                }
        }

        response = self.api_client.patch(
                self.member_url.format(self.member.id), 
                format='json',
                data=data,
                authentication=self.creds)
        
        self.assertHttpAccepted(response)
        self.assertEquals('Amsterdam', Member.objects.get(id=self.member.id).address.city)

    def test_member_address_update_postcode(self):
        data = {
                "address": {
                    "postal_code": "0977RT"
                }
        }

        response = self.api_client.patch(
                self.member_url.format(self.member.id),
                format='json',
                data=data,
                authentication=self.creds)

        self.assertHttpAccepted(response)
        self.assertEquals('0977RT', Member.objects.get(id=self.member.id).address.postal_code)

    def test_member_address_update_country(self):
        data = {
                "address": {
                    "country": "Netherlands"
                }
        }

        response = self.api_client.patch(
                self.member_url.format(self.member.id),
                format='json',
                data=data,
                authentication=self.creds)

        self.assertHttpAccepted(response)
        self.assertEquals(
                Country.objects.get(name="Netherlands"), 
                Member.objects.get(id=self.member.id).address.country)

    def test_member_adress_update_unknown_country(self):
        data = {
                "address": {
                    "country": "unknown"
                }
        }

        response = self.api_client.patch(
                self.member_url.format(self.member.id),
                format='json',
                data=data,
                authentication=self.creds)

        self.assertHttpForbidden(response)
        self.assertEquals('The country "unknown" does not exist.', response.content)

