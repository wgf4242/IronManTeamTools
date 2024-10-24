

def main(cipher):
    my_base64chars = "4103"
    STD_BASE64CHARS = "aloe"
    cipher = cipher.translate(str.maketrans(my_base64chars, STD_BASE64CHARS))
    cipher1 = cipher.translate(str.maketrans(STD_BASE64CHARS, my_base64chars))

    # from itertools import product
    # dic = {
    #     'i': ('1'),
    #     'l': ('1'),
    #     'o': ('0'),
    #     'e': ('3', '4')
    #     # 'e': ('e', '3', '4')
    # }
    # r1 =[dic.get(x, x) for x in cipher]
    # for tp in product(*r1):
    #     print(''.join(tp))

    return cipher + ',' + cipher1


# base64.urlsafe_b64decode(input + '==') # 补=解码更安全

if __name__ == '__main__':
    cipher = 'M41b0lg3'
    res = main(cipher)
    # assert res == 'Malbolge'
    print(res)

    cipher = 'SYC{Steg_4nd_Zip_1s_G00d!}'
    print(main(cipher))
