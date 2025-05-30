import pygame
from pygame import Color
from globals import screen

class Tower:
    def __init__(self, tower, pos):
        self.tower = tower
        self.pos = pos
        self.image = pygame.image.load("assets/"+tower+".png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)
        self.curr_color = Color(200, 100, 200)
        self.attack_cooldown = 120
        self.attack_cooldown_default = 120
        self.arrow_active = False
        self.startArrow_pos = [self.pos[0], self.pos[1]]
        self.endArrow_pos = [self.pos[0], self.pos[1]]
        self.arrow_target = None
        self.arrow_speed = 5
        match self.tower:
            case "ArcherTower":
                self.range = 160
    
    def draw(self, screen):
        screen.blit(self.image, self.image_rect)
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.updateArrow(screen)

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
            return

        dx_inc = dx / distance * self.arrow_speed
        dy_inc = dy / distance * self.arrow_speed

        self.startArrow_pos[0] += dx_inc
        self.startArrow_pos[1] += dy_inc

        self.endArrow_pos[0] += dx_inc
        self.endArrow_pos[1] += dy_inc

        purple = Color(157, 93, 206)
        pygame.draw.line(screen, purple, self.startArrow_pos, self.endArrow_pos, 1)
    
