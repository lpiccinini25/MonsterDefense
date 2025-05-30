import pygame
from pygame import Color

class Tower:
    def __init__(self, tower, pos):
        self.tower = tower
        self.pos = pos
        self.image = pygame.image.load("assets/"+tower+".png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)
        self.curr_color = Color(200, 100, 200)
    
    def draw(self, screen):
        screen.blit(self.image, self.image_rect)