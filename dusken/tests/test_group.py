from tastypie.test import ResourceTestCase

from dusken.authentication import create_access_token
from dusken.models import Member
from dusken.utils.tests import test_fixtures_group, do_get_request, do_post_request


class GroupTest(ResourceTestCase):
    fixtures = test_fixtures_group()

    #TODO Perhaps a subclass is better suited for these
    do_get_request = do_get_request
    do_post_request = do_post_request

    def setUp(self):
        self.member = Member.objects.get(pk=2)

        # Put OAuth2 Authorization in HTTP header
        self.creds = create_access_token(self.member)

        super(GroupTest, self).setUp()

        # URI to get all groups
        self.groups_url = '/api/v1/group/'

    def test_put_not_allowed(self):
        resp = self.api_client.put(self.groups_url)
        self.assertHttpMethodNotAllowed(resp)

    def test_delete_not_allowed(self):
        resp = self.api_client.delete(self.groups_url)
        self.assertHttpMethodNotAllowed(resp)

    def test_get_group(self):
        resp = self.do_get_request(self.groups_url + '1')
        #TODO Implement this :)
