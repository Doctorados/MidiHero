import pygame
import gameObjects

class score:
    def __init__(self, score):
        self.myfont = pygame.font.SysFont('Arial', 30)
        self.score = score
        self.score.calc_score()
        self.menuBg = pygame.Rect(420, 0, 440, 720)
    def draw(self, screen, colors):
        line1 = "Notes hit: " + str(self.score.scored)
        line2 = "Efficiency: " + str(self.score.efficiency)
        line3 = "Final Score:" + str(self.score.final)
        text1 = self.myfont.render(line1, True, colors["background"])
        text2 = self.myfont.render(line2, True, colors["background"])
        text3 = self.myfont.render(line3, True, colors["background"])
        pygame.draw.rect(screen, colors["primary"], self.menuBg, 0)
        screen.blit(text1,(420,100))
        screen.blit(text2,(420,200))
        screen.blit(text3,(420,300))
    def update(self):
        pass
