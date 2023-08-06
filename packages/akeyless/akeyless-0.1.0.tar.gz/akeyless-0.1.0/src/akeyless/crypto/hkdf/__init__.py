from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend


class HKDFHandler(object):

    def __init__(self, key):
        # type: (bytes) -> None
        self.key = key

    def derive(self, info, alg=hashes.SHA256(), length=32, salt=bytes()):
        return HKDF(
            algorithm=alg,
            info=info,
            length=length,
            salt=salt,
            backend=default_backend()
        ).derive(self.key)
