import pygame
import functions
import colors
from typing import Union, TYPE_CHECKING, Optional
pygame.init()
screen = pygame.display.set_mode((950, 840))

if TYPE_CHECKING:
    from views.towers import ArcherTower, BombTower, TeslaTower
    from views.buildings import House, TownHall
    from views.player_abilities import Bomb
    from views.enemies import Ghoul, Golem, Wizard, Enemy
    from models.upgrade_models import UpgradeModel
    from models.item_models import ItemModel

height = screen.get_height()
width = screen.get_width()

class GameInfo:
    def __init__(self):
        self.tower_list: list[ItemModel] = []
        self.building_list: list[ItemModel] = []
        self.all_purchasables: list[ItemModel] = []
        self.enemy_list: list[Enemy] = []
        self.unattackable_list: list[Bomb] = []
        self.point_total: int = 0

        self.gold: int = 6
        self.player_click_damage: int = 0
        self.caps: dict[str: int] = {
            'ArcherTowerCap' : 4,
            'HouseCap' : 3,
            'BombTowerCap' : 1,
            'BombCap': 1,
            'RepairCap': 1,
            'TeslaTowerCap': 1
        }
    
    def update(self) -> None:
        self.all_purchasables = list(self.building_list) + list(self.tower_list)



class EnemyGroup:
    pass