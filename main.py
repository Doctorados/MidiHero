import mido
import time
import pygame.midi
import gameObjects
import parse
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)


run = True
lastMsg = 0
lastObstacle = 0
pygame.init()
file ="./beverly.mid"
busName = mido.get_output_names()[0]
bus = mido.open_output(busName)
mid = mido.MidiFile(file)
tps = 160
tick = 0
rows = 4
clock = pygame.time.Clock()
size = (1280, 720) #window size
screen = pygame.display.set_mode(size)
midiHeroTrack = parse.midi_tick2(mid, tps)
messages = midiHeroTrack.track
instruments = midiHeroTrack.instruments
print(messages)
print(instruments)
channels = set([0,1,2,4])
obstacles = gameObjects.create_obstacles(messages,  channels)
obstaclesOnscreen = []
keys = []
scored = []
for i in range(0, rows):
    keys.append(gameObjects.pianoKey(i, pygame.Rect(i*(1280 // rows), 600, (1280 / rows),120)))

def bus_output(msg, bus):
    bus.send(msg)

def output():
    screen.fill((0, 0, 0))
    for x in obstaclesOnscreen:
        pygame.draw.rect(screen, RED, x, x.fill)
    for x in keys:
        pygame.draw.rect(screen, WHITE, x.rect, x.line)
    #pygame.draw.rect(screen, GREEN, pygame.Rect(0, 660, 1280, 2), 0)
    pygame.display.flip()

def input():
    global tps
    keybinds = [pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_l]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tps = tps*2
            if event.key in keybinds:
                i = keybinds.index(event.key)
                keys[i].switch(True)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                tps = tps / 2
            if event.key in keybinds:
                i = keybinds.index(event.key)
                keys[i].switch(False)


def logic():
    global lastMsg
    global lastObstacle
    global scored
    for x in obstaclesOnscreen:
        if x.rect[1] > 720:
            obstaclesOnscreen.remove(x)
        else:
            x.rect[1] += 1
            if x.isPlayed(keys[x.row]):
                if keys[x.row].active:
                    x.fill = 0
                    scored.append([x.note, x.start])

    for x in messages[lastMsg:]:
        if x.time + 660 > tick:
            break
        if x.time + 660 == tick:
            lastMsg += 1
            if x.type == "note_on":
                if x.channel in channels:
                    if not [x.note, x.time] in scored:
                        x.velocity = 0
                    else:
                        scored.remove([x.note, x.time])
            bus_output(x, bus)
    for x in obstacles[lastObstacle:]:
        if x.start > tick:
            break
        if x.start == tick:
            lastObstacle += 1
            x.row = (x.note % rows)
            x.rect = pygame.Rect(((1280 / rows) * x.row + ((1280 / rows)/ 2)), 0, 15, x.length)
            obstaclesOnscreen.append(x)

while run:
    start = time.time()
    input()
    logic()
    output()
    tick +=1
    clock.tick(tps)
sys.exit
