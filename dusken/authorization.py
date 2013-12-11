import logging
import provider.oauth2

from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from provider.oauth2.models import AccessToken
from tastypie.authentication import Authentication
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
                    key = auth_header_value.split(' ')[1]
            if not key:
                logging.error('OAuth20Authentication. No consumer_key found.')
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
