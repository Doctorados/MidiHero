import mido
import time
import pygame.midi
import gameObjects
import parse
import level
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)


run = True
pygame.init()
file ="./south_park.mid"
tps = 160
rows = 4
clock = pygame.time.Clock()
size = (1280, 720) #window size
screen = pygame.display.set_mode(size)
channels = [0]
level = level.level(file, tps, channels, rows)


def output(scene):
    screen.fill((0, 0, 0))
    scene.draw(screen, RED, WHITE)
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
        print(level.run)
        input()
        logic(level)
        output(level)
    print(level.score.calc_score())
    run = False
sys.exit
