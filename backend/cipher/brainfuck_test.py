from .brainfuck import evaluate_bf


def trans(data):
    import re
    data = re.sub('[^\.?!]+', '', data)
    dic = {'.?': '>', '?.': '<', '..': '+', '!!': '-', '!.': '.', '.!': ',', '!?': '[', '?!': ']'}
    output = ''
    for i in range(0, len(data), 2):
        output += dic[data[i] + data[i + 1]]
    return output
def evaluate(code):
    code1 = trans(code.replace(' ', ''))
    return evaluate_bf(code1)


if __name__ == '__main__':
    src = """++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++.>+.+++++++..+++."""
    res = evaluate_bf(src)
    assert res == 'Hello'

    src = """..... ..... ..... ..... !?!!. ?.... ..... ..... ..... .?.?! .?... .!... ..... ..... !.?.. ....."""
    res = evaluate(src)
    print(res)
    assert res == 'fl'
