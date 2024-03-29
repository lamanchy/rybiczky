from math import pi

import pygame
from pygame import Vector2

from src.constants import SCALE
from src.drawable import Drawable


class Fish(Drawable):
    min_size = 50 * SCALE
    max_size = 300 * SCALE

    def get_handicap(self):
        return self.handicap

    def get_value_based_on_size(self, start, end):
        result = (end - start) * (self.size - self.min_size) / (self.max_size - self.min_size) + start
        return result * SCALE * self.get_handicap()

    @property
    def acceleration_force(self):
        return self.get_value_based_on_size(0.02, 0.005)
    @property
    def deceleration_force(self):
        return self.get_value_based_on_size(0.04, 0.01)
    @property
    def inertia_force(self):
        return self.get_value_based_on_size(0.05, 0.01)
    @property
    def normal_speed(self):
        return self.get_value_based_on_size(3, 10)
    @property
    def maximum_speed(self):
        return self.get_value_based_on_size(5, 15)
    @property
    def minimum_speed(self):
        return self.get_value_based_on_size(0.1, 5)
    @property
    def turning_speed(self):
        return self.get_value_based_on_size(0.1, 0.025)

    fishes = []

    def __init__(self, position: Vector2, direction: Vector2, image, size, handicap=1):
        super().__init__(position, direction, image)
        self.handicap = handicap
        self.turning = 0
        self.size = size * SCALE
        self.actual_speed = self.normal_speed
        self.acceleration = 0
        self.speed = 'normal'
        self.fishes.append(self)

    def delete(self):
        super().delete()
        self.fishes.remove(self)

    def get_rotated_image(self):
        image = self.get_image_for_draw()
        scale = self.size / self.image.get_width()
        new_height = (self.size / self.image.get_width()) * self.image.get_height()
        image = pygame.transform.smoothscale(image, (self.size, new_height))
        angle = self.direction.angle_to(Vector2(1, 0))
        return pygame.transform.rotozoom(image, angle, 1)

    def swim(self, direction):
        self.position += self.direction * direction

    def turn(self, angle):
        self.direction = self.direction.rotate(angle / pi * 180)

    def turn_left(self):
        self.turning = -1

    def turn_right(self):
        self.turning = 1

    def reset_turing(self):
        self.turning = 0

    def slow_down(self):
        self.speed = 'slowing'

    def accelerate(self):
        self.speed = 'accelerating'

    def reset_speed(self):
        self.speed = 'normal'

    def compute_collisions(self):
        for fish in self.fishes:
            if fish.size > self.size:
                # if fish.mask.overlap(self.mask, (0, 0)):
                #     return True
                distance = fish.position.distance_to(self.position)
                # if distance is more than size of bigger fish, there wont be ever collision
                if distance < fish.size:
                    fish_mask = pygame.mask.Mask((1, 1), fill=True)
                    self_mask = self.get_mask()
                    if fish_mask.overlap(self_mask, (self.position - Vector2(self_mask.get_size())/2) - (fish.position + fish.direction*fish.size/2)) is not None:
                        self.transfer_health_to(fish)
                        return True

    def transfer_health_to(self, other):
        difference = (other.size ** 3 + 0.25 * self.size ** 3) ** (1 / 3) - other.size
        other.size += difference
        other.size = min(self.max_size * 1.1, other.size)
        self.size -= difference

    def move(self, ratio):
        if self.speed == 'normal':
            if self.actual_speed <= self.normal_speed:
                # speed up up to normal speed
                self.acceleration += self.acceleration_force
                if abs(self.acceleration) > (self.normal_speed - self.actual_speed) / 2:
                    self.acceleration = (self.normal_speed - self.actual_speed) / 2
            else:
                # slow down linearly to normal speed
                self.acceleration = -self.inertia_force

        if self.speed == 'accelerating':
            # accelerate to maximum speed
            self.acceleration += self.acceleration_force
            if abs(self.acceleration) > (self.maximum_speed - self.actual_speed) / 2:
                self.acceleration = (self.maximum_speed - self.actual_speed) / 2

        if self.speed == 'slowing':
            # slow down down to minimum speed
            self.acceleration -= self.deceleration_force
            if abs(self.acceleration) > (self.actual_speed - self.minimum_speed) / 2:
                self.acceleration = -(self.actual_speed - self.minimum_speed) / 2

        # determine speed change based on self.acceleration
        self.actual_speed += self.acceleration * ratio
        # if self.actual_speed < self.minimum_speed:
        #     self.actual_speed = self.minimum_speed
        self.swim(ratio * abs(self.actual_speed))
        self.turn(self.turning_speed * self.turning)

