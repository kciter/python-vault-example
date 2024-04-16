import base64
import subprocess
import os


def generate_random_key() -> bytes:
    return base64.b64encode(os.urandom(32)).decode('utf-8')

def keychain_get_password(service, account):
    command = f"/usr/bin/security find-generic-password -s '{service}' -a '{account}' -g -w"
    result = subprocess.run(command, shell=True, capture_output=True)
    password = result.stdout.decode().strip()
    return password

def keychain_store_password(service, account, password):
    cmd = 'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()


if __name__ == "__main__":
    if not keychain_get_password("local-vault", "manager"):
        print("Password does not exist")
        keychain_store_password("local-vault", "manager", generate_random_key())
        print("Password stored")

    print(keychain_get_password("local-vault", "manager"))
