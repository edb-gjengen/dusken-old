from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from dusken.api.member import MemberResource
from dusken.models import *


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
        detail_allowed_methods = [ 'get', 'post' ]
        authorization = Authorization() # TODO: for dev (VERY INSECURE)
        filtering = {
            'member' : ALL_WITH_RELATIONS,
            'expires' : [ 'exact','range','gt','gte','lt','lte' ], #TODO: Doesn't work.
        }

    def dehydrate(self, bundle):
        bundle.data['member'] = bundle.obj.member.id
        bundle.data['mtype'] = bundle.obj.mtype.id
        bundle.data['payment'] = None if not bundle.obj.payment else bundle.obj.payment.id
        return bundle
