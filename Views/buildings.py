from globals import screen, GameInfo
from models.item_models import ItemModel
from models.upgrade_models import UpgradeModel
import colors
import functions
import pygame

class building(ItemModel):
    def __init__(self, title, pos):
        #Basic Info
        self.pos: tuple[int, int] = pos
        self.title: str = title

        #Image
        self.image_width: int

        self.broken: bool = False


        self.current_level: int = 1

class House(building):
    def __init__(self, title: str, pos: tuple[int, int]) -> None:
        super().__init__(title, pos)
        #Image 
        self.image_width: int = 30
        self.load_images_and_rects()

        self.base_repair_time: int = 2000
        self.repair_time: int = self.base_repair_time


        self.base_health: int = 100
        self.current_health: int = self.base_health
        self.base_gold_generation_cooldown: int = 1000
        self.gold_generation_cooldown: int = self.base_gold_generation_cooldown

    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> bool:

        self.draw()

        if not self.broken:
            if self.gold_generation_cooldown == 0:
                self.gold_generation_cooldown = self.base_gold_generation_cooldown
                game_info.gold += 1
            else:
                self.gold_generation_cooldown -= 1
        elif self.repair_time != 0:
            self.repair_time -= 1
        else:
            self.repair_time = self.base_repair_time
            self.broken = False
            self.current_health = self.base_health
        
        if functions.is_clicked_on(self.image_rect, event_list):
            return True
        return False
    
    def upgrade_tower(self, newImage: str, upgrade_model: UpgradeModel, game_info: GameInfo) -> None:
        self.current_level += 1
        if upgrade_model.base_gold_generation_cooldown is not None:
            self.base_gold_generation_cooldown = upgrade_model.base_gold_generation_cooldown
        self.image, self.rect_image = functions.load_image_and_rect(upgrade_model.title, 30, self.pos)

class TownHall(building):
    def __init__(self, title: str, pos: tuple[int, int]):
        super().__init__(title, pos)
        self.broken: bool = False
        self.title: str = "TownHall"
        self.pos = (int(screen.get_width()/2), int(screen.get_height()/2))

        #Image 
        self.image_width: int = 75
        self.load_images_and_rects()

        self.base_health: int = 1000
        self.current_health: int = self.base_health

    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> bool:
        self.draw()
        
        if functions.is_clicked_on(self.image_rect, event_list):
            return True
        return False

    def draw(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if not self.broken:
            if self.image_rect.collidepoint(mouse_pos):
                functions.display_image_static(self.hover_image, self.hover_image_rect)
                functions.display_health_bar(self, self.current_health, self.base_health, colors.WHITE, 50, 20) 
            else:
                functions.display_image_static(self.image, self.image_rect)
                functions.display_health_bar(self, self.current_health, self.base_health, colors.WHITE, 50, 20)

    def upgrade_tower(self, newImage: str, tower_model: UpgradeModel, game_info: GameInfo):
        game_info.caps['ArcherTowerCap'] += 2
        game_info.caps['HouseCap'] += 2
        game_info.caps['BombTowerCap'] += 1
        game_info.caps['TeslaTowerCap'] += 1

        self.image = pygame.image.load(newImage).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.image_rect = self.image.get_rect(center=self.pos)

        self.current_level += 1