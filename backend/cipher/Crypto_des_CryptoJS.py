# https://blog.51cto.com/lang13002/6723766
import base64
from hashlib import md5

from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad, pad
from Crypto import Random
from Crypto.Util.Padding import unpad as pkcs7unpad

from cipher.utils import clean, printable


def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode()


def unpad(s):
    return pkcs7unpad(s, 16)


# def unpad(s):
#     return s[0:-ord(s[len(s) - 1:])]
#

def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


def decrypt(data, passphrase):
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:8]
    iv = key_iv[8:16]

    cipher = DES.new(key, DES.MODE_CBC, iv)
    plainbyte = unpad(cipher.decrypt(data[16:]))
    plain = clean(plainbyte)
    return plain

def decrypt_batch(data, file):
    from cipher.utils import longest_continuous_printable
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]

    with open(f'wordlists/{file}') as f:
        words = f.read().splitlines()
        for passphrase in words:
            passphrase = passphrase.encode()
            key_iv = bytes_to_key(passphrase, salt, 32 + 16)
            key = key_iv[:8]
            iv = key_iv[8:16]

            cipher = DES.new(key, DES.MODE_CBC, iv)
            # try:
            #     plainbyte = unpad(aes.decrypt(data[16:]))
            #     if plainbyte and printable(plainbyte):
            #         return clean(plainbyte) + ', key: ' + passphrase.decode()
            # except:
            #     ...
            try:
                plainbyte = unpad(cipher.decrypt(data[16:]))
                if plainbyte and printable(plainbyte):
                    return clean(plainbyte) + ', key: ' + passphrase.decode()
            except:
                ...
    return ''


if __name__ == '__main__':
    # wordArray = DES.decrypt('U2FsdGVkX1+/hEfItB2ChgHRgcG5Uz0acYzT3mYjA67ZW8XCoAJ96Q==', '12345678');

    decrypt_data = decrypt(b'U2FsdGVkX1+/hEfItB2ChgHRgcG5Uz0acYzT3mYjA67ZW8XCoAJ96Q==', b'12345678')
    assert decrypt_data == b'1234567812345678'

