
# Taken from husano896's PR thread (slightly modified)
import pygame
from shopMenu import Purchasable
from globals import screen

from pygame.locals import *
clock = pygame.time.Clock()

def main():

   item = Purchasable(100, 100, Color(244, 200, 100), "banana")
   item.draw(screen)
   pygame.display.update()
   while True:
      for event in pygame.event.get():
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

# Execute game:
main()