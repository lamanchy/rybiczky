import pygame
from pygame import Vector2
from time import time
from random import randint

from src.constants import FULLSCREEN, FPS, SCALE, RESET_DISTANCE, DEBUG
from src.drawable import Drawable
from src.text import render_text
from src.fishes.player_fish import PlayerFish
from src.fishes.computer_fish import ComputerFish
from src.fish import Fish

# The names of modes:
# main_menu
# leaderboard
# game
# restart
# won


class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        if FULLSCREEN:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((800, 800))
        Drawable.set_screen(screen)

        self.end_time = None
        self.start_time = None
        self.pause_time = None
        self.mode = 'main_menu'
        self.font = pygame.font.SysFont('Comics Sans', 30)
        self.running = True
        self.last_spawn_fish_time = time()
        self.player_fish = PlayerFish()
        self.background = Drawable(Vector2(0, 0), Vector2(0, 1), pygame.image.load('images/background.png').convert())


    def loop(self):
        keys = pygame.key.get_pressed()
        Drawable.screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if keys[pygame.K_ESCAPE]:
            self.running = False
        if keys[pygame.K_SPACE]:
            self.mode = 'pause'

        if self.mode == 'main_menu':
            self.main_menu()
        if self.mode == 'leaderboard':
            self.leaderboard()
        if self.mode == 'game':
            self.game()
        if self.mode == 'restart':
            self.restart()
        if self.mode == 'won':
            self.game()
            self.won()
        if self.mode == 'pause':
            self.pause()


        if keys[pygame.K_f] and DEBUG:
            self.mode = 'restart'
        if keys[pygame.K_g] and DEBUG:
            self.mode = 'won'


        pygame.display.flip()

    def main_menu(self):
        keys = pygame.key.get_pressed()
        # self.draw_background()
        render_text(['RYBICZKY', 'press p to play'], 'middle', self.font)
        if keys[pygame.K_p]:
            self.mode = 'game'

    def leaderboard(self):
        pass

    def game(self):
        if self.start_time is None:
            self.start_time = time()

        if time() - self.last_spawn_fish_time > 1:
            self.last_spawn_fish_time = time()
            categories = [
                ([50, 100], 16),
                ([100, 150], 9),
                ([150, 200], 4),
                ([200, 250], 2),
                ([250, 300], 1),
            ]
            for range, number in categories:
                fishes = [fish for fish in ComputerFish.computer_fishes if range[0]*SCALE <= fish.size < range[1]*SCALE]
                if len(fishes) < number:
                    position = Vector2(0, RESET_DISTANCE * 1.1)
                    position = position.rotate(randint(0, 360))
                    position = self.player_fish.position + position
                    size = randint(*range)
                    ComputerFish(position, size)

        self.running = self.handle_events(self.player_fish, self.running)

        self.move_fishes(self.duration, self.player_fish)

        Drawable.screen.fill((255, 255, 255))
        Drawable.set_offset(self.player_fish.position)

        self.draw_background_player()

        for fish in Fish.fishes:
            if fish.compute_collisions() and fish.size < 50 * SCALE:
                if fish == self.player_fish:
                    print('you failed')
                    self.mode = 'restart'
                fish.delete()

        for fish in Fish.fishes:
            fish.draw()

        self.print_stats()

        if self.player_fish.size > Fish.max_size:
            self.mode = 'won'

    def won(self):
        if self.end_time is None:
            self.end_time = time()
        render_text(f'YOU WON - time: {int(self.end_time - self.start_time)}s', 'middle', self.font)

    def restart(self):
        self.start_time = None
        self.end_time = None
        # self.end_time = None je tu akorat pro debug mod a dalsi mozne hrani
        keys = pygame.key.get_pressed()
        render_text([
            'You\'ve got eaten.',
            'Press r to restart'
        ], 'middle', self.font)
        if keys[pygame.K_r]:
            self.mode = 'game'
            while ComputerFish.computer_fishes:
                ComputerFish.computer_fishes[0].delete()
            self.player_fish = PlayerFish()

    def pause(self):
        if self.pause_time is None:
            self.pause_time = time()
        render_text(['Game is stopped', 'press p to play'], 'middle', self.font)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.start_time += time() - self.pause_time
            self.mode = 'game'

    def handle_events(self, player_fish, running):
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

    def move_fishes(self, duration, player_fish):
        ratio = duration / (1 / 30)
        player_fish.move(ratio)

        for fish in ComputerFish.computer_fishes:
            fish.behave()
            fish.reset_fish_position(player_fish)
            fish.move(ratio)

    def draw_background_player(self):
        background_position = Vector2(round(self.player_fish.position.x / 800), round(self.player_fish.position.y / 800))
        for x in [0, 1, 2]:
            for y in [0, 1, 2]:
                pos = background_position + Vector2(x, y)

                q = int((7 * pos.x + 13 * pos.y) % 4)
                self.background.direction = [Vector2(0, 1), Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0)][q]
                self.background.position = pos * 800 - Vector2(800)
                self.background.draw()

    # TODO working only for player, need to be modified, but mistake is on drawable side
    def draw_background(self):
        background_position = Vector2(800, 800)
        for x in [0, 1, 2]:
            for y in [0, 1, 2]:
                pos = background_position + Vector2(x, y)

                q = int((7 * pos.x + 13 * pos.y) % 4)
                self.background.direction = [Vector2(0, 1), Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0)][q]
                self.background.position = pos * 800 - Vector2(800)
                self.background.draw()

    def print_stats(self):
        render_text([
            f'FPS: {int(1 / (self.duration + 0.0001))}',
            f'Score: {self.player_fish.size - PlayerFish.starting_size * SCALE}'
        ], 'left', self.font, Vector2(0, 0))

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.duration = clock.tick(FPS) / 1000
            self.loop()

        print('it is done')
        pygame.quit()
