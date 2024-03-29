from os.path import join

import pygame
from pygame import Vector2

from src.constants import BASE_PATH
from src.fish import Fish


class PlayerFish(Fish):
    starting_size = 100

    def __init__(self, handicap):
        myimage = pygame.image.load(join(BASE_PATH, 'images', 'player_fish.png')).convert_alpha()
        super().__init__(Vector2(0, 0), Vector2(1, 0), myimage, self.starting_size, handicap)

    def get_handicap(self):
        start = self.handicap
        end = self.handicap - 0.2
        return (end - start) * (self.size - self.min_size) / (self.max_size - self.min_size) + start