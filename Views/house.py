from globals import screen
import pygame

class House:
    def __init__(self, pos):
        self.title = "House"
        self.pos = pos
        self.image = pygame.image.load("assets/House.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image_rect = self.image.get_rect(center=self.pos)
        self.totalHealth = 100
        self.currentHealth = self.totalHealth
        self.defaultGoldGenerationCoolDown = 400
        self.goldGenerationCoolDown = self.defaultGoldGenerationCoolDown

    def update(self):
        self.draw()

        if self.goldGenerationCoolDown == 0:
            self.goldGenerationCoolDown = self.defaultGoldGenerationCoolDown
            return True
        else:
            self.goldGenerationCoolDown -= 1
            return False
    
    def draw(self):
        screen.blit(self.image, self.image_rect)
        healthBar = pygame.Rect(0, 0, 30, 2)
        healthBar.center = ((self.pos[0], self.pos[1]+15))
        healthBar.width = (self.currentHealth/self.totalHealth)*30
        pygame.draw.rect(screen, (158, 78, 34), healthBar)
        outline = pygame.Rect(0, 0, 30, 4)
        outline.center = ((self.pos[0], self.pos[1]+15))
        pygame.draw.rect(screen, (158, 78, 34), outline, width=1)
    
    def take_damage(self, damage_amount):
        self.currentHealth -= damage_amount