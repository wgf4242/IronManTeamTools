
import numpy as np
def lsb_decrypt(data1: bytes):
    result1 = get_three_LSB(data1)

    result2 = get_lsb_column(data1)

    return b'\n'.join([result1, result2])


def get_lsb_column(data1):
    ar1 = np.frombuffer(data1, dtype=np.uint8)
    padding_length = (3 - (len(ar1) % 3)) % 3
    padded_data = np.pad(ar1, (0, padding_length), mode='constant', constant_values=0)
    reshaped_data = padded_data.reshape(-1, 3)

    ar2 = reshaped_data.transpose().flatten()
    padding_length = (8 - (len(ar2) % 8)) % 8
    padded_data = np.pad(ar2, (0, padding_length), mode='constant', constant_values=0)
    reshaped_data = padded_data.reshape(-1, 8)
    binary_data = reshaped_data & 1
    integer_values = binary_data.dot(2 ** np.arange(8)[::-1])
    result2 = integer_values.astype(np.uint8).tobytes()
    return result2


def get_three_LSB(data1):
    data = np.frombuffer(data1, dtype=np.uint8)
    padding_length = (8 - (len(data) % 8)) % 8
    padded_data = np.pad(data, (0, padding_length), mode='constant', constant_values=0)
    reshaped_data = padded_data.reshape(-1, 8)
    binary_data = reshaped_data & 1
    integer_values = binary_data.dot(2 ** np.arange(8)[::-1])
    result1 = integer_values.astype(np.uint8).tobytes()
    return result1