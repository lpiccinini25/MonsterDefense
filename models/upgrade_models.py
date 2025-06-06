from globals import GameInfo

class UpgradeModel:
    def __init__(self):
        self.title: str
        self.attack_range: int
        self.damage: int
        self.base_attack_cooldown: int

class ArcherTowerLevel2(UpgradeModel):
    def __init__(self):
        self.title: str = "ArcherTowerLevel2"
        self.attack_range: int = 250
        self.damage: int = 25
        self.base_attack_cooldown: int = 90

class TownHallLevelUp(UpgradeModel):
    def __init__(self):
        self.title: str = "TownHallLevel2"