class TowerModel:
    def __init__(self):
        self.title: str
        self.range: int
        self.damage: int
        self.default_attack_cooldown: int

class ArcherTowerLevel2(TowerModel):
    def __init__(self):
        self.title = "ArcherTowerLevel2"
        self.range = 275
        self.damage = 30
        self.default_attack_cooldown = 90

class TownHallLevel2(TowerModel):
    def __init__(self):
        self.title = "TownHallLevel2"
        self.ArcherTowerCap = 6
        self.HouseCap = 5
        self.BombTowerCap = 2