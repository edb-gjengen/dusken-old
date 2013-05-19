import logging

from support.test import ResourceTestCase
from dusken.models import Group, Member

class MembersByGroupTest(ResourceTestCase):
	def setUp(self):
		super(MembersByGroupTest, self).setUp()

		# URI to get all groups
		self.url = '/api/v1/membersbygroup/'

	def test_request_types(self):
		"""
		Tests that the endpoint responds to correct types of requests.
		"""
		resp = self.api_client.get(self.url, format='json')
		self.assertHttpMethodNotAllowed(resp)

		resp = self.api_client.post(self.url)
		self.assertNotEquals(resp.status_code, 405)

		resp = self.api_client.put(self.url)
		self.assertHttpMethodNotAllowed(resp)

		resp = self.api_client.delete(self.url)
		self.assertHttpMethodNotAllowed(resp)

