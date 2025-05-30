from globals import screen
import pygame

class TownHall:
    def __init__(self):
        self.pos = (screen.get_width()/2, screen.get_height()/2)
        self.image = pygame.image.load("assets/TownHall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.image_rect = self.image.get_rect(center=self.pos)
        self.health = 5000
    
    def draw(self, screen):
        screen.blit(self.image, self.image_rect)