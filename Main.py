
# Taken from husano896's PR thread (slightly modified)
import pygame
from Views.shopMenu import Shop
from Views.placingItem import placeItem
from Views.townHall import TownHall
from globals import screen
from Views.enemies import Enemy

from pygame.locals import *
clock = pygame.time.Clock()

def main():

   placing = False
   tower = ""

   towerList = []
   buildings = []
   pygame.display.update()

   enemyList = []
   enemyList.append(Enemy(0))

   townHall = TownHall()
   buildings.append(townHall)

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

        townHall.draw(screen)

        placingTower, towerNow = shop.updatePurchasables(event_list)

        if placingTower:
            placing = True
            tower = towerNow
        
        if placing:
            place = placeItem(tower)
            placing = place.update(towerList)
            place.draw(screen)

        for enemy in enemyList:
            if enemy.currentHealth <= 0:
                enemyList.remove(enemy)
                continue
            enemy.draw(screen)
            enemy.move(buildings)

        for towerUnit in towerList:
            towerUnit.draw(screen)
            towerUnit.update()
            if towerUnit.attack_cooldown == 0:
                towerUnit.shootEnemy(enemyList)

        shop.drawPurchasables()

        pygame.display.update()

# Execute game:
main()