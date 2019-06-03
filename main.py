import pygame
import mido
import time
import gameObjects
import parse
import scenes
import globalConst
import sys


clock = pygame.time.Clock()
screen = pygame.display.set_mode(globalConst.size)
scene = scenes.menu()

def output(scene):
    screen.fill(globalConst.colors["background"])
    scene.draw(screen)
    pygame.display.update()

while True:
    inpQ = pygame.event.get()
    if any(x.type == pygame.QUIT for x in inpQ): #check for window close
        print("BRUDER MUSS LOS")
        pygame.display.quit()
        pygame.quit()
        sys.exit(1)
    scene.update(inpQ)
    output(scene)
    scene = scene.next_scene()
    clock.tick(globalConst.tps)
