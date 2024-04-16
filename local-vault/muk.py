import base64
from hash import hash_password, hash_sha256
from random_key import generate_random_key, keychain_get_password, keychain_store_password


def xor_two_str(a: str, b: str) -> str:
    a = base64.b64decode(a)
    b = base64.b64decode(b)
    return base64.b64encode(bytes([x ^ y for x, y in zip(a, b)])).decode('utf-8')

def generate_master_unlock_key(master_password: str) -> str:
    hashed_master_password = hash_password(master_password, "salt")

    if not keychain_get_password("local-vault", "manager"):
        keychain_store_password("local-vault", "manager", generate_random_key())

    random_secret_key = keychain_get_password("local-vault", "manager")
    hashed_random_secret_key = hash_sha256(random_secret_key)

    return xor_two_str(hashed_master_password, hashed_random_secret_key)


if __name__ == "__main__":
    print(generate_master_unlock_key("master_password")) # ... 42 length string
