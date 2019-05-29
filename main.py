import mido
import time
import pygame.midi
import gameObjects
import parse
import level
import score
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)


run = True
pygame.init()
file ="./midi/south_park.mid"
tps = 160
rows = 4
clock = pygame.time.Clock()
size = (1280, 720) #window size
screen = pygame.display.set_mode(size)
channels = [0,1,2,3,6,7,8]
level = level.level(file, tps, channels, rows)
colors = {"primary": ( 255, 255, 255),
    "secondary": ( 0, 255, 0),
    "background": ( 0, 0, 0),
    }

def output(scene):
    screen.fill(colors["background"])
    scene.draw(screen, colors)
    pygame.display.flip()
    clock.tick(tps)

def logic(scene):
    scene.update()

def input():
    keybinds = [pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_l]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key in keybinds:
                i = keybinds.index(event.key)
                level.keys[i].switch(True)
        if event.type == pygame.KEYUP:
            if event.key in keybinds:
                i = keybinds.index(event.key)
                level.keys[i].switch(False)




while run:
    while level.run:
         input()
         logic(level)
         output(level)
    print(level.score.calc_score())
    score= score.score(level.score)
    while True:
        input()
        logic(score)
        output(score)
    run = False
sys.exit
