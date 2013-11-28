from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized

# TODO add django-guardian for object level/row level permissions.
# Ref: https://gist.github.com/7wonders/6557760
# Usage example: User in group x is admin of group y 
# Literal usage example: Runar in group KAK-styret is admin of group KAK.

"""
    Create
    ######

    All registered users should be allowed to create: 

    * Membership

    Unregistered users should be able to create:
    
    * Member

    Update
    ######

    All registered users should be allowed to update: 


    Delete
    ######

    All registered users should be allowed to delete:

"""

class MyDjangoAuthorization(DjangoAuthorization):

    def create_detail(self, object_list, bundle):
        # Special case for creating a new user
        if hasattr(bundle, '_anonymous_request_allowed'):
            return True

        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        # Skip permission check if the request is made by the object owner
        # Note: tastypie.authorization.DjangoAuthorization does not have this check
        if bundle.obj.owner() == bundle.request.user:
            return True

        permission = '%s.add_%s' % (klass._meta.app_label, klass._meta.module_name)

        if not bundle.request.user.has_perm(permission):
            raise Unauthorized("You are not allowed to access that resource.")

        return True

    def update_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        # Skip permission check if the request is made by the object owner
        # Note: tastypie.authorization.DjangoAuthorization does not have this check
        if bundle.obj.owner() == bundle.request.user:
            return True

        permission = '%s.change_%s' % (klass._meta.app_label, klass._meta.module_name)

        if not bundle.request.user.has_perm(permission):
            raise Unauthorized("You are not allowed to access that resource.")

        return True

