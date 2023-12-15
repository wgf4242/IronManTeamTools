import collections

import wordninja


def word_count(content: str):
    txt = content.replace('cryptosystem', 'crypto system')
    lst = wordninja.split(txt)

    counter1 = collections.Counter(lst)
    # print(counter1)
    lst = []
    for i, (word, count) in enumerate(counter1.most_common()[::-1]):
        data = f"{word:20}: {count:5}, {i + 1}"
        # print(f"{word:20}: {count:5}, {i + 1}")
        lst.append(data)
    return '\n'.join(lst)


def char_count(content: str):
    txt = content
    counter1 = collections.Counter(txt)
    lst = []
    for i, (word, count) in enumerate(counter1.most_common()[::-1]):
        data = f"{word:20}: {count:5}, {i + 1}"
        # print(f"{word:20}: {count:5}, {i + 1}")
        lst.append(data)
    return '\n'.join(lst)
