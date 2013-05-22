from tastypie import fields
from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization
from dusken.api.group import GroupResource
from dusken.api.member import MemberResource
from dusken.models import *


class GroupMembershipResource(ModelResource):
	"""
	This class provides following endpoints:
	(1) /api/v1/groupmembership/
	"""
	member = fields.ForeignKey(MemberResource, 'member')
	group = fields.ForeignKey(GroupResource, 'group')

	class Meta:
		queryset = GroupMembership.objects.all()
		resource_name = 'groupmembership'
		list_allowed_methods = [ 'get', 'post', 'put', 'delete' ]
		detail_allowed_methods = [ 'get', 'post', 'put', 'delete' ]
		authorization = Authorization() # TODO: for dev (VERY INSECURE)
		filtering = {
			'member' : ALL,
			'group' : ALL,
		}

	def dehydrate(self, bundle):
		bundle.data['member'] = bundle.obj.member.id
		bundle.data['group'] = bundle.obj.group.id
		return bundle

