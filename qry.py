import subprocess as bash
import sys
import errno
import os
import json
import base64
import pathlib

from getpass import getpass
from argparse import ArgumentParser
from urllib.parse import parse_qs, urlparse, unquote
from util import protect, totp

def _parse_qrcode(qrcode_file):
    """This function uses the binary "zbarimg" to parse the QR code from the
    provided file as an argument and returns the secret key from the QR code.

    Arguments:
        qrcode_file (str): path to the QR Code PNG image file

    Returns:
        tuple (str, int): returns a tuple with the secret and any error codes, If
        the error code is fatal then the str part will be None."""

    f = pathlib.Path(qrcode_file)
    if not f.is_file():
        print ("file {} does not exist".format(qrcode_file))
        return None, errno.ENOENT

    resp = bash.run(["zbarimg", "-q", qrcode_file], stdout=bash.PIPE)

    if resp.returncode != 0:
        print ("zbarimg failed to parse the {}".format(qrcode_file))
        return None, returncode

    otpauth_url = unquote(str(resp.stdout))
    query_params = parse_qs(urlparse(otpauth_url).query)

    return query_params["secret"][0], 0

def register(qrcode_file, qry_file="qry.json"):
    """This function registers a QR Code by extracting the secret, encrypting it
    and writing it to a config file "qry_file" which defaults to "qry.json" in
    the current directory

    Arguments:
        qrcode_file (str): path to the QR Code PNG image file
        qry_file (str): path where to write the config

    Returns:
        int: returns an error code value, 0 if no errors"""

    key, err = _parse_qrcode(qrcode_file)
    if err:
        print ("Failed to register, error code:", err)
        return err

    p = getpass("Input password for the seed: ")
    salt, token = protect.protect(str.encode(key), str.encode(p))
    mp = {}
    mp["alg"] = "cryptography.Fernet"
    mp["key"] = base64.b64encode(token).decode("utf-8")
    mp["salt"] = base64.b64encode(salt).decode("utf-8")

    print (mp)

    with open(qry_file, "w") as wp:
        json.dump(mp, wp)

    del mp, salt, token, key
    return 0

def run(qry_file="qry.json"):
    """This function is used to generate the TOTP. It parses the "qry_file" and
    gets the key and salt values, propmts the user for password and decrypts the
    values. Once decrypted successfully, then generates the OTP and returns

    Arguments:
        qry_file (str): path from where to read the config, defaults to "qry.json"
            in the current directory

    Returns:
        str: The OTP as a string"""

    f = pathlib.Path(qry_file)
    if not f.exists():
        print ("file {} does not exist".format(qrcode_file))
        return None, errno.ENOENT

    mp = {}
    with open(qry_file, "r") as rp:
        mp = json.load(rp)

    if mp["alg"] != "cryptography.Fernet":
        raise NotImplementedError("Encryption algorithm {} is not supported".format(mp["alg"]))

    p = getpass("Input password for the qry file: ")
    key = protect.access(base64.b64decode(mp["salt"]), base64.b64decode(mp["key"]), str.encode(p))

    token = totp.otp(key)

    del p, key, mp

    return token


if __name__ == '__main__':
    p = ArgumentParser(prog="QRy - TOTP generator")
    subparsers = p.add_subparsers(help="operations", dest="cmd")

    reg_p = subparsers.add_parser("reg")
    reg_p.add_argument("-c", "--config", dest="r_config", default="qry.json")
    reg_p.add_argument("-f", "--qrcode", dest="r_qrcode", default="qrcode.png")

    reg_o = subparsers.add_parser("gen")
    reg_o.add_argument("-c", "--config", dest="g_config", default="qry.json")

    args = p.parse_args(sys.argv[1:])

    if args.cmd == "reg":
        err = register(args.r_qrcode, args.r_config)
        print ("Registration successfull !!" if err == 0 else "Registration failed")
    else:
        print (run(args.g_config))
