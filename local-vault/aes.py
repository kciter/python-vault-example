import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCipher(object):
    def __init__(self, key: str):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message: str) -> str:
        message = message.encode()
        raw = pad(message, AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC)
        enc = cipher.encrypt(raw)

        ciphertext = base64.b64encode(enc).decode('utf-8')
        iv = base64.b64encode(cipher.iv).decode('utf-8')

        return ciphertext, iv

    def decrypt(self, enc: str, iv: str) -> str:
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, base64.b64decode(iv))
        dec = cipher.decrypt(enc)
        return unpad(dec, AES.block_size).decode('utf-8')


if __name__ == "__main__":
    aes = AESCipher("key")
    encrypted, iv = aes.encrypt("password")
    print(encrypted)
    decrypted = aes.decrypt(encrypted, iv)
    print(decrypted)
