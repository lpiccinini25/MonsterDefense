from globals import screen
import pygame

class House:
    def __init__(self, pos):
        self.title = "House"
        self.pos = pos

        self.broken = False
        self.base_repair_time = 1200
        self.repair_time = self.base_repair_time

        self.house_image = pygame.image.load("assets/House.png")
        self.house_image.set_colorkey((0, 0, 0))
        self.house_image = pygame.transform.scale(self.house_image, (30, 30))
        self.house_image_rect = self.house_image.get_rect(center=self.pos)

        self.broken_house_image = pygame.image.load("assets/BrokenHouse.png").convert()
        self.broken_house_image.set_colorkey((0, 0, 0))
        self.broken_house_image = pygame.transform.scale(self.broken_house_image, (30, 30))
        self.broken_house_image_rect = self.broken_house_image.get_rect(center=self.pos)

        self.totalHealth = 100
        self.currentHealth = self.totalHealth
        self.defaultGoldGenerationCoolDown = 800
        self.goldGenerationCoolDown = self.defaultGoldGenerationCoolDown

    def update(self):

        self.draw()

        if not self.broken:
            if self.goldGenerationCoolDown == 0:
                self.goldGenerationCoolDown = self.defaultGoldGenerationCoolDown
                return True
            else:
                self.goldGenerationCoolDown -= 1
        elif self.repair_time != 0:
            self.repair_time -= 1
        else:
            self.repair_time = self.base_repair_time
            self.broken = False
            self.currentHealth = self.totalHealth
        
        return False
        

    
    def draw(self):
        if not self.broken:
            screen.blit(self.house_image, self.house_image_rect)
            healthBar = pygame.Rect(0, 0, 30, 2)
            healthBar.center = ((self.pos[0], self.pos[1]+15))
            healthBar.width = (self.currentHealth/self.totalHealth)*30
            pygame.draw.rect(screen, (158, 78, 34), healthBar)
            outline = pygame.Rect(0, 0, 30, 4)
            outline.center = ((self.pos[0], self.pos[1]+15))
            pygame.draw.rect(screen, (158, 78, 34), outline, width=1)
        else:
            screen.blit(self.broken_house_image, self.broken_house_image_rect)
            respawnBar = pygame.Rect(0, 0, 30, 2)
            respawnBar.center = ((self.pos[0], self.pos[1]))
            respawnBar.width = ((self.base_repair_time - self.repair_time)/self.base_repair_time)*30
            pygame.draw.rect(screen, (255, 255, 255), respawnBar)
            outline = pygame.Rect(0, 0, 30, 4)
            outline.center = ((self.pos[0], self.pos[1]))
            pygame.draw.rect(screen, (255, 255, 255), outline, width=1)
    
    def take_damage(self, damage_amount):
        self.currentHealth -= damage_amount
        if self.currentHealth <= 0:
            self.broken = True