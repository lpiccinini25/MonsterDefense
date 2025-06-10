import functions
import pygame
import colors
from globals import GameInfo
from typing import Optional
from models.upgrade_models import UpgradeModel

class ItemModel:
    def __init__(self):
        #Basic Info 
        self.pos: tuple[int, int]
        self.title: str


        #Image Stuff
        self.image_width: int

        self.image: pygame.Surface
        self.image_rect: pygame.Rect
        self.image_hover: pygame.Rect
        self.image_hover_rect: pygame.Rect
        self.image_broken: pygame.Surface
        self.image_broken_rect: pygame.Rect



        self.broken: bool
        self.current_health: int
        self.base_health: int
        self.current_level: int

        #Repair Time
        self.base_repair_time: int
        self.repair_time: int

    def load_images_and_rects(self) -> None:
        self.image, self.image_rect = functions.load_image_and_rect(self.title, self.image_width, self.pos)
        self.hover_image, self.hover_image_rect = functions.load_image_and_rect(self.title, int(self.image_width*3/4), self.pos)
        self.broken_image, self.broken_image_rect = functions.load_image_and_rect("Broken"+self.title, self.image_width, self.pos)
    
    def draw(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if not self.broken:
            if self.image_rect.collidepoint(mouse_pos):
                functions.display_image_static(self.hover_image, self.hover_image_rect)
                functions.display_health_bar(self, self.current_health, self.base_health, colors.WHITE) 
            else:
                functions.display_image_static(self.image, self.image_rect)
                functions.display_health_bar(self, self.current_health, self.base_health, colors.WHITE)
        else:
            functions.display_image_static(self.broken_image, self.broken_image_rect)
            functions.display_respawn_bar(self, self.repair_time, self.base_repair_time, colors.WHITE)

    def take_damage(self, damage_amount: int) -> None:
        self.current_health -= damage_amount
        if self.current_health <= 0:
            self.broken = True
    
    def repair(self, repair_amount: int) -> None:
        if self.current_health + repair_amount >= self.base_health:
            self.current_health = self.base_health
        else:
            self.current_health += repair_amount

    #quotes added on UpgradeModel to avoid type checking error at runtime
    def upgrade_tower(self, newImage: str, upgrade_model: "UpgradeModel", game_info: GameInfo) -> None:
        self.current_level += 1
        self.damage = upgrade_model.damage
        self.attack_range = upgrade_model.attack_range
        self.base_attack_cooldown = upgrade_model.base_attack_cooldown
        self.image = pygame.image.load(newImage).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)

    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> Optional[bool]:
        return False
    
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
        self.damage: int = 10
        self.base_attack_cooldown: int = 180

        #Broken/Repair
        self.base_repair_time: int = 2000