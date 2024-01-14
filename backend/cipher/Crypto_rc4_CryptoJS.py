# https://blog.51cto.com/lang13002/6723766
import base64
from hashlib import md5
from Crypto.Cipher import ARC4

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad as pkcs7unpad

from cipher.utils import clean, printable


def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode()


def unpad(s):
    return pkcs7unpad(s, 16)


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
    key_iv = bytes_to_key(passphrase, salt, 32)
    key = key_iv[:32]

    cipher = ARC4.new(key)
    plainbyte = cipher.decrypt(data[16:])

    plain = clean(plainbyte)
    return plain


def decrypt_batch(data, file):
    data = base64.b64decode(data)
    salt = data[8:16]

    lst = []

    with open(f'wordlists/{file}', 'rb') as f:
        words = f.read().splitlines()
        for passphrase in words:
            key_iv = bytes_to_key(passphrase, salt, 32)
            key = key_iv[:32]

            try:
                cipher = ARC4.new(key)
                plainbyte= cipher.decrypt(data[16:])

                if plainbyte and printable(plainbyte):
                    # res = plainbyte + ', key: ' + passphrase.decode()
                    # lst.append(res)
                    return clean(plainbyte) + ', key: ' + passphrase.decode()
            except:
                ...
    return ''


if __name__ == '__main__':
    data = '12345678'
    passphrase = b'1234'

    # encrypt_data = encrypt(data, passphrase)
    # print('encrypt_data:', encrypt_data)

    encrypt_data = b"U2FsdGVkX19LT8ubEiyf6f7JBmN4IiNG"

    decrypt_data = decrypt(encrypt_data, passphrase)
    assert decrypt_data == data

    decrypt_batch(encrypt_data, r"../../wordlists/pass.txt")
