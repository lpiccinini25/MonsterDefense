import functions

import pygame
from Views.shopMenu import Shop
from Views.placingItem import placeItem
from Views.buildings import TownHall
from globals import screen
from Views.enemies import Ghoul, Golem
from random import randint
from fonts import font

from Views.upgradeShop import UpgradeShop

from pygame.locals import *

class Main:
    def __init__(self):
        pygame.init()

    def button(self, x, y, w, h, text, color, hover_color, text_color, text_font):
        rect = pygame.Rect(x, y, w, h)
        rect.center = (x, y)
        pygame.draw.rect(screen, color, rect)
        functions.display_text(text, text_color, text_font, x, y)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x - w//2 < mouse[0] < x + w//2 and y - h//2 < mouse[1] < y + h//2:
            if click[0] == 1:
                return True
        return False

    def mainGameLoop(self):
        while True:
            self.run()
            self.end_screen()

    def run(self):

        #Images Preloaded
        tombstone_image = pygame.image.load("assets/Tombstone.png").convert()

        clock = pygame.time.Clock()

        run_game = True
        placing = False
        towerUpgrading = False
        tower = ""

        #Player
        class GameInfo:
            def __init__(self):
                self.tower_list = []
                self.building_list = []
                self.all_purchasables = []

                self.gold = 6
                self.player_click_damage = 0
                self.caps = {
                    'ArcherTowerCap' : 4,
                    'HouseCap' : 3,
                    'BombTowerCap' : 1
                }
            
            def update(self):
                self.all_purchasables = self.building_list + self.tower_list
        
        game_info = GameInfo()
        
        townHall = TownHall('TownHall', (screen.get_width()/2, screen.get_height()/2))
        game_info.building_list.append(townHall)
        game_info.update()
        player_click_damage = 0


        #Enemies
        enemyList = []
        totalEnemiesSpawned = 0
        enemySpawnRange = 300

        #Enemies -- Wave Mechanic
        baseLowWaveCD = 3000
        LowWaveCD = baseLowWaveCD
        baseLowEnemySpawnCD = 150

        baseHighWaveCD = 1000
        HighWaveCD = baseHighWaveCD
        baseHighEnemySpawnCD = 60

        waveNumber = 1

        #Enemies -- Spawn Area
        screen_h = screen.get_height()
        screen_w = screen.get_width()

        spawn_zone_x = int(screen.get_width()*2/5)
        spawn_zone_y = 0
        spawn_zone_w = 150
        spawn_zone_h = 150

        enemySpawnCoolDown = baseLowEnemySpawnCD


        while run_game:
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

            #Placing Towers

            placingTower, towerNameNow, costInstant = shop.updatePurchasables(event_list, game_info)

            if placing:
                place = placeItem(towerNamePlacing)
                placing = place.update(game_info, placingCost, event_list)
                place.draw(screen)

            if placingTower:
                placing = True
                towerNamePlacing = towerNameNow
                placingCost = costInstant
        
            shop.drawPurchasables()

            #Player Stuff/Important Info Displaying
            """
            display_text(text, color, font, x, y)
            """
            text_surface = font.render("Gold: "+str(game_info.gold), True, (255, 215, 0))
            text_rect = text_surface.get_rect(center=(700, screen.get_height()-50))
            screen.blit(text_surface, text_rect)

            if LowWaveCD == 0:
                waveSecondsLeft = int(HighWaveCD/60)
                currentWave = "High Enemy Spawn Period: " + str(waveSecondsLeft) +" till change."
            else:
                waveSecondsLeft = int(LowWaveCD/60)
                currentWave = "Low Enemy Spawn Period: " + str(waveSecondsLeft) +" till change."

            functions.display_text(currentWave, (255, 255, 255), font, 700, screen.get_height()-75)

            functions.display_text("Wave Number: "+str(waveNumber), (255, 255, 255), font, 700, screen.get_height()-100)

            functions.display_image(tombstone_image, spawn_zone_x+int(spawn_zone_w/2), spawn_zone_y+int(spawn_zone_h/2), 35)

            #Enemy Spawning

            if LowWaveCD >= 0:
                if enemySpawnCoolDown == 0:
                    distance = 0
                    while distance < enemySpawnRange:
                        spawn_pos = (randint(0, screen.get_width()), randint(0, screen.get_height()))

                        dx = townHall.pos[0] - spawn_pos[0]
                        dy = townHall.pos[1] - spawn_pos[1]

                        distance = (dx**2+dy**2)**0.5

                        if distance >= enemySpawnRange:
                            enemyList.append(Ghoul("Ghoul", waveNumber, spawn_pos))
                            totalEnemiesSpawned += 1

                        enemySpawnCoolDown = baseLowEnemySpawnCD
                        LowWaveCD -= 1
                else:
                    enemySpawnCoolDown -= 1
                    LowWaveCD -= 1
            elif HighWaveCD >= 0:
                if enemySpawnCoolDown == 0:
                    distance = 0
                    while distance < enemySpawnRange:
                        spawn_pos = (randint(spawn_zone_x, spawn_zone_x+spawn_zone_w), randint(spawn_zone_y, spawn_zone_y+spawn_zone_h))
                        print("pos:" + str(spawn_pos[1]), str(spawn_pos[0]))
                        dx = townHall.pos[0] - spawn_pos[0]
                        dy = townHall.pos[1] - spawn_pos[1]

                        distance = (dx**2+dy**2)**0.5

                        print("dis:" + str(distance))

                        if distance >= enemySpawnRange:
                            randNum = randint(1, 10)
                            if randNum > 9:
                                enemyList.append(Golem("Golem",waveNumber, spawn_pos))
                            else:
                                enemyList.append(Ghoul("Ghoul",waveNumber, spawn_pos))
                            totalEnemiesSpawned += 1

                        HighWaveCD -= 1
                        enemySpawnCoolDown = baseHighEnemySpawnCD
                else:
                    HighWaveCD -= 1
                    enemySpawnCoolDown -= 1
            else:
                if waveNumber % 2 == 0:
                    spawn_zone_x = int(screen.get_width()*randint(0, 4)/5)
                    spawn_zone_y = 0
                else:
                    spawn_zone_x = 0
                    spawn_zone_y = int(screen.get_height()*randint(0, 4)/5)
                waveNumber += 1
                LowWaveCD = baseLowWaveCD
                HighWaveCD = baseHighWaveCD

            #Tower Stuff

            for purchasable in game_info.all_purchasables:
                if purchasable.currentHealth <= 0:
                    if purchasable.title == "TownHall":
                        run_game = False
                if purchasable.update(game_info, event_list, enemyList):
                    towerUpgrading = True
                    towerInstanceUpgrading = purchasable
                    towerUpgradingName = purchasable.title
            
            #Tower Upgrading

            if towerUpgrading:
                upgradeShop = UpgradeShop(towerInstanceUpgrading)
                upgradeShop.drawShop()
                upgradeShop.updateUpgrades(event_list, game_info)

                if functions.is_clicked_elsewhere(towerInstanceUpgrading.image_rect, event_list):
                    towerUpgrading = False
            
            #Enemy Updating
            #print("amount of enemies"+str(len(enemyList)))
            for enemy in enemyList:
                if enemy.currentHealth <= 0:
                    enemyList.remove(enemy)
                    randomNum = randint(0, 100)
                    if randomNum < 31:
                        game_info.gold += 1
                    continue
                enemy.update(game_info, player_click_damage, event_list)
                enemy.draw(screen)


            pygame.display.update()

    def end_screen(self):
        end_screen = True

        clock = pygame.time.Clock()

        while end_screen:

            screen.fill((0,0,0))
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

            #def button(x, y, w, h, text, color, hover_color, text_color, action=None)
            screen_width = screen.get_width()
            screen_height = screen.get_height()

            if self.button(screen_width*2/6, screen_height*4/5, 100, 50, "Try Again!", (0, 200, 0), (0, 220, 0), (0, 0, 0), font):
                end_screen = False

            pygame.display.update()

# Execute game:
game_instance = Main()
game_instance.mainGameLoop()