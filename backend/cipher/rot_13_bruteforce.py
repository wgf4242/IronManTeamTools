def rot13_decrypt(txt, rot_num=13):
    lst = []
    for ch in txt:
        och = ord(ch)
        if ord('0') <= och <= ord('9'):
            och = (och - ord('0') + rot_num) % 10 + ord('0')
        elif ord('a') <= och <= ord('z'):
            och = (och - ord('a') + rot_num) % 26 + ord('a')
        elif ord('A') <= och <= ord('Z'):
            och = (och - ord('a') + rot_num) % 26 + ord('A')
        lst.append(chr(och))
    return ''.join(lst)


print(rot13_decrypt('123'))
