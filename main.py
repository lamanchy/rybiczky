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

class PlayerFish(Fish):
    def __init__(self):
        myimage = pygame.image.load("fish.jpg")
        myimage = pygame.transform.scale(myimage, (200, 200))
        super().__init__([0, 0], [1, 0], myimage)


fish = PlayerFish()

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

    duration = time() - actual_time

    if keys[pygame.K_w]:
        fish.forward()
    if keys[pygame.K_s]:
        fish.backward()
    if keys[pygame.K_a]:
        fish.turn_left()
    if keys[pygame.K_d]:
        fish.turn_right()

    actual_time = time()

    screen.fill((255, 255, 255))
    fish.draw()
    pygame.display.flip()

pygame.quit()
