import math


class KeyEnum:
    C = 0
    C_SHARP = 1
    D_FLAT = 1
    D = 2
    D_SHARP = 3
    E_FLAT = 3
    E = 4
    F = 5
    F_SHARP = 6
    G_FLAT = 6
    G = 7
    G_SHARP = 8
    A_FLAT = 8
    A = 9
    A_SHARP = 10
    B_FLAT = 10
    B = 11
    
def key(key, octave=0):
    return key + (octave * 12)

def note_time(measure=0, bar=0, beat=0, half_beat=0, quarter=0, eigth=0, sixteenth=0):
    return (measure * 32 * 16) + (bar * 32 * 4) + (beat * 32) + (half_beat * 16) + (quarter * 8) + (eigth * 4) + (sixteenth * 2)

class Sampler:
    def __init__(self, bit_rate):
        self._bit_rate = bit_rate
        self._byte_length = math.ceil(bit_rate / 8)
        self._bit_value = 2 ** (bit_rate - 1) - 1
        self._max_bit_value = (2 ** bit_rate) - 1
    
    def get_sample(self, amplitude):
        value = int(self._bit_value * amplitude)
        data = value.to_bytes(self._byte_length, 'little', signed=True)
        return data
