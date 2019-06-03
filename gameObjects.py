import pygame
import random

class obstacle:
    def __init__(self, channel, note, start, end):
        self.channel = channel
        self.row = 0
        self.note = note
        self.start = start
        self.end = end
        self.length = (end - start)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.fill = 1
    def isPlayed(self, key):
        return self.rect.colliderect(key.rect)

class score:
    def __init__(self):
        self.multiplier = 1.0
        self.scored = 0
        self.wrongKey = 0
        self.max = 0
        self.final = 0
        self.efficiency = 100
    def calc_score(self):
         self.multiplier = (self.max / (self.wrongKey + self.max +1))
         self.efficiency = int(self.multiplier *100)
         self.final = round(self.scored * self.multiplier)


class progressBar:
    def __init__(self, max, bps, tps):
        self.progress = 0
        self.max = max
        self.flashTime = tps / (int(bps) * 2)
        self.flash = 0
    def get_bar(self, tick):
        self.progress = int((1280 * (tick / (self.max +660))))
        bar = pygame.Rect(0, 0, self.progress, 10)
        return bar
    def get_flash(self, tick):
        if tick % self.flashTime == 0:
            self.flash = 1 - self.flash
        return self.flash

class pianoKey:
    def __init__(self, row, rect):
        self.line = 1
        self.row = row
        self.active = False
        self.rect = rect
    def switch(self, val):
        if val:
            self.line = 0
            self.active = True
        else:
            self.active = False
            self.line = 1

class menuButton:
    def __init__(self, rect):
        self.rect = rect
    def draw(self, screen, color, string, font):
        text = font.render(string, False, color)
        pygame.draw.rect(screen, color, self.rect, 1)
        screen.blit(text, (self.rect[0] +5, self.rect[1]+(self.rect[3]/2)))
    def get_press(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                print(self.rect)
                print(pygame.mouse.get_pos())
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
                else:
                    return False
            if event.type == pygame.QUIT:
                sys.exit

def onlyNotes(msg):
    if msg.type == "note_on":
        return True
    else:
        return False

def create_obstacles(messages, channels): #creates list of obstacles
    obstacles = []
    messagesNotes= [x for x in messages if x.type == "note_on" or x.type == "note_off"]
    newO = None #new obstacle to be added
    for i,msg in enumerate(messagesNotes):
        if msg.type == "note_on":
            if msg.velocity != 0 and msg.channel in channels:
                nextMsg = next((x for x in messagesNotes[i+1:] if x.channel==msg.channel and x.note==msg.note), None) #find next message to end obstacle (might use nexts)
                if type(nextMsg) != None:
                    newO=obstacle(msg.channel, msg.note, msg.time, nextMsg.time)
                    obstacles.append(newO)
    obstacles.sort(key=lambda x: x.start, reverse=False)
    return obstacles
