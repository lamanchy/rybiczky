from math import sin, cos, atan2, pi
from time import sleep, time

import pygame

FPS = 30


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

        Drawable.screen.blit(rotated_image, [self.position[0] - center[0], self.position[1] - center[1]])


class Fish(Drawable):
    acceleration_force = 0.01
    deceleration_force = 0.01
    inertia_force = 0.01

    normal_speed = 2
    maximum_speed = 5
    minimum_speed = 1

    turning_speed = 0.01

    def __init__(self, position, direction, image):
        super().__init__(position, direction, image)
        self.acceleration_mode = 'normal'
        self.turning = 0
        self.actual_speed = 1
        self.acceleration = 0

    def swim(self, direction):
        self.position[0] += self.direction[0] * direction
        self.position[1] += self.direction[1] * direction

    def turn(self, angle):
        x1, y1 = self.direction

        x2 = cos(angle) * x1 - sin(angle) * y1
        y2 = sin(angle) * x1 + cos(angle) * y1

        self.direction = x2, y2

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
        self.turn(self.turning_speed * self.turning)


class Trout(Fish):
    acceleration_force = 0.05
    deceleration_force = 0.05
    inertia_force = 0.01

    normal_speed = 1.5
    maximum_speed = 3
    minimum_speed = 0.5

    turning_speed = 0.01

    def __init__(self):
        myimage = pygame.image.load("trout.png")
        myimage = pygame.transform.scale(myimage, (200, 200))
        super().__init__([400, 400], [1, 0], myimage)


class Shark(Fish):
    acceleration_force = 0.1
    deceleration_force = 0.01
    inertia_force = 0.02

    normal_speed = 2
    maximum_speed = 6
    minimum_speed = 1.5

    turning_speed = 0.03

    def __init__(self):
        myimage = pygame.image.load("shark.png")
        myimage = pygame.transform.scale(myimage, (100, 100))
        super().__init__([400, 400], [1, 0], myimage)


fish = Shark()

pygame.init()

screen = pygame.display.set_mode([800, 800])
Drawable.screen = screen

running = True
actual_time = time()

while running:
    duration = time() - actual_time
    actual_time = time()

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

    if duration < 1 / FPS:
        sleep(1 / FPS - duration)

pygame.quit()
