import cv2
import numpy as np


def from_binary_lsb(data):
    padding_length = (8 - (len(data) % 8)) % 8
    padded_data = np.pad(data, (0, padding_length), mode='constant', constant_values=0)
    reshaped_data = padded_data.reshape(-1, 8)
    binary_data = reshaped_data & 1
    integer_values = binary_data.dot(2 ** np.arange(8)[::-1])
    res = integer_values.astype(np.uint8).tobytes()
    return res


def image_pixel(img_bytes: bytes, start_x=5, start_y=5, gap=10):
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 设置起始点和间隔
    # start_x, start_y = 5, 5  # (x, y) 坐标
    # gap = 10
    height, width, channels = img_rgb.shape
    # 生成行和列的索引
    rows = np.arange(start_x, height, gap)
    cols = np.arange(start_y, width, gap)
    # 使用行和列的索引进行切片
    sliced_img = img_rgb[np.ix_(rows, cols)]
    # 从sliced_img分别提取R、G、B通道
    r_channel = sliced_img[:, :, 0].flatten()
    g_channel = sliced_img[:, :, 1].flatten()
    b_channel = sliced_img[:, :, 2].flatten()
    r1 = from_binary_lsb(r_channel)
    g1 = from_binary_lsb(g_channel)
    b1 = from_binary_lsb(b_channel)
    rgb_channel = sliced_img.flatten()
    rgb1 = from_binary_lsb(rgb_channel)
    # 打印每个通道的形状，以确认提取成功
    # print("R channel_lsb:", r1)
    # print("G channel_lsb:", g1)
    # print("B channel_lsb:", b1)
    # print("RGB channel_lsb:", rgb1)
    rb1 = r_channel.astype(np.uint8).tobytes()
    # print("R channel:", rb1)
    gb1 = g_channel.astype(np.uint8).tobytes()
    # print("G channel:", gb1)
    bb1 = b_channel.astype(np.uint8).tobytes()
    # print("B channel:", bb1)
    rgbb1 = rgb_channel.astype(np.uint8).tobytes()

    # print("RGB channel:", rgbb1)

    # 函数用于将RGB颜色转换为16进制字符串
    def rgb_to_hex(rgb):
        return '#{0:02x}{1:02x}{2:02x}'.format(rgb[0], rgb[1], rgb[2])

    vrgb_to_hex = np.vectorize(rgb_to_hex, signature='(n)->()')
    hex_colors = vrgb_to_hex(sliced_img)
    binary = ','.join(hex_colors.flatten()[:12])

    # print(binary)
    def foo(lst):
        res = [x.decode('utf-8', 'ignore') if isinstance(x, bytes) else x for x in lst]
        return '\n'.join(res)

    return foo([binary, r1, g1, b1, rgb1, rb1, gb1, bb1, rgbb1])


if __name__ == '__main__':
    # img = cv2.imread(img_bytes)
    # img = cv2.imread('Tinted.png')
    im = open('Tinted.png', 'rb').read()
    res =image_pixel(im, 5, 5, 10)
    print(res)
