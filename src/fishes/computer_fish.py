from random import random, randint
from time import time, sleep

import pygame
from pygame import Vector2

from src.constants import SCREEN_SIZE
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

    def __init__(self, size):
        myimage = pygame.image.load("images/medium_fish.png")
        position = Vector2(SCREEN_SIZE)
        position.x *= random()
        position.y *= random()
        self.switch_time = time()
        self.mode = 'attack'
        self.computer_fishes.append(self)
        super().__init__(position, Vector2(1, 0), myimage, size)

    def behave(self, player_fish):
        actual_time = time()
        if actual_time > self.switch_time:
            if self.mode == 'calm':
                self.mode = 'attack'
                self.switch_time = randint(3, 6) + time()
            else:
                self.mode = 'calm'
                self.switch_time = randint(15, 30) + time()

        if self.mode == 'calm':
            if self.calm_behave():
                return True

        if self.mode == 'attack':
            self.attack_behave()

        self.reset_fish_position(player_fish)

    def reset_fish_position(self, player_fish):
        distance = player_fish.position.distance_to(self.position)

        if distance > max(*SCREEN_SIZE.xy):
            vector = player_fish.position - self.position
            self.position = self.position + 1.9 * vector

    def attack_behave(self):

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
