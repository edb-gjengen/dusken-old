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
        self.url = '/api/v1/group/{member_id}/member/'.format(member_id=self.group.id)

    def test_get_all_relations(self):
        url = self.url + str(self.member.id) + "/"
        resp = self.api_client.get(url, format="json")
        self.assertValidJSONResponse(resp)
        data = self.deserialize(resp)

        groupmembers = data['objects']

        self.assertEquals(len(groupmembers), self.group.user_set.count())
        self.assertEquals(int(groupmembers[0]['member_id']), self.member.pk)

    def test_get_a_relation(self):
        url = self.url + str(self.group.pk) +"/"
        resp = self.api_client.get(url, format='json')
        self.assertValidJSONResponse(resp)

    def test_create_relation(self):
        group = Group(name="Design", posix_name="design")

        data = {
            'member_id': self.member.pk,
            'group_id': group.pk
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertNotEquals(self.member.groups.filter(name=group.name).count(), 0)

    def test_remove_relation(self):
        data = {
            'member_id': self.member.pk,
            'group_id': self.group.pk
        }
        resp = self.api_client.delete(self.url, format='json', data=data)
        self.assertHttpAccepted(resp)
        self.assertEquals(self.member.groups.filter(name=group.name).count(), 0)
        
        resp = self.api_client.delete(self.url, format='json', data=data)
        self.assertHttpGone(resp)

