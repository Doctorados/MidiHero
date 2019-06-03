import gameObjects
import mido
import parse
import pygame
import tkinter
import tkinter.filedialog
import threading
import globalConst

class level:
    def __init__(self, channels, track):
        self.obstaclesOnscreen = [] #list of obstacles currently on screen
        self.activeObs = [] # list of obstacles, that are already "hit"
        self.lastMsg = 0 # index of last midi message processed
        self.lastObstacle = 0 #index of last obstacle processed
        self.tick = 0 # current tick / current iteration
        self.channels = channels # list of channels that generate obstacles
        self.bus = mido.open_output(mido.get_output_names()[0]) # get name of first available midi output port and set it as the programs audio output
        self.midiHeroTrack = track #convert mido.mid object to custom midiHero object
        self.messages = self.midiHeroTrack.track #list of midi messages
        self.obstacles = gameObjects.create_obstacles(self.messages,  self.channels) #generate a list of obstacles
        self.keys = self.gen_keys() #generate keys the player has to play
        self.score = gameObjects.score() #create score instance
        self.progressBar = gameObjects.progressBar(self.midiHeroTrack.length, self.midiHeroTrack.bps, globalConst.tps)
        self.run = True #run variable

    def gen_keys(self):
        keys = []
        for i in range(0, globalConst.rows):
            keys.append(gameObjects.pianoKey(i, pygame.Rect(i*(1280 / globalConst.rows), 540, (1280 / globalConst.rows),120)))
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
                        self.score.wrongKey += (1 / globalConst.tps)

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
                x.row = (x.note % globalConst.rows)
                x.rect = pygame.Rect(((1280 / globalConst.rows) * x.row + ((1280 / globalConst.rows)/ 2)), 0, 15, x.length)
                self.obstaclesOnscreen.append(x)

    def draw(self, screen):
        for x in self.obstaclesOnscreen:
            pygame.draw.rect(screen, globalConst.colors["secondary"], x, x.fill)
        for x in self.keys:
            pygame.draw.rect(screen, globalConst.colors["primary"], x.rect, x.line)
        pygame.draw.rect(screen, globalConst.colors["primary"],self.progressBar.get_bar(self.tick), self.progressBar.get_flash(self.tick) )

    def inp(self, inpQ):
        for event in inpQ:
            if event.type == pygame.KEYDOWN:
                if event.key in globalConst.keybinds:
                    i = globalConst.keybinds.index(event.key)
                    self.keys[i].switch(True)
            if event.type == pygame.KEYUP:
                if event.key in globalConst.keybinds:
                    i = globalConst.keybinds.index(event.key)
                    self.keys[i].switch(False)

    def update(self, inpQ):
        self.inp(inpQ)
        self.update_onscreen_obs()
        self.play_messages()
        self.gen_onscreen_obs()
        self.tick += 1

    def next_scene(self):
        if len(self.messages) == (self.lastMsg):
            self.run = False
            return score(self.score)
        else:
            return self

class score:
    def __init__(self, score):
        self.score = score
        self.score.calc_score()
        self.menuBg = pygame.Rect(420, 0, 440, 720)
        self.tick = 0
        self.nextScene = self
        self.btn1 = gameObjects.menuButton(pygame.Rect(100,500,1080,100))
    def draw(self, screen):
        line1 = list("Notes hit: " + str(self.score.scored) + " / "+ str(self.score.max))
        line2 = list("Efficiency: " + str(self.score.efficiency) +"%")
        line3 = list("Final Score: " + str(self.score.final))
        for i in range (0, (self.tick//(globalConst.tps//20))):
            text1 = globalConst.font.render("".join(line1[0:i]), False, globalConst.colors["secondary"])
            text2 = globalConst.font.render("".join(line2[0:i]), False, globalConst.colors["secondary"])
            text3 = globalConst.font.render("".join(line3[0:i]), False, globalConst.colors["secondary"])
            screen.blit(text1,(420,100))
            screen.blit(text2,(420,200))
            screen.blit(text3,(420,300))
        self.btn1.draw(screen, globalConst.colors["secondary"], "Hauptmenü", globalConst.font)

    def update(self, inpQ):
        self.tick += 1
        if self.btn1.get_press(inpQ):
            self.nextScene = menu()
    def next_scene(self):
        return self.nextScene

class menu:
    def __init__(self):
        self.nextScene = self
        self.btn1 = gameObjects.menuButton(pygame.Rect(100,100,1080,100))
        self.btn2 = gameObjects.menuButton(pygame.Rect(100,300,1080,100))
        self.btn3 = gameObjects.menuButton(pygame.Rect(100,500,1080,100))

    def draw(self, screen):
        self.btn1.draw(screen, globalConst.colors["secondary"], "Custom Level", globalConst.font)
        self.btn2.draw(screen, globalConst.colors["secondary"], "TEXT", globalConst.font)
        self.btn3.draw(screen, globalConst.colors["secondary"], "TEXT", globalConst.font)

    def update(self, inpQ):
        if self.btn1.get_press(inpQ):
            window = tkinter.Tk()
            file = tkinter.filedialog.askopenfilename()
            window.destroy()
            self.nextScene = loading(file)

    def next_scene(self):
        return self.nextScene

class loading:
    def __init__(self, file):
        self.file = file
        self.nextScene = self
        self.firstCall = True
        self.tick = 0
        (threading.Thread(target=self.parseFile)).start()

    def draw(self, screen):
        strings = [
            "Loading level",
            "." * ((self.tick//(globalConst.tps//10))%10),
        ]
        for i,x in enumerate(strings):
            text = globalConst.font.render(x, False, globalConst.colors["secondary"])
            screen.blit(text, (420, 100*(i+1)))

    def update(self, inpQ):
        self.tick +=1

    def next_scene(self):
        return self.nextScene

    def parseFile(self):
        mid = mido.MidiFile(self.file) #convert midi file to mido.mid object
        midiHeroTrack = parse.midi_tick2(mid, globalConst.tps)
        self.nextScene = startlvl(self.file, midiHeroTrack)

class startlvl:
    def __init__(self, file, track, channels = [0]):
        self.file = file
        self.track = track
        self.nextScene = self
        self.channels = channels
        self.box1 = gameObjects.menuButton(pygame.Rect(100,100,800,100))
        self.box2 = gameObjects.menuButton(pygame.Rect(100,200,800,100))
        self.box3 = gameObjects.menuButton(pygame.Rect(100,300,800,100))
        self.btn1 = gameObjects.menuButton(pygame.Rect(100,600,800,100))
        self.chBtns = []
        for i in range (0, 16):
            self.chBtns.append(gameObjects.menuButton(pygame.Rect(100+(i*50),400,50,100)))

    def draw(self, screen):
        self.box1.draw(screen, globalConst.colors["secondary"], "File: " + ((self.file).split("/"))[-1], globalConst.font)
        self.box2.draw(screen, globalConst.colors["secondary"], "BPM: " + str(self.track.get_bpm()), globalConst.font)
        self.box3.draw(screen, globalConst.colors["secondary"], "Channels: ", globalConst.font)
        self.btn1.draw(screen, globalConst.colors["secondary"], "START", globalConst.font, 6)
        for i,x in enumerate(self.chBtns):
            line = 1
            if i in self.channels:
                line = 6
            x.draw(screen, globalConst.colors["secondary"], str(i), globalConst.font, line)

    def update(self, inpQ):
        for i,x in enumerate(self.chBtns):
            if x.get_press(inpQ):
                if i in self.channels:
                    self.channels.remove(i)
                else:
                    self.channels.append(i)
        if self.btn1.get_press(inpQ):
            self.nextScene= level(self.channels, self.track)

    def next_scene(self):
        return self.nextScene
