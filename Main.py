
# Taken from husano896's PR thread (slightly modified)
import pygame
from shopMenu import Shop
from globals import screen

from pygame.locals import *
clock = pygame.time.Clock()

def main():

   pygame.display.update()


   while True:
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

        shop.updatePurchasables(event_list)

        shop.drawPurchasables()

        pygame.display.update()

# Execute game:
main()