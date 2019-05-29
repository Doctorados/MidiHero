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
                #if msg.type == "note_on": #ticks to game ticks
                #print(multiplier)
                #print(msg)
                msg.time = int(round(float(msg.time) * multiplier))
                #print(msg)
                tick = tick + msg.time
                msg.time = tick
                #print(msg)
                new.track.append(msg)
    print("beats per second", end=" ")
    print(new.bps)
    print("beats per Minute", end=" ")
    print(new.get_bpm())
    new.length = tick
    new.track.sort(key=lambda x: x.time, reverse=False)
    return new
