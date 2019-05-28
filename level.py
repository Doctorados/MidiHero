import gameObjects
import mido
import parse
import pygame

class level:
    def __init__(self, file, tps, channels, rows):
        self.tps = tps
        self.obstaclesOnscreen = []
        self.activeObs = []
        self.lastMsg = 0
        self.lastObstacle = 0
        self.tick = 0
        self.channels = channels
        self.rows = rows
        self.bus = mido.open_output(mido.get_output_names()[0])
        self.mid = mido.MidiFile(file)
        self.midiHeroTrack = parse.midi_tick2(self.mid, tps)
        self.messages = self.midiHeroTrack.track
        self.instruments = self.midiHeroTrack.instruments
        self.obstacles = gameObjects.create_obstacles(self.messages,  self.channels)
        self.keys = self.gen_keys()
        self.score = score_obj()
        self.run = True
    def gen_keys(self):
        keys = []
        for i in range(0, self.rows):
            keys.append(gameObjects.pianoKey(i, pygame.Rect(i*(1280 / self.rows), 600, (1280 / self.rows),120)))
        return keys

    def bus_output(self, msg):
        self.bus.send(msg)

    def update_onscreen_obs(self):
        for x in self.obstaclesOnscreen:
            if x.rect[1] > 720:
                self.obstaclesOnscreen.remove(x)
            else:
                x.rect[1] += 1
                if self.keys[x.row].active:
                    if x.isPlayed(self.keys[x.row]):#checks for collision between key and obstacle
                        x.fill = 0
                        self.activeObs.append([x.note, x.start])



    def play_messages(self):
        for x in self.messages[self.lastMsg:]:
            if x.time + 660 > self.tick:
                break
            if x.time + 660 == self.tick:
                self.lastMsg += 1
                if x.type == "note_on":
                    if x.channel in self.channels and x.velocity != 0:
                        self.score.max +=1
                        if not [x.note, x.time] in self.activeObs:
                            self.score.wrongKey +=1
                            x.velocity = 0
                        else:
                            self.score.scored +=1
                            self.activeObs.remove([x.note, x.time])
                self.bus_output(x)

    def gen_onscreen_obs(self):
        for x in self.obstacles[self.lastObstacle:]:
            if x.start > self.tick:
                break
            if x.start == self.tick:
                self.lastObstacle += 1
                x.row = (x.note % self.rows)
                x.rect = pygame.Rect(((1280 / self.rows) * x.row + ((1280 / self.rows)/ 2)), 0, 15, x.length)
                self.obstaclesOnscreen.append(x)

    def draw(self, screen, colorObs, colorKeys):
        for x in self.obstaclesOnscreen:
            pygame.draw.rect(screen, colorObs, x, x.fill)
        for x in self.keys:
            pygame.draw.rect(screen, colorKeys, x.rect, x.line)


    def update(self):
        self.update_onscreen_obs()
        self.play_messages()
        self.gen_onscreen_obs()
        self.tick += 1
        if len(self.messages) == (self.lastMsg):
            self.run = False

class score_obj:
    def __init__(self):
        self.multiplier = 1.0
        self.scored = 0
        self.wrongKey = 0
        self.max = 0
    def calc_score(self):
         missed = self.max - self.scored
         print(self.max)
         print(self.scored)
         print(self.wrongKey)
         self.multiplier = (self.max / (self.wrongKey + self.max))
         final = self.scored * self.multiplier
         return final
