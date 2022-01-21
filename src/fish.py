from math import pi
from math import sqrt

import pygame

from pygame import Vector2

from src.drawable import Drawable


class Fish(Drawable):
    acceleration_force = 0.01
    deceleration_force = 0.01
    inertia_force = 0.01

    normal_speed = 2
    maximum_speed = 5
    minimum_speed = 1

    turning_speed = 0.05

    fishes = []

    def __init__(self, position: Vector2, direction: Vector2, image, size):
        super().__init__(position, direction, image)
        self.turning = 0
        self.actual_speed = self.normal_speed
        self.acceleration = 0
        self.speed = 'normal'
        self.size = size
        self.fishes.append(self)

    def delete(self):
        super().delete()
        self.fishes.remove(self)

    def get_image_for_draw(self):
        new_height = (self.size / self.image.get_width()) * self.image.get_height()
        return pygame.transform.scale(self.image, (self.size, new_height))

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
                if distance < fish.size/2:
                    angle = (self.position - fish.position).angle_to(fish.direction)
                    if abs(angle) <= 15:
                        fish.size = (fish.size ** 3 + 0.5 * self.size ** 3)**(1/3)
                        return True

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
        self.swim(ratio * self.actual_speed)
        self.turn(self.turning_speed * self.turning)
