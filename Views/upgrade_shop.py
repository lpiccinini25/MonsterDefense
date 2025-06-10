import pygame
from pygame import Color
from globals import screen, GameInfo
from fonts import font
import functions

from models.item_models import ItemModel
from models.upgrade_models import ArcherTowerLevel2, ArcherTowerLevel3, TeslaTowerLevel2, TownHallLevelUp, HouseLevel2, UpgradeModel

class Upgrade:
    def __init__(self, x: int, y: int, upgrade_name: str, upgrade_model: UpgradeModel, current_item_level: int):

        #Image
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 100, 50)
        self.rect.center = (self.x, self.y)
        self.curr_color = (200, 100, 200)
        self.cannot_buy_color = (50, 50, 50)
        self.hover_color = (100, 100, 100)
        self.text_color = (255, 255, 255)

        #Basic Info
        self.upgrade_name: str = upgrade_name
        self.upgrade_model: UpgradeModel = upgrade_model
        self.cost: int = upgrade_model.cost
        self.upgrade_level: int = upgrade_model.level #level of the potential upgrade
        self.current_item_level = current_item_level #level of the item being upgraded
        self.clicked = False

        #State
        self.can_buy: bool = False

    def draw(self) -> None:
        if self.can_buy:
            pygame.draw.rect(screen, self.curr_color, self.rect)
            functions.display_text(self.upgrade_name + " costs: " + str(self.cost), self.text_color, font, self.x, self.y)
        else:
            pygame.draw.rect(screen, self.cannot_buy_color, self.rect)
            functions.display_text(self.upgrade_name + " costs: " + str(self.cost), self.text_color, font, self.x, self.y)

    def check_can_buy(self, game_info: GameInfo) -> None:
        if game_info.gold >= self.cost and self.upgrade_level == self.current_item_level + 1:
            self.can_buy = True
        else:
            self.can_buy = False


class UpgradeShop:
    def __init__(self, tower_instance: ItemModel) -> None:
        self.tower_instance: ItemModel = tower_instance
        current_level: int = self.tower_instance.current_level

        y_base: int = 50
        y_inc: int = 55
        match self.tower_instance.title:
            case "ArcherTower":
                self.upgrades = [
                    Upgrade(800, y_base, "Level 2", ArcherTowerLevel2(), current_level),
                    Upgrade(800, y_base+y_inc, "Level 3", ArcherTowerLevel3(), current_level)
                ]
            case "TownHall": 
                self.upgrades = [
                    Upgrade(800, y_base, "Level +1", TownHallLevelUp(current_level), current_level)
                ]
            case "TeslaTower":
                self.upgrades = [
                    Upgrade(800, y_base, "Level 2", TeslaTowerLevel2(), current_level)
                ]
            case "House":
                self.upgrades = [
                    Upgrade(800, y_base, "Level 2", HouseLevel2(), current_level)
                ]
            case _:
                self.upgrades = []

    def drawShop(self) -> None:
        for upgrade in self.upgrades:
            upgrade.draw()

    def updateUpgrades(self, event_list: list[pygame.event.Event], game_info: GameInfo) -> None:
        mouse_pos = pygame.mouse.get_pos()

        for upgrade in self.upgrades:
            upgrade.check_can_buy(game_info)
            if upgrade.rect.collidepoint(mouse_pos): 
                upgrade.curr_color = upgrade.hover_color

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if upgrade.can_buy:
                            game_info.gold -= upgrade.cost
                            self.tower_instance.upgrade_tower("assets/"+upgrade.upgrade_model.title+".png", upgrade.upgrade_model, game_info)