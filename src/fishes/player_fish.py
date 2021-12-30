import pygame
from pygame import Vector2

from src.fish import Fish


class PlayerFish(Fish):
    acceleration_force = 0.02
    deceleration_force = 0.05
    inertia_force = 0.01

    normal_speed = 1.5
    maximum_speed = 10
    minimum_speed = 0.5

    turning_speed = 0.03

    def __init__(self):
        myimage = pygame.image.load("images/player_fish.png")
        super().__init__(Vector2(400, 400), Vector2(1, 0), myimage, 100)

