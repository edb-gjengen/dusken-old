from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden
from tastypie.resources import ModelResource, ALL
from main.models import *


class MemberResource(ModelResource):
    """
    This class provides following endpoints:
    (1) /api/v1/member/
    (2) /api/v1/member/{id}/
    """
    username = fields.CharField(attribute='username', readonly=True)
    email = fields.CharField(attribute='email', readonly=True)
    first_name = fields.CharField(attribute='first_name', readonly=True)
    last_name = fields.CharField(attribute='last_name', readonly=True)

    class Meta:
        queryset = Member.objects.all()
        resource_name = 'member'
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'patch' ]
        authorization = Authorization() # TODO: for dev (VERY INSECURE)
        excludes = [ 'password' ]
        filtering = {
            'username' : [ 'exact' ],
            'email' : [ 'exact' ],
            'first_name' : [ 'exact' ],
            'last_name' : [ 'exact' ],
            'phone_number' : [ 'exact' ],
        }

    def build_filters(self, filters=None):
        # This is actually vanilla implementation and currently redundant, but I didn't
        # delete it in case we're going to use it for something.
        if filters is None:
            filters = {}

        orm_filters = super(MemberResource, self).build_filters(filters)
        return orm_filters

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
            filtered = filter(lambda m: getattr(m.user, key) == value, filtered)

        return filtered

    def hydrate(self, bundle):
        """
        Catches POST and PATCH requests and intercepts data that are supposed to go into 
        User class and not in Member.
        """

        # Fields that are in the User class and not in Member:
        possible_fields = [ 'username', 'password', 'email', 'first_name', 'last_name' ]

        # From above possibilities, contains fields that are actually in the request:
        user_params = {}

        for field in possible_fields:
            if field in bundle.data:
                data = bundle.data.pop(field)
                user_params[field] = data

        # Check if we also need to create User when creating Member:
        if bundle.obj.user_id == None: # true if new user
            user = User(**user_params)
            user.save()
            self.member_created(**user_params)
            bundle.data['user_id'] = user.id
            bundle.obj.user_id = user.id
        else:
            # This happens only if we're editing existing user.
            new_password = None # Needed later if we're changing password.
            for key, value in user_params.items():
                if key == 'password':
                    # Password has to be hashed before it can be set:
                    bundle.obj.user.set_password(value)
                    new_password = value
                elif key == 'username':
                    if value != bundle.obj.user.username:
                        # We can't change username.
                        raise ImmediateHttpResponse(HttpForbidden("You can't change your username."))
                else:
                    # For all other fields, just change the damn field:
                    setattr(bundle.obj.user, key, value)
            # hydrate is normally NOT used for updating Model objects, so we have to save it manually:
            bundle.obj.user.save()
            if new_password is not None: 
                self.member_password_changed(bundle.obj.user.username, new_password)
        return bundle

    def dehydrate(self, bundle):
        return bundle

    def member_created(self, **kwargs):
        """
        TODO: This function is called every time new user is created.
        """
        pass

    def member_password_changed(self, username, new_password):
        """
        TODO: This function is called every time user changes his password.
        """
        pass
