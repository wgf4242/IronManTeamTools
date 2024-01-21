def offset(even, rails, rail):
    if rail == 0 or rail == rails - 1:
        return (rails - 1) * 2

    if even:
        return 2 * rail
    else:
        return 2 * (rails - 1 - rail)


def decryptRailFence(encrypted, rails, showOff=0):
    array = [[" " for col in range(len(encrypted))] for row in range(rails)]
    read = 0

    # build our fence
    for rail in range(rails):
        pos = offset(1, rails, rail)
        even = 0;

        if rail == 0:
            pos = 0
        else:
            pos = int(pos / 2)

        while pos < len(encrypted):
            if read == len(encrypted):
                break

            array[rail][pos] = encrypted[read];
            read = read + 1

            pos = pos + offset(even, rails, rail)
            even = not even

    if showOff:
        # hooray, done! show our handy work
        for row in array:
            print(row)

    # now return the decoded message
    decoded = ""

    for x in range(len(encrypted)):
        for y in range(rails):
            if array[y][x] != " ":
                decoded += array[y][x]

    return decoded


if __name__ == '__main__':
    # (reference: http://en.wikipedia.org/wiki/Rail_Fence_Cipher)
    assert decryptRailFence("WECRLTEERDSOEEFEAOCAIVDEN", 3, 0) == "WEAREDISCOVEREDFLEEATONCE"
    assert decryptRailFence("f{52bgb-281lg00ff-46f7-ca009c8e}a381-b7191", 3, 0) == "flag{0305f8f2-14b6-fg7b-bc7a-010299c881e1}"
    assert decryptRailFence("WWHLIAATTEHSDITETH", 7, 0) == "WHATSTHEDEALWITHIT"
