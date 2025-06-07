import pygame
from typing import Union, TYPE_CHECKING
pygame.init()
screen = pygame.display.set_mode((950, 840))

if TYPE_CHECKING:
    from views.towers import ArcherTower, BombTower, TeslaTower
    from views.buildings import House, TownHall
    from views.player_abilities import Bomb
    from views.enemies import Ghoul, Golem, Wizard, Enemy

height = screen.get_height()
width = screen.get_width()

class GameInfo:
    def __init__(self):
        self.tower_list: list[ArcherTower | BombTower | TeslaTower] = []
        self.building_list: list[House | TownHall] = []
        self.all_purchasables: list[ItemGroup] = []
        self.enemy_list: list[Enemy] = []
        self.unattackable_list: list[Bomb] = []

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

class ItemGroup:
    def __init__(self):
        self.broken: bool
        self.pos: tuple[int, int]
        self.title: str
        self.current_health: int
        self.base_health: int
        self.image: pygame.Surface
        self.image_rect: pygame.Rect
        self.current_level: int

    def take_damage(self, damage_amount: int) -> None:
        self.current_health -= damage_amount
        if self.current_health <= 0:
            self.broken = True
    
    def repair(self, repair_amount: int) -> None:
        if self.current_health + repair_amount >= self.base_health:
            self.current_health = self.base_health
        else:
            self.current_health += repair_amount



class EnemyGroup:
    pass