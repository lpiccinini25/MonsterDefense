import pygame
from pygame import Color
from Views.tower import Tower

class placeItem:
    def __init__(self, tower):
        self.pos = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 100, 50)
        self.curr_color = Color(200, 100, 200)
        self.hover_color = Color(100, 100, 100)
        self.default_color = Color(200, 100, 200)
        self.tower = "archer"
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.curr_color, self.rect)
        # Add text rendering here

    def update(self, towerList):
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.placeTower(self.pos, towerList)
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                return False
        
        return True

    def placeTower(self, pos, towerList):
        towerList.append(Tower(self.tower, pos))
        
