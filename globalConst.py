import pygame
pygame.init()
tps = 160 #ticks per second
rows = 4
keybinds = [pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_l]
size = (1280, 720) #window size
colors = {"primary": ( 255, 255, 255),
    "secondary": ( 210, 60, 34),
    "background": ( 22, 22, 24),
    }
font = pygame.font.SysFont('Courier New', 30, bold=True)

def update_dif(dif):
    global rows
    global keybinds
    if dif == 1:
        rows = 4
        keybinds = [pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_l]
    if dif == 2:
        rows = 8
        keybinds = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l]
