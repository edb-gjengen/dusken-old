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

from dusken.api.groupsbymember import GroupsByMemberResource
from dusken.authentication import MyApiKeyAuthentication, ServiceAuthentication
from dusken.authorization import MyDjangoAuthorization
from dusken.models import *
from dusken.utils.api import generate_username, random_string


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
        authentication = MyApiKeyAuthentication() # Who are you?
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
        print "yoyo"
        resource = MemberCreateResource()
        return resource.dispatch_list(request, **kwargs)

    #def apply_filters(self, request, applicable_filters):
    #    # Extra filters are used for filtering by attributes in User class. Find out if there
    #    # are any, and if so, apply them.

    #    extra_filters = {}
    #    if 'username__exact' in applicable_filters:
    #        extra_filters['username'] = applicable_filters.pop('username__exact')
    #    if 'first_name__exact' in applicable_filters:
    #        extra_filters['first_name'] = applicable_filters.pop('first_name__exact')
    #    if 'last_name__exact' in applicable_filters:
    #        extra_filters['last_name'] = applicable_filters.pop('last_name__exact')
    #    if 'email__exact' in applicable_filters:
    #        extra_filters['email'] = applicable_filters.pop('email__exact')


    #    filtered = super(MemberResource, self).apply_filters(request, applicable_filters)

    #    for key,value in extra_filters.items():
    #        filtered = filter(lambda m: getattr(m, key) == value, filtered)

    #    return filtered

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
        if 'city' in new_address:
            address.city = new_address['city']
        if 'postal_code' in new_address:
            address.postal_code = new_address['postal_code']
        if 'country' in new_address:
            try:
                country = Country.objects.get(name=new_address['country'])
            except Country.DoesNotExist, e:
                # FIXME change to badrequest?
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
    # - do not return fields in excludes list
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
        authentication = ServiceAuthentication() # anyone
        authorization = Authorization() # can do what they want with anything
        always_return_data = True
        excludes = [ 'date_joined', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login' ]

    def obj_create(self, bundle, request=None, **kwargs):
        # TODO factor out validation http://django-tastypie.readthedocs.org/en/latest/validation.html
        # email must be unique
        email = bundle.data.get('email')
        if(len(Member.objects.filter(email__iexact=email)) > 0):
            raise BadRequest("E-mail '{0}' already exists".format(email))

        bundle.data['email'] = Member.objects.normalize_email(email)

        password = bundle.data.get('password')
        if not password:
            # generate a random password if it is not set
            bundle.data['password'] = Member.objects.make_random_password(length=32)

        username = bundle.data.get('username')
        if not username:
            username = bundle.data['username'] = generate_username(bundle.data)
            # FIXME unsafe
            while(len(Member.objects.filter(username=username)) > 0):
                username = bundle.data['username'] = generate_username(bundle.data)

        # When creating a new user, check if it already exists:
        try:
            bundle = super(MemberCreateResource, self).obj_create(bundle, **kwargs)
            bundle.obj.set_password(password)
            bundle.obj.save()
        except IntegrityError as e:
            print e
            raise BadRequest('That username already exists')

        return bundle
