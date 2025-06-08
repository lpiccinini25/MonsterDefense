from globals import screen, ItemGroup, GameInfo
from models.upgrade_models import UpgradeModel
import functions
import pygame

class building(ItemGroup):
    def __init__(self, title, pos):
        self.pos: tuple[int, int] = pos
        self.title: str = title

        self.broken: bool = False

        self.image: pygame.Surface = pygame.image.load("assets/"+title+".png")
        self.image.set_colorkey((0, 0, 0))

        self.current_level: int = 1

class House(building):
    def __init__(self, title: str, pos: tuple[int, int]) -> None:
        super().__init__(title, pos)

        self.base_repair_time: int = 2000
        self.repair_time: int = self.base_repair_time

        self.size: int = 30
        self.image: pygame.Surface = pygame.transform.scale(self.image, (self.size, self.size))
        self.image_rect: pygame.Rect = self.image.get_rect(center=self.pos)

        self.broken_image: pygame.Surface = pygame.image.load("assets/BrokenHouse.png").convert()
        self.broken_image.set_colorkey((0, 0, 0))
        self.broken_image = pygame.transform.scale(self.broken_image, (30, 30))
        self.broken_image_rect: pygame.Rect = self.broken_image.get_rect(center=self.pos)

        self.base_health: int = 100
        self.current_health: int = self.base_health
        self.defaultGoldGenerationCoolDown: int = 1000
        self.goldGenerationCoolDown: int = self.defaultGoldGenerationCoolDown

    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> None:

        self.draw()

        if not self.broken:
            if self.goldGenerationCoolDown == 0:
                self.goldGenerationCoolDown = self.defaultGoldGenerationCoolDown
                game_info.gold += 1
            else:
                self.goldGenerationCoolDown -= 1
        elif self.repair_time != 0:
            self.repair_time -= 1
        else:
            self.repair_time = self.base_repair_time
            self.broken = False
            self.current_health = self.base_health
            
    def draw(self) -> None:
        if not self.broken:
            screen.blit(self.image, self.image_rect)
            health_bar_color = (255, 255, 255)
            functions.display_health_bar(self, self.current_health, self.base_health, health_bar_color)
        else:
            screen.blit(self.broken_image, self.broken_image_rect)
            respawn_bar_color = (255, 255, 255)
            functions.display_respawn_bar(self, self.repair_time, self.base_repair_time, respawn_bar_color)

class TownHall(building):
    def __init__(self, title: str, pos: tuple[int, int]):
        super().__init__(title, pos)
        self.broken: bool = False
        self.title: str = "TownHall"
        self.pos = (int(screen.get_width()/2), int(screen.get_height()/2))

        self.size: int = 75
        self.image: pygame.Surface = pygame.transform.scale(self.image, (self.size, self.size))
        self.image_rect: pygame.Rect = self.image.get_rect(center=self.pos)
        self.base_health: int = 1000
        self.current_health: int = self.base_health

    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> bool:
        self.draw()
        
        if functions.is_clicked_on(self.image_rect, event_list):
            return True
        return False
    
    def draw(self) -> None:
        screen.blit(self.image, self.image_rect)
        health_bar_color = (255, 255, 255)
        functions.display_health_bar(self, self.current_health, self.base_health, health_bar_color, override_size=50, override_gap=21)
        
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