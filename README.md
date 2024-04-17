# Vault Sample for Python

This repository contains sample code written for [blog post](https://kciter.so/posts/encrypted-vault-system).

## Usage

```console
$ python main.py -a
Enter master password: 
Enter item name: Google
Enter password: 
Entry Google added

$ python main.py -l
* Google

$ python main.py -q Google
Enter master password:
Password for Google: password # Your password

$ python main.py -u Google
Enter master password:
Enter new password:
Entry Google updated

$ python main.py -d Google
Entry Google deleted
```
