import gameObjects
import mido
import parse
import pygame

class level:
    def __init__(self, file, tps, channels, rows):
        self.tps = tps # ticks per second
        self.obstaclesOnscreen = [] #list of obstacles currently on screen
        self.activeObs = [] # list of obstacles, that are already "hit"
        self.lastMsg = 0 # index of last midi message processed
        self.lastObstacle = 0 #index of last obstacle processed
        self.tick = 0 # current tick / current iteration
        self.channels = channels # list of channels that generate obstacles
        self.rows = rows #number of rows, determines how many keys the player has to play
        self.bus = mido.open_output(mido.get_output_names()[0]) # get name of first available midi output port and set it as the programs audio output
        self.mid = mido.MidiFile(file) #convert midi file to mido.mid object
        self.midiHeroTrack = parse.midi_tick2(self.mid, tps) #convert mido.mid object to custom midiHero object
        self.messages = self.midiHeroTrack.track #list of midi messages
        self.obstacles = gameObjects.create_obstacles(self.messages,  self.channels) #generate a list of obstacles
        self.keys = self.gen_keys() #generate keys the player has to play
        self.score = gameObjects.score() #create score instance
        self.progressBar = gameObjects.progressBar(self.midiHeroTrack.length, self.midiHeroTrack.bps, self.tps)
        self.run = True #run variable
    def gen_keys(self):
        keys = []
        for i in range(0, self.rows):
            keys.append(gameObjects.pianoKey(i, pygame.Rect(i*(1280 / self.rows), 540, (1280 / self.rows),120)))
        return keys

    def bus_output(self, msg):
        self.bus.send(msg)

    def update_onscreen_obs(self):
        for x in self.obstaclesOnscreen:
            if x.rect[1] > 720: #check if obstacle is of screen
                self.obstaclesOnscreen.remove(x)
            else:
                x.rect[1] += 1 #move down one pixel
                if self.keys[x.row].active: #check if key is pressed
                    if x.isPlayed(self.keys[x.row]):#checks for collision between key and obstacle
                        x.fill = 0
                        self.activeObs.append([x.note, x.start])
                    else:
                        self.score.wrongKey += ((1 / len(self.obstaclesOnscreen)) / self.tps)

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

    def draw(self, screen, colors):
        for x in self.obstaclesOnscreen:
            pygame.draw.rect(screen, colors["secondary"], x, x.fill)
        for x in self.keys:
            pygame.draw.rect(screen, colors["primary"], x.rect, x.line)
        pygame.draw.rect(screen, colors["primary"],self.progressBar.get_bar(self.tick), self.progressBar.get_flash(self.tick) )

    def update(self):
        self.update_onscreen_obs()
        self.play_messages()
        self.gen_onscreen_obs()
        self.tick += 1
        if len(self.messages) == (self.lastMsg):
            self.run = False
