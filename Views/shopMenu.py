import pygame
from pygame import Color
from globals import screen
import functions

from fonts import font

class Purchasable:
    def __init__(self, x, y, text, item, cost):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 100, 50)
        self.curr_color = Color(200, 100, 200)
        self.hover_color = Color(100, 100, 100)
        self.default_color = Color(200, 100, 200)
        self.text_color = Color(255, 255, 255)
        self.text = text
        self.item = item
        self.cost = cost
        self.clicked = False

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.curr_color, self.rect)
        functions.display_text(self.text + " costs: " + str(self.cost), self.text_color, font, self.x, self.y)

    def is_clicked(self, pos):
        print("click" + self.item)
        return True, self.item, self.cost

class Shop:
    def __init__(self):

        inc = 60
        base = 75
        y = 50
        self.purchasables = [
            Purchasable(base, y, "Archer Tower", "ArcherTower", 2),
            Purchasable(base, y+inc, "House", "House", 2),
            Purchasable(base, y+inc*2, "Bomb Tower", "BombTower", 6)
        ]

    def drawPurchasables(self):
        for purchasable in self.purchasables:
            purchasable.draw(screen)
        # Add text rendering here

    def updatePurchasables(self, event_list, gold):
        mouse_pos = pygame.mouse.get_pos()

        for purchasable in self.purchasables:
            if purchasable.rect.collidepoint(mouse_pos):
                purchasable.curr_color = purchasable.hover_color

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if gold >= purchasable.cost:
                            return purchasable.is_clicked(mouse_pos)
                        
        
        return False, None, None