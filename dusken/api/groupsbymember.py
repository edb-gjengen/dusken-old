from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from dusken.models import Member, Group

class GroupsByMemberObject(object):
    def __init__(self):
        self.member_id = 0
        self.groups = []

class GroupsByMemberResource(Resource):
    member_id = fields.IntegerField(attribute='member_id')
    groups = fields.ListField(attribute='groups')

    class Meta:
        resource_name = 'groupsbymember'
        object_class = GroupsByMemberObject
        list_allowed_methods = [ 'post' ]
        detail_allowed_methods = [ 'get', 'delete' ]
        authorization = Authorization() # TODO: look up
        filtering = {
            'member_id' : [ 'exact' ]
        }

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }
 
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.member_id
        else:
            kwargs['pk'] = bundle_or_obj.member_id
        
        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name
        
        return kwargs

    def get_object_list(self, request):
        pass # We can't return lists.

    def obj_get_list(self, request=None, **kwargs):
        pass # We can't return lists.

    def obj_get(self, request=None, **kwargs):
        member_id = int(kwargs['pk'])
        member = Member.objects.get(id=member_id)

        if member is None:
            return None

        obj = GroupsByMemberObject()
        obj.member_id = member.id
        for group in member.groups.all():
            obj.groups.append(group.id)

        return obj

    def obj_create(self, request=None, **kwargs):
        group  = Group.objects.get(id=group_id)
        member = Member.objects.get(id=user_id)
        group.user_set.add(member) 

    def obj_update(self, bundle, request=None, **kwargs):
        pass # We can't update.

    def obj_delete_list(self, request=None, **kwargs):
        pass # We can't delete lists.

    def obj_delete(self, request=None, **kwargs):
        group  = Group.objects.get(id=group_id)
        member = Member.objects.get(id=user_id)
        group.user_set.remove(member) 


    def rollback(self, bundles):
        pass
