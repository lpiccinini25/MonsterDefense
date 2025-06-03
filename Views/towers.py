import pygame
from pygame import Color
from globals import screen, ItemGroup
import functions

from assetsHovered import hover_ArcherTower

class Tower(ItemGroup):
    def __init__(self, title, pos):
        self.title = title
        self.pos = pos
        self.broken = False

        self.image = pygame.image.load("assets/"+title+".png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)

    def draw(self, health_bar_color):
        mouse_pos = pygame.mouse.get_pos()
        if not self.broken:
            if self.image_rect.collidepoint(mouse_pos):
                screen.blit(self.hover, self.hover_rect)
                healthBar = pygame.Rect(0, 0, 30, 2)
                healthBar.center = ((self.pos[0], self.pos[1]+15))
                healthBar.width = (self.currentHealth/self.totalHealth)*30
                pygame.draw.rect(screen, health_bar_color, healthBar)
                outline = pygame.Rect(0, 0, 30, 4)
                outline.center = ((self.pos[0], self.pos[1]+15))
                pygame.draw.rect(screen, health_bar_color, outline, width=1)
            else:
                screen.blit(self.image, self.image_rect)
                healthBar = pygame.Rect(0, 0, 30, 2)
                healthBar.center = ((self.pos[0], self.pos[1]+15))
                healthBar.width = (self.currentHealth/self.totalHealth)*30
                pygame.draw.rect(screen, health_bar_color, healthBar)
                outline = pygame.Rect(0, 0, 30, 4)
                outline.center = ((self.pos[0], self.pos[1]+15))
                pygame.draw.rect(screen, health_bar_color, outline, width=1)
        else:
            screen.blit(self.broken_image, self.broken_image_rect)
            respawnBar = pygame.Rect(0, 0, 30, 2)
            respawnBar.center = ((self.pos[0], self.pos[1]))
            respawnBar.width = ((self.base_repair_time - self.repair_time)/self.base_repair_time)*30
            pygame.draw.rect(screen, (255, 255, 255), respawnBar)
            outline = pygame.Rect(0, 0, 30, 4)
            outline.center = ((self.pos[0], self.pos[1]))
            pygame.draw.rect(screen, (255, 255, 255), outline, width=1)

    def upgradeTower(self, newImage, towerModel, game_info):
        self.range = towerModel.range
        self.damage = towerModel.damage
        self.default_attack_cooldown = towerModel.default_attack_cooldown
        self.image = pygame.image.load(newImage).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)

    def take_damage(self, damage_amount):
        self.currentHealth -= damage_amount
        if self.currentHealth <= 0:
            self.broken = True

class ArcherTower(Tower):
    def __init__(self, title, pos):
        super().__init__(title, pos)

        self.hover = hover_ArcherTower
        self.hover = pygame.transform.scale(self.hover, (40, 40))
        self.hover_rect = self.hover.get_rect(center=self.pos)

        #Broken/Repair
        self.base_repair_time = 1400
        self.repair_time = self.base_repair_time

        image_size = 30

        self.broken_image = pygame.image.load("assets/BrokenArcherTower.png").convert()
        self.broken_image.set_colorkey((0, 0, 0))
        self.broken_image = pygame.transform.scale(self.broken_image, (30, 30))
        self.broken_image_rect = self.broken_image.get_rect(center=self.pos)

        self.totalHealth = 200
        self.currentHealth = self.totalHealth

        #Arrow
        self.arrow_active = False
        self.startArrow_pos = [self.pos[0], self.pos[1]]
        self.endArrow_pos = [self.pos[0], self.pos[1]]
        self.arrow_target = None
        self.arrow_speed = 5

        #Archer Tower Stats
        self.attack_cooldown_default = 100
        self.attack_cooldown = self.attack_cooldown_default
        self.range = 200
        self.damage = 15
    
    def update(self, game_info, event_list, enemyList) -> bool:

        self.draw((168, 96, 216))

        if not self.broken:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            elif not self.arrow_active:
               self.shootEnemy(enemyList)
        else:
            if self.repair_time == 0:
                self.broken = False
                self.currentHealth = self.totalHealth
                self.repair_time = self.base_repair_time
            else:
                self.repair_time -= 1
        
        self.updateArrow(screen)

        if functions.is_clicked_on(self.image_rect, event_list):
            return True


    def shootEnemy(self, enemyList):
        minDistance = self.range
        closestEnemy = None
        for enemy in enemyList:
            dx = self.pos[0] - enemy.pos[0]
            dy = self.pos[1] - enemy.pos[1]

            distance = (dx**2+dy**2)**(0.5)

            if distance < minDistance:
                minDistance = distance
                closestEnemy = enemy
            
        if closestEnemy is not None:
            self.arrow_target = closestEnemy
            self.startArrow_pos = list(self.pos)
            self.arrow_active = True
            self.attack_cooldown = self.attack_cooldown_default

            dx = self.arrow_target.pos[0] - self.startArrow_pos[0]
            dy = self.arrow_target.pos[1] - self.startArrow_pos[1]
            distance = (dx**2 + dy**2) ** 0.5

            dx_inc = dx / distance * self.arrow_speed
            dy_inc = dy / distance * self.arrow_speed
            self.endArrow_pos = [self.pos[0]+dx_inc, self.pos[1]+dy_inc]
        
    def updateArrow(self, screen):
        if not self.arrow_active or self.arrow_target is None:
            return

        dx = self.arrow_target.pos[0] - self.startArrow_pos[0]
        dy = self.arrow_target.pos[1] - self.startArrow_pos[1]
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.arrow_speed:
            self.arrow_active = False 
            self.startArrow_pos = [self.pos[0], self.pos[1]]
            self.endArrow_pos = [self.pos[0], self.pos[1]]
            self.arrow_target.take_damage(self.damage)
            return

        dx_inc = dx / distance * self.arrow_speed
        dy_inc = dy / distance * self.arrow_speed

        self.startArrow_pos[0] += dx_inc
        self.startArrow_pos[1] += dy_inc

        self.endArrow_pos[0] += dx_inc
        self.endArrow_pos[1] += dy_inc

        purple = Color(157, 93, 206)
        pygame.draw.line(screen, purple, self.startArrow_pos, self.endArrow_pos, 1)


class BombTower(Tower):
    def __init__(self, title, pos):
        super().__init__(title, pos)
        self.hover = self.image
        self.hover = pygame.transform.scale(self.hover, (40, 40))
        self.hover_rect = self.hover.get_rect(center=self.pos)

        self.attack_cooldown_default = 180
        self.attack_cooldown = self.attack_cooldown_default

        #Arrow Info
        self.arrow_active = False
        self.arrow_pos = [self.pos[0], self.pos[1]]
        self.arrow_target = None
        self.arrow_speed = 5

        #Bomb Tower Stats

        self.attack_cooldown_default = 180
        self.attack_cooldown = self.attack_cooldown_default

        self.damage = 30
        self.range = 100

        self.explosion_radius = 10

        #Broken/Repair
        self.base_repair_time = 1400
        self.repair_time = self.base_repair_time

        image_size = 30

        self.broken_image = pygame.image.load("assets/BrokenBombTower.png").convert()
        self.broken_image.set_colorkey((0, 0, 0))
        self.broken_image = pygame.transform.scale(self.broken_image, (30, 30))
        self.broken_image_rect = self.broken_image.get_rect(center=self.pos)

        self.totalHealth = 150
        self.currentHealth = self.totalHealth
    
    def update(self, game_info, event_list, enemyList) -> bool:

        self.draw((61, 64, 67))

        if not self.broken:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            elif not self.arrow_active:
               self.shootEnemy(enemyList)
        else:
            if self.repair_time == 0:
                self.broken = False
                self.currentHealth = self.totalHealth
            else:
                self.repair_time -= 1
        
        self.updateArrow(enemyList)

        if functions.is_clicked_on(self.image_rect, event_list):
            return True


    def shootEnemy(self, enemyList):
        minDistance = self.range
        closestEnemy = None
        for enemy in enemyList:
            dx = self.pos[0] - enemy.pos[0]
            dy = self.pos[1] - enemy.pos[1]

            distance = (dx**2+dy**2)**(0.5)

            if distance < minDistance:
                minDistance = distance
                closestEnemy = enemy
            
        if closestEnemy is not None:
            self.arrow_target = closestEnemy
            self.arrow_pos = list(self.pos)
            self.arrow_active = True
            self.attack_cooldown = self.attack_cooldown_default
        
    def updateArrow(self, enemyList):
        if not self.arrow_active or self.arrow_target is None:
            return

        dx = self.arrow_target.pos[0] - self.arrow_pos[0]
        dy = self.arrow_target.pos[1] - self.arrow_pos[1]
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.arrow_speed:
            self.arrow_active = False 

            for enemy in enemyList:
                dx = enemy.pos[0] - self.arrow_pos[0]
                dy = enemy.pos[1] - self.arrow_pos[1]
                distance = (dx**2 + dy**2) ** 0.5

                if distance < self.explosion_radius:
                    enemy.take_damage(self.damage)
            
            self.arrow_pos = [self.pos[0], self.pos[1]]

            return

        dx_inc = dx / distance * self.arrow_speed
        dy_inc = dy / distance * self.arrow_speed

        self.arrow_pos[0] += dx_inc
        self.arrow_pos[1] += dy_inc

        grey = Color(200, 200, 200)
        bomb_radius = 3
        pygame.draw.circle(screen, grey, self.arrow_pos, bomb_radius, width=0)
