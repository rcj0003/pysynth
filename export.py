from pysynth.machine import Note
from pysynth.utils import note_time

TRANSPOSE_KEYS_BY = 12

Note.export(
    'song_synth.json',
    [
        Note(TRANSPOSE_KEYS_BY + 0, note_time(), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 2, note_time(quarter=1), Note.QUARTER_TIME, 0.35),
        Note(TRANSPOSE_KEYS_BY + 3, note_time(half_beat=1), Note.QUARTER_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 2, note_time(beat=1, half_beat=1), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 0, note_time(beat=2), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 2, note_time(beat=2, half_beat=1), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 5, note_time(beat=3), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY - 1, note_time(beat=3, half_beat=1), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 0, note_time(bar=1), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 2, note_time(bar=1, quarter=1), Note.QUARTER_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 3, note_time(bar=1, half_beat=1), Note.QUARTER_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 2, note_time(bar=1, beat=1, half_beat=1), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 0, note_time(bar=1, beat=2), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 2, note_time(bar=1, beat=2, half_beat=1), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 5, note_time(bar=1, beat=3), Note.HALF_TIME, 0.5),
        Note(TRANSPOSE_KEYS_BY + 1, note_time(bar=1, beat=3, half_beat=1), Note.HALF_TIME - 1, 0.5),
    ]
)
