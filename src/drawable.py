import pygame
from pygame import Vector2

from src.constants import SCREEN_SIZE


class Drawable:
    screen = None
    drawables = []

    def __init__(self, position: Vector2, direction: Vector2, image, scale=1):
        self.position = position
        self.direction = direction
        self.image = image
        self.scale = scale
        self.drawables.append(self)

    def delete(self):
        self.drawables.remove(self)

    def get_image_for_draw(self):
        return self.image

    def draw(self):
        image = self.get_image_for_draw()
        angle = self.direction.angle_to(Vector2(1, 0))
        rotated_image = pygame.transform.rotate(image, angle)
        center = Vector2(rotated_image.get_rect().center)
        Drawable.screen.blit(rotated_image, (self.position - center).xy - self.offset + SCREEN_SIZE/2)

    @classmethod
    def set_offset(cls, position):
        cls.offset = position

