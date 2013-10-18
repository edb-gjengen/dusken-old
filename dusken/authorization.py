from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized

class MyDjangoAuthorization(DjangoAuthorization):

    def update_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        # Skip permission check if the request is made by the object owner
        # Note: Standard DjangoAuthorization does not have this check
        if bundle.obj == bundle.request.user:
            return True

        permission = '%s.change_%s' % (klass._meta.app_label, klass._meta.module_name)

        if not bundle.request.user.has_perm(permission):
            raise Unauthorized("You are not allowed to access that resource.")

        return True
