import pygame
import random

class obstacle:
    def __init__(self, channel, note, start, end):
        self.channel = channel
        self.note = note
        self.start = start
        self.end = end
        self.length = (end - start) /20
        self.rect = pygame.Rect(0, 0, 0, 0)
    def debugMsg(self):
        print("Channel", end=" ")
        print(self.channel)
        print("note", end=" ")
        print(self.note)
        print("start at tick", end=" ")
        print(self.start)
        print("end at tick", end=" ")
        print(self.end)
        print("length", end=" ")
        print(self.length)

class pianoKey:
    def __init__(self, pos):
        self.line = 1
        self.pos = pos
        self.active = False
    def switch(self, val):
        if val:
            self.line = 0
            self.active = True
        else:
            self.active = False
            self.line = 1

def onlyNotes(msg):
    if msg.type == "note_on":
        return True
    else:
        return False

def create_obstacles(messages, channels): #creates list of obstacles
    obstacles = []
    messagesNotes= [x for x in messages if x.type == "note_on" or x.type == "note_off"]
    newO = None #new obstacle to be added
    for msg in messagesNotes:
        if msg.type == "note_on":
            if msg.velocity != 0 and msg.channel in channels:
                nextMsg = next((x for x in messagesNotes if x.channel==msg.channel and x.note==msg.note), None) #find next message to end obstacle (might use nexts)
                if type(nextMsg) != None:
                    newO=obstacle(msg.channel, msg.note, msg.time, nextMsg.time)
                    obstacles.append(newO)
    obstacles.sort(key=lambda x: x.start, reverse=False)
    return obstacles
