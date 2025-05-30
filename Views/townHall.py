from globals import screen
import pygame

class TownHall:
    def __init__(self):
        self.pos = (screen.get_width()/2, screen.get_height()/2)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 75, 75)
        self.image = pygame.image.load("assets/TownHall.png")
        self.health = 5000
    
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (75, 75)), self.pos)