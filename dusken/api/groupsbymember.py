from django.shortcuts import get_object_or_404
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound, HttpAccepted, HttpCreated, HttpResponse, HttpBadRequest
from tastypie.resources import Resource
from dusken.models import Member, Group

import logging

class GroupsByMemberObject(object):
    def __init__(self):
        self.member_id = 0
        self.groups = []

class GroupsByMemberResource(Resource):
    member_id = fields.IntegerField(attribute='member_id')
    groups = fields.ListField(attribute='groups')

    class Meta:
        object_class = GroupsByMemberObject
        list_allowed_methods = []
        detail_allowed_methods = [ 'get', 'delete', 'post' ]
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
        logging.info("Someone tried to get_object_list, but I can't do that, man, I can't do that!")
        pass # We can't return lists.

    def obj_get_list(self, request=None, **kwargs):
        member_id = int(kwargs['pk'])
        member = get_object_or_404(Member, pk=member_id)

        obj = GroupsByMemberObject()
        obj.member_id = member_id

        #print "\n\n\n" +str(member.groups.all()) +"\n\n\n"
        for group in member.groups.all():
            obj.groups.append(group)

        return obj

    def obj_get(self, request=None, **kwargs):
        member_id = int(kwargs['pk'])
        member = Member.objects.get(id=member_id)

        member = None
        if len(keys) > 1:
            member_id = int(keys[1])
            member = Member.objects.get(id=member_id)

            if member is None:
                return None

            if member.groups.filter(name=group.name).count() == 0:
                raise ImmediateHttpResponse(HttpNotFound())

        if group is None:
            return None

        obj = MembersByGroupObject()
        obj.group_id = group.id

        if member is None:
            for member in group.user_set.all():
                obj.members.append(member.id)
        else:
            obj.members.append(member.id)

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

        
        logging.error("Calling create function with parameters {0}".format(str(kwargs)))
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
