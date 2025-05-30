import pygame
from pygame import Color

class placeItem:
    def __init__(self, item):
        self.pos = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 100, 50)
        self.curr_color = Color(200, 100, 200)
        self.hover_color = Color(100, 100, 100)
        self.default_color = Color(200, 100, 200)
        self.item = "archer"
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.curr_color, self.rect)
        # Add text rendering here

    def is_clicked(self, pos):
        print("click" + self.item)
        return True, self.item