import pygame
from pygame import Color
from Views.towers import ArcherTower, BombTower
from Views.buildings import House

class placeItem:
    def __init__(self, tower):
        self.pos = pygame.mouse.get_pos()
        self.tower = tower
        self.image = pygame.image.load("assets/"+tower+".png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image_rect = self.image.get_rect(center=self.pos)
        self.curr_color = Color(200, 100, 200)
        self.hover_color = Color(100, 100, 100)
        self.default_color = Color(200, 100, 200)
        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)
        # Add text rendering here

    def update(self, game_info, cost, event_list):

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.placeTower(self.pos, game_info)
                game_info.gold -= cost
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                return False
        
        return True

    def placeTower(self, pos, game_info):
        match self.tower:
            case "House":
                game_info.building_list.append(House(self.tower, self.pos))
            case "ArcherTower":
                game_info.tower_list.append(ArcherTower(self.tower, pos))
            case "BombTower":
                game_info.tower_list.append(BombTower(self.tower, pos))
        
