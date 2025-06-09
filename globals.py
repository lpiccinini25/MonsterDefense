import pygame
import functions
import colors
from typing import Union, TYPE_CHECKING, Optional
pygame.init()
screen = pygame.display.set_mode((950, 840))

if TYPE_CHECKING:
    from views.towers import ArcherTower, BombTower, TeslaTower
    from views.buildings import House, TownHall
    from views.player_abilities import Bomb
    from views.enemies import Ghoul, Golem, Wizard, Enemy
    from models.upgrade_models import UpgradeModel

height = screen.get_height()
width = screen.get_width()

class GameInfo:
    def __init__(self):
        self.tower_list: list[ItemGroup] = []
        self.building_list: list[ItemGroup] = []
        self.all_purchasables: list[ItemGroup] = []
        self.enemy_list: list[Enemy] = []
        self.unattackable_list: list[Bomb] = []
        self.point_total: int = 0

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



class EnemyGroup:
    pass