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
def count_not_printable(text:bytes):
    return sum(1 for x in text if chr(x) not in string.printable)
