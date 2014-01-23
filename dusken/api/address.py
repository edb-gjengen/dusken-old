from tastypie.resources import ModelResource
from tastypie import fields

from dusken.models import Address
from dusken.authorization import MyDjangoAuthorization
from dusken.authentication import OAuth20Authentication

class AddressResource(ModelResource):
    class Meta:
        queryset = Address.objects.all()
        resource_name = 'address'
        authorization = MyDjangoAuthorization()
        authentication = OAuth20Authentication()

    def dehydrate(self, bundle):
        bundle.data['full'] = bundle.obj.full

        return bundle
