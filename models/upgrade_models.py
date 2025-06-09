from globals import GameInfo
from typing import Optional

class UpgradeModel:
    def __init__(self):
        #Basic Info
        self.title: str
        self.level: int
        self.cost: int

        #Stats
        self.attack_range: int
        self.damage: int
        self.base_attack_cooldown: int

        #Optionals
        self.bolt_spread_amount: Optional[int]
        self.base_gold_generation_cooldown: Optional[int]

class ArcherTowerLevel2(UpgradeModel):
    def __init__(self):
        #Basic Info
        self.title: str = "ArcherTowerLevel2"
        self.level: int = 2
        self.cost: int = 5

        #Stats
        self.attack_range: int = 250
        self.damage: int = 40
        self.base_attack_cooldown: int = 90

class ArcherTowerLevel3(UpgradeModel):
    def __init__(self):
        #Basic Info
        self.title: str = "ArcherTowerLevel3"
        self.level: int = 3
        self.cost: int = 15

        #Stats
        self.attack_range: int = 250
        self.damage: int = 70
        self.base_attack_cooldown: int = 80


class TeslaTowerLevel2(UpgradeModel):
    def __init__(self):
        #Basic Info
        self.title: str = "TeslaTowerLevel2"
        self.level: int = 2
        self.cost: int = 10

        #Stats
        self.attack_range: int = 175
        self.damage: int = 15
        self.base_attack_cooldown: int = 130

        #Tesla Tower Specific
        self.bolt_spread_amount: Optional[int] = 8

class TownHallLevelUp(UpgradeModel):
    def __init__(self, current_level: int):
        #Basic Info
        self.title: str = "TownHallLevel2"
        self.level: int = current_level + 1
        self.cost: int = 10 + current_level * 5

class HouseLevel2(UpgradeModel):
    def __init__(self):
        #Basic Info
        self.title: str = "HouseLevel2"
        self.level: int = 2
        self.cost: int = 2

        #Stats
        self.base_gold_generation_cooldown = 600
