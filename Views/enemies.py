import pygame
import random
from pygame import Color
import functions
from globals import screen, GameInfo

from typing import Optional
from models.enemy_models import EnemyModel
from models.item_models import ItemModel


class Enemy():
    def __init__(self, enemy_model: EnemyModel, scaling: float, pos: tuple[float, float]):

        self.title = enemy_model.title
        self.points = enemy_model.points


        self.pos: tuple[float, float] = pos
        self.scaling: float = scaling**2

        #Image
        self.image_width: int = enemy_model.size
        self.image: pygame.Surface = functions.load_image(self.title, self.image_width)
        self.image_rect: pygame.Rect = self.image.get_rect(center=self.pos)

        #Stats -- 
        #Health
        health_low_bound: int = int(enemy_model.start_health+self.scaling*enemy_model.health_scaling_factor*(0.5))
        health_high_bound: int = int(enemy_model.start_health+self.scaling*enemy_model.health_scaling_factor*(1))
        self.base_health: int = random.randint(health_low_bound, health_high_bound)
        self.current_health: int = self.base_health
        #Damage
        damage_low_bound: int = int(enemy_model.start_damage+self.scaling*enemy_model.damage_scaling_factor*(0.5))
        damage_high_bound: int = int(enemy_model.start_damage+self.scaling*enemy_model.damage_scaling_factor*(1))
        self.damage: int = random.randint(damage_low_bound, damage_high_bound)
        #Speed
        #Speed_scaling bc exponential increase in speed looks dumb
        speed_scaling: float = self.scaling**(0.5)
        speed_low_bound: int = int(enemy_model.start_speed+speed_scaling*enemy_model.speed_scaling_factor*(0.5))
        speed_high_bound: int = int(enemy_model.start_speed+self.scaling*enemy_model.speed_scaling_factor*(1))
        self.speed: int = random.randint(speed_low_bound, speed_high_bound)
        #Attack Cooldown
        self.base_attack_cooldown: int = enemy_model.base_attack_cooldown
        self.attack_cooldown: int = self.base_attack_cooldown
        #Attack Range
        self.attack_range: Optional[int] = enemy_model.attack_range

        #Status Effects
        self.on_click_slow_strength = 40
        self.on_click_slow_duration = 50
        self.slow_strength: int = 0
        self.slow_duration: int = 0
    
    def draw(self) -> None:
        screen.blit(self.image, self.image_rect)
        health_bar_color = (255, 0, 0)
        functions.display_health_bar(self, self.current_health, self.base_health, health_bar_color)
    
    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> None:
        self.on_click(event_list)
        self.moveAndAttack(game_info.all_purchasables)
        self.update_slow_status()

    def take_damage(self, damage_taken: int) -> None:
        self.current_health -= damage_taken
    
    def attack(self, building: ItemModel) -> None:
        building.take_damage(self.damage)
    
    def slow_enemy(self, slow_strength: int, slow_duration: int) -> None:
        self.slow_strength = slow_strength
        self.slow_duration = slow_duration
    
    def update_slow_status(self) -> None:
        if self.slow_duration == 0:
            self.slow_strength = 0
        else:
            self.slow_duration -= 1
    
    def on_click(self, event_list: list[pygame.event.Event]) -> None:
        if functions.is_clicked_on(self.image_rect, event_list):
            self.slow_enemy(self.on_click_slow_strength, self.on_click_slow_duration)
            

    def moveAndAttack(self, buildings: list[ItemModel]) -> None:
        minDistance = 2000000
        closestBuilding = None

        stepDistance = self.speed * 0.1 * ((100-self.slow_strength)/100)

        for building in buildings:
            if building.broken:
                continue
            curr_distance = ((building.pos[0]-self.pos[0])**2+(building.pos[1]-self.pos[1])**2)**0.5
            if curr_distance < minDistance:
                minDistance = curr_distance
                closestBuilding = building

        if closestBuilding is not None:
            dx = closestBuilding.pos[0] - self.pos[0]
            dy = closestBuilding.pos[1] - self.pos[1]
            
            distance = (dx**2 + dy**2)**0.5
            
            if -1 < distance < 1:
                if self.attack_cooldown == 0:
                    self.attack(closestBuilding)
                    self.attack_cooldown = self.base_attack_cooldown
                else:
                    self.attack_cooldown -= 1
            
            else:
                if distance != 0:
                    dx /= distance
                    dy /= distance

                new_x = self.pos[0] + dx * stepDistance
                new_y = self.pos[1] + dy * stepDistance

                self.pos = (new_x, new_y)
                self.image_rect = self.image.get_rect(center=self.pos)

class Ghoul(Enemy):
    def __init__(self, enemy_model: EnemyModel, scaling: float, pos: tuple[int, int]):
        super().__init__(enemy_model, scaling, pos)


class Golem(Enemy):
    def __init__(self, enemy_model: EnemyModel, scaling: float, pos: tuple[int, int]):
        super().__init__(enemy_model, scaling, pos)


class Wizard(Enemy):
    def __init__(self, enemy_model: EnemyModel, scaling: float, pos: tuple[int, int]):
        super().__init__(enemy_model, scaling, pos)

        #Arrow Info
        self.arrow_active: bool = False
        self.arrow_pos: tuple[float, float] = (self.pos[0], self.pos[1])
        self.arrow_target: Optional[ItemModel] = None
        self.arrow_speed: int = 3

    
    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> None:
        self.on_click(event_list)
        self.moveAndAttack(game_info.all_purchasables)
        self.updateArrow()
        self.update_slow_status()


    def moveAndAttack(self, buildings: list[ItemModel]) -> None:
        minDistance = 2000000
        closestBuilding = None

        stepDistance = self.speed * 0.1 * (100-self.slow_strength)/100

        for building in buildings:
            if building.broken:
                continue
            curr_distance = ((building.pos[0]-self.pos[0])**2+(building.pos[1]-self.pos[1])**2)**0.5
            if curr_distance < minDistance:
                minDistance = curr_distance
                closestBuilding = building

        if closestBuilding is not None:
            dx = closestBuilding.pos[0] - self.pos[0]
            dy = closestBuilding.pos[1] - self.pos[1]
            
            distance = (dx**2 + dy**2)**0.5
            
            if distance < self.attack_range:
                if self.attack_cooldown == 0:
                    self.attack(closestBuilding)
                    self.attack_cooldown = self.base_attack_cooldown
                else:
                    self.attack_cooldown -= 1
            
            else:
                if distance != 0:
                    dx /= distance
                    dy /= distance

                new_x = self.pos[0] + dx * stepDistance
                new_y = self.pos[1] + dy * stepDistance

                self.pos = (new_x, new_y)
                self.image_rect = self.image.get_rect(center=self.pos)
        
    def attack(self, building: ItemModel) -> None:
        self.arrow_target = building
        self.arrow_pos = self.pos
        self.arrow_active = True
        self.attack_cooldown = self.base_attack_cooldown
    
    def updateArrow(self) -> None:
        if not self.arrow_active or self.arrow_target is None:
            return

        dx = self.arrow_target.pos[0] - self.arrow_pos[0]
        dy = self.arrow_target.pos[1] - self.arrow_pos[1]
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.arrow_speed:
            self.arrow_active = False 

            self.arrow_target.take_damage(self.damage)
            self.arrow_pos = self.pos[0], self.pos[1]
            return

        dx_inc = dx / distance * self.arrow_speed
        dy_inc = dy / distance * self.arrow_speed

        self.arrow_pos = self.arrow_pos[0]+dx_inc, self.arrow_pos[1]+dy_inc

        grey = Color(255, 255, 255)
        bomb_radius = 3
        pygame.draw.circle(screen, grey, self.arrow_pos, bomb_radius, width=0)