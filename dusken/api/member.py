from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.conf.urls import url
from django.shortcuts import get_object_or_404
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden, HttpNoContent, HttpResponse
from tastypie.resources import ModelResource, ALL
from dusken.models import *
from dusken.api.groupsbymember import GroupsByMemberResource


class MemberResource(ModelResource):
    """
    This class provides following endpoints:
    (1) /api/v1/member/
    (2) /api/v1/member/{id}/
    """
    class Meta:
        queryset = Member.objects.all()
        resource_name = 'member'
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'patch', 'delete' ]
        authorization = Authorization() # TODO: for dev (VERY INSECURE)
        excludes = [ 'date_joined', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login' ]
        filtering = {
            'username' : [ 'exact' ],
            'email' : [ 'exact' ],
            'first_name' : [ 'exact' ],
            'last_name' : [ 'exact' ],
            'phone_number' : [ 'exact' ],
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<member_id>\d+)/groups/$" % (self._meta.resource_name), self.wrap_view("list_groups"), name="api_groups"),
            url(r"^(?P<resource_name>%s)/(?P<member_id>\d+)/groups/(?P<group_id>\d+)/$" % (self._meta.resource_name), self.wrap_view("detail_groups"), name="api_detail_groups"),
        ]

    def list_groups(self, request, **kwargs):
        resource = GroupsByMemberResource()
        return resource.dispatch_list(request, **kwargs)

    def detail_groups(self, request, **kwargs):
        resource = GroupsByMemberResource()
        return resource.dispatch_detail(request, **kwargs)

    def apply_filters(self, request, applicable_filters):
        # Extra filters are used for filtering by attributes in User class. Find out if there
        # are any, and if so, apply them.

        extra_filters = {}
        if 'username__exact' in applicable_filters:
            extra_filters['username'] = applicable_filters.pop('username__exact')
        if 'first_name__exact' in applicable_filters:
            extra_filters['first_name'] = applicable_filters.pop('first_name__exact')
        if 'last_name__exact' in applicable_filters:
            extra_filters['last_name'] = applicable_filters.pop('last_name__exact')
        if 'email__exact' in applicable_filters:
            extra_filters['email'] = applicable_filters.pop('email__exact')


        filtered = super(MemberResource, self).apply_filters(request, applicable_filters)

        for key,value in extra_filters.items():
            filtered = filter(lambda m: getattr(m, key) == value, filtered)

        return filtered

    def hydrate(self, bundle):
        """
        Catches POST and PATCH requests and intercepts data.
        """
        update_existing_user = bundle.obj.user_ptr_id is not None

        if update_existing_user: 
            # If the user already exists, return an error when attempting to change the username.
            if bundle.data['username'] != bundle.obj.username:
                raise ImmediateHttpResponse(HttpForbidden("You can't change your username."))
        else:
            # If creating new user, check if it already exists:
            member_count = len(Member.objects.filter(username=bundle.data['username'])) \
                + len(Member.objects.filter(email=bundle.data['email'])) \
                + len(Member.objects.filter(phone_number=bundle.data['phone_number']))
            if member_count > 0:
                raise ImmediateHttpResponse(HttpForbidden("User with given data already exists"))
        return bundle

    def obj_update(self, bundle, request, **kwargs):
        if bundle.data.get('password') is not None:
            bundle.obj.set_password(bundle.data['password'])
            bundle.obj.save()

        if 'address' in bundle.data and bundle.data['address'] is not None:
            new_address = bundle.data.get('address')
            address = bundle.obj.address
            
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
                    raise ImmediateHttpResponse(HttpForbidden('The country "{}" does not exist.'.format(new_address['country'])))
                else:
                    address.country = country

            address.save()

        return super(MemberResource, self).obj_update(bundle, request, **kwargs)

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

    def post(self, request, **kwargs):
        pass #TODO Activate user or...
        return super(MemberResource, self).post(request, **kwargs)

    def delete_detail(self, request, **kwargs):
        member = Member.objects.get(kwargs['pk'])
        member.is_active = False
        member.save()
        return HttpNoContent()
