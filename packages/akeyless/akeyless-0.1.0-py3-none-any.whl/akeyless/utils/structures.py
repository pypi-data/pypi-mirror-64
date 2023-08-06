import base64

import ecdsa


class ApiKey(object):

    def __init__(self, api_key):
        # type: (ecdsa.SigningKey) -> None
        self._api_key = api_key

    def get_key_seed_str(self):
        # type: () -> str
        return base64.b64encode(self._api_key.to_string())

    def __str__(self):
        # type: () -> str
        return str(self.get_key_seed_str())


class ClientAccessApi(object):

    def __init__(self, auth_method_name, access_id, key):
        # type: (str, str, ecdsa.SigningKey) -> None
        self._auth_method_name = auth_method_name
        self._access_id = access_id
        self._api_key = ApiKey(key)

    @property
    def auth_method_name(self):
        return self._auth_method_name

    @property
    def access_id(self):
        return self._access_id

    @property
    def api_key(self):
        return self._api_key.get_key_seed_str()

    def __repr__(self):
        return 'ClientAccessApi({},{},{})'.format(self.auth_method_name,
                                                  self.access_id,
                                                  self.api_key)

    def __str__(self):
        return "Auth Method Name: {}\nAccess Id: {}\nAPI Key: {}\n".format(self.auth_method_name,
                                                                           self.access_id,
                                                                           self.api_key)
