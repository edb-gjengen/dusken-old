from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization
from main.models import *


class MemberResource(ModelResource):
	"""
	This class provides following endpoints:
	(1) /api/v1/member/
	(2) /api/v1/member/{id}/
	"""
	class Meta:
		queryset = Member.objects.all()
		resource_name = 'member'
		list_allowed_methods = [ 'get', 'post' ]
		detail_allowed_methods = [ 'get', 'post' ]
		authorization = Authorization() # TODO: for dev (VERY INSECURE)
		filtering = {
			'username' : ALL
		}

