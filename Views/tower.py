import pygame
from pygame import Color

class Tower:
    def __init__(self, tower, pos):
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 40, 40)
        self.curr_color = Color(200, 100, 200)
        self.tower = tower
        #self.image = pygame.image.load("assets/ArcherTower.png")
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.curr_color, self.rect)