import pygame
from pygame import Color
from Views.tower import ArcherTower, BombTower
from Views.house import House

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

    def update(self, towerList, buildingList, gold, cost, event_list):

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.placeTower(self.pos, towerList, buildingList)
                gold -= cost
                return False, gold
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                return False, gold
        
        return True, gold

    def placeTower(self, pos, towerList, buildingList):
        match self.tower:
            case "House":
                buildingList.append(House(self.pos))
            case "ArcherTower":
                towerList.append(ArcherTower(self.tower, pos))
            case "BombTower":
                towerList.append(BombTower(self.tower, pos))
        
