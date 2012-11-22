from django.conf.urls.defaults import *
from tastypie.api import Api
from main.api import MemberResource

v1_api = Api(api_name='v1')
v1_api.register(MemberResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)
