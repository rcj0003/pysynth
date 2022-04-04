class SimpleEnvelope:
    def __init__(self, attack, hold):
        self.attack = attack
        self.hold = hold
        self.release = 1 - hold
    
    def __call__(self, sample_rate, time, note_length):
        note_time = time / note_length
        if note_time < self.attack:
            return (note_time / self.attack) ** 2
        if note_time < self.hold:
            return 1
        return 1 - (((self.hold - note_time) / self.release) ** 2)
