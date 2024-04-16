import os
import getpass
import argparse
import json
from muk import generate_master_unlock_key
from aes import AESCipher


class App:
    def setup(self):
        master_password = getpass.getpass("Enter master password: ")
        self.muk = generate_master_unlock_key(master_password)
        self.aes = AESCipher(self.muk)

    def add(self):
        name = input("Enter item name: ")
        password = getpass.getpass("Enter password: ")
        cipher, iv = self.aes.encrypt(password)

        ## Read from file as JSON
        if os.path.isfile("vault.json") == False:
            data = {}
        else:
            file = open("vault.json", "r")
            data = json.load(file)
            file.close()

        ## Update JSON
        data[name] = {"cipher": cipher, "iv": iv}

        ## Save to file as JSON
        file = open("vault.json", "w")
        json.dump(data, file)
        file.close()

        print(f"Entry {name} added")

    def list(self):
        if os.path.isfile("vault.json") == False:
            print("No entries found")
            return

        file = open("vault.json", "r")
        data = json.load(file)
        file.close()

        for entry in data:
            print(f"* {entry}")

    def query(self, name):
        if os.path.isfile("vault.json") == False:
            print("No entries found")
            return

        file = open("vault.json", "r")
        data = json.load(file)
        file.close()

        if name in data:
            cipher = data[name]["cipher"]
            iv = data[name]["iv"]
            password = self.aes.decrypt(cipher, iv)
            print(f"Password for {name}: {password}")
        else:
            print("Entry not found")

    def delete(self, name):
        if os.path.isfile("vault.json") == False:
            print("No entries found")
            return

        file = open("vault.json", "r")
        data = json.load(file)
        file.close()

        if name in data:
            del data[name]

            file = open("vault.json", "w")
            json.dump(data, file)
            file.close()

            print(f"Entry {name} deleted")
        else:
            print("Entry not found")

    def update(self, name):
        if os.path.isfile("vault.json") == False:
            print("No entries found")
            return

        file = open("vault.json", "r")
        data = json.load(file)
        file.close()

        if name in data:
            password = getpass.getpass("Enter new password: ")
            cipher, iv = self.aes.encrypt(password)
            data[name] = {"cipher": cipher, "iv": iv}

            file = open("vault.json", "w")
            json.dump(data, file)
            file.close()

            print(f"Entry {name} updated")
        else:
            print("Entry not found")

    def run(self):
        parser = argparse.ArgumentParser(description="Vault: Add, Update, Delete and Query Passwords", usage="[options]")

        parser.add_argument("-a", "--add", action="store_true", help="Add new password along with name")
        parser.add_argument("-u", "--update", type=str, nargs=1, help="Update a password by name", metavar=("[name]"))
        parser.add_argument("-d", "--delete", type=str, nargs=1, help="Delete entry by name", metavar=("[name]"))
        parser.add_argument("-q", "--query", type=str, nargs=1, help="Look up password by name", metavar=("[name]"))
        parser.add_argument("-l", "--list", action="store_true", help="List all entries in vault")

        args = parser.parse_args()

        if args.add:
            self.setup()
            self.add()
        elif args.update:
            self.setup()
            self.update(args.update[0])
        elif args.delete:
            self.delete(args.delete[0])
        elif args.query:
            self.setup()
            self.query(args.query[0])
        elif args.list:
            self.list()
        else:
            parser.print_help()


if __name__ == "__main__":
    app = App()
    app.run()
