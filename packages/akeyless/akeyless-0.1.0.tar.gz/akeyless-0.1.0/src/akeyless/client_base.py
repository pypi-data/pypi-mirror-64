import abc
import six
from akeyless_uam_api import GetItemReplyObj, ListItemsReplyObj, ListItemsInPathReplyObj

from akeyless.api import AkeylessApi
from akeyless.auth import ApiKeyAuthenticator, CredsRenewal
from akeyless.caching import KeyOperationsCredsCache
from akeyless.config import AkeylessClientConfig
from akeyless.crypto import CryptoAlgorithm


@six.add_metaclass(abc.ABCMeta)
class AkeylessClientI(object):

    def __init__(self, config):
        # type: (AkeylessClientConfig) -> None
        self.config = config
        self.api = AkeylessApi(self.config)
        self.auth = ApiKeyAuthenticator(self.api, config.access_id, config.prv_key_seed)
        self.cr = CredsRenewal(self.auth)
        self.key_ops_cache = KeyOperationsCredsCache(self.api, self.cr)

    @abc.abstractmethod
    def create_aes_key(self, key_name, alg, metadata, split_level):
        # type: (str, CryptoAlgorithm, str, int) -> None
        """Creates a new AES key.

        :param str key_name: The key name to be created (required)
        :param CryptoAlgorithm alg: The algorithm for the key to be created. Types available are: [AES128GCM,
                                    AES256GCM, AES128SIV, AES256SIV] (required)
        :param str metadata: Metadata about the key. (required)
        :param int split_level: The splitting level represent the number of fragments that the key will be
                                split into. (required)
        """

    @abc.abstractmethod
    def update_key(self, key_name, new_key_name, metadata):
        # type: (str, str, str) -> None
        """Updating name and metadata of an existing key in the account

        :param str key_name: Key name. (required)
        :param str new_key_name: The new key name that will replace the existing one (required)
        :param str metadata: Metadata about the key.
        """
    @abc.abstractmethod
    def create_secret(self, secret_name, secret_val, metadata, protection_key=None):
        # type: (str, str, str, str) -> None
        """Creates a new secret.

        :param str secret_name: The secret name to be created (required)
        :param str secret_val: The value of the secret to be created (required)
        :param str metadata: Metadata about the secret. (required)
        :param str protection_key: The name of a key that used to encrypt the secret value (if empty,
                                   the account default protection key will be used)
        """

    @abc.abstractmethod
    def get_secret_value(self, secret_name):
        # type: (str) -> str
        """return secret value.

        :param str secret_name: The secret name to be created (required)
        :return: The secret value in plaintext
        :rtype: srt
        """

    @abc.abstractmethod
    def update_secret(self, secret_name, new_secret_name, metadata):
        # type: (str, str, str) -> None
        """Updating name and metadata of an existing secret in the account

        :param str secret_name: Secret name. (required)
        :param str new_secret_name: The new secret name that will replace the existing one (required)
        :param str metadata: Metadata about the secret.
        """

    @abc.abstractmethod
    def update_secret_value(self, secret_name, new_secret_val, protection_key=""):
        # type: (str, str, str) -> None
        """Update secret value.

        :param str secret_name: The secret name to be created (required)
        :param str new_secret_val: The new value of the secret to be updated (required)
        :param str protection_key: The name of a key that used to encrypt the secret value (if empty,
                                    the account default protection key will be used)
        """

    @abc.abstractmethod
    def delete_item(self, item_name):
        # type: (str) -> None
        """Deleting an existing item (key or secret) from the account

        :param str item_name: The name of the item (key or secret) to be deleted. (required)
        """

    @abc.abstractmethod
    def encrypt_string(self, key_name, plaintext):
        # type: (str, str) -> str
        """Encrypts plaintext into ciphertext by using an AES key.

        :param str key_name: The name of the key to use in the encryption process (required)
        :param str plaintext: Data to be encrypted (required)
        :return: The encrypted data in base64 encoding.
        :rtype: str
        """

    @abc.abstractmethod
    def decrypt_string(self, key_name, ciphertext):
        # type: (str, str) -> str
        """Decrypts ciphertext into plaintext by using an AES key.

        :param str key_name: The name of the key to use in the decryption process (required)
        :param str ciphertext: Cipher to be decrypted in base64 encoding (required)
        :return: The decrypted data.
        :rtype: str
        """

    @abc.abstractmethod
    def encrypt_data(self, key_name, plaintext, associated_data=b""):
        # type: (str, bytes, bytes) -> bytes
        """Encrypts plaintext into ciphertext by using an AES key.

        :param str key_name: The name of the key to use in the encryption process (required)
        :param bytes plaintext: Data to be encrypted (required)
        :param bytes associated_data: Additional authenticated data (AAD) is any string that specifies the encryption
                                      context to be used for authenticated encryption. If used here, the same value must
                                      be supplied to the decrypt command or decryption will fail. (optional)
        :return: The encrypted data in bytes.
        :rtype: bytes
        """

    @abc.abstractmethod
    def decrypt_data(self, key_name, ciphertext, associated_data=b""):
        # type: (str, bytes, bytes) -> bytes
        """Decrypts ciphertext into plaintext by using an AES key.

        :param str key_name: The name of the key to use in the decryption process (required)
        :param bytes ciphertext: Cipher to be decrypted (required)
        :param bytes associated_data: The Additional authenticated data. If this was specified in the encrypt process,
                                      it must be specified in the decrypt process or the decryption operation will
                                      fail. (optional)
        :return: The decrypted data.
        :rtype: bytes
        """

    @abc.abstractmethod
    def describe_item(self, item_name):
        # type: (str) -> GetItemReplyObj
        """Return item details (key or secret).

        :param str item_name: Item name (required)
        :return: The item details.
        :rtype: GetItemReplyObj
        """

    @abc.abstractmethod
    def list_items(self, item_types):
        # type: (list) -> ListItemsReplyObj
        """Return a list of all the items associated with the client.

        :param list item_types: A list with the type names of the items requested. In case it is None or empty, all
                                the items will be returned.
        :return: A list of all the items associated with the client.
        :rtype: ListItemsReplyObj
        """

    @abc.abstractmethod
    def list_items_in_path(self, path, includes_folders=True, item_types=None):
        # type: (str, bool, list) -> ListItemsInPathReplyObj
        """Return a list of all the items associated with the client.

        :param str path: The path from which the list of the items and folders is returned (required)
        :param bool includes_folders: Include in the list the folders in the requested path
        :param list item_types: A list with the type names of the items requested. In case it is None or empty, all
                                the items will be returned.
        :return: A list of all the items associated with the client.
        :rtype: ListItemsInPathReplyObj
        """

    def close(self):
        self.api.close()
