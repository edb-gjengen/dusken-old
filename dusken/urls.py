from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from dusken.api.member import MemberResource
from dusken.api.membership import MembershipResource
from dusken.api.group import GroupResource
from dusken.api.groupsbymember import GroupsByMemberResource
from dusken.api.membersbygroup import MembersByGroupResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(MemberResource())
v1_api.register(MembershipResource())
v1_api.register(GroupResource())
v1_api.register(GroupsByMemberResource())
v1_api.register(MembersByGroupResource())

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
