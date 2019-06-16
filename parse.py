class midiHeroTrack:
    def __init__(self):
        self.track = []
        self.instruments = [0] *16
        self.bps = 2
        self.length = 0 #track length in ticks
    def get_bpm(self): #return bpm
        bpm = self.bps * 60
        return round(bpm)
    def update_length(self, tick):
        if tick > self.length:
            self.length = tick

def midi_tick2(mid, gametps):
    new = midiHeroTrack()
    tpb = mid.ticks_per_beat
    mspb = 500000 #120BPM default tempo / 500000microseconds per beat
    new.bps = 1000000 / mspb #beats per second
    tps = new.bps * tpb #miditicks per second
    multiplier = gametps / tps #multiplier to convert to game speed

    for track in mid.tracks:
        tick = 0
        for msg in track:
            if msg.type == "set_tempo":
                mspb = msg.tempo
                new.bps = 1000000 / mspb #beats per second
                tps = new.bps * tpb #miditicks per second
                multiplier = gametps / tps
            if not msg.is_meta: #filter meta messages
                if msg.type =="program_change": #get insturments
                    new.instruments[msg.channel] = msg.program
                msg.time = int(round(float(msg.time) * multiplier)) #convert to game speed
                tick = tick + msg.time #proceed time
                msg.time = tick # set to absolute time
                new.track.append(msg)
                new.update_length(tick)
    new.track.sort(key=lambda x: x.time, reverse=False) # sort messages by time
    return new
