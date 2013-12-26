from django.conf.urls import url
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL

from django.contrib.auth.models import Group
from dusken.api.membersbygroup import MembersByGroupResource

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

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<group_id>\d+)/members/$" % (self._meta.resource_name), self.wrap_view("members"), name="api_members"),
            url(r"^(?P<resource_name>%s)/(?P<group_id>\d+)/members/(?P<member_id>\d+)/$" % (self._meta.resource_name), self.wrap_view("detail_members"), name="api_detail_members"),
        ]

    def members(self, request, **kwargs):
        resource = MembersByGroupResource()
        return resource.dispatch_list(request, **kwargs)

    def detail_members(self, request, **kwargs):
        resource = MembersByGroupResource()
        return resource.dispatch_detail(request, **kwargs)
