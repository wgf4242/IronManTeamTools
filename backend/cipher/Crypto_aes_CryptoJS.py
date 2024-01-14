# https://blog.51cto.com/lang13002/6723766
import base64
from hashlib import md5

from Crypto.Cipher import AES
from Crypto import Random
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


def encrypt(data, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    cipherbyte = base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(data)))
    return cipherbyte


def decrypt(data, passphrase):
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    plainbyte = unpad(aes.decrypt(data[16:]))
    plain = clean(plainbyte)
    return plain


def decrypt_batch(data, file):
    from cipher.utils import longest_continuous_printable
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]

    with open(f'wordlists/{file}', 'rb') as f:
        words = f.read().splitlines()
        for passphrase in words:
            key_iv = bytes_to_key(passphrase, salt, 32 + 16)
            key = key_iv[:32]
            iv = key_iv[32:]

            aes = AES.new(key, AES.MODE_CBC, iv)
            try:
                plainbyte = unpad(aes.decrypt(data[16:]))
                if plainbyte and printable(plainbyte):
                    return clean(plainbyte) + ', key: ' + passphrase.decode()
            except:
                ...
    return ''


if __name__ == '__main__':
    data = b'123456'
    passphrase = b'0123456789asdfgh'

    # encrypt_data = encrypt(data, passphrase)
    # print('encrypt_data:', encrypt_data)

    encrypt_data = b"U2FsdGVkX18hyuQnNnZyAe7emBZrUR/YGmy90QN1DI4="

    decrypt_data = decrypt(encrypt_data, passphrase)
    assert decrypt_data == data

    decrypt_data = decrypt(b'U2FsdGVkX1/n7WFLXVdK4ajNfidyvxPe3em7alLKl1k=', b'12345678')
    assert decrypt_data == b'12345678'
