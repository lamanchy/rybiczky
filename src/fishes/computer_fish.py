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
        self.target = None
        super().__init__(position, Vector2(1, 0), None, size)

    def delete(self):
        super().delete()
        self.computer_fishes.remove(self)

    def switch_mode(self):
        if self.mode == 'calm':
            self.mode = 'attack'
            self.switch_time = randint(3, 6) + time()
        else:
            self.mode = 'calm'
            self.target = None
            self.switch_time = randint(15, 30) + time()

    def behave(self):
        actual_time = time()
        if actual_time > self.switch_time:
            self.switch_mode()

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
        if self.target is None:
            fishes = [fish for fish in Fish.fishes if self.size - 60 <= fish.size < self.size]
            fishes.sort(key=lambda fish: fish.position.distance_to(self.position))
            if fishes:
                self.target = fishes[0]

        if self.target:
            # if catched
            if self.target not in Fish.fishes:
                self.switch_mode()
                self.calm_behave()
                return

            fishes = [
                fish
                for fish in Fish.fishes
                if self.size < fish.size and
                   abs(self.direction.angle_to(fish.position - self.position)) < 60 and
                   fish.position.distance_to(self.position) < 100
            ]

            if fishes:
                self.switch_mode()
                self.calm_behave()
                return

            # hunt target
            target_position = self.target.position
            angle = (target_position - self.position).angle_to(self.direction)
            if angle < 180: angle += 360
            if angle > 180: angle -= 360

            if angle > 0:
                self.turn_left()
            else:
                self.turn_right()

            if abs(angle) < 30:
                self.accelerate()
            else:
                self.slow_down()

    def calm_behave(self):
        fishes = [
            (fish.position.distance_to(self.position), fish)
            for fish in Fish.fishes if self.size < fish.size
        ]
        fishes.sort(key=lambda t: t[0])
        for distance, fish in fishes:
            if distance < 100 or (fish.size <= self.size + 60 and distance < 300):
                # run away
                bigger_fish_position = fish.position + 50 * fish.direction
                angle = (self.position - bigger_fish_position).angle_to(self.direction)
                if angle < 180: angle += 360
                if angle > 180: angle -= 360

                if angle > 0:
                    self.turn_left()
                else:
                    self.turn_right()

                if abs(angle) > 150:
                    self.slow_down()
                else:
                    self.accelerate()

                break

        else:
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

        return False
