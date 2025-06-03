import pygame
from globals import screen, GameInfo
from Views.enemies import Ghoul, Golem, Wizard
import functions

from random import randint


class WaveManager:
    def __init__(self):

        #Wave Strength
        self.wave_number: int = 1
        self.number_of_enemies: int = 6
        self.left_to_spawn: int = self.number_of_enemies
        self.enemy_strength: int = self.wave_number

        #Wave duration
        self.low_enemy_spawn_duration: int = 2700
        self.wave_duration: int = self.low_enemy_spawn_duration
        self.low_enemy_spawn: bool = True

        #Big Wave Zone Size
        self.spawn_zone_x = int(screen.get_width()*2/5)
        self.spawn_zone_y = 0
        self.spawn_zone_w = 150
        self.spawn_zone_h = 150

        #Spawn cooldowns
        self.high_enemy_spawn_cooldown: int = 40
        self.low_enemy_spawn_cooldown: int = 240
        self.enemy_spawn_cooldown: int = self.low_enemy_spawn_cooldown

        #Spawn Restrictions
        self.spawn_distance: int = 300

    def spawn_ghoul(self, game_info: GameInfo, pos: list[int]) -> None:
        game_info.enemy_list.append(Ghoul("Ghoul", self.enemy_strength, pos))
    
    def spawn_golem(self, game_info: GameInfo, pos: list[int]) -> None:
        game_info.enemy_list.append(Golem("Golem", self.enemy_strength, pos))
    
    def spawn_wizard(self, game_info: GameInfo, pos: list[int]) -> None:
        game_info.enemy_list.append(Wizard("Wizard", self.enemy_strength, pos))

    def spawn_in_zone(self, game_info: GameInfo, spawn_zone_x: int, spawn_zone_y: int):
        if self.left_to_spawn > 0:
            if self.enemy_spawn_cooldown == 0:
                spawn_pos = (randint(spawn_zone_x, spawn_zone_x+self.spawn_zone_w), randint(spawn_zone_y, spawn_zone_y+self.spawn_zone_h))
                randNum = randint(1, 100)
                if randNum < 60:
                    self.spawn_ghoul(game_info, spawn_pos)
                elif randNum < 90 :
                    self.spawn_wizard(game_info, spawn_pos)
                else:
                    self.spawn_golem(game_info, spawn_pos)

                self.left_to_spawn -= 1
                self.enemy_spawn_cooldown = self.high_enemy_spawn_cooldown
            else:
                self.enemy_spawn_cooldown -= 1
        else:
            if self.wave_number % 2 == 0:
                self.spawn_zone_x = int(screen.get_width()*randint(0, 4)/5)
                rand = randint(1, 2)
                if rand % 2 == 0:
                    self.spawn_zone_y = 0
                else:
                    self.spawn_zone_y = 4*screen.get_height()/5
            else:
                self.spawn_zone_y = int(screen.get_height()*randint(0, 4)/5)
                rand = randint(1, 2)
                if rand % 2 == 0:
                    self.spawn_zone_x = 0
                else:
                    self.spawn_zone_x = 4*screen.get_width()/5
            self.number_of_enemies += 2
            self.left_to_spawn = self.number_of_enemies
            self.wave_number += 1
            self.low_enemy_spawn = True
    
    def spawn_random(self, game_info: GameInfo) -> None:
            if self.wave_duration <= 0:
                self.low_enemy_spawn = False
                self.wave_duration = self.low_enemy_spawn_duration

            if self.enemy_spawn_cooldown == 0:
                distance = 0
                while distance < self.spawn_distance:
                    spawn_pos = (randint(0, screen.get_width()), randint(0, screen.get_height()))
                    middle_of_screen = [screen.get_width()/2, screen.get_height()/2]

                    distance = functions.find_distance(spawn_pos, middle_of_screen)

                    if distance >= self.spawn_distance:
                        randNum = randint(1, 100)
                        if randNum < 70:
                            self.spawn_ghoul(game_info, spawn_pos)
                        else:
                            self.spawn_wizard(game_info, spawn_pos)

                    self.enemy_spawn_cooldown = self.low_enemy_spawn_cooldown
                    self.wave_duration -= 1
            else:
                self.enemy_spawn_cooldown -= 1
                self.wave_duration -= 1
    
    def update_wave(self, game_info: GameInfo) -> None:
        if self.low_enemy_spawn:
            self.spawn_random(game_info)
        else:
            self.spawn_in_zone(game_info, self.spawn_zone_x, self.spawn_zone_y)