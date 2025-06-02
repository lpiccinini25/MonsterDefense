import pygame
from pygame import Color
from globals import screen
import functions

from assetsHovered import hover_ArcherTower

class Tower:
    def __init__(self, title, pos):
        self.title = title
        self.pos = pos

        self.image = pygame.image.load("assets/"+title+".png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(mouse_pos):
            screen.blit(self.hover, self.hover_rect)
            print(self.hover)
        else:
            screen.blit(self.image, self.image_rect)

    def upgradeTower(self, newImage, towerModel):
        self.range = towerModel.range
        self.damage = towerModel.damage
        self.default_attack_cooldown = towerModel.default_attack_cooldown
        self.image = pygame.image.load(newImage).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)

class ArcherTower(Tower):
    def __init__(self, title, pos):
        super().__init__(title, pos)

        self.hover = hover_ArcherTower
        self.hover = pygame.transform.scale(self.hover, (40, 40))
        self.hover_rect = self.hover.get_rect(center=self.pos)


        self.arrow_active = False
        self.startArrow_pos = [self.pos[0], self.pos[1]]
        self.endArrow_pos = [self.pos[0], self.pos[1]]
        self.arrow_target = None
        self.arrow_speed = 5

        #Archer Tower Stats
        self.attack_cooldown = 120
        self.attack_cooldown_default = 120
        self.range = 200
        self.damage = 10
    
    def update(self, event_list, enemyList) -> bool:

        self.draw()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
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
    
    def update(self, event_list, enemyList) -> bool:

        self.draw()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
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
