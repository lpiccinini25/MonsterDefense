
# Taken from husano896's PR thread (slightly modified)
import pygame
from Views.shopMenu import Shop
from Views.placingItem import placeItem
from globals import screen

from pygame.locals import *
clock = pygame.time.Clock()

def main():
   placing = False
   tower = ""
   pygame.display.update()


   while True:
        screen.fill((0, 0, 0))
        shop = Shop()

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == QUIT:
               pygame.quit()
               return
            elif event.type == MOUSEWHEEL:
               print(event)
               print(event.x, event.y)
               print(event.flipped)
               print(event.which)
               # can access properties with
               # proper notation(ex: event.y)
        clock.tick(60)

        placingTower, towerNow = shop.updatePurchasables(event_list)
        if placingTower:
            placing = True
            tower = towerNow
        
        if placing:
            place = placeItem(tower)
            place.draw(screen)

        shop.drawPurchasables()

        pygame.display.update()

# Execute game:
main()