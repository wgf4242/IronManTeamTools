# https://github.com/Robin-Pwner/Rabbit-Cipher
# Cyberchef rabbit也试试
# CryptoJS 3.0.2 版本的 rabit和后面的版本不一样, 84行是唯一区别
from hashlib import md5
import base64
import struct
from Crypto.Util.Padding import unpad as pkcs7unpad

from cipher.utils import count_not_printable, longest_continuous_printable, clean, printable

ROTL = lambda x, n: ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)


def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode()


def unpad(s):
    return pkcs7unpad(s, 16)


def ROTL8(v, n):
    return (((v << n) & 0xff) | ((v >> (8 - n)) & 0xff))


def ROTL16(v, n):
    return (((v << n) & 0xffff) | ((v >> (16 - n)) & 0xffff))


def ROTL32(v, n):
    return (((v << n) & 0xffffffff) | ((v >> (32 - n)) & 0xffffffff))


def ROTL64(v, n):
    return (((v << n) & 0xffffffffffffffff) | ((v >> (64 - n)) & 0xffffffffffffffff))


def ROTR8(v, n):
    return ROTL(v, 8 - n)


def ROTR16(v, n):
    return ROTL(v, 16 - n)


def ROTR32(v, n):
    return ROTL(v, 32 - n)


def ROTR64(v, n):
    return ROTL(v, 64 - n)


def SWAP32(v):
    return ((ROTL32(v, 8) & 0x00ff00ff) | (ROTL32(v, 24) & 0xff00ff00))


class Rabbit_state(object):
    def __init__(self):
        self.x = [0] * 8
        self.c = [0] * 8
        self.carry = 0


class Rabbit_ctx(object):
    def __init__(self):
        self.m = Rabbit_state()
        self.w = Rabbit_state()


class Rabbit(object):
    def __init__(self, key, iv):
        self.ctx = Rabbit_ctx()
        self.set_key(key)
        if (len(iv)):
            self.set_iv(iv)

    def g_func(self, x):
        x = x & 0xffffffff
        x = (x * x) & 0xffffffffffffffff
        result = (x >> 32) ^ (x & 0xffffffff)
        return result

    def set_key(self, key: bytes):
        # K0, K1, K2, K3 = struct.unpack('<4I', key) # 正常这里是小端的， 3.0.2是大端的
        # generate four subkeys
        K0, K1, K2, K3 = struct.unpack('>4I', key)
        s = self.ctx.m
        # generate initial state variables
        s.x = [
            K0, ((K3 << 16) & 0xffffffff) | ((K2 >> 16) & 0xffff),
            K1, ((K0 << 16) & 0xffffffff) | ((K3 >> 16) & 0xffff),
            K2, ((K1 << 16) & 0xffffffff) | ((K0 >> 16) & 0xffff),
            K3, ((K2 << 16) & 0xffffffff) | ((K1 >> 16) & 0xffff)
        ]
        # generate initial counter values
        s.c[0] = ROTL32(K2, 16)
        s.c[2] = ROTL32(K3, 16)
        s.c[4] = ROTL32(K0, 16)
        s.c[6] = ROTL32(K1, 16)
        s.c[1] = (K0 & 0xffff0000) | (K1 & 0xffff)
        s.c[3] = (K1 & 0xffff0000) | (K2 & 0xffff)
        s.c[5] = (K2 & 0xffff0000) | (K3 & 0xffff)
        s.c[7] = (K3 & 0xffff0000) | (K0 & 0xffff)
        s.carry = 0

        # Iterate system four times
        for i in range(4):
            self.next_state(self.ctx.m)

        for i in range(8):
            # modify the counters
            self.ctx.m.c[i] ^= self.ctx.m.x[(i + 4) & 7]

        # Copy master instance to work instance
        self.ctx.w = self.copy_state(self.ctx.m)

    def copy_state(self, state):
        n = Rabbit_state()
        n.carry = state.carry

        for i, j in enumerate(state.x):
            n.x[i] = j
        for i, j in enumerate(state.c):
            n.c[i] = j
        return n

    def set_iv(self, iv: bytes):
        # generate four subvectors
        v = [0] * 4
        v[0], v[2] = struct.unpack('<2I', iv)
        v[1] = (v[0] >> 16) | (v[2] & 0xffff0000)
        v[3] = ((v[2] << 16) | (v[0] & 0x0000ffff)) & 0xffffffff
        # Modify work's counter values
        for i in range(8):
            self.ctx.w.c[i] = self.ctx.m.c[i] ^ v[i & 3]
        # Copy state variables but not carry flag
        tmp = []

        for cc in self.ctx.m.x:
            tmp += [cc]
        self.ctx.w.x = tmp

        # Iterate system four times
        for i in range(4):
            self.next_state(self.ctx.w)

    def next_state(self, state):
        g = [0] * 8
        x = [0x4D34D34D, 0xD34D34D3, 0x34D34D34]
        # calculate new counter values
        for i in range(8):
            tmp = state.c[i]
            state.c[i] = (state.c[i] + x[i % 3] + state.carry) & 0xffffffff
            state.carry = (state.c[i] < tmp)
        # calculate the g-values
        for i in range(8):
            g[i] = self.g_func(state.x[i] + state.c[i])
        # calculate new state values

        j = 7
        i = 0
        while (i < 8):
            state.x[i] = (g[i] + ROTL32(g[j], 16) +
                          ROTL32(g[j - 1], 16)) & 0xffffffff
            i += 1
            j += 1
            state.x[i] = (g[i] + ROTL32(g[j & 7], 8) + g[j - 1]) & 0xffffffff
            i += 1
            j += 1
            j &= 7

    def decrypt(self, msg):
        plain = b""
        l = len(msg)
        c = self.ctx
        x = [0] * 4
        start = 0
        while (True):
            self.next_state(c.w)
            for i in range(4):
                x[i] = c.w.x[i << 1]
            x[0] ^= (c.w.x[5] >> 16) ^ (c.w.x[3] << 16)
            x[1] ^= (c.w.x[7] >> 16) ^ (c.w.x[5] << 16)
            x[2] ^= (c.w.x[1] >> 16) ^ (c.w.x[7] << 16)
            x[3] ^= (c.w.x[3] >> 16) ^ (c.w.x[1] << 16)
            b = [0] * 16
            for i, j in enumerate(x):
                for z in range(4):
                    b[z + 4 * i] = 0xff & (j >> (8 * z))
            for i in range(16):
                plain += bytes([(msg[start]) ^ b[i]])
                start += 1
                if (start == l):
                    return plain


def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


def dec(data, passphrase):
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:16]
    iv = key_iv[16:16 + 8]
    return key, iv, data[16:]


def decrypt_batch(data, file):
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]

    lst = []
    with open(f'wordlists/{file}', 'rb') as f:
        words = f.read().splitlines()
        for passphrase in words:
            key_iv = bytes_to_key(passphrase, salt, 32 + 16)
            key = key_iv[:16]
            iv = key_iv[16:16 + 8]

            cipher = Rabbit(key, iv)
            plainbyte = cipher.decrypt(data[16:])
            if plainbyte and printable(plainbyte):
                return clean(plainbyte) + ', key: ' + passphrase.decode()
            # if plainbyte and longest_continuous_printable(plainbyte) > 5 and count_not_printable(plainbyte) < 8:
            #     tmp = plainbyte + b'  , key: ' + passphrase
            #     return tmp
                # lst.append(tmp)
        # return b'\n'.join(lst)
    return ''


def decrypt(data, passphrase):
    data = base64.b64decode(data)
    assert data[:8] == b'Salted__'
    salt = data[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:16]
    iv = key_iv[16:16 + 8]
    cipher = Rabbit(key, iv)
    plainbyte = cipher.decrypt(data[16:])
    return plainbyte


if __name__ == '__main__':
    # msg = decrypt(b'U2FsdGVkX18HEuPc1ObV849yaR+NB7pEUTnCfst0S1E=', b'12345678')
    # assert msg == b'1234567812345678'
    msg = decrypt(b'U2FsdGVkX18hXTEdmaHlK9Wa0JuJu4UApkMzMe69xXg8yBK0Fw5q4HtQ5+qK6BCB+WkHQDiIxks=', b'2014')
    assert msg == b'flag{Hold_high_the_banner_of _socialism}'
