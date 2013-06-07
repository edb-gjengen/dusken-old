from django.contrib.auth.models import User
from django.conf.urls import url
from django.shortcuts import get_object_or_404
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden, HttpNoContent, HttpResponse
from tastypie.resources import ModelResource, ALL
from dusken.models import *
from dusken.api.membersbygroup import MembersByGroupResource
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
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/groups/$" % (self._meta.resource_name), self.wrap_view("get_groups"), name="api_get_groups"),
        ]

    def get_groups(self, request, **kwargs):
        pk = kwargs['pk']
        member = get_object_or_404(Member, pk=pk)

        #response = HttpResponse(self._meta.serializer.serialize(member, self.determine_format(request)))
        resource = GroupsByMemberResource()
        return resource.get_list(request, pk=pk)

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
        if bundle.obj.user_ptr_id is not None: # happens only if user exists
            for key, value in bundle.data.items():
                if key == 'username':
                    if value != bundle.obj.username:
                        # We can't change username.
                        raise ImmediateHttpResponse(HttpForbidden("You can't change your username."))
                elif key == 'password':
                    bundle.obj.set_password(value) #TODO Set password only once we know that we can trust the request.
        return bundle     

    def post(self, request, **kwargs):
        pass #TODO Activate user or...
        return super(MemberResource, self).post(request, **kwargs)

    def delete_detail(self, request, **kwargs):
        member = Member.objects.get(kwargs['pk'])
        member.is_active = False
        member.save()
        return HttpNoContent()
