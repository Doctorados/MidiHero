import mido

class midiHeroTrack:
    def __init__(self):
        self.track = []
        self.instruments = [0] *16

class midiHeroInfo:
    def __init__(self, ticks_per_beat = 4, tempo = 500000):
        self.tpb = ticks_per_beat
        self.tempo = set_tempo
        self.bps = 2
        self.bpm = 120
    def update():
        self.bps = 1000000 / self.bps
        self.bpm = self.bps *60

def getInfo(mid):
    info = midiHeroInfo(mid.ticks_per_beat)
    for msg in mid:
        if msg.type =="set_tempo":
            info.tempo = msg.tempo
    info.update()
    return info

def midi_tick2(mid, gametps):
    new = midiHeroTrack()
    tpb = mid.ticks_per_beat
    mspb = 500000 #120BPM default tempo / 500000microseconds per beat
    bps = 1000000 / mspb #beats per second
    tps = bps * tpb #miditicks per second
    multiplier = gametps / tps

    for i, track in enumerate(mid.tracks):
        tick = 0
        for msg in track:
            print(msg)
            if msg.type == "set_tempo":
                mspb = msg.tempo
                bps = 1000000 / mspb #beats per second
                print("beats per second", end=" ")
                print(bps)
                tps = bps * tpb #miditicks per second
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
    print(bps)
    new.track.sort(key=lambda x: x.time, reverse=False)
    return new
