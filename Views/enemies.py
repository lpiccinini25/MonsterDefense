import pygame
import random

class Enemy:
    def __init__(scaling):
        self.health = random.randint(40, scaling*3)
        self.speed = random.randint(1, scaling*0.25)
        self.damage = random.randint(10, scaling)