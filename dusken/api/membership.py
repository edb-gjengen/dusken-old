from django.conf.urls import url
from dusken.api.member import MemberResource
from dusken.models import *
from tastypie import fields
from dusken.authorization import MyDjangoAuthorization
from dusken.authentication import MyApiKeyAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class MembershipResource(ModelResource):
    """
    This class provides following endpoints:
    (1) /api/v1/membership/
    """
    member = fields.ForeignKey(MemberResource, 'member')
    expires = fields.DateTimeField(attribute='expires', readonly=True)

    class Meta:
        queryset = Membership.objects.all()
        resource_name = 'membership'
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'patch' ]
        authorization = MyDjangoAuthorization()
        authentication = MyApiKeyAuthentication()
        excludes = [ 'end_date']
        filtering = {
            'member' : ALL_WITH_RELATIONS,
            'expires' : [ 'exact','range','gt','gte','lt','lte' ], #TODO: Doesn't work.
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/type/$" % (self._meta.resource_name), self.wrap_view("list_type"), name="api_type"),
            url(r"^(?P<resource_name>%s)/type/(?P<id>\d+)/$" % (self._meta.resource_name), self.wrap_view("detail_type"), name="api_detail_type"),
        ]

    def list_type(self, request, **kwargs):
        resource = MembershipTypeResource()
        return resource.dispatch_list(request, **kwargs)

    def detail_type(self, request, **kwargs):
        resource = MembershipTypeResource()
        return resource.dispatch_detail(request, **kwargs)

    def hydrate(self, bundle):
        if 'membership_type' in bundle.data:
            bundle.obj.membership_type = MembershipType.objects.get(id=bundle.data['membership_type'])

        if 'member' in bundle.data:
            bundle.data['member'] = Member.objects.get(id=bundle.data['member'])

        return bundle

    def dehydrate(self, bundle):
        bundle.data['member'] = bundle.obj.member.id
        bundle.data['membership_type'] = bundle.obj.membership_type.id
        bundle.data['payment'] = None if not bundle.obj.payment else bundle.obj.payment.id
        return bundle

    def obj_update(self, bundle, request, **kwargs):
        member_id = bundle.data.get('member')
        membership_type = bundle.data.get('membership_type')
        start_date = bundle.data.get('start_date')

        if None in (member_id, membership_type, start_date):
            return super(MembershipResource, self).obj_update(bundle, request, **kwargs)

        # TODO: Refuse to update to exactly the same object.

        return super(MembershipResource, self).obj_update(bundle, request, **kwargs)


class MembershipTypeResource(ModelResource):
    class Meta:
        object_class = MembershipType
        queryset = MembershipType.objects.all()
        resource_name = "membership/type"
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'delete' ]
        authorization = MyDjangoAuthorization()

    def delete_detail(self, request, **kwarg):
        #TODO set is_active flag to False
        pass
