import pygame
from globals import screen
import functions

class Ability:
    def __init__(self, title, pos):
        self.title = title
        self.pos = pos

        self.image = pygame.image.load("assets/"+title+".png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image_rect = self.image.get_rect(center=self.pos)
    
    def draw(self):
        screen.blit(self.image, self.image_rect)

class Bomb(Ability):
    def __init__(self, title, pos):
        super().__init__(title, pos)

        #Bomb Stats
        self.base_fuse_time = 100
        self.fuse_time = self.base_fuse_time

        self.damage = 40
        self.explosion_radius = 60

        #Image Stuff
        self.size = 20
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image_rect = self.image.get_rect(center=self.pos)
    
    def draw(self):
        screen.blit(self.image, self.image_rect)
        functions.display_health_bar(self, self.fuse_time, self.base_fuse_time)

    def is_exploding(self):
        if self.fuse_time <= 0:
            return True
        else:
            self.fuse_time -= 1
            return False
    
    def explode(self, enemy_list):
        for enemy in enemy_list:
            distance_between = functions.find_distance(self.pos, enemy.pos)
            if distance_between <= self.explosion_radius:
                enemy.take_damage(self.damage)
    
    def update(self, game_info):
        self.draw()
        
        if self.is_exploding():
            self.explode(game_info.enemy_list)
            game_info.unattackable_list.remove(self)


        




