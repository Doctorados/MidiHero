import mido
import time
import pygame.midi
import gameObjects
import parse
import scenes



run = True
pygame.init()
file ="./midi/south_park.mid"
tps = 160
rows = 4
clock = pygame.time.Clock()
size = (1280, 720) #window size
screen = pygame.display.set_mode(size)
channels = [0,1]
scene = scenes.menu(rows, tps)
colors = {"primary": ( 255, 255, 255),
    "secondary": ( 0, 255, 0),
    "background": ( 0, 0, 0),
    }
font = pygame.font.SysFont('Courier New', 30, bold=True)

def output(scene):
    screen.fill(colors["background"])
    scene.draw(screen, colors, font)
    pygame.display.flip()

def inp(scene):
    keybinds = [pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_l]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key in keybinds:
                i = keybinds.index(event.key)
                scene.inpQ[i] = True
        if event.type == pygame.KEYUP:
            if event.key in keybinds:
                i = keybinds.index(event.key)
                scene.inpQ[i] = False
while run:
     inp(scene)
     scene.update()
     output(scene)
     scene = scene.next_scene()
     clock.tick(tps)

run = False
sys.exit
