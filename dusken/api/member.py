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

from dusken.api.groupsbymember import GroupsByMemberResource
from dusken.authentication import ServiceAuthentication, OAuth20Authentication
from dusken.authorization import MyDjangoAuthorization
from dusken.models import *
from dusken.utils.api import generate_username, random_string
from dusken.forms import MemberCreateForm

class MemberResource(ModelResource):
    """
    This class provides following endpoints:
    (1) /api/v1/member/
    (2) /api/v1/member/{id}/
    """
    class Meta:
        queryset = Member.objects.all()
        resource_name = 'member'
        list_allowed_methods = [ 'get' ]
        detail_allowed_methods = [ 'get', 'patch', 'delete' ]
        authentication = OAuth20Authentication()  # Who are you?
        authorization = MyDjangoAuthorization() # What are you allowed to do?
        excludes = [ 'date_joined', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login' ]
        filtering = {
            'first_name' : [ 'exact' ],
            'last_name' : [ 'exact' ],
            'phone_number' : [ 'exact' ],
            'email' : [ 'exact' ],
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<member_id>\d+)/groups/$" % (self._meta.resource_name), self.wrap_view("list_groups"), name="api_groups"),
            url(r"^(?P<resource_name>%s)/(?P<member_id>\d+)/groups/(?P<group_id>\d+)/$" % (self._meta.resource_name), self.wrap_view("detail_groups"), name="api_detail_groups"),
            url(r"^(?P<resource_name>%s)/register/$" % (self._meta.resource_name), self.wrap_view("register_member"), name="api_register_member"),
        ]

    def list_groups(self, request, **kwargs):
        resource = GroupsByMemberResource()
        return resource.dispatch_list(request, **kwargs)

    def detail_groups(self, request, **kwargs):
        resource = GroupsByMemberResource()
        return resource.dispatch_detail(request, **kwargs)

    def register_member(self, request, **kwargs):
        resource = MemberCreateResource()
        return resource.dispatch_list(request, **kwargs)

    def hydrate(self, bundle):
        """
        Catches PATCH requests and intercepts data.
        """

        # If the user already exists, return an error when attempting to change the username.
        if bundle.data['username'] != bundle.obj.username:
            raise ImmediateHttpResponse(HttpForbidden("You can't change your username."))

        return bundle

    def obj_update(self, bundle, **kwargs):
        if bundle.data.get('password') is not None:
            bundle.obj.set_password(bundle.data['password'])
            bundle.obj.save()

        if 'address' in bundle.data and bundle.data['address'] is not None:
            new_address = bundle.data.get('address')
            address = bundle.obj.address
            self._update_address(address, new_address)
            
        return super(MemberResource, self).obj_update(bundle, **kwargs)

    def _update_address(self, address, new_address):
        if 'street_address' in new_address:
            address.street_address = new_address['street_address']
        if 'street_address_two' in new_address:
            address.street_address_two = new_address['street_address_two']
        if 'city' in new_address:
            address.city = new_address['city']
        if 'postal_code' in new_address:
            address.postal_code = new_address['postal_code']
        if 'country' in new_address:
            try:
                country = Country.objects.get(name=new_address['country'])
            except Country.DoesNotExist, e:
                raise ImmediateHttpResponse(HttpForbidden(
                        'The country "{}" does not exist.'.format(new_address['country']))
                      )
            else:
                address.country = country

        address.save()

    def dehydrate(self, bundle):
        """
        Catches GET requests and adds more data.
        """
        # Add address:
        address = bundle.obj.address
        if address is None:
            bundle.data['address'] = None
        else:
            # TODO: There has to be a better way...
            bundle.data['address'] = {
                'city' : address.city,
                'country' : address.country.name,
                'postal_code' : address.postal_code,
                'street_address' : address.street_address,
            }

        return bundle

    def post_detail(self, request, **kwargs):
        try:
            member = MemberResource.objects.get(kwargs['pk'])
            member.is_active = True
            member.save()
            return HttpAccepted()
        except MemberResource.DoesNotExist:
            pass
        return super(MemberResource, self).post_detail(request, **kwargs)

    def patch_list(self, request, **kwargs):
        return super(MemberResource, self).patch_list(request, **kwargs)

    def patch_detail(self, request, **kwargs):
        return super(MemberResource, self).patch_detail(request, **kwargs)

    def delete_list(self, request, **kwargs):
        return super(MemberResource, self).delete_list(request, **kwargs)

    def delete_detail(self, request, **kwargs):
        member = MemberResource.objects.get(kwargs['pk'])
        member.is_active = False
        member.save()
        return HttpNoContent()

class MemberCreateResource(ModelResource):
    # TODO 
    # - get the post request to return auth info
    # - Code 400 is triggered on validation error instead of 403 in tastypie.resource.ModelResource.save(). 
    """
    This class provides the following endpoint:
     (1) /api/v1/member/register/

    The create Member resource is needed because:
     - You need a user account to authenticate to our API
     - and you need to to be authenticated to create a user account.

    Ref: http://psjinx.com/programming/2013/06/07/so-you-want-to-create-users-using-djangotastypie/
    """
    class Meta:
        list_allowed_methods = [ 'post' ]
        detail_allowed_methods = []
        default_format = "application/json"
        queryset = Member.objects.all()
        authentication = OAuth20Authentication() # anyone
        authorization = Authorization() # can do what they want with anything
        always_return_data = True
        excludes = [ 'date_joined', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login' ]
        validation = CleanedDataFormValidation(form_class=MemberCreateForm)

    def dehydrate(self, bundle):
        # Do not return fields in excludes
        # Ref: https://groups.google.com/forum/#!topic/django-tastypie/WE_d92Fkl-I/discussion
        for field in getattr(self.Meta, 'excludes', []):
            if field in bundle.data:
                del bundle.data[field]
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        # TODO factor out validation and cleaning of fields:
        # * password
        # * username
        password = bundle.data.get('password')
        if not password:
            # generate a random password if it is not provided
            bundle.data['password'] = Member.objects.make_random_password(length=32)

        if not bundle.data.get('username'):
            # Simply use the provided email
            bundle.data['username'] = bundle.data['email']

        # When creating a new user, check if it already exists:
        try:
            bundle = super(MemberCreateResource, self).obj_create(bundle, **kwargs)
            bundle.obj.set_password(password)
            bundle.obj.save()
        except IntegrityError as e:
            raise ImmediateHttpResponse(HttpForbidden("Database error: {0}".format(e)))

        return bundle
