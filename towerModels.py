class TowerModel:
    def __init__(self):
        self.title: str
        self.range: int
        self.damage: int
        self.default_attack_cooldown: int

class TownHallLevel2(TowerModel):
    def __init__(self):
        self.title = "TownHallLevel2"
        self.ArcherTowerCap = 6
        self.HouseCap = 5
        self.BombTowerCap = 2
        self.RepairCap = 2
        self.TeslaTowerCap = 2