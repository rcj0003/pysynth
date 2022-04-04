from instruments import KICK, SYNTH, TEST
from pysynth.audio import AudioOut
from pysynth.effects import SimpleEnvelope
from pysynth.machine import BeatMachine, Instrument, Note
from pysynth.postprocess import basic_fft
from pysynth.utils import KeyEnum, key, note_time

SAMPLE_RATE = 44100
BIT_RATE = 24

machine = BeatMachine(
    bpm=140,
    instruments=[
        Instrument(
            timbre=TEST,
            notes=Note.load('song_synth.json'),
            effects=[
                SimpleEnvelope(attack=0.1, hold=0.2)
            ]
        ),
        #Instrument(
        #    timbre=KICK,
        #    notes=[
        #        Note(key(KeyEnum.C, 1), note_time(beat=0, quarter=0), 32, 1),
        #        Note(key(KeyEnum.C, 1), note_time(beat=0, quarter=2), 32, 1),
        #        Note(key(KeyEnum.C, 1), note_time(beat=2, quarter=0), 32, 1),
        #        Note(key(KeyEnum.C, 1), note_time(beat=2, quarter=2), 32, 1),
        #    ],
        #    effects=[
        #        SimpleEnvelope(attack=0.01, hold=0.05)
        #    ]
        #)
    ],
    sample_rate=SAMPLE_RATE,
    bit_rate=BIT_RATE
)
machine._bake_loop(basic_fft, loop_length=8, export=True)

audio = AudioOut(1, SAMPLE_RATE, BIT_RATE, machine)
audio.start()
input('Press enter to stop.')
audio.stop()


