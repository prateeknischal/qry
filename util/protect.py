import pathlib
import base64
import os

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def file_to_bytes(filename):
    fp = pathlib.Path(filename)
    if not fp.is_file():
        print ("The file {} does not exist !!".format(filename))
        return 1

    img = []
    with open(filename, "rb") as f:
        img = f.read()

    return img

def protect(plain, password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 100000,
        backend = default_backend()
    )

    cipher = Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
    token = cipher.encrypt(plain)

    return salt, token

def access(salt, token, password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 100000,
        backend = default_backend()
    )

    cipher = Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
    plain = cipher.decrypt(token)

    return plain
