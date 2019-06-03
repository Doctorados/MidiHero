import mido
import time
import pygame.midi
import gameObjects
import parse
import scenes

pygame.init()
tps = 120
rows = 4
clock = pygame.time.Clock()
size = (1280, 720) #window size
screen = pygame.display.set_mode(size)
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

while True:
     scene.update()
     output(scene)
     scene = scene.next_scene()
     clock.tick(tps)
