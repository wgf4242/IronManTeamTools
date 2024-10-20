def main(cipher):
    my_base64chars = "4103"
    STD_BASE64CHARS = "aloe"
    cipher = cipher.translate(str.maketrans(my_base64chars, STD_BASE64CHARS))
    cipher1 = cipher.translate(str.maketrans(STD_BASE64CHARS, my_base64chars))
    return cipher + ',' + cipher1


# base64.urlsafe_b64decode(input + '==') # 补=解码更安全

if __name__ == '__main__':
    cipher = 'M41b0lg3'
    res = main(cipher)
    # assert res == 'Malbolge'
    print(res)
