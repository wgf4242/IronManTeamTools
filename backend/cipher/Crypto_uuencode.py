def decode_uuencode(uu_string):
    # 将字符串按行分割，过滤空行
    lines = [line.strip() for line in uu_string.splitlines() if line.strip()]

    # 解码单行
    def uu_decode_line(line):
        if not line:
            return bytearray()
        # 每行第一个字符表示字节数
        count = ord(line[0]) - 32
        if count <= 0:
            return bytearray()

        # 解码后续字符
        decoded = bytearray()
        encoded = line[1:]
        for i in range(0, len(encoded), 4):
            # 每 4 个字符解码为 3 个字节
            group = encoded[i:i + 4]
            if len(group) < 4:
                group = group + ' ' * (4 - len(group))  # 填充空格
            bytes_out = [0] * 3
            for j, char in enumerate(group):
                if 32 <= ord(char) <= 95:
                    val = ord(char) - 32
                else:
                    val = 0  # 处理无效字符
                # 根据 uuencode 解码公式
                if j == 0:
                    bytes_out[0] |= (val & 0x3F) << 2
                elif j == 1:
                    bytes_out[0] |= (val & 0x30) >> 4
                    bytes_out[1] |= (val & 0x0F) << 4
                elif j == 2:
                    bytes_out[1] |= (val & 0x3C) >> 2
                    bytes_out[2] |= (val & 0x03) << 6
                elif j == 3:
                    bytes_out[2] |= (val & 0x3F)
            decoded.extend(bytes_out[:min(count, 3)])
            count -= 3
            if count <= 0:
                break
        return decoded

    # 解码所有行
    result = bytearray()
    for line in lines:
        result.extend(uu_decode_line(line))

    return bytes(result)


if __name__ == '__main__':
    # 测试你的字符串
    uu_string = r'''29FQA9WMT:&ES<&]R='T`'''
    decoded_data = decode_uuencode(uu_string)

    # 打印解码结果（二进制和尝试转文本）
    print("解码后的二进制数据:", decoded_data)
    try:
        print("解码后的文本（UTF-8）:", decoded_data.decode('utf-8'))
    except UnicodeDecodeError:
        print("解码结果不是有效的 UTF-8 文本，可能为二进制数据")
