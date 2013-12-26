from django.conf.urls import url
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse, BadRequest
from tastypie.http import HttpForbidden, HttpNoContent, HttpResponse, HttpAccepted
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from tastypie.validation import CleanedDataFormValidation

from dusken.authentication import ServiceAuthentication, OAuth20Authentication
from dusken.authorization import MyDjangoAuthorization
from dusken.models import *
from dusken.utils.api import generate_username, random_string
from dusken.forms import MemberCreateForm

from dusken.api.division import DivisionResource
from dusken.api.membership import MembershipResource
from dusken.api.address import AddressResource
from dusken.api.groupsbymember import GroupsByMemberResource

class MeResource(ModelResource):
    """
    This class provides following endpoints:
    (1) /api/v1/me/
    """
    groups = fields.ToManyField(GroupsByMemberResource, 'groups')
    divisions = fields.ToManyField(DivisionResource, 'division_set')
    memberships = fields.ToManyField(MembershipResource, 'membership_set')
    #address = fields.ForeignKey(AddressResource, 'address')

    class Meta:
        queryset = Member.objects.all()
        resource_name = 'me'
        list_allowed_methods = [ 'get' ]
        detail_allowed_methods = [ 'get']
        authentication = OAuth20Authentication()  # Who are you?
        authorization = MyDjangoAuthorization() # What are you allowed to do?
        excludes = [ 'date_joined', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login' ]

    def get_object_list(self, request):
        # Only return the authenticated user's member object
        return super(MeResource, self).get_object_list(request).filter(pk=request.user.id)

    def detail_groups(self, request, **kwargs):
        resource = GroupsByMemberResource()
        return resource.dispatch_detail(request, **kwargs)

    def dehydrate(self, bundle):
        """
        Catches GET requests and adds more data.
        """
        bundle.data['has_valid_membership'] = bundle.obj.has_valid_membership()
        # Add address:
        #address = bundle.obj.address
        #if address is None:
        #    bundle.data['address'] = None
        #else:
        #    # TODO: There has to be a better way...
        #    bundle.data['address'] = {
        #        'city' : address.city,
        #        'country' : address.country.name,
        #        'postal_code' : address.postal_code,
        #        'street_address' : address.street_address,
        #    }

        return bundle
