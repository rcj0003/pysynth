import math
from fractions import Fraction


class TimbreFrequency:
    @staticmethod
    def from_equation(equation, low=20, high=20000):
        freqs = []

        for x in range(low, high):
            value = equation(x)
            
            if value <= 0:
                continue
            freqs.append(TimbreFrequency(x, value))
        
        return freqs

    @staticmethod
    def equation_over_ranges(equation, *ranges):
        freqs = []

        for r in ranges:
            for x in range(*r):
                value = equation(x)
                
                if value <= 0:
                    continue
                freqs.append(TimbreFrequency(x, value))
        
        return freqs

    def __init__(self, frequency, amplitude):
        self.frequency = frequency
        self.amplitude = amplitude
    
    def value(self, time, semitone=1):
        return 0xFFFF * self.amplitude * math.sin(time * self.frequency * semitone)

class BasicTimbre:
    @staticmethod
    def new(data):
        return BasicTimbre(
            *(TimbreFrequency(freq, amplitude)
            for freq, amplitude in data.items())
        )

    def __init__(self, *freq):
        self._freq = freq
    
    def get_amplitude(self, time, intensity=1, semitone=0):
        current = 0
        semitone = Fraction(106, 100) ** semitone

        for freq in self._freq:
            current += freq.value(time, semitone)

        return intensity * current
