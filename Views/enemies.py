import pygame
import random
from globals import screen
from pygame import Color
import functions

class Enemy():
    def __init__(self, enemy_name, scaling, pos):
        self.pos = pos
        self.image = pygame.image.load("assets/"+enemy_name+".png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image_rect = self.image.get_rect(center=self.pos)
    
    def draw(self):
        screen.blit(self.image, self.image_rect)
        health_bar_color = (255, 255, 255)
        functions.display_health_bar(self, self.current_health, self.base_health, health_bar_color)
    
    def update(self, game_info):
        self.moveAndAttack(game_info.all_purchasables)
    
    def on_click(self, player_click_damage, event_list):
        mouse_pos = pygame.mouse.get_pos()

        if self.image_rect.collidepoint(mouse_pos):
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.take_damage(player_click_damage)

    def take_damage(self, damage_taken):
        self.current_health -= damage_taken
    
    def attack(self, building):
        building.take_damage(self.damage)

    def moveAndAttack(self, buildings):
        minDistance = 2000000
        closestBuilding = None

        stepDistance = self.speed * 0.2

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
    def __init__(self, enemy_name, scaling, pos):
        super().__init__(enemy_name, scaling, pos)
        self.size = 25
        self.image: pygame.Surface = pygame.transform.scale(self.image, (self.size, self.size))

        self.base_health: int = random.randint(40, 40+scaling*30)
        self.current_health: int = self.base_health
        self.speed: int = random.randint(1, 1+scaling)

        self.damage: int = random.randint(10, 10+scaling*10)
        self.default_attack_cooldown: int = 60
        self.attack_cooldown: int = self.default_attack_cooldown




class Golem(Enemy):
    def __init__(self, enemy_name, scaling, pos):
        super().__init__(enemy_name, scaling, pos)
        self.size = 35
        self.image: pygame.Surface = pygame.transform.scale(self.image, (self.size, self.size))

        self.base_health: int = random.randint(200, 200+scaling*100)
        self.current_health: int = self.base_health
        self.speed: int = random.randint(1, 1+int(scaling*0.5))

        self.damage: int = random.randint(10, 10)
        self.default_attack_cooldown: int = 120
        self.attack_cooldown: int = self.default_attack_cooldown


class Wizard(Enemy):
    def __init__(self, enemy_name: str, scaling: int, pos: list[int]):
        super().__init__(enemy_name, scaling, pos)
        self.size = 25
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.base_health: int = random.randint(75, 75+scaling*15)
        self.current_health: int = self.base_health
        self.speed = random.randint(1, 1+int(scaling*0.5))

        #Stats
        self.damage = random.randint(10, 10)
        self.default_attack_cooldown = 120
        self.attack_cooldown = self.default_attack_cooldown
        self.attack_range = 150

        #Arrow Info
        self.arrow_active = False
        self.arrow_pos = [self.pos[0], self.pos[1]]
        self.arrow_target = None
        self.arrow_speed = 3

    
    def update(self, game_info):
        self.moveAndAttack(game_info.all_purchasables)
        self.updateArrow()

    def moveAndAttack(self, buildings):
        minDistance = 2000000
        closestBuilding = None

        stepDistance = self.speed * 0.2

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


        building.take_damage(self.damage)
    
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
        bomb_radius = 4
        pygame.draw.circle(screen, grey, self.arrow_pos, bomb_radius, width=0)