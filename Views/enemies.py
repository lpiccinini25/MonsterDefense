import pygame
import random
from globals import screen, GameInfo, ItemGroup
from pygame import Color
import functions

from typing import Optional

class Enemy():
    def __init__(self, enemy_name: str, scaling: int, pos: tuple[float, float]):
        self.pos: tuple[float, float] = pos
        self.image: pygame.Surface = pygame.image.load("assets/"+enemy_name+".png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image_rect: pygame.Rect = self.image.get_rect(center=self.pos)

        #Stats:
        self.current_health: int
        self.base_health: int
        self.damage: int
        self.speed: int
        self.attack_cooldown: int
        self.default_attack_cooldown: int

        #Status Effects
        self.on_click_slow_strength = 40
        self.on_click_slow_duration = 50
        self.slow_strength: int = 0
        self.slow_duration: int = 0
    
    def draw(self) -> None:
        screen.blit(self.image, self.image_rect)
        health_bar_color = (255, 255, 255)
        functions.display_health_bar(self, self.current_health, self.base_health, health_bar_color)
    
    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> None:
        self.on_click(event_list)
        self.moveAndAttack(game_info.all_purchasables)
        self.update_slow_status()

    def take_damage(self, damage_taken: int) -> None:
        self.current_health -= damage_taken
    
    def attack(self, building: ItemGroup) -> None:
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
            

    def moveAndAttack(self, buildings: list[ItemGroup]) -> None:
        minDistance = 2000000
        closestBuilding = None

        stepDistance = self.speed * 0.2 * ((100-self.slow_strength)/100)

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
                    self.attack_cooldown = self.default_attack_cooldown
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
    def __init__(self, enemy_name: str, scaling: int, pos: tuple[int, int]):
        super().__init__(enemy_name, scaling, pos)
        self.size: int = 25
        self.image: pygame.Surface = pygame.transform.scale(self.image, (self.size, self.size))

        self.base_health: int = random.randint(40, 40+scaling*30)
        self.current_health: int = self.base_health
        self.speed: int = random.randint(1, 1+scaling)

        self.damage: int = random.randint(10, 10+scaling*10)
        self.default_attack_cooldown: int = 60
        self.attack_cooldown: int = self.default_attack_cooldown




class Golem(Enemy):
    def __init__(self, enemy_name: str, scaling: int, pos: tuple[int, int]):
        super().__init__(enemy_name, scaling, pos)
        self.size: int = 35
        self.image: pygame.Surface = pygame.transform.scale(self.image, (self.size, self.size))

        self.base_health: int = random.randint(200, 200+scaling*100)
        self.current_health: int = self.base_health
        self.speed: int = random.randint(1, 1+int(scaling*0.5))

        self.damage: int = random.randint(10, 10)
        self.default_attack_cooldown: int = 120
        self.attack_cooldown: int = self.default_attack_cooldown


class Wizard(Enemy):
    def __init__(self, enemy_name: str, scaling: int, pos: tuple[int, int]):
        super().__init__(enemy_name, scaling, pos)
        self.size: int = 25
        self.image: pygame.Surface = pygame.transform.scale(self.image, (self.size, self.size))

        self.base_health: int = random.randint(75, 75+scaling*15)
        self.current_health: int = self.base_health
        self.speed = random.randint(1, 1+int(scaling*0.5))

        #Stats
        self.damage: int = random.randint(10, 10)
        self.default_attack_cooldown: int = 120
        self.attack_cooldown: int = self.default_attack_cooldown
        self.attack_range: int = 150

        #Arrow Info
        self.arrow_active: bool = False
        self.arrow_pos: tuple[float, float] = (self.pos[0], self.pos[1])
        self.arrow_target: Optional[ItemGroup] = None
        self.arrow_speed: int = 3

    
    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> None:
        self.on_click(event_list)
        self.moveAndAttack(game_info.all_purchasables)
        self.updateArrow()
        self.update_slow_status()


    def moveAndAttack(self, buildings: list[ItemGroup]):
        minDistance = 2000000
        closestBuilding = None

        stepDistance = self.speed * 0.2 * (100-self.slow_strength)/100

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
                    self.attack_cooldown = self.default_attack_cooldown
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
        
    def attack(self, building):
        self.arrow_target = building
        self.arrow_pos = list(self.pos)
        self.arrow_active = True
        self.attack_cooldown = self.default_attack_cooldown
    
    def updateArrow(self):
        if not self.arrow_active or self.arrow_target is None:
            return

        dx = self.arrow_target.pos[0] - self.arrow_pos[0]
        dy = self.arrow_target.pos[1] - self.arrow_pos[1]
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.arrow_speed:
            self.arrow_active = False 

            self.arrow_target.take_damage(self.damage)
            self.arrow_pos = [self.pos[0], self.pos[1]]
            return

        dx_inc = dx / distance * self.arrow_speed
        dy_inc = dy / distance * self.arrow_speed

        self.arrow_pos[0] += dx_inc
        self.arrow_pos[1] += dy_inc

        grey = Color(255, 255, 255)
        bomb_radius = 3
        pygame.draw.circle(screen, grey, self.arrow_pos, bomb_radius, width=0)