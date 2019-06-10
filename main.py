import pygame
import scenes
import globalConst
import sys


clock = pygame.time.Clock()
screen = pygame.display.set_mode(globalConst.size, pygame.HWSURFACE)
scene = scenes.menu()

def output(scene):
    screen.fill(globalConst.colors["background"])
    scene.draw(screen)
    pygame.display.update()

while True:
    inpQ = pygame.event.get()
    if any(x.type == pygame.QUIT for x in inpQ): #check for window close
        pygame.display.quit()
        pygame.quit()
        sys.exit(1)
    scene.update(inpQ)
    output(scene)
    scene = scene.next_scene()
    clock.tick(globalConst.tps)
