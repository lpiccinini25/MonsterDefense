from globals import GameInfo
from typing import Optional

class UpgradeModel:
    def __init__(self):
        self.title: str
        self.attack_range: int
        self.damage: int
        self.base_attack_cooldown: int

        #Optionals
        self.bolt_spread_amount: Optional[int]

class ArcherTowerLevel2(UpgradeModel):
    def __init__(self):
        self.title: str = "ArcherTowerLevel2"
        self.attack_range: int = 250
        self.damage: int = 40
        self.base_attack_cooldown: int = 90


class TeslaTowerLevel2(UpgradeModel):
    def __init__(self):
        self.title: str = "TeslaTowerLevel2"
        self.attack_range: int = 175
        self.damage: int = 23
        self.base_attack_cooldown: int = 130

        self.bolt_spread_amount: Optional[int] = 8

class TownHallLevelUp(UpgradeModel):
    def __init__(self):
        self.title: str = "TownHallLevel2"
