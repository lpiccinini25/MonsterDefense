import pygame
from pygame import Color
from globals import screen
from fonts import font
import functions

from towerModels import ArcherTowerLevel2

class Upgrade:
    def __init__(self, x: int, y: int, upgradeName: str, upgradeModel, cost: int):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 100, 50)
        self.curr_color = Color(200, 100, 200)
        self.hover_color = Color(100, 100, 100)
        self.text_color = Color(255, 255, 255)
        self.upgradeName = upgradeName
        self.upgradeModel = upgradeModel
        self.cost = cost
        self.clicked = False

    def draw(self):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.curr_color, self.rect)
        functions.display_text(self.upgradeName + " costs: " + str(self.cost), self.text_color, font, self.x, self.y)

class UpgradeShop:
    def __init__(self, towerInstance):
        self.towerInstance = towerInstance

        match self.towerInstance.tower:
            case "ArcherTower":
                self.upgrades = [
                    Upgrade(800, 50, "Level 2", ArcherTowerLevel2(), 4)
                ]

    def drawShop(self):
        for upgrade in self.upgrades:
            upgrade.draw()

    def updateUpgrades(self, event_list, gold):
        mouse_pos = pygame.mouse.get_pos()

        for upgrade in self.upgrades:
            if upgrade.rect.collidepoint(mouse_pos):
                upgrade.curr_color = upgrade.hover_color

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if gold >= 4:
                            gold -= 4
                            self.towerInstance.upgradeTower("assets/"+upgrade.upgradeModel.title+".png", upgrade.upgradeModel)
                            return gold
        
        return gold
                        