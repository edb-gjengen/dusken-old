import logging

from support.test import ResourceTestCase
from dusken.models import Group, Member

class MembersByGroupTest(ResourceTestCase):
    def setUp(self):
        super(MembersByGroupTest, self).setUp()

        self.member = Member(username='robert', email='robert.kolner@gmail.com', phone_number=90567268)
        self.member.save()

        self.group = Group(name="EDB", posix_name="edb")
        self.group.save()
        self.group.user_set.add(self.member)
        self.group.save()

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
        url = self.url + str(self.group.pk) + "/"
        resp = self.api_client.get(url, format="json")
        self.assertValidJSONResponse(resp)
        data = self.deserialize(resp)
        self.assertEquals(len(data['members']), self.group.user_set.count())
        self.assertEquals(data['members'][0], self.member.pk)

    def test_get_a_relation(self):
        url = self.url + str(self.group.pk) +"/" +str(self.member.pk) +"/"
        resp = self.api_client.get(url, format='json')
        self.assertValidJSONResponse(resp)

    def test_create_relation(self):
        pass

    def test_remove_relation(self):
        pass
