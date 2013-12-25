import logging
import provider.oauth2

from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from provider.oauth2.models import AccessToken, Client
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.http import HttpUnauthorized

class OAuth20Authentication(Authentication):
    """
    OAuth authenticator. 

    This Authentication method checks for a provided HTTP_AUTHORIZATION
    and looks up to see if this is a valid OAuth Access Token
    """
    def __init__(self, realm='API'):
        self.realm = realm

    def is_authenticated(self, request, **kwargs):
        """
        Verify 2-legged oauth request. Parameters accepted as
        values in "Authorization" header, or as a GET request
        or in a POST body.
        """
        logging.info("OAuth20Authentication")

        try:
            key = request.GET.get('oauth_consumer_key')
            if not key:
                key = request.POST.get('oauth_consumer_key')
            if not key:
                auth_header_value = request.META.get('HTTP_AUTHORIZATION')
                if auth_header_value:
                    if 'Authorization' in auth_header_value:
                        key = auth_header_value.split(': ')[1].split(" ")[1]
                    else:
                        key = auth_header_value.split(' ')[1]
            if not key:
                logging.info('OAuth20Authentication. No consumer_key found.')
                return None
            """
            If verify_access_token() does not pass, it will raise an error
            """
            token = verify_access_token(key)

            # If OAuth authentication is successful, set the request user to the token user for authorization
            request.user = token.user

            # If OAuth authentication is successful, set oauth_consumer_key on request in case we need it later
            request.META['oauth_consumer_key'] = key
            return True
        except KeyError, e:
            logging.exception("Error in OAuth20Authentication.")
            request.user = AnonymousUser()
            return False
        except Exception, e:
            logging.exception("Error in OAuth20Authentication.")
            return False
        return True

def verify_access_token(key):
    # Check if key is in AccessToken key
    try:
        token = AccessToken.objects.get(token=key)

        # Check if token has expired
        if token.expires < timezone.now():
            raise OAuthError('AccessToken has expired.')
    except AccessToken.DoesNotExist, e:
        raise OAuthError("AccessToken not found at all.")

    logging.info('Valid access')
    return token

def create_access_token(user):
    # Create a Oauth2 Client (each test gets a new one)
    oauth2_client = Client.objects.create(
        user=user,
        name="example.com testclient",
        client_type=1, # ??
        url="http://example.com")
    # Create a Oauth2 AccessToken (each test gets a new one)
    access_token = AccessToken(user=user, client=oauth2_client)
    access_token.save()

    # Return HTTP authorization header
    return "Authorization: OAuth {}".format(access_token.token)


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

"""
This is a simple OAuth 2.0 authentication model for tastypie

Copied nearly verbatim from amrox's example 
 - https://github.com/amrox/django-tastypie-two-legged-oauth

Dependencies: 
 - django-oauth2-provider: https://github.com/caffeinehit/django-oauth2-provider

Example:
 - http://ianalexandr.com
"""

# stolen from piston
class OAuthError(RuntimeError):
    """Generic exception class."""
    def __init__(self, message='OAuth error occured.'):
        self.message = message
