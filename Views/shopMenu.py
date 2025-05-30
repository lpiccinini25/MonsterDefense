import pygame
from pygame import Color
from globals import screen

class Purchasable:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, 100, 50)
        self.curr_color = Color(200, 100, 200)
        self.hover_color = Color(100, 100, 100)
        self.default_color = Color(200, 100, 200)
        self.text = text
        self.item = "archer"
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.curr_color, self.rect)
        # Add text rendering here

    def is_clicked(self, pos):
        print("click" + self.item)
        return True, self.item

class Shop:
    def __init__(self):
        self.purchasables = [
            Purchasable(50, 50, "banana")
        ]

    def drawPurchasables(self):
        for purchasable in self.purchasables:
            purchasable.draw(screen)
        # Add text rendering here

    def updatePurchasables(self, event_list):
        mouse_pos = pygame.mouse.get_pos()

        for purchasable in self.purchasables:
            if purchasable.rect.collidepoint(mouse_pos):
                purchasable.curr_color = purchasable.hover_color

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        return purchasable.is_clicked(mouse_pos)
        
        return False, None