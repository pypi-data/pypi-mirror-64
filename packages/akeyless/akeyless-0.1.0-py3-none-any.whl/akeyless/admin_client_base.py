import abc

import six
from akeyless_uam_api import GetAccountDetailsReplyObj, GetAuthMethodReplyObj, GetRoleReplyObj, \
    GetAccountRolesReplyObj, GetAccountAuthMethodsReplyObj, Rules, CreateRoleAuthMethodAssocReplyObj

from akeyless.config import AkeylessClientConfig
from akeyless.client_base import AkeylessClientI
from akeyless.utils import ClientAccessApi
from akeyless.utils.structures import ApiKey


@six.add_metaclass(abc.ABCMeta)
class AkeylessAdminClientI(AkeylessClientI):

    def __init__(self, config):
        # type: (AkeylessClientConfig) -> None
        super(AkeylessAdminClientI, self).__init__(config)

    @abc.abstractmethod
    def get_account_details(self):
        # type: () -> GetAccountDetailsReplyObj
        """Get account details.

        This endpoint is accessible only by administrator

        :return: The account details
        :rtype: GetAccountDetailsReplyObj
        """

    @abc.abstractmethod
    def create_auth_method(self, auth_method_name, expires=0, cidr_whitelist=None):
        # type: (str, int, list) -> ClientAccessApi
        """Add a new auth method to the account.

        This endpoint is accessible only by administrator

        :param str auth_method_name: The auth method name to be created (required)
        :param int expires: Access expiration date in Unix timestamp. In case of 0 or null the
                            access will not be limited in time.
        :param list cidr_whitelist: An CIDR Whitelisting. Only requests from the ip addresses that match the CIDR
                                    list will be able to obtain temporary access credentials. The list length is
                                    limited to 10 CIDRs. In the case of None or an empty string there will be no
                                    restriction of IP addresses.
        :return: An object that contains the auth method name, access id and access key
        :rtype: ClientAccessApi
        """

    @abc.abstractmethod
    def get_auth_method(self, auth_method_name):
        # type: (str) -> GetAuthMethodReplyObj
        """Get auth method details.

        This endpoint is accessible only by administrator

        :param str auth_method_name: Auth method name. (required)
        :return: The auth method details
        :rtype: GetAuthMethodReplyObj
        """

    @abc.abstractmethod
    def get_account_auth_methods(self):
        # type: () -> GetAccountAuthMethodsReplyObj
        """Get all the existing auth methods in the account.

        This endpoint is accessible only by administrator

        :return: A list of all the existing auth methods in the account.
        :rtype: GetAccountAuthMethodsReplyObj
        """

    @abc.abstractmethod
    def update_auth_method_name(self, auth_method_name, new_auth_method_name):
        # type: (str, str) -> None
        """Updating auth method name

        This endpoint is accessible only by administrator

        :param str auth_method_name: Auth method name. (required)
        :param str new_auth_method_name: The new auth method name that will replace the existing one (required)
        """

    @abc.abstractmethod
    def update_auth_method_access_expires(self, auth_method_name, expires):
        # type: (str, int) -> None
        """Updating auth method access expiration date

        This endpoint is accessible only by administrator

        :param str auth_method_name: Auth method name. (required)
        :param int expires: Access expiration date in Unix timestamp. In case of 0 or null the access will
                            not be limited in time.
        """

    @abc.abstractmethod
    def update_auth_method_cidr_whitelist(self, auth_method_name, cidr_whitelist=None):
        # type: (str , list) -> None
        """Updating auth method CIDR whitelist

        This endpoint is accessible only by administrator

        :param str auth_method_name: Auth method name. (required)
        :param list cidr_whitelist: An CIDR Whitelisting. Only requests from the ip addresses that match the CIDR
                                    list will be able to obtain temporary access credentials. The list length is
                                    limited to 10 CIDRs. In the case of None or an empty string there will be no
                                    restriction of IP addresses
        """

    @abc.abstractmethod
    def update_auth_method(self, auth_method_name, new_auth_method_name, expires=0, cidr_whitelist=None):
        # type: (str, str, int , list) -> None
        """Updating auth method parameters

        This endpoint is accessible only by administrator

        :param str auth_method_name: Auth method name. (required)
        :param str new_auth_method_name: The new auth method name that will replace the existing one (required)
        :param int expires: Access expiration date in Unix timestamp. In case of 0 or null the access will
                            not be limited in time.
        :param list cidr_whitelist: An CIDR Whitelisting. Only requests from the ip addresses that match the CIDR
                                    list will be able to obtain temporary access credentials. The list length is
                                    limited to 10 CIDRs. In the case of None or an empty string there will be no
                                    restriction of IP addresses
        """

    @abc.abstractmethod
    def reset_auth_method_access_key(self, auth_method_name):
        # type: (str) -> ApiKey
        """Replacing the auth methos's access API key

        This endpoint is accessible only by administrator

        :param str auth_method_name: Auth method name. (required)
        :return: The new access key
        :rtype: ApiKey
        """

    @abc.abstractmethod
    def delete_auth_method(self, auth_method_name):
        # type: (str) -> None
        """Deleting an existing auth method from the account.

        This endpoint is accessible only by administrator

        :param str auth_method_name: Auth method name. (required)
        """

    @abc.abstractmethod
    def create_role(self, role_name, rules=None, comment=""):
        # type: (str, Rules, str) -> None
        """Add a new role to the account.

        This endpoint is accessible only by administrator

        :param str role_name: The role name to be created (required)
        :param Rules rules: Role rules.
        :param str comment: Comments
        """

    @abc.abstractmethod
    def get_role(self, role_name):
        # type: (str) -> GetRoleReplyObj
        """Get role details.

        This endpoint is accessible only by administrator

        :param str role_name: Role name. (required)
        :return: The role details
        :rtype: GetRoleReplyObj
        """

    @abc.abstractmethod
    def get_account_roles(self):
        # type: () -> GetAccountRolesReplyObj
        """Get All the existing roles in the account.

        This endpoint is accessible only by administrator

        :return: A list of all the existing roles in the account.
        :rtype: GetAccountRolesReplyObj
        """

    @abc.abstractmethod
    def update_role(self, role_name, new_role_name, rules, comment):
        # type: (str, str, Rules, str) -> None
        """Updating an existing role in the account

        This endpoint is accessible only by administrator

        :param str role_name: Role name. (required)
        :param str new_role_name: The new role name that will replace the existing one (required)
        :param Rules rules: Role rules.
        :param str comment: Comments
        """

    @abc.abstractmethod
    def delete_role(self, role_name):
        # type: (str) -> None
        """Deleting an existing role from the account.

        This endpoint is accessible only by administrator

        :param str role_name: Role name. (required)
        """

    @abc.abstractmethod
    def create_role_auth_method_assoc(self, role_name, associated_name, sub_claims):
        # type: (str, str, dict) -> CreateRoleAuthMethodAssocReplyObj
        """Add an association between a role and an auth method.

        This endpoint is accessible only by administrator

        :param str role_name: The role name to be associated (required)
        :param str associated_name: The auth method name to be associated. (required)
        :param dict sub_claims: The auth method name to be associated.
        :return: Association id
        :rtype: CreateRoleAuthMethodAssocReplyObj
        """

    @abc.abstractmethod
    def delete_role_auth_method_assoc(self, association_id):
        # type: (str) -> None
        """Deleting an association between a role and an auth method.

        This endpoint is accessible only by administrator

        :param str association_id: The association id to be deleted (required)
        """