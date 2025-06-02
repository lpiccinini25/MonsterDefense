from globals import screen
import pygame

class building:
    def __init__(self, title, pos):
        self.pos = pos
        self.title = title

        self.broken = False

        self.image = pygame.image.load("assets/"+title+".png")
        self.image.set_colorkey((0, 0, 0))
    
    def take_damage(self, damage_amount):
        self.currentHealth -= damage_amount
        if self.currentHealth <= 0:
            self.broken = True

class House(building):
    def __init__(self, title, pos):
        super().__init__(title, pos)

        self.base_repair_time = 1400
        self.repair_time = self.base_repair_time

        image_size = 30
        self.image = pygame.transform.scale(self.image, (image_size, image_size))
        self.image_rect = self.image.get_rect(center=self.pos)

        self.broken_image = pygame.image.load("assets/BrokenHouse.png").convert()
        self.broken_image.set_colorkey((0, 0, 0))
        self.broken_image = pygame.transform.scale(self.broken_image, (30, 30))
        self.broken_image_rect = self.broken_image.get_rect(center=self.pos)

        self.totalHealth = 100
        self.currentHealth = self.totalHealth
        self.defaultGoldGenerationCoolDown = 700
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
            screen.blit(self.image, self.image_rect)
            healthBar = pygame.Rect(0, 0, 30, 2)
            healthBar.center = ((self.pos[0], self.pos[1]+15))
            healthBar.width = (self.currentHealth/self.totalHealth)*30
            pygame.draw.rect(screen, (158, 78, 34), healthBar)
            outline = pygame.Rect(0, 0, 30, 4)
            outline.center = ((self.pos[0], self.pos[1]+15))
            pygame.draw.rect(screen, (158, 78, 34), outline, width=1)
        else:
            screen.blit(self.broken_image, self.broken_image_rect)
            respawnBar = pygame.Rect(0, 0, 30, 2)
            respawnBar.center = ((self.pos[0], self.pos[1]))
            respawnBar.width = ((self.base_repair_time - self.repair_time)/self.base_repair_time)*30
            pygame.draw.rect(screen, (255, 255, 255), respawnBar)
            outline = pygame.Rect(0, 0, 30, 4)
            outline.center = ((self.pos[0], self.pos[1]))
            pygame.draw.rect(screen, (255, 255, 255), outline, width=1)

class TownHall(building):
    def __init__(self):
        super().__init__()
        self.broken = False
        self.building_name = "TownHall"
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