import pygame
from typing import Optional
from pygame import Color
from globals import screen, GameInfo
import functions
import colors

from hovered_assets import hover_ArcherTower
from views.enemies import Enemy
from models.item_models import ItemModel, TowerModel
from models.upgrade_models import UpgradeModel

class Tower(ItemModel):
    def __init__(self, tower_model: TowerModel, pos: tuple[int, int]):
        #Tower Info
        self.title: str = tower_model.title
        self.pos: tuple[int, int] = pos
        self.broken: bool = False
        self.current_level: int = 1

        #Image 
        self.image_width: int = 40
        self.load_images_and_rects()

        #Tower Stats
        self.attack_range: int = tower_model.attack_range
        self.base_health: int = tower_model.base_health
        self.current_health: int = self.base_health
        self.damage: int = tower_model.damage
        self.base_attack_cooldown: int = tower_model.base_attack_cooldown
        self.attack_cooldown: int = self.base_attack_cooldown

        #Repair Stats
        self.base_repair_time: int = tower_model.base_repair_time
        self.repair_time: int = self.base_repair_time
    
    def draw(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if not self.broken:
            if self.image_rect.collidepoint(mouse_pos):
                functions.display_image_static(self.hover_image, self.hover_image_rect)
                functions.display_health_bar(self, self.current_health, self.base_health, colors.WHITE, int(self.image_width*7/10), 14) 
            else:
                functions.display_image_static(self.image, self.image_rect)
                functions.display_health_bar(self, self.current_health, self.base_health, colors.WHITE, int(self.image_width*7/10), 14) 
        else:
            functions.display_image_static(self.broken_image, self.broken_image_rect)
            functions.display_respawn_bar(self, self.repair_time, self.base_repair_time, colors.WHITE, int(self.image_width*7/10), 14)

    def upgrade_tower(self, newImage: str, upgrade_model: UpgradeModel, game_info: GameInfo) -> None:
        self.current_level += 1
        self.damage = upgrade_model.damage
        self.attack_range = upgrade_model.attack_range
        self.base_attack_cooldown = upgrade_model.base_attack_cooldown
        self.image = pygame.image.load(newImage).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)

class ArcherTower(Tower):
    def __init__(self, tower_model: TowerModel, pos: tuple[int, int]):
        super().__init__(tower_model, pos)

        #Arrow
        self.arrow_active: bool = False
        self.startArrow_pos: tuple[int, int] = self.pos[0], self.pos[1]
        self.endArrow_pos: tuple[int, int] = self.pos[0], self.pos[1]
        self.arrow_target: Optional[Enemy] = None
        self.arrow_speed: int = 5
    
    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> bool:

        self.draw()
        enemy_list = game_info.enemy_list
 
        #if not broken, either decrement attackcooldown or fire an attack, else, check to see if building fully repaired and if so
        #change tower to not broken and reset hp to full, else, decrease repair_time left. 
        if not self.broken:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            elif not self.arrow_active:
               self.shootEnemy(enemy_list)
        else:
            if self.repair_time == 0:
                self.broken = False
                self.current_health = self.base_health
                self.repair_time = self.base_repair_time
            else:
                self.repair_time -= 1
        
        #update arrow
        self.updateArrow()

        #see if clicked. important for upgrading
        if functions.is_clicked_on(self.image_rect, event_list):
            return True
        
        return False


    def shootEnemy(self, enemy_list: list[Enemy]) -> None:
        minDistance = self.attack_range
        closestEnemy = None

        #find the closest enemy within tower range
        for enemy in enemy_list:
            distance = functions.find_distance(self.pos, enemy.pos)

            if distance < minDistance:
                minDistance = distance
                closestEnemy = enemy
            
        #if enemy found in tower range, set the target to the closest one and launch arrow
        if closestEnemy is not None:
            self.arrow_target = closestEnemy
            self.startArrow_pos = self.pos
            self.arrow_active = True
            self.attack_cooldown = self.base_attack_cooldown

            dx = self.arrow_target.pos[0] - self.startArrow_pos[0]
            dy = self.arrow_target.pos[1] - self.startArrow_pos[1]
            distance = (dx**2 + dy**2) ** 0.5

            dx_inc = round(dx / distance * self.arrow_speed)
            dy_inc = round(dy / distance * self.arrow_speed)
            self.endArrow_pos = (self.pos[0]+dx_inc, self.pos[1]+dy_inc)
        
    def updateArrow(self) -> None:
        if not self.arrow_active or self.arrow_target is None:
            return

        dx = self.arrow_target.pos[0] - self.startArrow_pos[0]
        dy = self.arrow_target.pos[1] - self.startArrow_pos[1]
        distance = (dx**2 + dy**2) ** 0.5

        #if arrow would overshoot/hit enemy, deal damage to that enemy and remove arrow.
        if distance < self.arrow_speed:
            self.arrow_active = False 
            self.startArrow_pos = self.pos[0], self.pos[1]
            self.endArrow_pos = self.pos[0], self.pos[1]
            self.arrow_target.take_damage(self.damage)
            return

        #else, increment the arrow along the newly calculated trajectory
        dx_inc = round(dx / distance * self.arrow_speed)
        dy_inc = round(dy / distance * self.arrow_speed)

        self.endArrow_pos = self.endArrow_pos[0]+dx_inc, self.endArrow_pos[1]+dy_inc
        self.startArrow_pos = self.endArrow_pos[0]+dx_inc, self.endArrow_pos[1]+dy_inc

        #draw arrow
        purple = Color(157, 93, 206)
        pygame.draw.line(screen, purple, self.startArrow_pos, self.endArrow_pos, 1)


class BombTower(Tower):
    def __init__(self, tower_model: TowerModel, pos: tuple[int, int]):
        super().__init__(tower_model, pos)

        #Bomb Tower Stats
        self.attack_cooldown: int = self.base_attack_cooldown
        self.explosion_radius: int = 25

        #Arrow Info
        self.arrow_active: bool = False
        self.arrow_pos: tuple[int, int] = self.pos[0], self.pos[1]
        self.arrow_target: Optional[Enemy] = None
        self.arrow_speed: int = 5
    
    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> bool:
        self.draw()
        enemy_list = game_info.enemy_list

        #if not broken, either decrement attackcooldown or fire an attack, else, check to see if building fully repaired and if so
        #change tower to not broken and reset hp to full, else, decrease repair_time left. 
        if not self.broken:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            elif not self.arrow_active:
               self.shootEnemy(enemy_list)
        else:
            if self.repair_time <= 0:
                self.broken = False
                self.current_health = self.base_health
                self.repair_time = self.base_repair_time
            else:
                self.repair_time -= 1
        
        #update bomb
        self.updateArrow(enemy_list)

        #see if clicked. important for upgrading
        if functions.is_clicked_on(self.image_rect, event_list):
            return True
        
        return False
    

    def shootEnemy(self, enemy_list: list[Enemy]) -> None:
        minDistance = self.attack_range
        closestEnemy = None

        #find the closest enemy within tower range
        for enemy in enemy_list:
            distance = functions.find_distance(self.pos, enemy.pos)

            if distance < minDistance:
                minDistance = distance
                closestEnemy = enemy
        
        #if enemy found in tower range, set the target to the closest one and launch arrow
        if closestEnemy is not None:
            self.arrow_target = closestEnemy
            self.arrow_pos = self.pos
            self.arrow_active = True
            self.attack_cooldown = self.base_attack_cooldown
        
    def updateArrow(self, enemy_list: list[Enemy]) -> None:
        if not self.arrow_active or self.arrow_target is None:
            return

        dx = self.arrow_target.pos[0] - self.arrow_pos[0]
        dy = self.arrow_target.pos[1] - self.arrow_pos[1]
        distance = (dx**2 + dy**2) ** 0.5

        #if bomb would overshoot/hit enemy, explode the bomb.
        if distance < self.arrow_speed:
            self.arrow_active = False 

            #deal damage to all enemies that are within the explosion radius of the bomb at time of impact with main target
            for enemy in enemy_list:
                distance = functions.find_distance(self.arrow_pos, enemy.pos)

                if distance < self.explosion_radius:
                    enemy.take_damage(self.damage)
            
            #reset bomb position for next fire
            self.arrow_pos = self.pos[0], self.pos[1]
            return

        dx_inc = round(dx / distance * self.arrow_speed)
        dy_inc = round(dy / distance * self.arrow_speed)

        self.arrow_pos = self.arrow_pos[0]+dx_inc, self.arrow_pos[1]+dy_inc

        grey = Color(200, 200, 200)
        bomb_radius = 3
        pygame.draw.circle(screen, grey, self.arrow_pos, bomb_radius, width=0)
    
    def upgrade_tower(self, newImage: str, upgrade_model: UpgradeModel, game_info: GameInfo) -> None:
        self.current_level += 1
        self.damage = upgrade_model.damage
        self.attack_range = upgrade_model.attack_range
        self.base_attack_cooldown = upgrade_model.base_attack_cooldown
        if upgrade_model.explosion_radius is None:
            return
        self.explosion_radius = upgrade_model.explosion_radius
        self.image = pygame.image.load(newImage).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)

class TeslaTower(Tower):
    def __init__(self, tower_model: TowerModel, pos: tuple[int, int]):
        super().__init__(tower_model, pos)

        #Tesla Tower Stats
        self.attack_cooldown: int = self.base_attack_cooldown
        self.bolt_slow_duration: int = 100
        self.bolt_slow_power: int = 60


        #Bolt Info
        self.bolt_spread_radius: int = 100
        self.base_bolt_spread_amount: int = 8
        self.bolt_spread_amount: int = self.base_bolt_spread_amount
        self.bolt_active: bool = False
        self.bolt_pos: tuple[int, int] = self.pos[0], self.pos[1]
        self.bolt_target: Optional[Enemy] = None
        self.bolt_speed: int = 3

        #Keep track of enemies already hit
        self.not_hit: list[Enemy]

        #Bolt Image
        self.bolt_width_size: int = 40
        self.bolt_image: pygame.Surface = functions.load_image("ElectricBolt", self.bolt_width_size)
    
    def upgrade_tower(self, newImage: str, upgrade_model: UpgradeModel, game_info: GameInfo) -> None:
        self.current_level += 1
        self.damage = upgrade_model.damage
        self.attack_range = upgrade_model.attack_range
        self.base_attack_cooldown = upgrade_model.base_attack_cooldown
        if upgrade_model.bolt_spread_amount is None:
            return
        self.bolt_spread_amount = upgrade_model.bolt_spread_amount
        self.image = pygame.image.load(newImage).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)
    
    def update(self, game_info: GameInfo, event_list: list[pygame.event.Event]) -> bool:
        self.draw()
        enemy_list = game_info.enemy_list

        #if not broken, either decrement attackcooldown or fire an attack, else, check to see if building fully repaired and if so
        #change tower to not broken and reset hp to full, else, decrease repair_time left. 
        if not self.broken:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            elif not self.bolt_active:
               self.shoot_enemy(enemy_list)
        else:
            if self.repair_time <= 0:
                self.broken = False
                self.current_health = self.base_health
                self.repair_time = self.base_repair_time
            else:
                self.repair_time -= 1
        
        #update bomb
        self.update_bolt()

        #see if clicked. important for upgrading
        if functions.is_clicked_on(self.image_rect, event_list):
            return True
        
        return False
    

    def shoot_enemy(self, enemy_list: list[Enemy]) -> None:
        minDistance = self.attack_range
        closest_enemy = None

        #find the closest enemy within tower range
        for enemy in enemy_list:
            distance = functions.find_distance(self.pos, enemy.pos)

            if distance <= minDistance:
                minDistance = distance
                closest_enemy = enemy
        
        #if enemy found in tower range, set the target to the closest one and launch arrow
        if closest_enemy is not None:
            self.bolt_target = closest_enemy
            self.bolt_pos = self.pos
            self.bolt_active = True
            self.attack_cooldown = self.base_attack_cooldown
            self.not_hit = enemy_list.copy()
        
    def update_bolt(self) -> None:
        if not self.bolt_active or self.bolt_target is None:
            return

        dx = self.bolt_target.pos[0] - self.bolt_pos[0]
        dy = self.bolt_target.pos[1] - self.bolt_pos[1]
        distance = (dx**2 + dy**2) ** 0.5

        #if bomb would overshoot/hit enemy, explode the bomb.
        if distance < self.bolt_speed:

            self.bolt_target.take_damage(self.damage)
            self.bolt_target.slow_enemy(self.bolt_slow_power, self.bolt_slow_duration)
            self.not_hit.remove(self.bolt_target)
            #deal damage to all enemies that are within the explosion radius of the bomb at time of impact with main target


            min_distance = self.bolt_spread_radius
            closest_enemy = None
            for enemy in self.not_hit:
                distance = functions.find_distance(self.bolt_pos, enemy.pos)

                if distance <= min_distance:
                    min_distance = distance
                    closest_enemy = enemy
            
            if closest_enemy is not None and self.bolt_spread_amount > 0:
                self.bolt_spread_amount -= 1
                self.bolt_target = closest_enemy
            else:
                self.bolt_spread_amount = self.base_bolt_spread_amount
                self.bolt_target = None
                self.bolt_active = False
                self.bolt_pos = self.pos[0], self.pos[1]
                return

        dx_inc = round(dx / distance * self.bolt_speed)
        dy_inc = round(dy / distance * self.bolt_speed)

        self.bolt_pos = self.bolt_pos[0]+dx_inc, self.bolt_pos[1]+dy_inc

        functions.display_image_new_rect(self.bolt_image, self.bolt_pos[0], self.bolt_pos[1])