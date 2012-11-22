from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from main.models import *


class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.all()
        resource_name = 'member'
        authorization= Authorization() # for dev (VERY INSECURE)
