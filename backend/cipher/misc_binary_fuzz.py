import re


def convert_n_base_to_ascii(n_base_string, base):
    """
    将指定基数的字符串转换为ASCII字符串。

    :param n_base_string: 基数字符串
    :param base: 基数（必须在2到36之间）
    :return: ASCII字符串
    """
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36")

    # 计算每个字符或字符组合的长度
    bits_per_char = (base - 1).bit_length()  # 最多需要多少位来表示一个字符
    if bits_per_char * 8 % (base - 1).bit_length() == 0:
        chars_per_byte = 8 // bits_per_char
    else:
        chars_per_byte = (8 + bits_per_char - 1) // bits_per_char  # 向上取整

    if len(n_base_string) % chars_per_byte != 0:
        raise ValueError("Input string length is not compatible with the specified base")

    result = []
    for i in range(0, len(n_base_string), chars_per_byte):
        # 取出一个字节对应的字符
        segment = n_base_string[i:i + chars_per_byte]
        # 转换为整数
        value = int(segment, base)
        # 转换为ASCII字符
        result.append(chr(value))

    return ''.join(result)


def process_text(binary_data, group_size):
    """
    处理二进制数据，将其转换为指定基数的ASCII字符串。

    :param binary_data: 二进制数据
    :param group_size: 分组大小
    :return: 转换后的ASCII字符串
    """
    # 每group_size个一组检测有几种
    groups = re.findall(rb'.{%d}' % group_size, binary_data)
    if len(set(groups)) != group_size:
        return

    # 将set转换为字典
    unique_groups = dict(enumerate(sorted(set(groups))))
    group_to_index = {v: str(k) for k, v in unique_groups.items()}
    index_string = ''.join(group_to_index[group] for group in groups)

    output = convert_n_base_to_ascii(index_string, 4)
    return output


if __name__ == "__main__":
    # 读取附件文件
    with open('attachment', 'rb') as file:
        binary_data = file.read()

    n_base_string = '1302'  # 假设这是一个4进制字符串
    base = 4
    assert convert_n_base_to_ascii(n_base_string, base) == 'r'
    print(process_text(binary_data, base))
