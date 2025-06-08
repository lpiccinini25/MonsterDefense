from typing import Optional

class EnemyModel:
    def __init__(self):
        #Basic Info
        self.title: str
        self.points: int

        #Image Size
        self.size: int

        #Scaling
        self.health_scaling_factor: int
        self.damage_scaling_factor: int
        self.speed_scaling_factor: int

        #Starting Stats
        self.start_damage: int
        self.start_health: int
        self.start_speed: int

        #Cooldown
        self.base_attack_cooldown: int
        self.attack_range: Optional[int]

class GhoulModel(EnemyModel):
    def __init__(self):
        self.title = "Ghoul"
        self.points = 5

        self.size: int = 25

        self.health_scaling_factor: int = 30
        self.damage_scaling_factor: int = 14
        self.speed_scaling_factor: int = 2

        self.start_damage: int = 15
        self.start_health: int = 80
        self.start_speed: int = 2

        self.base_attack_cooldown: int = 80
        self.attack_range: Optional[int] = None

class GolemModel(EnemyModel):
    def __init__(self):
        self.title = "Golem"
        self.points = 15

        self.size: int = 35

        self.health_scaling_factor: int = 100
        self.damage_scaling_factor: int = 5
        self.speed_scaling_factor: int = 2

        self.start_damage: int = 10
        self.start_health: int = 260
        self.start_speed: int = 2

        self.base_attack_cooldown: int = 80
        self.attack_range: Optional[int] = None

class WizardModel(EnemyModel):
    def __init__(self):
        self.title = "Wizard"
        self.points = 10

        self.size: int = 25

        self.health_scaling_factor: int = 20
        self.damage_scaling_factor: int = 5
        self.speed_scaling_factor: int = 2

        self.start_damage: int = 10
        self.start_health: int = 60
        self.start_speed: int = 2

        self.base_attack_cooldown: int = 120
        self.attack_range: Optional[int] = 120