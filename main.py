from time import sleep, time

import pygame
from pygame import Vector2

from src.constants import SCREEN_SIZE, FPS
from src.drawable import Drawable
from src.fishes.computer_fish import ComputerFish
from src.fishes.player_fish import PlayerFish


def main():
    computer_fishes = [ComputerFish() for _ in range(50)]

    player_fish = PlayerFish()
    background = Drawable(Vector2(0, 0), Vector2(0, 1), pygame.image.load('images/background.png'))

    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans ', 30)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    Drawable.screen = screen

    running = True
    actual_time = time()
    start_time = time()
    end_time = None

    while running:
        duration = time() - actual_time
        actual_time = time()

        running = handle_events(player_fish, running)

        move_fishes(computer_fishes, duration, player_fish)

        screen.fill((255, 255, 255))
        Drawable.set_offset(player_fish.position)

        background_position = Vector2(round(player_fish.position.x / 800), round(player_fish.position.y / 800))
        for x in [0, 1]:
            for y in [0, 1]:
                pos = background_position + Vector2(x, y)

                q = int((7*pos.x + 13*pos.y) % 4)
                background.direction = [Vector2(0, 1), Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0)][q]
                background.position = pos*800 - Vector2(400)
                background.draw()

        player_fish.draw()
        for fish in computer_fishes:
            fish.draw()

        if computer_fishes:
            textsurface = myfont.render(f'Remaining: {len(computer_fishes)}', False, (0, 0, 0))
            screen.blit(textsurface, (0, 0))
        else:
            if end_time is None:
                end_time = time()
            textsurface = myfont.render(f'Time: {int(end_time - start_time)}s', False, (0, 0, 0))
            screen.blit(textsurface, (400, 400))

        textsurface = myfont.render(f'FPS: {int(1 / (duration + 0.0001))}', False, (0, 0, 0))
        screen.blit(textsurface, (650, 0))

        pygame.display.flip()

        if duration < 1 / FPS:
            sleep(1 / FPS - duration)

    pygame.quit()


def move_fishes(computer_fishes, duration, player_fish):
    ratio = duration / (1 / FPS)
    player_fish.move(ratio)
    for fish in computer_fishes:
        distance = player_fish.position.distance_to(fish.position)
        if distance < 50:
            computer_fishes.remove(fish)
        if distance < 300:
            player_fish_position = player_fish.position + 50 * player_fish.direction
            angle = (fish.position - player_fish_position).angle_to(fish.direction)
            if angle < 180: angle += 360
            if angle > 180: angle -= 360

            if angle > 0:
                fish.turn_left()
            else:
                fish.turn_right()

            if abs(angle) > 150:
                fish.slow_down()
            else:
                fish.accelerate()
            # sdasdasdasdasdasdadw

        if distance > max(*SCREEN_SIZE.xy):
            vector = player_fish.position - fish.position
            fish.position = fish.position + 1.9 * vector

        fish.move(ratio)


def handle_events(player_fish, running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_fish.accelerate()
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_fish.slow_down()
    else:
        player_fish.reset_speed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_fish.turn_left()
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_fish.turn_right()
    else:
        player_fish.reset_turing()

    return running


if __name__ == "__main__":
    main()
