import pygame
from typing import Union, TYPE_CHECKING
pygame.init()
screen = pygame.display.set_mode((850, 700))

if TYPE_CHECKING:
    from Views.towers import ArcherTower, BombTower
    from Views.buildings import House, TownHall
    from Views.playerabilities import Bomb
    from Views.enemies import Ghoul, Golem


class GameInfo:
    def __init__(self):
        self.tower_list: list[ArcherTower | BombTower] = []
        self.building_list: list[House | TownHall] = []
        self.all_purchasables: list[ItemGroup] = []
        self.enemy_list: list[EnemyGroup] = []
        self.unattackable_list: list[Bomb] = []

        self.gold: int = 6
        self.player_click_damage: int = 0
        self.caps: dict[str: int] = {
            'ArcherTowerCap' : 4,
            'HouseCap' : 3,
            'BombTowerCap' : 1,
            'BombCap': 1
        }
    
    def update(self) -> None:
        self.all_purchasables = self.building_list + self.tower_list

class ItemGroup:
    def __init__(self):
        self.broken: bool
        self.pos: tuple[int, int]
        self.title: str

    def take_damage(self, damage_amount: int) -> None:
        self.current_health -= damage_amount
        if self.current_health <= 0:
            self.broken = True


class EnemyGroup:
    pass