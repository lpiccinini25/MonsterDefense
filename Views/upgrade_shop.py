import pygame
from pygame import Color
from globals import screen, ItemGroup
from fonts import font
import functions

from models.upgrade_models import ArcherTowerLevel2, ArcherTowerLevel3, TeslaTowerLevel2, TownHallLevelUp, UpgradeModel

class Upgrade:
    def __init__(self, x: int, y: int, upgrade_name: str, upgrade_model: UpgradeModel, cost: int, current_item_level: int):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 100, 50)
        self.curr_color = Color(200, 100, 200)
        self.hover_color = Color(100, 100, 100)
        self.text_color = Color(255, 255, 255)
        self.upgrade_name: str = upgrade_name
        self.upgrade_model: UpgradeModel = upgrade_model
        self.cost = cost
        self.clicked = False
        self.current_level = current_item_level

    def draw(self):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.curr_color, self.rect)
        functions.display_text(self.upgrade_name + " costs: " + str(self.cost), self.text_color, font, self.x, self.y)

class UpgradeShop:
    def __init__(self, tower_instance: ItemGroup):
        self.tower_instance = tower_instance
        current_level = self.tower_instance.current_level

        match self.tower_instance.title:
            case "ArcherTower":
                self.upgrades = [
                    Upgrade(800, 50, "Level 2", ArcherTowerLevel2(), 4, current_level),
                    Upgrade(800, 80, "Level 3", ArcherTowerLevel3(), 15, current_level)
                ]
            case "TownHall": 
                self.upgrades = [
                    Upgrade(800, 50, "Level +1", TownHallLevelUp(), 10+current_level*5, current_level)
                ]
            case "TeslaTower":
                self.upgrades = [
                    Upgrade(800, 50, "Level 2", TeslaTowerLevel2(), 8, current_level)
                ]
            case _:
                self.upgrades = []

    def drawShop(self):
        for upgrade in self.upgrades:
            upgrade.draw()

    def updateUpgrades(self, event_list, game_info):
        mouse_pos = pygame.mouse.get_pos()

        for upgrade in self.upgrades:
            if upgrade.rect.collidepoint(mouse_pos): 
                upgrade.curr_color = upgrade.hover_color

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if game_info.gold >= upgrade.cost:
                            game_info.gold -= upgrade.cost
                            self.tower_instance.upgrade_tower("assets/"+upgrade.upgrade_model.title+".png", upgrade.upgrade_model, game_info)