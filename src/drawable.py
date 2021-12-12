import pygame
from pygame import Vector2

from src.constants import SCREEN_SIZE


class Drawable:
    screen = None

    def __init__(self, position: Vector2, direction: Vector2, image, scale=1):
        self.position = position
        self.direction = direction
        self.image = image
        self.scale = scale

    def draw(self):
        angle = self.direction.angle_to(Vector2(1, 0))
        rotated_image = pygame.transform.rotate(self.image, angle)
        center = Vector2(rotated_image.get_rect().center)
        #
        Drawable.screen.blit(rotated_image, (self.position - center).xy - self.offset + SCREEN_SIZE/2)
        # print(self.image)
        # Drawable.screen.blit(self.image, (self.position).xy)

    @classmethod
    def set_offset(cls, position):
        cls.offset = position

