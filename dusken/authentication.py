from tastypie.authentication import ApiKeyAuthentication as tastypieApiKeyAuth

class ApiKeyAuthentication(tastypieApiKeyAuth):
    """
        Override with our own ApiKey model.
    """
    def get_key(self, user, api_key):
        """
        Attempts to find the API key for the user. Uses ``ApiKey`` by default
        but can be overridden.
        """
        from dusken.models import ApiKey

        try:
            ApiKey.objects.get(user=user, key=api_key)
        except ApiKey.DoesNotExist:
            return self._unauthorized()

        return True
