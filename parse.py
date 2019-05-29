import mido

class midiHeroTrack:
    def __init__(self):
        self.track = []
        self.instruments = [0] *16
        self.bps = 2
        self.length = 0
    def get_bpm(self):
        bpm = self.bps * 60
        return bpm
    def update_length(self, tick):
        if tick > self.length:
            self.length = tick

def midi_tick2(mid, gametps):
    new = midiHeroTrack()
    tpb = mid.ticks_per_beat
    mspb = 500000 #120BPM default tempo / 500000microseconds per beat
    new.bps = 1000000 / mspb #beats per second
    tps = new.bps * tpb #miditicks per second
    multiplier = gametps / tps

    for i, track in enumerate(mid.tracks):
        tick = 0
        for msg in track:
            print(msg)
            if msg.type == "set_tempo":
                mspb = msg.tempo
                new.bps = 1000000 / mspb #beats per second
                tps = new.bps * tpb #miditicks per second
                multiplier = gametps / tps
            if not msg.is_meta:
                if msg.type =="program_change": #get insturments
                    new.instruments[msg.channel] = msg.program
                msg.time = int(round(float(msg.time) * multiplier))
                tick = tick + msg.time
                msg.time = tick
                new.track.append(msg)
                new.update_length(tick)
    print("beats per second", end=" ")
    print(new.bps)
    print("beats per Minute", end=" ")
    print(new.get_bpm())
    new.track.sort(key=lambda x: x.time, reverse=False)
    return new
