from django.conf.urls.defaults import *
from tastypie.api import Api
from main.api.member import MemberResource
from main.api.membership import MembershipResource
from main.api.group import GroupResource
from main.api.groupsbymember import GroupsByMemberResource

v1_api = Api(api_name='v1')
v1_api.register(MemberResource())
v1_api.register(MembershipResource())
v1_api.register(GroupResource())
v1_api.register(GroupsByMemberResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)
