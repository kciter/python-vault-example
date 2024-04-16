import base64
import hashlib
from Crypto.Protocol.KDF import PBKDF2


def hash_password(password: str, salt: str) -> str:
    return base64.b64encode(PBKDF2(password, salt, dkLen=48, count=100000)).decode('utf-8')

def hash_sha256(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == "__main__":
    print(hash_password("password", "salt"))
    print(hash_sha256("password"))
