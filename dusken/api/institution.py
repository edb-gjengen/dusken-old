from django.contrib.auth.models import User
from django.conf.urls import url
from django.shortcuts import get_object_or_404
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden, HttpNoContent, HttpResponse
from tastypie.resources import ModelResource, ALL
from dusken.models import *
from dusken.api.membersbygroup import MembersByGroupResource
from dusken.api.groupsbymember import GroupsByMemberResource


class InstitutionResource(ModelResource):

    class Meta:
        queryset = Institution.objects.all()
        resource_name = 'institution'
        list_allowed_methods = [ 'get', 'post' ]
        detail_allowed_methods = [ 'get', 'patch', 'delete' ]
        authorization = Authorization() # TODO: for dev (VERY INSECURE)
        filtering = {
            'name' : [ 'exact' ],
        }

