import json
import math
import wave
from fractions import Fraction

import pyaudio

from .utils import Sampler


class Note:
    EIGHTH_TIME = 4
    QUARTER_TIME = 8
    HALF_TIME = 16
    BEAT = 32

    def __init__(self, semitone, start, duration, intensity=1):
        self.semitone = semitone
        self.duration = duration
        self.start = start
        self.intensity = intensity
        self._start_frame = None
        self._end_frame = None
        self._duration_frames = None
    
    @property
    def ends_on(self):
        return math.ceil(self.start + self.duration)
    
    @classmethod
    def _get_frame(self, beat, beat_time, sample_rate):
        return int(beat_time * (beat / 32) * sample_rate)
    
    def get_start_frame(self, sample_rate, beat_time):
        if self._start_frame is not None:
            return self._start_frame
        self._start_frame = self._get_frame(self.start, beat_time, sample_rate)
        return self._start_frame
    
    def get_duration_frames(self, sample_rate, beat_time):
        if self._duration_frames is not None:
            return self._duration_frames
        self._duration_frames = self._get_frame(self.duration, beat_time, sample_rate)
        return self._duration_frames
    
    def get_end_frame(self, sample_rate, beat_time):
        if self._end_frame is not None:
            return self._end_frame
        self._end_frame = self._get_frame(self.start + self.duration, beat_time, sample_rate)
        return self._end_frame

    @staticmethod
    def load(file_name):
        notes = []
        with open(file_name, 'r') as file:
            data = json.load(file)
            notes = [
                Note(
                    note_data['semitone'],
                    note_data['time_data']['start'],
                    note_data['time_data']['end'],
                    note_data['intensity']
                )
                for note_data in data
            ]
        return notes

    @staticmethod
    def export(file_name, notes):
        with open(file_name, 'w') as file:
            data = [
                {
                    'semitone': note.semitone,
                    'time_data': {
                        'resolution': 'beat32',
                        'start': note.start,
                        'end': note.duration,
                    },
                    'intensity': note.intensity
                }
                for note in notes
            ]
            json.dump(data, file)

class Instrument:
    def __init__(self, timbre, notes, effects=[]):
        self._timbre = timbre
        self._notes = notes
        self.effects = effects

    def value(self, sample_rate, frame, beat_time):
        amplitude = 0
        for note in self._notes:
            current_frame = frame - note.get_start_frame(sample_rate, beat_time)
            if frame < note.get_start_frame(sample_rate, beat_time) or frame > note.get_end_frame(sample_rate, beat_time):
                continue
            intensity = 1
            for effect in self.effects:
                intensity *= effect(sample_rate, current_frame, note.get_duration_frames(sample_rate, beat_time))
            intensity = max(0, intensity)
            amplitude += self._timbre.get_amplitude(current_frame/sample_rate, note.intensity * intensity, note.semitone)
        return amplitude

    @property
    def loop_length(self):
        longest_duration = max(
            math.ceil(note.duration + note.start)
            for note in self._notes
        )
        return longest_duration

class BeatMachine:
    def __init__(self, bpm, instruments, sample_rate, bit_rate):
        self._beat_time = 60 / bpm
        self._start_time = 0
        self._instruments = instruments

        self._bit_rate = bit_rate
        self._sample_rate = sample_rate
        self._sampler = Sampler(bit_rate)
        self._current_frame = 0
        self._total_frames = 0
        self._byte_count = 0
        self._baked = []
        self._bake_done = False

        self._frame_size = (bit_rate // 8)
    
    def _bake_loop(self, *processors, loop_length=None, export=False):
        if not loop_length:
            print('Getting loop data...')
            loop_lengths = [
                instrument.loop_length
                for instrument in self._instruments
            ]
            loop_length = math.ceil(math.lcm(*loop_lengths) / 32)
        
        self._total_frames = int((self._beat_time * loop_length * self._sample_rate) + 0.01)
        amplitudes = []
        
        print('Baking frames...')
        for frame in range(self._total_frames):
            amplitude = 0
            for instrument in self._instruments:
                amplitude += instrument.value(self._sample_rate, frame, self._beat_time)
            amplitudes.append(amplitude)
        
        print('Processing data...')
        for processor in processors:
            amplitudes = processor(amplitudes, self._sample_rate, self._bit_rate)
        amplitudes = self._normalize(amplitudes, self._sample_rate, self._bit_rate)

        self._baked = bytes(amplitudes + amplitudes[:1024 * self._frame_size])
        self._total_bytes = len(amplitudes)
        print('Bake complete.')
        self._bake_done = True

        if export:
            print('Exporting')
            export = wave.open('exported.wav', 'w')
            export.setnchannels(1)
            export.setframerate(self._sample_rate)
            export.setsampwidth(self._bit_rate // 8)
            export.writeframesraw(bytes(amplitudes))
            export.close()
    
    @classmethod
    def _normalize(cls, amplitudes, sample_rate, bit_rate):
        print('Normalizing...')
        byte_length = bit_rate // 8
        smallest = min(amplitudes)
        biggest = int(max(max(amplitudes), abs(smallest)) or 1) + 1
        ratio = Fraction(2 ** (bit_rate - 1), biggest)
        _amplitudes = []
        for amplitude in amplitudes:
            value = int(amplitude.real * ratio)
            _amplitudes.extend(value.to_bytes(byte_length, 'little', signed=True))
        return _amplitudes

    def __call__(self, input_data, frame_count, time_info, status_flag):
        data = self._baked[self._current_frame * self._frame_size:(self._current_frame + frame_count) * self._frame_size]
        self._current_frame += frame_count
        self._current_frame %= self._total_frames
        return data, pyaudio.paContinue
