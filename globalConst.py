import pygame
pygame.init()
tps = 160 #ticks per second
rows = 8
size = (1280, 720) #window size
colors = {"primary": ( 255, 255, 255),
    "secondary": ( 0, 255, 0),
    "background": ( 0, 0, 0),
    }
font = pygame.font.SysFont('Courier New', 30, bold=True)
if rows == 4:
    keybinds = [pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_l]
else:
    keybinds = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l]
