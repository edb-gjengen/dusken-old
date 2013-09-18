import logging
import utils.tests

from dusken.models import Group
from support.test import ResourceTestCase

class GroupTest(ResourceTestCase):

	def setUp(self):
		super(GroupTest, self).setUp()

		# URI to get all groups
		self.groups_url = '/api/v1/group/'

	def test_put_not_allowed(self):
		resp = self.api_client.put(self.groups_url)
		self.assertHttpMethodNotAllowed(resp)

	def test_delete_not_allowed(self):
		resp = self.api_client.delete(self.groups_url)
		self.assertHttpMethodNotAllowed(resp)
		