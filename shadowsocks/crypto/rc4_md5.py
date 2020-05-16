#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import hashlib
from shadowsocks.crypto import openssl

__all__ = ['ciphers']


def create_cipher(alg, key, iv, op, crypto_path=None,
                  key_as_bytes=0, d=None, salt=None,
                  i=1, padding=1):
    md5 = hashlib.md5()
    md5.update(key)
    md5.update(iv)
    rc4_key = md5.digest()
    return openssl.OpenSSLStreamCrypto(b'rc4', rc4_key, b'', op, crypto_path)


ciphers = {
    'rc4-md5': (16, 16, create_cipher),
    'rc4-md5-6': (16, 6, create_cipher),
}


def test():
    from shadowsocks.crypto import util

    cipher = create_cipher('rc4-md5', b'k' * 32, b'i' * 16, 1)
    decipher = create_cipher('rc4-md5', b'k' * 32, b'i' * 16, 0)

    util.run_cipher(cipher, decipher)


if __name__ == '__main__':
    test()
