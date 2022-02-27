import pygame
from pygame import Vector2, mask


class Drawable:
    screen = None
    screen_size = None

    @classmethod
    def set_screen(cls, screen):
        cls.screen = screen
        cls.screen_size = Vector2(pygame.display.get_surface().get_size())

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

    def get_rotated_image(self):
        image = self.get_image_for_draw()
        angle = self.direction.angle_to(Vector2(1, 0))
        return pygame.transform.rotate(image, angle)

    def draw(self):
        rotated_image = self.get_rotated_image()
        center = Vector2(rotated_image.get_rect().center)
        position = (self.position - center).xy - self.offset + self.screen_size/2
        Drawable.screen.blit(rotated_image, position)

    def get_mask(self):
        rotated_image = self.get_rotated_image()
        return pygame.mask.from_surface(rotated_image)

    @classmethod
    def set_offset(cls, position):
        cls.offset = position
