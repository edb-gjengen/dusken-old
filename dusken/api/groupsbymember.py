from django.shortcuts import get_object_or_404
from dusken.api.abstract_groupmember import GroupMemberObject, AbstractGroupMemberResource
from dusken.models import Member, Group

import logging

class GroupsByMemberResource(AbstractGroupMemberResource):
    def obj_get_list(self, request=None, **kwargs):
        member_id = int(kwargs['member_id'])
        member = get_object_or_404(Member, pk=member_id)
        groups = []
        for group in member.groups.all():
            obj = GroupMemberObject()
            obj.member_id = member.id
            obj.group_id = group.id
            obj.is_member = True
            groups.append(obj)

        return groups

