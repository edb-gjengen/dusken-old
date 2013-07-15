from django.shortcuts import get_object_or_404
from dusken.api.abstract_groupmember import GroupMemberObject, AbstractGroupMemberResource
from dusken.models import Member, Group

import logging

class MembersByGroupResource(AbstractGroupMemberResource):
    def obj_get_list(self, request=None, **kwargs):
        group_id = int(kwargs['group_id'])
        group = get_object_or_404(Group, pk=group_id)
        members = []
        for member in group.user_set.all():
            obj = GroupMemberObject()
            obj.member_id = member.id
            obj.group_id = group.id
            obj.is_member = True
            members.append(obj)

        return members

