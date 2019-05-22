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
file ="./number_one.mid"
busName = mido.get_output_names()[0]
bus = mido.open_output(busName)
mid = mido.MidiFile(file)
tps = 162
tick = 0
rows = 12
keybinds = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k]
clock = pygame.time.Clock()
print(pygame.display.get_init())
print(pygame.display.get_driver())
size = (1280, 720) #window size
screen = pygame.display.set_mode(size)
midiHeroTrack = parse.midi_tick2(mid, tps)
messages = midiHeroTrack.track
instruments = midiHeroTrack.instruments
print(messages)
print(instruments)
obstacles = gameObjects.create_obstacles(messages,  {2})
obstaclesOnscreen = []

def output():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, GREEN, pygame.Rect(0, 600, 1280, 2), 0)
    for x in obstaclesOnscreen:
        pygame.draw.rect(screen, WHITE, x, 1)
    pygame.display.flip()

def input():
    global tps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                tps = tps*2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                tps = tps / 2


def logic():
    global lastMsg
    global lastObstacle
    for x in obstaclesOnscreen:
        if x.rect[1] == 600:
            obstaclesOnscreen.remove(x)
        else:
            x.rect[1] = x.rect[1] + 2
    for x in messages[lastMsg:]:
        if x.time + 240 > tick:
            break
        if x.time + 240 == tick:
            lastMsg += 1
            bus.send(x)
    for x in obstacles[lastObstacle:]:
        if x.start > tick:
            break
        if x.start == tick:
            lastObstacle += 1
            x.rect = pygame.Rect((1280 // rows) * (x.note % rows), 0, 50, x.length)
            obstaclesOnscreen.append(x)

while run:
    start = time.time()
    input()
    logic()
    output()
    tick +=1
    clock.tick(tps)
sys.exit
