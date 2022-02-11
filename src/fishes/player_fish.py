import pygame
from pygame import Vector2

from src.fish import Fish


class PlayerFish(Fish):
    starting_size = 100

    def __init__(self):
        myimage = pygame.image.load("images/player_fish.png")
        super().__init__(Vector2(0, 0), Vector2(1, 0), myimage, self.starting_size)

