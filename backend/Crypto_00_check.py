import base64
import unittest


# 装饰器: 装饰函数处理异常, str in 自动转encode, str out 自动 decode
def dec(func):
    def trim(msg):
        return msg.strip(b'\t').strip(b' ')

    def inner(*args, **kwargs):
        try:
            txt, *lst = list(args)
            if not txt:
                return
            if type(txt) != bytes:
                txt = txt.encode()
            txt = trim(txt)
            res = func(txt, **kwargs)
            if isinstance(res, bytes):
                return res.decode('utf8', errors='ignore')
            return res
        except:
            r = f'---- {func.__name__} failed ----'
            print(r)
            return r

    return inner


@dec
def utf7_d(txt):
    r = txt.decode('utf7')
    print('utf7 is \t\t' + r)
    return r


@dec
def fence_d(txt):
    from itertools import zip_longest
    import math
    txt = txt.decode()
    lst = []
    for length in range(2, 7):
        step = math.ceil(len(txt) / length)
        x2lst = [txt[i:i + step] for i in range(0, len(txt), step)]
        r = ''.join(''.join(filter(None, lst)) for lst in zip_longest(*x2lst))
        lst.append(r)
    return '\n'.join(lst)


@dec
def atbash_d(txt):
    transform = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba")
    return str.translate(txt.decode(), transform)


@dec
def base64_d(txt):
    r = base64.b64decode(txt)
    print('base64 is \t\t' + r.decode('utf8', errors='ignore'))
    return r


@dec
def base64_d_rev(txt):
    r = base64.b64decode(txt[::-1] + b'=====')
    print('base64 is \t\t' + r.decode('utf8', errors='ignore'))
    return r


@dec
def base64_en(txt):
    data = bytearray().fromhex(txt.decode())
    en = base64.b64encode(data)
    return en


@dec
def base64_d_itoa(b: bytes):
    _b64alphabet = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    _b64alphabet_itoa = b'./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz='
    tab = bytes.maketrans(_b64alphabet_itoa, _b64alphabet)
    res = b.translate(tab)
    return base64.b64decode(res)


@dec
def base85_d(txt):
    # base64._b85alphabet = b"""!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstu"""
    return base64.a85decode(txt)


@dec
def base85_bd(txt):
    # base64._b85alphabet = b"""!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstu"""
    return base64.b85decode(txt)


@dec
def base45_d(txt):
    import base45
    return base45.b45decode(txt)


@dec
def base58_d(txt):
    import base58
    return base58.b58decode(txt)


@dec
def base32_d(txt):
    txt = txt + len(txt) % 8 * b'='
    return base64.b32decode(txt)


@dec
def base16_d(txt):
    return base64.b16decode(txt)


@dec
def bublble_d(txt):
    from bubblepy import BubbleBabble
    bb = BubbleBabble()
    return bb.decode(txt.decode())


@dec
def rot5_d(txt):
    rot5 = str.maketrans(
        '0123456789',
        '5678901234')
    return txt.decode().translate(rot5)


@dec
def rot13_d(txt):
    import codecs
    return codecs.encode(txt.decode(), 'rot_13')


@dec
def rot13_bf_d(txt):
    from cipher.rot_13_bruteforce import rot13_decrypt

    lst = []
    for i in range(26):
        res = rot13_decrypt(txt.decode(), i)
        lst.append(res)
    return '\n'.join(lst)


@dec
def rot47_d(txt):
    s = txt.decode()
    x = []
    for i in range(len(s)):
        j = ord(s[i])
        if j >= 33 and j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(s[i])
    return ''.join(x)


@dec
def rot18_d(txt):
    ROT18 = str.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz0123456789",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm5678901234",
    )
    return txt.decode().translate(ROT18)


@dec
def base62_d(txt):
    import os
    stdout = os.popen(f"node Crypto_base62.js {txt.decode()}").read()  # 执行并输出命令的执行结果
    return stdout.strip('\n')


@dec
def xxencode_d(txt):
    import os
    stdout = os.popen(f'''node -e "const xxencode = require('./Crypto_xxencode');console.log(xxencode.decode('{txt.decode()}'))"''').read()  # 执行并输出命令的执行结果
    return stdout.strip('\n')


@dec
def base91_d(txt):
    import base91
    return base91.decode(txt.decode('utf8')).decode('utf8')


@dec
def reverse_hex_d(txt):
    rev = txt.decode().replace(' ', '')
    return bytes.fromhex(rev[::-1])


@dec
def base92_d(txt):
    def base92_encode(bytstr):
        if not bytstr:
            return '~'
        bitstr = ''
        while len(bitstr) < 13 and bytstr:
            bitstr += '{:08b}'.format(ord(bytstr[0]))
            bytstr = bytstr[1:]
        resstr = ''
        while len(bitstr) > 13 or bytstr:
            i = int(bitstr[:13], 2)
            resstr += base92_chr(i // 91)
            resstr += base92_chr(i % 91)
            bitstr = bitstr[13:]
            while len(bitstr) < 13 and bytstr:
                bitstr += '{:08b}'.format(ord(bytstr[0]))
                bytstr = bytstr[1:]
        if bitstr:
            if len(bitstr) < 7:
                bitstr += '0' * (6 - len(bitstr))
                resstr += base92_chr(int(bitstr, 2))
            else:
                bitstr += '0' * (13 - len(bitstr))
                i = int(bitstr, 2)
                resstr += base92_chr(i // 91)
                resstr += base92_chr(i % 91)
        return resstr

    def base92_chr(val):
        if val < 0 or val >= 91:
            raise ValueError('val must be in [0, 91)')
        if val == 0:
            return '!'
        elif val <= 61:
            return chr(ord('#') + val - 1)
        else:
            return chr(ord('a') + val - 62)

    def base92_ord(val):
        num = ord(val)
        if val == '!':
            return 0
        elif ord('#') <= num and num <= ord('_'):
            return num - ord('#') + 1
        elif ord('a') <= num and num <= ord('}'):
            return num - ord('a') + 62
        else:
            raise ValueError('val is not a base92 character')

    def base92_decode(bstr):
        bitstr = ''
        resstr = ''
        if bstr == '~':
            return ''
        # we always have pairs of characters
        for i in range(len(bstr) // 2):
            x = base92_ord(bstr[2 * i]) * 91 + base92_ord(bstr[2 * i + 1])
            bitstr += '{:013b}'.format(x)
            while 8 <= len(bitstr):
                resstr += chr(int(bitstr[0:8], 2))
                bitstr = bitstr[8:]
        # if we have an extra char, check for extras
        if len(bstr) % 2 == 1:
            x = base92_ord(bstr[-1])
            bitstr += '{:06b}'.format(x)
            while 8 <= len(bitstr):
                resstr += chr(int(bitstr[0:8], 2))
                bitstr = bitstr[8:]
        return resstr

    return base92_decode(txt.decode())


@dec
def base100_d(txt):
    import pybase100 as pb
    return pb.decode(txt)


@dec
def rail_fences_d(txt):
    from cipher.Crypto_railFence import decryptRailFence
    lst = []
    for i in range(1, 10):
        r = decryptRailFence(txt.decode(), i, 0)
        lst.append(r)
    return '\n'.join(lst)


@dec
def z_caesar_box_d(txt):
    from itertools import zip_longest
    def caesar_box_cipher(data, n):
        chunks = [data[i:i + n] for i in range(0, len(data), n)]
        transposed = list(map(''.join, zip_longest(*chunks, fillvalue='')))
        return ''.join(transposed)

    res = []
    for i in range(1, 36):
        res.append(caesar_box_cipher(txt.decode(), i))
    return '\n'.join(res)


class __Test(unittest.TestCase):
    def test_base85(self):
        self.assertEqual(base85_d(b'Ao(mgHY?i2ARAkQB5_^!?Y!Sj0ms'), 'flag{have_a_good_day1}')
        self.assertEqual(base85_d(b'Ao(mgHX^E)ARAnTF(J]f@<6".'), 'flag{base_base_base}')


if __name__ == "__main__":
    txt = 'MTIzNA=='
    unittest.main()
    # utf7(txt)
    # base64(txt)
