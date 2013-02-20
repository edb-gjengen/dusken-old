import logging

from support.test import ResourceTestCase
from main.models import GroupMembership

class GroupMembershipTest(ResourceTestCase):
	fixtures = [ 'testdata.json' ]

	def assertValidGroupgroupmembershipshipData(self, groupmembership):
		self.assertEquals(type(groupmembership), dict)	
		self.assertKeys(groupmembership, [ 
			u'id',
			u'groupmembership',
			u'group',
			u'created',
			u'updated',
			u'resource_uri' 
		])
		self.assertNotEquals(None,groupmembership['id'])
		self.assertNotEquals(None,groupmembership['groupmembership'])
		self.assertNotEquals(None,groupmembership['group'])
		self.assertNotEquals(None,groupmembership['created'])
		self.assertNotEquals(None,groupmembership['updated'])
		self.assertNotEquals(None,groupmembership['resource_uri'])

	def setUp(self):
		super(GroupMembershipTest, self).setUp()

		# URI to get all groups
		self.groupmembership_url = '/api/v1/groupmembership/'

	def test_request_types(self):
		"""
		Tests that the endpoint responds to correct types of requests.
		"""
		resp = self.api_client.get(self.groupmembership_url, format='json')
		self.assertNotEquals(resp.status_code, 405)

		resp = self.api_client.post(self.groupmembership_url)
		self.assertNotEquals(resp.status_code, 405)

		resp = self.api_client.put(self.groupmembership_url)
		self.assertNotEquals(resp.status_code, 405)

		resp = self.api_client.delete(self.groupmembership_url)
		self.assertNotEquals(resp.status_code, 405)

