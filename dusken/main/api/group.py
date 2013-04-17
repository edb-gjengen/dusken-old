from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL
from main.models import Group


class GroupResource(ModelResource):
	"""
	This class provides following endpoints:
	(1) /api/v1/group/
	(2) /api/v1/group/{id}/
	"""
	class Meta:
		queryset = Group.objects.all()
		resource_name = 'group'
		list_allowed_methods = [ 'get', 'post' ]
		detail_allowed_methods = [ 'get', 'post' ]
		authorization = Authorization() # TODO: for dev (VERY INSECURE)
		filtering = {
		}

