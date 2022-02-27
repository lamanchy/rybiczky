from random import randint
from time import sleep, time


import pygame
from pygame import Vector2

from src.constants import FPS, RESET_DISTANCE, SCALE, FULLSCREEN, DEBUG
from src.drawable import Drawable
from src.fish import Fish
from src.fishes.computer_fish import ComputerFish
from src.fishes.player_fish import PlayerFish

from src.text import render_text


def main():

    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Consolas ', 30)

    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 800))
    Drawable.set_screen(screen)

    player_fish = PlayerFish()
    background = Drawable(Vector2(0, 0), Vector2(0, 1), pygame.image.load('images/background.png').convert())

    running = True
    start_time = time()
    end_time = None

    failed = False

    last_spawn_fish_time = time()
    clock = pygame.time.Clock()

    while running:
        duration = clock.tick(FPS) / 1000

        key_pressed = pygame.key.get_pressed()

        if time() - last_spawn_fish_time > 1:
            last_spawn_fish_time = time()
            categories = [
                ([50, 100], 4),
                ([100, 150], 4),
                ([150, 200], 4),
                ([200, 250], 4),
                ([250, 300], 4),
            ]
            for range, number in categories:
                fishes = [fish for fish in ComputerFish.computer_fishes if range[0]*SCALE <= fish.size < range[1]*SCALE]
                if len(fishes) < number:
                    position = Vector2(0, RESET_DISTANCE * 1.1)
                    position = position.rotate(randint(0, 360))
                    position = player_fish.position + position
                    size = randint(*range)
                    ComputerFish(position, size)

        running = handle_events(player_fish, running)

        move_fishes(duration, player_fish)

        screen.fill((255, 255, 255))
        Drawable.set_offset(player_fish.position)

        background_position = Vector2(round(player_fish.position.x / 800), round(player_fish.position.y / 800))
        for x in [0, 1, 2]:
            for y in [0, 1, 2]:
                pos = background_position + Vector2(x, y)

                q = int((7 * pos.x + 13 * pos.y) % 4)
                background.direction = [Vector2(0, 1), Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0)][q]
                background.position = pos * 800 - Vector2(800)
                background.draw()

        for fish in Fish.fishes:
            if fish.compute_collisions() and fish.size < 50 *  SCALE:
                if fish == player_fish:
                    print('you failed')
                    failed = True
                    # player_fish.size = player_fish.starting_size
                    # exit(0)
                fish.delete()

        for fish in Fish.fishes:
            fish.draw()

        if key_pressed[pygame.K_f] and DEBUG:
            failed = True

        if failed:
            render_text([
                'You\'ve got eaten.',
                'Press r to restart'
            ], 'middle', myfont)
            if key_pressed[pygame.K_r]:
                failed = False

                while ComputerFish.computer_fishes:
                    ComputerFish.computer_fishes[0].delete()
                player_fish = PlayerFish()

        if player_fish.size > Fish.max_size:
            # print('succes')
            if end_time is None:
                end_time = time()
            render_text(f'YOU WON - time: {int(end_time - start_time)}s', 'middle', myfont)

        render_text([
            f'FPS: {int(1 / (duration + 0.0001))}',
            f'Score: {player_fish.size - PlayerFish.starting_size * SCALE}'
        ], 'left', myfont, Vector2(0, 0))

        pygame.display.flip()

    pygame.quit()


def move_fishes(duration, player_fish):
    ratio = duration / (1 / 30)
    player_fish.move(ratio)

    for fish in ComputerFish.computer_fishes:
        fish.behave()
        fish.reset_fish_position(player_fish)
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
    elif keys[pygame.K_ESCAPE]:
        exit(0)
    else:
        player_fish.reset_turing()

    return running


if __name__ == "__main__":
    main()
