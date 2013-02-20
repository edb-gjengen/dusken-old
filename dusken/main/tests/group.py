import logging

from support.test import ResourceTestCase
from main.models import Group

class GroupTest(ResourceTestCase):
	fixtures = [ 'testdata.json' ]

	def assertValidMemberData(self, member):
		self.assertEquals(type(member), dict)	
		self.assertKeys(member, [ 
			u'id',
			u'name',
			u'posix_name',
			u'created',
			u'updated',
			u'resource_uri' 
		])
		self.assertNotEquals(None,member['id'])
		self.assertNotEquals(None,member['name'])
		self.assertNotEquals(None,member['posix_name'])
		self.assertNotEquals(None,member['created'])
		self.assertNotEquals(None,member['updated'])
		self.assertNotEquals(None,member['resource_uri'])

	def setUp(self):
		super(GroupTest, self).setUp()

		# URI to get all groups
		self.groups_url = '/api/v1/group/'

	def test_request_types(self):
		"""
		Tests that the endpoint responds to correct types of requests.
		"""
		resp = self.api_client.get(self.groups_url, format='json')
		self.assertNotEquals(resp.status_code, 405)

		resp = self.api_client.post(self.groups_url)
		self.assertNotEquals(resp.status_code, 405)

		resp = self.api_client.put(self.groups_url)
		self.assertHttpMethodNotAllowed(resp)

		resp = self.api_client.delete(self.groups_url)
		self.assertHttpMethodNotAllowed(resp)

