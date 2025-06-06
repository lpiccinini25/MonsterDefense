class TowerModel:
    def __init__(self):
        #Image Info
        self.size: int

        #Tower Info
        self.title: str

        #Tower Stats
        self.attack_range: int
        self.base_health: int
        self.damage: int
        self.base_attack_cooldown: int

        #Repair Stats
        self.base_repair_time: int

class ArcherTowerModel(TowerModel):
    def __init__(self):
        #Image Info
        self.size: int = 30

        #Tower Info
        self.title: str = "ArcherTower"

        #Tower Stats
        self.attack_range: int = 200
        self.base_health: int = 200
        self.damage: int = 15
        self.base_attack_cooldown: int = 100

        #Repair Stats
        self.base_repair_time: int = 2000

class BombTowerModel(TowerModel):
    def __init__(self):
        #Image Info
        self.size: int = 30

        #Tower Info
        self.title: str = "BombTower"

        #Bomb Tower Stats
        self.attack_range: int = 125
        self.base_health: int = 150
        self.damage: int = 30
        self.base_attack_cooldown: int = 160

        #Broken/Repair
        self.base_repair_time: int = 2000

class TeslaTowerModel(TowerModel):
    def __init__(self):
        #Image Info
        self.size: int = 30

        #Tower Info
        self.title: str = "TeslaTower"

        #Bomb Tower Stats
        self.attack_range: int = 150
        self.base_health: int = 200
        self.damage: int = 20
        self.base_attack_cooldown: int = 180

        #Broken/Repair
        self.base_repair_time: int = 2000