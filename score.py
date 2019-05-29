import pygame
import gameObjects

class score:
    def __init__(self, score):
        self.myfont = pygame.font.SysFont('Arial', 30)
        self.score = score
        self.score.calc_score()
    def draw(self, screen, colors):
        line1 = "Notes hit:" + str(self.score.scored)
        line2 = "Efficiency" + str(self.score.multiplier)
        line3 = "Final Score:" + str(self.score.final)
        text1 = self.myfont.render(line1, True, colors["secondary"])
        text2 = self.myfont.render(line2, True, colors["secondary"])
        text3 = self.myfont.render(line3, True, colors["secondary"])
        screen.blit(text1,(0,0))
        screen.blit(text2,(0,100))
        screen.blit(text3,(0,200))
    def update(self):
        pass
