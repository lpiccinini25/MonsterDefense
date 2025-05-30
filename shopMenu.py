import pygame
from globals import screen

class Purchasable:
    def __init__(self, x, y, color, text):
        self.rect = pygame.Rect(x, y, 100, 50)
        self.color = color
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Add text rendering here

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Shop:
    def __init__(self, x, y, w, h, color, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Add text rendering here

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)