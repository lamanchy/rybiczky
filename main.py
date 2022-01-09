from random import randint
from time import sleep, time

import pygame
from pygame import Vector2

from src.constants import SCREEN_SIZE, FPS
from src.drawable import Drawable
from src.fish import Fish
from src.fishes.computer_fish import ComputerFish
from src.fishes.player_fish import PlayerFish


# tady jsou fajne radky na upravu dat rybizcek
def main():
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

    last_spawn_fish_time = time()

    while running:
        duration = time() - actual_time
        actual_time = time()

        if time() - last_spawn_fish_time > 1:
            last_spawn_fish_time = time()
            categories = [
                ([50, 100], 36),
                ([100, 150], 25),
                ([150, 200], 16),
                ([200, 250], 9),
                ([250, 300], 4),
            ]
            for range, number in categories:
                fishes = [fish for fish in ComputerFish.computer_fishes if range[0] <= fish.size < range[1]]
                if len(fishes) < number:
                    r = max(*SCREEN_SIZE.xy) * 0.95
                    position = Vector2(0, r)
                    position = position.rotate(randint(0, 360))
                    position = player_fish.position + position
                    size = randint(*range)
                    if size < player_fish.size - 30:
                        image = pygame.image.load("images/smallest_fish.png")
                    elif size < player_fish.size:
                        image = pygame.image.load("images/medium_fish.png")
                    elif size < player_fish.size + 30:
                        image = pygame.image.load("images/big_fish.png")
                    else:
                        image = pygame.image.load("images/biggest_fishRed.png")
                    ComputerFish(image, position, size)
                    break

        running = handle_events(player_fish, running)

        move_fishes(duration, player_fish)

        screen.fill((255, 255, 255))
        Drawable.set_offset(player_fish.position)

        background_position = Vector2(round(player_fish.position.x / 800), round(player_fish.position.y / 800))
        for x in [0, 1]:
            for y in [0, 1]:
                pos = background_position + Vector2(x, y)

                q = int((7 * pos.x + 13 * pos.y) % 4)
                background.direction = [Vector2(0, 1), Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0)][q]
                background.position = pos * 800 - Vector2(400)
                background.draw()

        for fish in Fish.fishes:
            if fish.compute_collisions():
                if fish == player_fish:
                    print('you failed')
                    exit(0)
                Fish.fishes.remove(fish)

        player_fish.draw()
        for fish in ComputerFish.fishes:
            fish.draw()

        if ComputerFish.fishes:
            text_surface = myfont.render(f'Remaining: {len(ComputerFish.fishes)}', False, (0, 0, 0))
            screen.blit(text_surface, (0, 0))
        else:
            if end_time is None:
                end_time = time()
            text_surface = myfont.render(f'Time: {int(end_time - start_time)}s', False, (0, 0, 0))
            screen.blit(text_surface, (400, 400))

        if player_fish.size > 300:
            # print('succes')
            if end_time is None:
                end_time = time()
            text_surface = myfont.render(f'YOU WON - time: {int(end_time - start_time)}s', False, (0, 0, 0))
            screen.blit(text_surface, (350, 400))

        text_surface = myfont.render(f'FPS: {int(1 / (duration + 0.0001))}', False, (0, 0, 0))
        screen.blit(text_surface, (650, 0))

        pygame.display.flip()

        if duration < 1 / FPS:
            sleep(1 / FPS - duration)

    pygame.quit()


def move_fishes(duration, player_fish):
    ratio = duration / (1 / FPS)
    player_fish.move(ratio)

    for fish in ComputerFish.computer_fishes:
        fish.behave(player_fish)
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
