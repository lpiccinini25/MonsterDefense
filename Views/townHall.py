from globals import screen
import pygame

class TownHall:
    def __init__(self):
        self.broken = False
        self.title = "TownHall"
        self.pos = (screen.get_width()/2, screen.get_height()/2)
        self.image = pygame.image.load("assets/TownHall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.image_rect = self.image.get_rect(center=self.pos)
        self.totalHealth = 1000
        self.currentHealth = self.totalHealth

    def update(self):
        self.draw()
        return False
    
    def draw(self):
        screen.blit(self.image, self.image_rect)
        healthBar = pygame.Rect(0, 0, 50, 2)
        healthBar.center = ((self.pos[0], self.pos[1]+22))
        healthBar.width = (self.currentHealth/self.totalHealth)*50
        pygame.draw.rect(screen, (255, 215, 0), healthBar)
        outline = pygame.Rect(0, 0, 50, 4)
        outline.center = ((self.pos[0], self.pos[1]+22))
        pygame.draw.rect(screen, (255, 215, 0), outline, width=1)
    
    def take_damage(self, damage_amount):
        self.currentHealth -= damage_amount
