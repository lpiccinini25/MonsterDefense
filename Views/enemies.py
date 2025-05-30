import pygame
import random

class Enemy:
    def __init__(self, scaling):
        self.pos = (150, 150)
        self.image = pygame.image.load("assets/Ghoul.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image_rect = self.image.get_rect(center=self.pos)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.totalHealth = random.randint(40, 40+scaling*40)
        self.currentHealth = 40
        self.speed = random.randint(1, 1+scaling*1)
        self.damage = random.randint(10, 10+scaling)
        self.totalPower = (self.totalHealth*0.25 + self.speed*100 + self.damage*20)
    
    def draw(self, screen):
        screen.blit(self.image, self.image_rect)
        healthBar = pygame.Rect(0, 0, 25, 2)
        healthBar.center = ((self.pos[0], self.pos[1]+13))
        healthBar.width = (self.currentHealth/self.totalHealth)*25
        pygame.draw.rect(screen, (255, 255, 255), healthBar)
        outline = pygame.Rect(0, 0, 25, 4)
        outline.center = ((self.pos[0], self.pos[1]+13))
        pygame.draw.rect(screen, (255, 255, 255), outline, width=1)

    def move(self, buildings):
        minDistance = 2000000
        closestBuilding = None

        stepDistance = self.speed * 0.2

        for building in buildings:
            curr_distance = ((building.pos[0]-self.pos[0])**2+(building.pos[1]-self.pos[1])**2)**0.5
            if curr_distance < minDistance:
                minDistance = curr_distance
                closestBuilding = building

        if closestBuilding is not None:
            dx = closestBuilding.pos[0] - self.pos[0]
            dy = closestBuilding.pos[1] - self.pos[1]
            
            distance = (dx**2 + dy**2)**0.5
            
            if distance != 0:
                dx /= distance
                dy /= distance

            new_x = self.pos[0] + dx * stepDistance
            new_y = self.pos[1] + dy * stepDistance

            self.pos = (new_x, new_y)
            self.image_rect = self.image.get_rect(center=self.pos)

    def take_damage(self, damage_taken):
        self.currentHealth -= damage_taken




