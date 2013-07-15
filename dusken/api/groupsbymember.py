from django.shortcuts import get_object_or_404
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound, HttpAccepted, HttpCreated, HttpResponse, HttpBadRequest
from tastypie.resources import Resource
from dusken.models import Member, Group

import logging

class GroupByMemberObject(object):
    def __init__(self):
        self.member_id = 0
        self.group_id = []
        self.is_member = True

class GroupsByMemberResource(Resource):
    member_id = fields.IntegerField(attribute='member_id')
    group_id = fields.IntegerField(attribute='group_id')
    is_member = fields.BooleanField(attribute='is_member')

    class Meta:
        object_class = GroupByMemberObject
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
        member_id = int(kwargs['member_id'])
        member = get_object_or_404(Member, pk=member_id)
        groups = []
        for group in member.groups.all():
            obj = GroupByMemberObject
            obj.member_id = member_id
            obj.group_id = group.id
            obj.is_member = True
            groups.append(obj)

        return groups

    def obj_get(self, request=None, **kwargs):
        member_id = int(kwargs['member_id'])
        member = get_object_or_404(Member, pk=member_id)

        group_id = int(kwargs['group_id'])
        group = get_object_or_404(Group, pk=group_id)

        obj = GroupByMemberObject()
        obj.member_id = member_id
        obj.group_id = group_id

        if member.groups.filter(id=group_id).count() == 0:
            obj.is_member = False
        else:
            obj.is_member = True

        return obj

    def post_detail(self, request=None, **kwargs):
        """
        Creates a new relationship be.
        """

        keys = kwargs['pk'].split('/')
        if len(keys) < 2:
            raise ImmediateHttpResponse(HttpBadRequest())

        member_id = keys[0]
        group_id = keys[1]

        
        print("Calling create function with parameters {0}".format(str(kwargs)))
        return HttpCreated()

    def obj_update(self, bundle, request=None, **kwargs):
        logging.info("Someone tried to obj_update, but I can't do that, man, I can't do that!")
        return # We can't update.

    def obj_delete_list(self, request=None, **kwargs):
        logging.info("Someone tried to obj_delete_list, but I can't do that, man, I can't do that!")
        return # We can't delete lists.

    def obj_delete(self, request=None, **kwargs):
        print str(kwargs +"\n\n\n\n")
        group  = Group.objects.get(id=group_id)
        member = Member.objects.get(id=user_id)
        group.user_set.remove(member) 


    def rollback(self, bundles):
        logging.info("Someone tried to rollback, but I can't do that, man, I can't do that!")
        return
