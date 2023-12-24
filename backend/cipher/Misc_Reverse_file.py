
import numpy as np


def cipher_test_split_byte_l4_h4_swap_file(content, folder):
    def rev(content, folder):
        # ar = np.fromfile(file, dtype='uint8')
        ar = np.frombuffer(content, dtype=np.uint8)
        b1 = (ar & 0xf0) >> 4
        b2 = (ar & 0xf) << 4
        c = b1 + b2
        c[::-1].tofile(folder + '/file1')
        c.tofile(folder + '/file2')

    rev(content, folder)

if __name__ == '__main__':
    from io import BytesIO

    # file_object = BytesIO()
    # file_object.write(b'Hello')
    # cipher_test_split_byte_l4_h4_swap_file(file_object)
    cipher_test_split_byte_l4_h4_swap_file(b'123456', '../tmp')

