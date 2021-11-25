from math import sin, cos, atan2, pi
from time import sleep, time

import pygame

class Drawable:
    screen = None
    def __init__(self, position, direction, image, scale=1):
        self.position = position
        self.direction = direction
        self.image = image
        self.scale = scale

    def draw(self):
        angle = atan2(*reversed(self.direction)) * 180 / pi * -1
        rotated_image = pygame.transform.rotate(self.image, angle)
        center = rotated_image.get_rect().center
        print(rotated_image.get_rect(), center)

        Drawable.screen.blit(rotated_image, [self.position[0]-center[0], self.position[1]-center[1]])

class Fish(Drawable):
    def __init__(self, position, direction, image, speed=0.1):
        super().__init__(position, direction, image)
        self.speed = speed

    def swim(self, direction):
        self.position[0] += self.direction[0] * direction * self.speed
        self.position[1] += self.direction[1] * direction * self.speed

    def turn(self, angle):
        x1, y1 = self.direction

        x2 = cos(angle) * x1 - sin(angle) * y1
        y2 = sin(angle) * x1 + cos(angle) * y1

        self.direction = x2, y2

    def forward(self):
        self.swim(1)

    def backward(self):
        self.swim(-1)

    def turn_left(self):
        self.turn(-0.001)

    def turn_right(self):
        self.turn(0.001)

    def slow_down(self):
        self.speed = 'slowing'

    def accelerate(self):
        self.speed = 'accelerating'

    def reset_speed(self):
        self.speed = 'normal'

    def move(self, ratio):
        if self.speed == 'normal':
            if self.actual_speed <= self.normal_speed:
                # speed up up to normal speed
                self.acceleration += self.acceleration_force
                self.acceleration = min(self.acceleration, (self.normal_speed - self.actual_speed) / 2)
            else:
                # slow down linearly to normal speed
                self.acceleration = -self.inertia_force

        if self.speed == 'accelerating':
            # accelerate to maximum speed
            self.acceleration += self.acceleration_force
            self.acceleration = min(self.acceleration, (self.maximum_speed - self.actual_speed) / 2)

        if self.speed == 'slowing':
            # slow down down to minimum speed
            self.acceleration -= self.deceleration_force
            if abs(self.acceleration) > (self.actual_speed - self.minimum_speed) / 2:
                self.acceleration = -(self.actual_speed - self.minimum_speed) / 2

        # determine speed change based on self.acceleration
        self.actual_speed += self.acceleration * ratio
        self.swim(ratio * self.actual_speed)
        self.turn(0.01 * self.turning)

        print(f"{self.speed=}, {self.actual_speed=}, {self.acceleration=}")


class PlayerFish(Fish):
    def __init__(self):
        myimage = pygame.image.load("fish.jpg")
        myimage = pygame.transform.scale(myimage, (200, 200))
        super().__init__([0, 0], [1, 0], myimage)


fish = Shark()

pygame.init()

screen = pygame.display.set_mode([500, 500])
Drawable.screen = screen

x, y = 250, 250

running = True
actual_time = time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        fish.accelerate()
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        fish.slow_down()
    else:
        fish.reset_speed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        fish.turn_left()
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        fish.turn_right()
    else:
        fish.reset_turing()

    ratio = duration / (1 / FPS)
    fish.move(ratio)

    screen.fill((255, 255, 255))
    fish.draw()
    pygame.display.flip()

pygame.quit()
