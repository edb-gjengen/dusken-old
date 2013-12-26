from django.shortcuts import get_object_or_404
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound, HttpAccepted, HttpCreated, HttpResponse, HttpBadRequest, HttpNoContent
from tastypie.resources import Resource
from dusken.models import Member
from django.contrib.auth.models import Group

import logging

class GroupMemberObject(object):
    def __init__(self):
        self.member_id = 0
        self.group_id = []
        self.is_member = True

class AbstractGroupMemberResource(Resource):
    member_id = fields.IntegerField(attribute='member_id')
    group_id = fields.IntegerField(attribute='group_id')
    is_member = fields.BooleanField(attribute='is_member')

    class Meta:
        object_class = GroupMemberObject
        list_allowed_methods = [ 'get' ]
        detail_allowed_methods = [ 'get', 'delete', 'post' ]
        authorization = Authorization() # TODO: Obvious

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        return kwargs

    def get_object_list(self, request):
        return self.obj_get_list(request)


    def obj_get_list(self, request=None, **kwargs):
        raise NotImplementedError

    def obj_get(self, request=None, **kwargs):
        member_id = int(kwargs['member_id'])
        member = get_object_or_404(Member, pk=member_id)

        group_id = int(kwargs['group_id'])
        group = get_object_or_404(Group, pk=group_id)

        obj = GroupMemberObject()
        obj.member_id = member_id
        obj.group_id = group_id

        if self._member_has_group(member, group):
            obj.is_member = True
        else:
            obj.is_member = False

        return obj

    def post_detail(self, request=None, **kwargs):
        """
        Creates a new relationship between a member and a group.
        """
        member_id = int(kwargs['member_id'])
        member = get_object_or_404(Member, pk=member_id)

        group_id = int(kwargs['group_id'])
        group = get_object_or_404(Group, pk=group_id)

        if self._member_has_group(member, group):
            # TODO: Check for a correct status code to return in this case.
            return HttpCreated()

        member.groups.add(group)
        member.save()

        return HttpCreated()

    def obj_update(self, bundle, request=None, **kwargs):
        logging.info("Someone tried to obj_update, but I can't do that, man, I can't do that!")
        return # We can't update.

    def obj_delete_list(self, request=None, **kwargs):
        logging.info("Someone tried to obj_delete_list, but I can't do that, man, I can't do that!")
        return # We can't delete lists.

    def obj_delete(self, request=None, **kwargs):
        member_id = int(kwargs['member_id'])
        member = get_object_or_404(Member, pk=member_id)

        group_id = int(kwargs['group_id'])
        group  = get_object_or_404(Group, pk=group_id)
        
        group.user_set.remove(member) 
        return HttpNoContent()

    def rollback(self, bundles):
        logging.info("Someone tried to rollback, but I can't do that, man, I can't do that!")
        return

    def _member_has_group(self, member, group):
        return member.groups.filter(id=group.id).count() != 0

