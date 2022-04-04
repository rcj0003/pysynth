import numpy as np


def basic_fft(amplitudes, sample_rate, bit_rate):
    print('Transforming...')
    _amplitudes = np.fft.fft(amplitudes)
    _amplitudes = np.fft.ifft(_amplitudes)
    return list(_amplitudes)
