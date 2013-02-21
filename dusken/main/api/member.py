from tastypie import fields
from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization
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
        detail_allowed_methods = [ 'get', 'post' ]
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
        if filters is None:
            filters = {}

        orm_filters = super(MemberResource, self).build_filters(filters)
        return orm_filters

    def apply_filters(self, request, applicable_filters):
        extra_filters = {}
        if 'username__exact' in applicable_filters:
            extra_filters['username'] = applicable_filters.pop('username__exact')
        if 'first_name__exact' in applicable_filters:
            extra_filters['first_name'] = applicable_filters.pop('first_name__exact')
        if 'last_name__exact' in applicable_filters:
            extra_filters['last_name'] = applicable_filters.pop('last_name__exact')
        if 'email__exact' in applicable_filters:
            extra_filters['email'] = applicable_filters.pop('email__exact')


        filters = super(MemberResource, self).apply_filters(request, applicable_filters)

        for key,value in extra_filters.items():
            filters = filter(lambda m: getattr(m.user, key) == value, filters)

        return filters

    def hydrate(self, bundle):
        if bundle.obj.user_id == None:
            possible_fields = [ 'username', 'password', 'email', 'first_name', 'last_name' ]
            user_params = {}

            for field in possible_fields:
                data = bundle.data.get(field)
                if data is not None:
                    user_params[field] = data

            user = User(**user_params)
            user.save()
            bundle.data['user_id'] = user.id
            bundle.obj.user_id = user.id
        return bundle

    def dehydrate(self, bundle):
        return bundle
