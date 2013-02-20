from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization
from main.models import *


class MembershipResource(ModelResource):
    """
    This class provides following endpoints:
    (1) /api/v1/membership/
    """
    class Meta:
        queryset = Membership.objects.all()
        resource_name = 'membership'
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'post' ]
        authorization = Authorization() # TODO: for dev (VERY INSECURE)

