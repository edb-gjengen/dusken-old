import logging

from support.test import ResourceTestCase
from main.models import Member

class MemberTest(ResourceTestCase):
	fixtures = [ 'members.json' ]

	def setUp(self):
		super(MemberTest, self).setUp()

		# Get the preloaded member, which will be used for 
		# comparison with fetched object.
		self.member = Member.objects.get(username='robertko')

		# URI to get the existing member. We'll probably 
		# need it at one point or another.
		self.member_url = '/api/v1/member/{0}/'.format(self.member.pk)

	def test_get_member(self):
		"""
		Tests that we can get a premade user correctly.
		"""
		resp = self.api_client.get(self.member_url, format='json')
		self.assertValidJSONResponse(resp)

		# Check if the returned data is correct:
		member = self.deserialize(resp)
		
		self.assertKeys(member, [ u'member_id', u'email', u'username', u'phonenumber', u'givenname', u'dateofbirth', u'surname', u'resource_uri' ])
		self.assertEqual(member['username'], 'robertko')
		self.assertEqual(member['email'], 'robert.kolner@studentersamfundet.no')

