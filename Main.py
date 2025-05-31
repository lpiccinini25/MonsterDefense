import functions

import pygame
from Views.shopMenu import Shop
from Views.placingItem import placeItem
from Views.townHall import TownHall
from globals import screen
from Views.enemies import Enemy
from random import randint
from fonts import font

from Views.upgradeShop import UpgradeShop

from pygame.locals import *
clock = pygame.time.Clock()

def main():

   placing = False
   towerUpgrading = False
   tower = ""

   #Player
   towerList = []
   gold = 10
   buildings = []
   townHall = TownHall()
   buildings.append(townHall)
   player_click_damage = 5


   #Enemies
   enemyList = []
   totalEnemiesSpawned = 0
   enemySpawnRange = 400

   #Enemies -- Wave Mechanic
   baseLowWaveCD = 3000
   LowWaveCD = baseLowWaveCD
   baseLowEnemySpawnCD = 150

   baseHighWaveCD = 1000
   HighWaveCD = baseHighWaveCD
   baseHighEnemySpawnCD = 40

   enemySpawnCoolDown = baseLowEnemySpawnCD


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

        #Building Stuff

        for building in buildings:
            if building.currentHealth <= 0:
                if building.title == "House":
                    buildings.remove(building)
                    continue
            if building.update():
                gold += 1


        #Placing Towers

        placingTower, towerNameNow, costInstant = shop.updatePurchasables(event_list, gold)

        if placing:
            place = placeItem(towerNamePlacing)
            placing, gold = place.update(towerList, buildings, gold, placingCost, event_list)
            place.draw(screen)

        if placingTower:
            placing = True
            towerNamePlacing = towerNameNow
            placingCost = costInstant
    
        shop.drawPurchasables()

        #Player Stuff/Important Info Displaying
        """
        goldBox = pygame.Rect(0, 0, 100, 50)
        goldBox.get_rect(center=(800, 650))
        pygame.draw.rect(screen, self.curr_color, goldBox)


        display_text(text, color, font, x, y)
        """
        text_surface = font.render("Gold: "+str(gold), True, (255, 215, 0))
        text_rect = text_surface.get_rect(center=(800, 650))
        screen.blit(text_surface, text_rect)

        if LowWaveCD == 0:
            currentWave = "High Enemy Spawn Period"
        else:
            currentWave = "Low Enemy Spawn Period"

        functions.display_text(currentWave, (255, 255, 255), font, 750, 50)

        #Enemy Spawning

        if LowWaveCD != 0:
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

                    enemySpawnCoolDown = baseLowEnemySpawnCD
                    LowWaveCD -= 1
                    print(LowWaveCD)
            else:
                enemySpawnCoolDown -= 1
                LowWaveCD -= 1
        elif HighWaveCD != 0:
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

                    HighWaveCD -= 1
                    enemySpawnCoolDown = baseHighEnemySpawnCD
            else:
                HighWaveCD -= 1
                enemySpawnCoolDown -= 1
        else:
            LowWaveCD = baseLowWaveCD
            HighWaveCD = baseHighWaveCD
    
        #Enemy Updating

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
            if towerUnit.update(event_list):
                towerUpgrading = True
                towerInstanceUpgrading = towerUnit
                towerUpgradingName = towerUnit.tower

            if towerUnit.attack_cooldown == 0:
                towerUnit.shootEnemy(enemyList)
        
        #Tower Upgrading

        if towerUpgrading:
            upgradeShop = UpgradeShop(towerInstanceUpgrading)
            upgradeShop.drawShop()
            gold = upgradeShop.updateUpgrades(event_list, gold)

            if functions.is_clicked_elsewhere(towerInstanceUpgrading.image_rect, event_list):
                towerUpgrading = False


        pygame.display.update()

# Execute game:
main()