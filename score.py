import pygame
import gameObjects

class score:
    def __init__(self, score, tps):
        self.myfont = pygame.font.SysFont('Arial', 30, bold=True)
        self.score = score
        self.score.calc_score()
        self.menuBg = pygame.Rect(420, 0, 440, 720)
        self.tick = 0
        self.tps = tps
    def draw(self, screen, colors):
        line1 = list("Notes hit: " + str(self.score.scored))
        line2 = list("Efficiency: " + str(self.score.efficiency) +"%")
        line3 = list("Final Score: " + str(self.score.final))
        for i in range (0, (self.tick//(self.tps//10))):
            text1 = self.myfont.render("".join(line1[0:i]), False, colors["secondary"])
            text2 = self.myfont.render("".join(line2[0:i]), False, colors["secondary"])
            text3 = self.myfont.render("".join(line3[0:i]), False, colors["secondary"])
            screen.blit(text1,(420,100))
            screen.blit(text2,(420,200))
            screen.blit(text3,(420,300))
    def update(self):
        self.tick += 1
