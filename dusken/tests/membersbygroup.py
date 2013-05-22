import logging

from support.test import ResourceTestCase
from dusken.models import Group, Member

class MembersByGroupTest(ResourceTestCase):
    def setUp(self):
        super(MembersByGroupTest, self).setUp()

        # URI to get all members by group relations (not functional, needs more things at the end)
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

    def test_get_all_relations(self):
        pass

    def test_get_a_relation(self):
        pass

    def test_create_relation(self):
        pass

    def test_remove_relation(self):
        pass
