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



    def draw(self):
        rotated_image = self.get_rotated_image()
        center = Vector2(rotated_image.get_rect().center)
        position = (self.position - center).xy - self.offset + self.screen_size/2
        PlayerFish.screen.blit(rotated_image, position)
