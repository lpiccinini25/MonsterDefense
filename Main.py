
# Taken from husano896's PR thread (slightly modified)
import pygame
from Views.shopMenu import Shop
from Views.placingItem import placeItem
from Views.townHall import TownHall
from globals import screen
from Views.enemies import Enemy
from random import randint

from pygame.locals import *
clock = pygame.time.Clock()

def main():

   placing = False
   tower = ""

   #Player
   gold = 10
   towerList = []
   buildings = []
   townHall = TownHall()
   buildings.append(townHall)
   player_click_damage = 10


   #Enemies
   enemyList = []
   defaultEnemySpawnCoolDown = 120
   enemySpawnCoolDown = 120
   totalEnemiesSpawned = 0
   enemySpawnRange = 400

   #Font
   font = pygame.font.SysFont(None, 36)


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

        #Placing Towers

        placingTower, towerNow, cost = shop.updatePurchasables(event_list, gold)

        if placing:
            place = placeItem(tower)
            placing, gold = place.update(towerList, gold, placingCost, event_list)
            place.draw(screen)

        if placingTower:
            placing = True
            tower = towerNow
            placingCost = cost
    

        #Player Stuff
        """
        goldBox = pygame.Rect(0, 0, 100, 50)
        goldBox.get_rect(center=(800, 650))
        pygame.draw.rect(screen, self.curr_color, goldBox)
        """
        text_surface = font.render("Gold: "+str(gold), True, (255, 215, 0))
        text_rect = text_surface.get_rect(center=(800, 650))
        screen.blit(text_surface, text_rect)

        #Enemy Stuff

        if enemySpawnCoolDown == 0:
            distance = 0
            while distance < enemySpawnRange:
                spawn_pos = (randint(0, screen.get_width()), randint(0, screen.get_height()))

                dx = townHall.pos[0] - spawn_pos[0]
                dy = townHall.pos[1] - spawn_pos[1]

                distance = (dx**2+dy**2)**0.5

                if distance >= enemySpawnRange:
                    enemyList.append(Enemy(int(totalEnemiesSpawned/4), spawn_pos))
                    totalEnemiesSpawned += 1

                enemySpawnCoolDown = defaultEnemySpawnCoolDown
        else:
            enemySpawnCoolDown -= 1

        for enemy in enemyList:
            if enemy.currentHealth <= 0:
                enemyList.remove(enemy)
                randomNum = randint(0, 100)
                if randomNum < 31:
                    gold += 1
                continue
            enemy.update(buildings, player_click_damage, event_list)
            enemy.draw(screen)

        #Tower Stuff

        for towerUnit in towerList:
            towerUnit.draw(screen)
            towerUnit.update()
            if towerUnit.attack_cooldown == 0:
                towerUnit.shootEnemy(enemyList)

        shop.drawPurchasables()

        pygame.display.update()

# Execute game:
main()