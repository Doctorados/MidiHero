import gameObjects
import mido
import parse
import pygame
import tkinter
import tkinter.filedialog
import threading

class level:
    def __init__(self, tps, channels, rows, track):
        self.tps = tps # ticks per second
        self.inpQ= [False] *rows #queue of inputs (False no inp, True = keydown)
        self.obstaclesOnscreen = [] #list of obstacles currently on screen
        self.activeObs = [] # list of obstacles, that are already "hit"
        self.lastMsg = 0 # index of last midi message processed
        self.lastObstacle = 0 #index of last obstacle processed
        self.tick = 0 # current tick / current iteration
        self.channels = channels # list of channels that generate obstacles
        self.rows = rows #number of rows, determines how many keys the player has to play
        self.bus = mido.open_output(mido.get_output_names()[0]) # get name of first available midi output port and set it as the programs audio output
        self.midiHeroTrack = track #convert mido.mid object to custom midiHero object
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

    def draw(self, screen, colors, font):
        for x in self.obstaclesOnscreen:
            pygame.draw.rect(screen, colors["secondary"], x, x.fill)
        for x in self.keys:
            pygame.draw.rect(screen, colors["primary"], x.rect, x.line)
        pygame.draw.rect(screen, colors["primary"],self.progressBar.get_bar(self.tick), self.progressBar.get_flash(self.tick) )

    def inp(self):
        for i,x in enumerate(self.inpQ):
                self.keys[i].switch(x)

    def update(self):
        self.inp()
        self.update_onscreen_obs()
        self.play_messages()
        self.gen_onscreen_obs()
        self.tick += 1

    def next_scene(self):
        if len(self.messages) == (self.lastMsg):
            self.run = False
            return score(self.score, self.tps, self.rows)
        else:
            return self

class score:
    def __init__(self, score, tps, rows):
        self.score = score
        self.score.calc_score()
        self.menuBg = pygame.Rect(420, 0, 440, 720)
        self.tick = 0
        self.inpQ= [False] *rows
        self.rows = rows
        self.tps = tps
        self.nextScene = self
    def draw(self, screen, colors, font):
        line1 = list("Notes hit: " + str(self.score.scored))
        line2 = list("Efficiency: " + str(self.score.efficiency) +"%")
        line3 = list("Final Score: " + str(self.score.final))
        line4 = "Press Key1 to continue"
        for i in range (0, (self.tick//(self.tps//20))):
            text1 = font.render("".join(line1[0:i]), False, colors["secondary"])
            text2 = font.render("".join(line2[0:i]), False, colors["secondary"])
            text3 = font.render("".join(line3[0:i]), False, colors["secondary"])
            screen.blit(text1,(420,100))
            screen.blit(text2,(420,200))
            screen.blit(text3,(420,300))
        text4 = font.render(line4, False, colors["secondary"])
        screen.blit(text4, (420, 600))

    def inp(self):
        if self.inpQ[0]:
            self.nextScene = menu(self.rows, self.tps)

    def update(self):
        self.inp()
        self.tick += 1

    def next_scene(self):
        return self.nextScene

class menu:
    def __init__(self, rows, tps):
        self.inpQ = [False] *rows
        self.rows = rows
        self.tps = tps
        self.nextScene = self

    def draw(self, screen, colors, font):
        strings = [
            "Press Key1 to select file",
            "Press Key2 for Levels",
            "Press Key3 for settigns"
        ]
        for i,x in enumerate(strings):
            text = font.render(x, False, colors["secondary"])
            screen.blit(text, (420, 100*(i+1)))

    def inp(self):
        if self.inpQ[0]:
            window = tkinter.Tk()
            file = tkinter.filedialog.askopenfilename()
            window.destroy()
            self.nextScene = loading(self.rows, file, self.tps)

    def update(self):
        self.inp()

    def next_scene(self):
        return self.nextScene

class loading:
    def __init__(self, rows, file, tps):
        self.inpQ = [False] *rows
        self.file = file
        self.nextScene = self
        self.rows = rows
        self.tps = tps
        self.firstCall = True
        self.tick = 0
        (threading.Thread(target=self.parseFile)).start()

    def draw(self, screen, colors, font):
        strings = [
            "Loading level",
            "." * ((self.tick//(self.tps//10))%10),
        ]
        for i,x in enumerate(strings):
            text = font.render(x, False, colors["secondary"])
            screen.blit(text, (420, 100*(i+1)))

    def update(self):
        self.tick +=1

    def next_scene(self):
        return self.nextScene

    def parseFile(self):
        mid = mido.MidiFile(self.file) #convert midi file to mido.mid object
        midiHeroTrack = parse.midi_tick2(mid, self.tps)
        self.nextScene = startlvl(self.rows, self.file, midiHeroTrack, self.tps)

class startlvl:
    def __init__(self, rows, file, track, tps, channels = [0]):
        self.inpQ = [False] *rows
        self.inpQNum = []
        self.tempInp = ""
        self.file = file
        self.tps = tps
        self.rows = rows
        self.track = track
        self.nextScene = self
        self.channels = channels

    def draw(self, screen, colors, font):
        strings = [
            "File: " + ((self.file).split("/"))[-1],
            "BPM: " + str(self.track.get_bpm()),
            "Channels: " +str(self.channels),
            "Press Key1 to start",
            "Press number keys and return",
            "to (de)select channels"
        ]
        for i,x in enumerate(strings):
            text = font.render(x, False, colors["secondary"])
            screen.blit(text, (420, 100*(i+1)))

    def inp(self):
        if self.inpQ[0]:
            self.nextScene = level(self.tps, self.channels, self.rows, self.track)
        for x in self.inpQNum:
            if pygame.key.name(x) == "return":
                if int(self.tempInp) in self.channels:
                    self.channels.remove(int(self.tempInp))
                    self.tempInp = ""
                else:
                    if int(self.tempInp) < 16:
                        self.channels.append(int(self.tempInp))
                self.tempInp = ""
            else:
                self.tempInp += pygame.key.name(x)
            self.inpQNum.remove(x)

    def update(self):
        self.inp()

    def next_scene(self):
        return self.nextScene
