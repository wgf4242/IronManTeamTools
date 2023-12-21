import re
import string


def longest_continuous_printable(text):
    table = string.punctuation + string.ascii_letters + string.digits
    longest_seq = ""
    current_seq = ""

    for num in text:
        char = chr(num)
        if char in table:
            current_seq += char
        else:
            if len(current_seq) > len(longest_seq):
                longest_seq = current_seq
            current_seq = ""

    # 检查最后的序列是否是最长的
    if len(current_seq) > len(longest_seq):
        longest_seq = current_seq

    return len(longest_seq)


def count_not_printable(text: bytes):
    return sum(1 for x in text if chr(x) not in string.printable)


def clean(text: bytes):
    text1 = re.sub(b'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]+$', b'', text)
    text2 = str(text1)[2:-1]
    return text2


def printable(text):
    return count_not_printable(text) < 1
