import pygame
from pygame import Color
from globals import screen
import functions

from fonts import font

class Purchasable:
    def __init__(self, x, y, text, title, cost):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 100, 50)
        self.curr_color = Color(200, 100, 200)
        self.hover_color = Color(100, 100, 100)
        self.default_color = Color(200, 100, 200)
        self.text_color = Color(255, 255, 255)
        self.text = text
        self.title = title
        self.cost = cost
        self.clicked = False

    def draw(self, amount_owned):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.curr_color, self.rect)
        functions.display_text(self.text + " costs: " + str(self.cost), self.text_color, font, self.x, self.y)
        functions.display_text("Owned: " + str(amount_owned), (255, 255, 255), font, self.x+80, self.y)

    def is_clicked(self, pos):
        print("click" + self.title)
        return True, self.title, self.cost

class Shop:
    def __init__(self):

        inc = 60
        base = 75
        y = 50
        self.purchasables = [
            Purchasable(base, y, "Archer Tower", "ArcherTower", 2),
            Purchasable(base, y+inc, "House", "House", 2),
            Purchasable(base, y+inc*2, "Bomb Tower", "BombTower", 6)
        ]

        self.purchasables_owned = dict()

    def drawPurchasables(self):
        for purchasable in self.purchasables:
            amount_owned = self.purchasables_owned[purchasable.title]
            purchasable.draw(amount_owned)
        # Add text rendering here
    
    def update_purchasables_owned(self, game_info):
        all_purchasables_owned = dict()

        all_purchasables_owned = game_info.building_list.copy()
        all_purchasables_owned += game_info.tower_list


        self.purchasables_owned = dict()
        for purchasable in self.purchasables:
            self.purchasables_owned[purchasable.title] = 0

        for purchasable in all_purchasables_owned:
            if not purchasable.title == "TownHall":
                self.purchasables_owned[purchasable.title] += 1


    def updatePurchasables(self, event_list, game_info):
        mouse_pos = pygame.mouse.get_pos()

        self.update_purchasables_owned(game_info)

        for purchasable in self.purchasables:
            if purchasable.rect.collidepoint(mouse_pos):
                purchasable.curr_color = purchasable.hover_color

                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if game_info.gold >= purchasable.cost and self.purchasables_owned[purchasable.title] < game_info.caps[purchasable.title+'Cap']:
                            return purchasable.is_clicked(mouse_pos)
                        
        
        return False, None, None