from tastypie.resources import ModelResource
from tastypie import fields

from dusken.models import Division
from dusken.authorization import MyDjangoAuthorization
from dusken.authentication import OAuth20Authentication

class DivisionResource(ModelResource):
    class Meta:
        queryset = Division.objects.all()
        resource_name = 'division'
        authorization = MyDjangoAuthorization()
        authentication = OAuth20Authentication()
