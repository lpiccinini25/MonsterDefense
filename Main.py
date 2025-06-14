import functions

import pygame
from views.item_shop import Shop
from views.buildings import TownHall
from globals import screen, GameInfo, height, width
from views.enemies import Ghoul, Golem, Wizard
from random import randint
from fonts import font

from views.upgrade_shop import UpgradeShop

from pygame.locals import *

from wave_manager import WaveManager

class Main:
    def __init__(self):
        pygame.init()
        self.state: str = "START_SCREEN"
        self.points_earned: list[int] = []
        self.monster_logo_image: pygame.Surface = functions.load_image("MonsterDefense", 200)

    def button(self, x, y, w, h, text, color, hover_color, text_color, text_font) -> bool:
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

    def mainGameLoop(self) -> None:
        while True:
            if self.state == "START_SCREEN":
                self.start_screen()
            elif self.state == "RUN_GAME":
                self.run()
            elif self.state == "END_SCREEN":
                self.end_screen()

    def start_screen(self) -> None:
        start_screen = True

        clock = pygame.time.Clock()

        while start_screen:

            screen.fill((0,0,0))
            functions.display_image_new_rect(self.monster_logo_image, int(width/2), 200)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == QUIT:
                    pygame.quit()
                    return
            clock.tick(60)

            if self.button(int(width/2), height*3/5, 100, 50, "Start a Game!", (0, 200, 0), (0, 220, 0), (0, 0, 0), font):
                start_screen = False
                self.state = "RUN_GAME"

            pygame.display.update()

    def run(self) -> None:

        clock = pygame.time.Clock()
        def pause_screen() -> None:
            paused = True
            while paused:
                event_list = pygame.event.get()
                for event in event_list:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        paused = False
                clock.tick(60)
                functions.display_rect(int(width/2), int(height/2), 200, 200, (100, 100, 100))
                functions.display_text("Paused! Press Escape To Return", (255, 255, 255), font, int(width/2), int(height/2))
                pygame.display.update()

        #Images Preloaded
        tombstone_image = functions.load_image("Tombstone", 35)

        run_game = True
        placing = False
        towerUpgrading = False
        tower = ""

        game_info = GameInfo()
        
        townHall = TownHall('TownHall', (int(screen.get_width()/2), int(screen.get_height()/2)))
        game_info.building_list.append(townHall)
        game_info.update()
        player_click_damage = 0

        #Testing
        #game_info.enemy_list.append(Wizard("Wizard", 1, (0,0)))

        #initialize core classes
        shop = Shop(game_info)
        wave_manager = WaveManager()

        while run_game:
            screen.fill((0, 0, 0))

            event_list = pygame.event.get()
            for event in event_list:
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_screen()
                    
            clock.tick(60)
            #if item is in process of being placed, constantly check if user presses mouse. cannot place over buttons.

            #Player Stuff/Important Info Displaying
            """
            display_text(text, color, font, x, y)
            """
            text_surface = font.render("Gold: "+str(game_info.gold), True, (255, 215, 0))
            text_rect = text_surface.get_rect(center=(700, screen.get_height()-50))
            screen.blit(text_surface, text_rect)

            if wave_manager.low_enemy_spawn:
                waveSecondsLeft = int(wave_manager.wave_duration/60)
                currentWave = "Low Enemy Spawn Period: " + str(waveSecondsLeft) +" till change."
            else:
                currentWave = "Wave Incoming!"

            functions.display_text(currentWave, (255, 255, 255), font, 700, screen.get_height()-75)

            functions.display_text("Wave Number: "+str(wave_manager.wave_number), (255, 255, 255), font, 700, screen.get_height()-100)

            functions.display_text("Points: "+str(game_info.point_total), (255, 255, 255), font, 700, screen.get_height()-125)

            functions.display_image_new_rect(tombstone_image, wave_manager.spawn_zone_x+int(wave_manager.spawn_zone_w/2), wave_manager.spawn_zone_y+int(wave_manager.spawn_zone_h/2))

            #Tower Stuff

            for purchasable in game_info.all_purchasables:
                if purchasable.current_health <= 0:
                    if purchasable.title == "TownHall":
                        self.state = "END_SCREEN"
                        self.points_earned.append(game_info.point_total)
                        run_game = False
                if purchasable.update(game_info, event_list):
                    towerUpgrading = True
                    towerInstanceUpgrading = purchasable
                    towerUpgradingName = purchasable.title

            #Placing Towers
            shop.update_menu(event_list, game_info)
            
            #Unattackables

            for unattackable in game_info.unattackable_list:
                unattackable.update(game_info)
            
            #Tower Upgrading

            if towerUpgrading:
                upgradeShop = UpgradeShop(towerInstanceUpgrading)
                upgradeShop.updateUpgrades(event_list, game_info)
                upgradeShop.drawShop()

                if functions.is_clicked_elsewhere(towerInstanceUpgrading.image_rect, event_list):
                    towerUpgrading = False
            
            #Enemy Spawning 

            wave_manager.update_wave(game_info)

            #Enemy Updating
            #print("amount of enemies"+str(len(enemyList)))
            for enemy in game_info.enemy_list:
                if enemy.current_health <= 0:
                    game_info.enemy_list.remove(enemy)
                    game_info.point_total += enemy.points
                    randomNum = randint(0, 100)
                    if randomNum < 31:
                        game_info.gold += 1
                    continue
                enemy.update(game_info, event_list)
                enemy.draw()


            pygame.display.update()

    def end_screen(self) -> None:
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

            functions.display_image_new_rect(self.monster_logo_image, int(width/2), 200)

            functions.display_text("You earned " + str(self.points_earned[len(self.points_earned)-1]) + " points!", (255, 255, 255), font, int(width/2), 550)

            for i in range(1, len(self.points_earned)):
                inc = i*25
                functions.display_text(str(self.points_earned[i]) + " points!", (255, 255, 255), font, int(width/2), 550+inc)

            if self.button(screen_width/2, screen_height*4/5, 100, 50, "Try Again!", (0, 200, 0), (0, 220, 0), (0, 0, 0), font):
                end_screen = False
                self.state = "RUN_GAME"

            pygame.display.update()

# Execute game:
game_instance = Main()
game_instance.mainGameLoop()