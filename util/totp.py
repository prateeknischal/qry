#!/usr/bin/python3

import hashlib
import hmac
import struct
import os
import time
import sys
import base64


def _otp(key, counter, hash="SHA1", otp_len=6):
    """This function is used to generate an OTP based on the counter using HMAC,
    The algorithm is defined in RFC4226. The algorithm in general is:
    Steps:
    1. calculate h_bytes = hmac.digest(key, counter, hash_algo)
    2. get offset = last 4 bits of the byte array
    3. get 4 bytes from the 'offset' postion in the byte array
    4. return required number of bytes

    Arguments:
        key (bytes): the key used to perform HMAC, the length depends on the hash being
            used, eg: for SHA-1, key should be atleast 20bytes, for SHA-256 it
            should be atleast 32bytes

        counter (int): the counter value to be used as the data in the hmac

        hash (str): the hash algorithm to be used to compute hmac, by default it's
            SHA-1

        otp_len (int): the length of OTP to be returned, the default value is 6

    Returns:
        str: OTP string of length otp_len"""

    counter = struct.pack(">Q", counter)

    h_bytes = hmac.digest(key , counter, hashlib.sha1)
    offset = h_bytes[-1] & 0xf

    truncated_hash = (h_bytes[offset] & 0x7f) << 24 | \
        (h_bytes[offset + 1] & 0xff) << 16 | \
        (h_bytes[offset + 2] & 0xff) << 8  | \
        (h_bytes[offset + 3] & 0xff)

    return str.rjust(str(truncated_hash % pow(10, otp_len)), otp_len, '0')

def _get_totp_counter(time_step=30):
    """This function returns the counter value based on the time_step, which is
    30 by default. It will return the number of time steps since the Epoch time

    Arguments:
        time_step (int): the size of time_step, default is 30s

    Returns:
        int: the number of steps, which will act as the counter for hotp
    """
    return int(time.time()) // time_step

def _pre_process_key(key):
    """This function takes in the base32 encoded string and returns the bytearray
    key required for the otp function

    Arguments:
        key (bytes): base32 encoded key string

    Returns:
        bytes: byte array representation of the key"""
    key_len = len(key)

    # pad the key
    padding = key_len + (8 - (key_len % 8))

    # make the key of appropriate size with the base32 padding char
    key = key.ljust(padding, b'=')

    return base64.b32decode(key)

def otp(key, hash="SHA1", otp_len=6):
    """OTP wrapper function..
    Arguments:
        key (bytes): The OTP secret
        hash (str) : the HMAC hash algorithm
        otp_len(int) : the length of OTP, defaults to 6

    Returns:
        (str): the OTP of size otp_len"""
        
    key = _pre_process_key(key)
    t = _get_totp_counter()

    return _otp(key, t)
