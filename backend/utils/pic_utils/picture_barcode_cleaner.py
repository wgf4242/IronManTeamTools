# 2024年第八届工业信息安全技能大赛 “三峡杯”工控安全锦标赛 脏脏的二维码



def clean_barcode(image_path):
    import cv2
    import numpy as np
    from io import BytesIO

    # 读取图像
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 获取图像尺寸
    height, width = img.shape

    # 找到条形码的最高点和最低点
    top = 0
    bottom = height - 1
    for i in range(height):
        if np.any(img[i, :] < 128):
            top = i
            break
    for i in range(height - 1, -1, -1):
        if np.any(img[i, :] < 128):
            bottom = i
            break

    # 创建新的图像用于存储恢复的条形码
    cleaned = np.ones((bottom - top + 1, width), dtype=np.uint8) * 255

    # 纵向扫描并恢复条形码
    for x in range(width):
        column = img[top:bottom + 1, x]
        if np.any(column < 15):  # 如果列中有任何黑色像素
            cleaned[:, x] = 0  # 将整列涂黑
        # 否则保持白色

    # cv2.imwrite(output_path, cleaned)

    # 将结果转换为二进制数据
    is_success, buffer = cv2.imencode(".png", cleaned)
    io_buf = BytesIO(buffer)

    return io_buf.getvalue()

if __name__ == '__main__':
    binary_data = clean_barcode(r'F:\Fshare\del1\vmware\del1\flag.png')
    with open('cleaned_flag.png', 'wb') as f:
        f.write(binary_data)
    print("清理后的条形码已保存到 cleaned_flag.png")
