import pyaudio


class AudioOut:
    def __init__(self, channels, sample_rate, bit_rate, callback):
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(
            format=self._audio.get_format_from_width(bit_rate // 8),
            channels=channels,
            rate=sample_rate,
            output=True,
            stream_callback=callback
        )
    
    def start(self):
        self._stream.start_stream()
        return self
    
    def stop(self):
        self._stream.stop_stream()
        self._stream.close()
        return self
    
    def close(self):
        self._stream.stop_stream()
        self._stream.close()
