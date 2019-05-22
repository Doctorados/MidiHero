import mido

class midiheroTrack:
    def __init__(self):
        self.track = []
        self.instruments = [0] *16

def midi_tick2(mid, gametps):
    new = midiheroTrack()
    tpb = mid.ticks_per_beat
    print("ticks_per_beat", end=" ")
    print(tpb)
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
