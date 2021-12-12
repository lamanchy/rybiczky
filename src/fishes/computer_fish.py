from random import random

import pygame
from pygame import Vector2

from src.constants import SCREEN_SIZE
from src.fish import Fish


class ComputerFish(Fish):
    acceleration_force = 0.1
    deceleration_force = 0.05
    inertia_force = 0.1

    normal_speed = 2
    maximum_speed = 8
    minimum_speed = 1.5

    turning_speed = 0.04

    def __init__(self):
        myimage = pygame.image.load("images/fish2.png")
        position = Vector2(SCREEN_SIZE)
        position.x *= random()
        position.y *= random()
        # size = 300
        # myimage = pygame.transform.scale(myimage, (size, size/3))
        super().__init__(position, Vector2(1, 0), myimage, automatic=True)

