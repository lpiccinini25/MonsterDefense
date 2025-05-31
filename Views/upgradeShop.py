import pygame
from pygame import Color
from globals import screen
from fonts import font
import functions

class Upgrade:
    def __init__(self, x: int, y: int, upgradeName: str, item: str, cost: int):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 100, 50)
        self.curr_color = Color(200, 100, 200)
        self.text_color = Color(255, 255, 255)
        self.upgradeName = upgradeName
        self.item = item
        self.cost = cost
        self.clicked = False

    def draw(self):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.curr_color, self.rect)
        functions.display_text(self.upgradeName, self.text_color, font, self.x, self.y)

    def is_clicked(self, pos):
        print("click" + self.item)
        return True, self.item, self.cost

class UpgradeShop:
    def __init__(self, towerInstance):

        match towerInstance.tower:
            case "ArcherTower":
                self.upgrades = [
                    Upgrade(800, 50, "Level 2", "ArcherTower", 2)
                ]

    def drawShop(self):
        for upgrade in self.upgrades:
            upgrade.draw()

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