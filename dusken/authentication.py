from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.http import HttpUnauthorized

# TODO replace with Oauth2 http://django-tastypie.readthedocs.org/en/latest/cookbook.html#creating-a-full-oauth-2-0-api

class MyApiKeyAuthentication(ApiKeyAuthentication):
    """
        Override method below to use our custom User model
    """

    def is_authenticated(self, request, **kwargs):
        """
        Finds the user and checks their API key.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """
        # Ninjafix to get our custom model working
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username_field = User.USERNAME_FIELD

        try:
            username, api_key = self.extract_credentials(request)
        except ValueError:
            return self._unauthorized()

        if not username or not api_key:
            return self._unauthorized()

        try:
            lookup_kwargs = {username_field: username}
            user = User.objects.get(**lookup_kwargs)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return self._unauthorized()

        if not self.check_active(user):
            return False

        key_auth_check = self.get_key(user, api_key)
        if key_auth_check and not isinstance(key_auth_check, HttpUnauthorized):
            request.user = user

        return key_auth_check


class ServiceAuthentication(Authentication):
    pass
#
    # TODO auth for services
    #
    #def is_authenticated(self, request, **kwargs):
    #    return True
    #    return False

