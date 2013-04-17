from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from main.models import Member, Group

class MembersByGroupObject(object):
    def __init__(self):
        self.group_id = 0
        self.members = []

class MembersByGroupResource(Resource):
    group_id = fields.IntegerField(attribute='group_id')
    members = fields.ListField(attribute='members')

    class Meta:
        resource_name = 'membersbygroup'
        object_class = MembersByGroupObject
        list_allowed_methods = [ 'post' ]
        detail_allowed_methods = [ 'get', 'delete' ]
        authorization = Authorization() # TODO: Obvious

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }
 
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.group_id
        else:
            kwargs['pk'] = bundle_or_obj.group_id
        
        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name
        
        return kwargs

    def get_object_list(self, request):
        pass # We can't return lists.

    def obj_get_list(self, request=None, **kwargs):
        pass # We can't return lists.

    def obj_get(self, request=None, **kwargs):
        group_id = int(kwargs['pk'])
        group = Group.objects.get(id=group_id)

        if group is None:
            return None

        obj = MembersByGroupObject()
        obj.group_id = group.id
        for member in group.user_set.all():
            obj.members.append(member.id)

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
