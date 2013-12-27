from tastypie import fields
from tastypie.resources import ModelResource

from dusken.authentication import OAuth20Authentication
from dusken.authorization import MyDjangoAuthorization
from dusken.models import Member

from dusken.api.division import DivisionResource
from dusken.api.membership import MembershipResource
from dusken.api.address import AddressResource
from dusken.api.group import GroupResource

class MeResource(ModelResource):
    """
    This class provides following endpoint:
      /api/v1/me/
    """
    groups = fields.ToManyField(GroupResource, 'groups', full=True)
    divisions = fields.ToManyField(DivisionResource, 'division_set', full=True)
    memberships = fields.ToManyField(MembershipResource, 'membership_set', full=True)
    address = fields.ForeignKey(AddressResource, 'address', full=True)

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

    def dehydrate(self, bundle):
        """
        Catches GET requests and adds more data.
        """
        bundle.data['has_valid_membership'] = bundle.obj.has_valid_membership()

        return bundle
