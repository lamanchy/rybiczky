a = [
    'Eduard',
    'John',
    'Evans',
    'Šimon',
    'Adam',
    'Zuzka'
]

a.sort()

print(a)

exit()














from time import sleep, time

import pygame

pygame.init()

screen = pygame.display.set_mode([500, 500])

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
        y -= duration * 10
    if keys[pygame.K_s]:
        y += duration * 10
    if keys[pygame.K_a]:
        x -= duration * 10
    if keys[pygame.K_d]:
        x += duration * 10

    actual_time = time()

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 255), (x, y), 75)
    pygame.display.flip()

pygame.quit()
