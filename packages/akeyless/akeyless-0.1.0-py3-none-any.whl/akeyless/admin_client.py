import base64
import json

import ecdsa
from hashlib import sha256

from akeyless_auth_api import SetUAMAccessCredsParams
from akeyless_uam_api import GetAccountDetailsReplyObj, AccessRules, GetRoleReplyObj, GetAuthMethodReplyObj, \
    GetAccountAuthMethodsReplyObj, GetAccountRolesReplyObj, Rules, APIKeyAccessRules, SetRoleRequestParams, \
    CreateRoleAuthMethodAssocReplyObj
from akeyless_uam_api.rest import ApiException

from akeyless.admin_client_base import AkeylessAdminClientI
from akeyless.config import AkeylessClientConfig
from akeyless.client import AkeylessClient
from akeyless.utils import ClientAccessApi
from akeyless.utils.structures import ApiKey


class AkeylessAdminClient(AkeylessAdminClientI, AkeylessClient):

    def __init__(self, config):
        # type: (AkeylessClientConfig) -> None
        super(AkeylessAdminClient, self).__init__(config)

    def get_account_details(self):
        # type: () -> GetAccountDetailsReplyObj
        return self.api.get_account_details(self.cr.get_uam_creds())

    def create_auth_method(self, auth_method_name, expires=0, cidr_whitelist=None):
        # type: (str, int, list) -> ClientAccessApi
        api_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc=sha256)
        pub_key_der = api_key.get_verifying_key().to_der()
        pub_key_encoded = base64.b64encode(pub_key_der).decode()
        cidr_str = ""
        if cidr_whitelist is not None:
            cidr_str = ','.join(cidr_whitelist)

        api_key_ar = APIKeyAccessRules(alg="ECDSA_P256_SHA256", key=pub_key_encoded)
        access_rules = AccessRules(api_key_access_rules=api_key_ar, cidr_whitelist=cidr_str)
        access_params = SetUAMAccessCredsParams("api_key", expires, access_rules, None)

        set_access_creds = self.api.set_uam_access_creds(self.cr.get_auth_creds(), access_params)
        res = self.api.create_auth_method(self.cr.get_uam_creds(), set_access_creds.credential, auth_method_name)

        return ClientAccessApi(auth_method_name, res.auth_method_access_id, api_key)

    def get_auth_method(self, auth_method_name):
        # type: (str) -> GetAuthMethodReplyObj
        return self.api.get_auth_method(self.cr.get_uam_creds(), auth_method_name)

    def get_account_auth_methods(self):
        # type: () -> GetAccountAuthMethodsReplyObj
        try:
            return self.api.get_account_auth_methods(self.cr.get_uam_creds())
        except ApiException as e:
            if "NotFound" not in e.body:
                raise e
            return GetAccountAuthMethodsReplyObj([])

    def update_auth_method_name(self, auth_method_name, new_auth_method_name):
        # type: (str, str) -> None
        access_params = SetUAMAccessCredsParams(None, None, None, None)
        set_access_creds = self.api.set_uam_access_creds(self.cr.get_auth_creds(), access_params)
        return self.api.update_auth_method(self.cr.get_uam_creds(),
                                           set_access_creds.credential,
                                           new_auth_method_name,
                                           auth_method_name)

    def update_auth_method_access_expires(self, auth_method_name, expires):
        # type: (str, int) -> None

        update_modes = ["update_exp"]
        access_params = SetUAMAccessCredsParams(None, expires, None, update_modes)
        set_access_creds = self.api.set_uam_access_creds(self.cr.get_auth_creds(), access_params)
        return self.api.update_auth_method(self.cr.get_uam_creds(),
                                           set_access_creds.credential,
                                           auth_method_name,
                                           auth_method_name)

    def update_auth_method_cidr_whitelist(self, auth_method_name, cidr_whitelist=None):
        # type: (str, list) -> None

        cidr_str = ""
        if cidr_whitelist is not None:
            cidr_str = ','.join(cidr_whitelist)

        update_modes = ["update_cidr"]
        access_rules = AccessRules(cidr_whitelist=cidr_str)
        access_params = SetUAMAccessCredsParams(None, None, access_rules, update_modes)
        set_access_creds = self.api.set_uam_access_creds(self.cr.get_auth_creds(), access_params)
        return self.api.update_auth_method(self.cr.get_uam_creds(),
                                           set_access_creds.credential,
                                           auth_method_name,
                                           auth_method_name)

    def update_auth_method(self, auth_method_name, new_auth_method_name, expires=None, cidr_whitelist=None):
        # type: (str, str, int, list) -> None

        cidr_str = ""
        if cidr_whitelist is not None:
            cidr_str = ','.join(cidr_whitelist)

        update_modes = ["update_exp", "update_cidr"]
        rules = AccessRules(cidr_whitelist=cidr_str)
        access_params = SetUAMAccessCredsParams(None, expires, rules, update_modes)
        set_access_creds = self.api.set_uam_access_creds(self.cr.get_auth_creds(), access_params)
        return self.api.update_auth_method(self.cr.get_uam_creds(),
                                           set_access_creds.credential,
                                           new_auth_method_name,
                                           auth_method_name)

    def reset_auth_method_access_key(self, auth_method_name):
        # type: (str) -> ApiKey
        api_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc=sha256)
        pub_key_der = api_key.get_verifying_key().to_der()
        pub_key_encoded = base64.b64encode(pub_key_der).decode()
        api_key_ar = APIKeyAccessRules(alg="ECDSA_P256_SHA256", key=pub_key_encoded)
        rules = AccessRules(api_key_access_rules=api_key_ar)
        access_params = SetUAMAccessCredsParams("api_key", None, rules, ["update_key"])

        set_access_creds = self.api.set_uam_access_creds(self.cr.get_auth_creds(), access_params)
        self.api.update_auth_method(self.cr.get_uam_creds(), set_access_creds.credential,
                                    auth_method_name, auth_method_name)

        return ApiKey(api_key)

    def delete_auth_method(self, auth_method_name):
        # type: (str) -> None
        return self.api.delete_auth_method(self.cr.get_uam_creds(), auth_method_name)

    def create_role(self, role_name, rules=None, comment=""):
        # type: (str, Rules, str) -> None
        body = SetRoleRequestParams(new_role_name=role_name, rules=rules, comment=comment)
        return self.api.create_role(self.cr.get_uam_creds(), body)

    def get_role(self, role_name):
        # type: (str) -> GetRoleReplyObj
        return self.api.get_role(self.cr.get_uam_creds(), role_name)

    def get_account_roles(self):
        # type: () -> GetAccountRolesReplyObj
        try:
            return self.api.get_account_roles(self.cr.get_uam_creds())
        except ApiException as e:
            if "NotFound" not in e.body:
                raise e
            return GetAccountRolesReplyObj([])

    def update_role(self, role_name, new_role_name, rules, comment):
        # type: (str, str, Rules, str) -> None
        body = SetRoleRequestParams(new_role_name=new_role_name, rules=rules, comment=comment)
        return self.api.update_role(self.cr.get_uam_creds(), role_name, body)

    def delete_role(self, role_name):
        # type: (str) -> None
        return self.api.delete_role(self.cr.get_uam_creds(), role_name)

    def create_role_auth_method_assoc(self, role_name, associated_name, sub_claims=None):
        # type: (str, str, dict) -> CreateRoleAuthMethodAssocReplyObj
        if sub_claims is None:
            sub_claims = {}
        return self.api.create_role_auth_method_assoc(self.cr.get_uam_creds(),
                                                      role_name,
                                                      associated_name,
                                                      sub_claims_base64=base64.b64encode(
                                                          json.dumps(sub_claims).encode()))

    def delete_role_auth_method_assoc(self, association_id):
        # type: (str) -> None
        return self.api.delete_role_auth_method_assoc(self.cr.get_uam_creds(), association_id)
