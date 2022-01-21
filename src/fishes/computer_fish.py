from random import random, randint
from time import time, sleep

import pygame
from pygame import Vector2

from src.constants import RESET_DISTANCE
from src.fish import Fish


class ComputerFish(Fish):
    acceleration_force = 0.1
    deceleration_force = 0.05
    inertia_force = 0.1

    normal_speed = 2
    maximum_speed = 8
    minimum_speed = 1.5

    turning_speed = 0.04

    computer_fishes = []

    def __init__(self, position, size):
        self.switch_time = time()
        self.mode = 'attack'
        self.computer_fishes.append(self)
        super().__init__(position, Vector2(1, 0), None, size)

    def delete(self):
        super().delete()
        self.computer_fishes.remove(self)

    def behave(self):
        actual_time = time()
        if actual_time > self.switch_time:
            if self.mode == 'calm':
                self.mode = 'attack'
                self.switch_time = randint(3, 6) + time()
            else:
                self.mode = 'calm'
                self.switch_time = randint(15, 30) + time()

        if self.mode == 'calm':
            self.calm_behave()

        if self.mode == 'attack':
            self.attack_behave()

    def reset_fish_position(self, player_fish):
        distance = player_fish.position.distance_to(self.position)

        if distance > RESET_DISTANCE:
            vector = player_fish.position - self.position
            self.position += 1.9 * vector

            category = self.size % 120

            if category <= 30:
                self.image = pygame.image.load("images/big_fish.png")
            elif category <= 60:
                self.image = pygame.image.load("images/biggest_fishRed.png")
            elif category <= 90:
                self.image = pygame.image.load("images/smallest_fish.png")
            else:
                self.image = pygame.image.load("images/medium_fish.png")

        if self.size > 300:
            self.delete()

    def attack_behave(self):
        # TODO
        pass

    def calm_behave(self):
        if random() < 0.01:
            self.accelerate()
        if random() < 0.01:
            self.slow_down()
        if random() < 0.01:
            self.reset_speed()
        if random() < 0.01:
            self.turn_left()
        if random() < 0.01:
            self.turn_right()
        if random() < 0.01:
            self.reset_turing()

        # TODO
        # for closest bigger fish
            # if distance < 300:
            #     player_fish_position = fish.position + 50 * fish.direction
            #     angle = (self.position - player_fish_position).angle_to(self.direction)
            #     if angle < 180: angle += 360
            #     if angle > 180: angle -= 360
            #
            #     if angle > 0:
            #         self.turn_left()
            #     else:
            #         self.turn_right()
            #
            #     if abs(angle) > 150:
            #         self.slow_down()
            #     else:
            #         self.accelerate()

        return False
