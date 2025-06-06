import pygame
from pygame import Color
from typing import Optional

from globals import screen, GameInfo, ItemGroup
import functions

from views.towers import ArcherTower, BombTower, TeslaTower
from models.item_models import ArcherTowerModel, BombTowerModel, TeslaTowerModel
from views.buildings import House
from views.player_abilities import Bomb

from fonts import font

class Item:
    def __init__(self, x: int, y: int, text: str, title: str, cost: Optional[int]=None, base_cooldown: Optional[int]=None, repair_amount: Optional[int]=None):
        self.x: int = x
        self.y: int = y
        self.rect = pygame.Rect(self.x, self.y, 100, 50)
        self.curr_color = (200, 100, 200)
        self.hover_color = (100, 100, 100)
        self.default_color = (200, 100, 200)
        self.text_color = (255, 255, 255)
        self.text: str = text
        self.title: str = title
        self.cost: Optional[int] = cost
        self.base_cooldown: Optional[int] = base_cooldown
        self.cooldown: int = 0
        self.repair_amount: Optional[int] = repair_amount

        #Item Image
        self.base_image: pygame.Surface = pygame.image.load("assets/"+self.title+".png").convert()

    def draw(self, amount_owned: int) -> None:
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.curr_color, self.rect)

        #if costs money display price, if is cooldown based show cooldown
        if self.cost is not None:
            functions.display_text(self.text + " costs: " + str(self.cost), self.text_color, font, self.x, self.y)
        elif self.cooldown is not None:
            functions.display_text(self.text + " cooldown is: " + str(self.cooldown) + " seconds.", self.text_color, font, self.x, self.y)
        functions.display_text("Owned: " + str(amount_owned), (255, 255, 255), font, self.x+80, self.y)

class Shop:
    def __init__(self, game_info: GameInfo):
        self.placing_item: bool = False
        self.item_being_placed: Optional[Item] = None

        inc: int = 60
        base: int = 75
        y: int = 50
        self.items: list[Item] = [
            Item(base, y, "Archer Tower", "ArcherTower", cost=2),
            Item(base, y+inc, "Tesla Tower", "TeslaTower", cost=4),
            Item(base, y+inc*2, "Bomb Tower", "BombTower", cost=6),
            Item(base, y+inc*3, "House", "House", cost=2),
            Item(base, y+inc*4, "Bomb", "Bomb", base_cooldown=2000),
            Item(base, y+inc*5, "Repair", "Repair", base_cooldown=3000, repair_amount=150)
        ]

        self.items_owned: dict[str, int] = dict()

    def draw_items(self) -> None:
        for item in self.items:
            amount_owned = self.items_owned[item.title]
            item.draw(amount_owned)
    
    def draw_item_being_placed(self) -> None:
        if self.item_being_placed is None:
            return
        else:
            #blit the image of the item being placed at ur mouse position
            mouse_pos = pygame.mouse.get_pos()
            functions.display_image(self.item_being_placed.base_image, mouse_pos[0], mouse_pos[1], 40)
    
    def update_items_owned(self, game_info: GameInfo) -> None:
        all_items_owned: list[ItemGroup] = game_info.all_purchasables

        #create dict for all items possible to place and set vals to 0
        self.items_owned = dict() 
        for item in self.items:
            self.items_owned[item.title] = 0

        #increment item value by one for each instance existing
        for owned in all_items_owned:
            if not owned.title == "TownHall":
                self.items_owned[owned.title] += 1

    def check_place_item(self, event_list: list[pygame.event.Event], game_info: GameInfo) -> None:
        if self.item_being_placed is None:
            return
        elif functions.pressed_left_click(event_list):
            print('click')
            mouse_pos = pygame.mouse.get_pos()
            item_being_placed = self.item_being_placed
            item_title = item_being_placed.title
            item_cost = item_being_placed.cost
    
            #if left click, place item at mouse position and append an item instance to corresponding list
            match item_title:
                case "House":
                    game_info.building_list.append(House(item_title, mouse_pos))
                case "ArcherTower":
                    print('append')
                    game_info.tower_list.append(ArcherTower(ArcherTowerModel(), mouse_pos))
                case "BombTower":
                    game_info.tower_list.append(BombTower(BombTowerModel(), mouse_pos))
                case "Bomb":
                    game_info.unattackable_list.append(Bomb(item_title, mouse_pos))
                case "Repair":
                    if self.item_being_placed.repair_amount is None:
                        return
                    elif not functions.repair_tower_clicked(self.item_being_placed.repair_amount, game_info, event_list):
                        self.placing_item = False
                        self.item_being_placed = None
                        return
                case "TeslaTower":
                    game_info.tower_list.append(TeslaTower(TeslaTowerModel(), mouse_pos))
                    
            #update gold/cooldown depending on if a tower/ability.
            if item_cost is not None:
                game_info.gold -= item_cost
            elif item_being_placed.base_cooldown is not None:
                item_being_placed.cooldown = item_being_placed.base_cooldown

            self.placing_item = False
            self.item_being_placed = None
            game_info.update()
        
        #cancel placing tower by rightclick
        elif functions.pressed_right_click(event_list):
            self.placing_item = False
            self.item_being_placed = None
    
    def can_get_item(self, item: Item, game_info: GameInfo) -> bool:
        #if below item cap, and have enough gold / item is not on cooldown, return True, else False
        if self.items_owned[item.title] < game_info.caps[item.title+'Cap']:
            if item.cost is not None:
                if game_info.gold >= item.cost:
                    return True
            elif item.cooldown is not None:
                if item.cooldown <= 0:
                    return True
        return False

    def update_menu(self, event_list: list[pygame.event.Event], game_info: GameInfo) -> None:
        mouse_pos = pygame.mouse.get_pos()

        #make sure items owned is up to date
        self.update_items_owned(game_info)

        #draw items
        self.draw_items()

        #If item was clicked previously, begin drawing that image at ur mouse pos. 
        if self.placing_item:
            self.draw_item_being_placed()
            self.check_place_item(event_list, game_info)
    

        for item in self.items:
            if item.rect.collidepoint(mouse_pos):
                item.curr_color = item.hover_color

                #if someone clicks on item in menu, begin placing that item
                if functions.is_clicked_on(item.rect, event_list): 
                    if self.can_get_item(item, game_info):
                        self.placing_item = True
                        self.item_being_placed = item
            else:
                item.curr_color = item.default_color
            
            if item.cooldown is not None:
                if item.cooldown > 0:
                    item.cooldown -= 1