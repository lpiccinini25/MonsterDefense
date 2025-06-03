import pygame
pygame.init()
screen = pygame.display.set_mode((850, 700))

gold = 10

class GameInfo:
    def __init__(self):
        self.tower_list = []
        self.building_list = []
        self.all_purchasables = []
        self.enemy_list = []
        self.unattackable_list = []

        self.gold = 6
        self.player_click_damage = 0
        self.caps = {
            'ArcherTowerCap' : 4,
            'HouseCap' : 3,
            'BombTowerCap' : 1,
            'BombCap': 1
        }
    
    def update(self):
        self.all_purchasables = self.building_list + self.tower_list