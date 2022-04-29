import json
from os.path import exists
from random import randint
from time import time

import pygame
from pygame import Vector2

from src.constants import FULLSCREEN, FPS, SCALE, RESET_DISTANCE, DEBUG
from src.drawable import Drawable
from src.fish import Fish
from src.fishes.computer_fish import ComputerFish
from src.fishes.player_fish import PlayerFish
from src.text import render_text


# The names of modes:
# main_menu
# leaderboard
# game
# restart
# won
# new_game
# pause
# fail

class Game():
    leaderboards_file_name = 'leaderboards.json'

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
        self.head_font = pygame.font.SysFont('Comics Sans', 45)
        self.running = True
        self.last_spawn_fish_time = time()
        self.player_fish = None
        self.background = Drawable(Vector2(0, 0), Vector2(0, 1), pygame.image.load('images/background.png').convert())
        self.keys = None
        self.handicap = None

    def loop(self):
        self.keys = pygame.key.get_pressed()
        Drawable.screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.game()
        if self.mode == 'main_menu':
            self.main_menu()
        if self.mode == 'leaderboard':
            self.leaderboard()
        if self.mode == 'game':
            if self.keys[pygame.K_SPACE]:
                self.mode = 'pause'
            if self.keys[pygame.K_r]:
                self.restart()
            if self.keys[pygame.K_q]:
                self.mode = 'main_menu'
            if self.keys[pygame.K_f] and DEBUG:
                self.mode = 'fail'
            if self.keys[pygame.K_g] and DEBUG:
                self.mark_win()

        if self.mode == 'restart':
            self.restart()
        if self.mode == 'won':
            self.won()
            if self.keys[pygame.K_q]:
                self.mode = 'main_menu'
            if self.keys[pygame.K_ESCAPE]:
                self.running = False
        if self.mode == 'pause':
            self.pause()
        if self.mode == 'new_game':
            self.new_game()
        if self.mode == 'fail':
            self.fail()

        pygame.display.flip()

    def main_menu(self):
        # self.draw_background(Vector2(0, 0))
        self.handicap = None
        render_text('RYBICZKY', 'middle', self.head_font,
                    Vector2(Drawable.screen_size[0] / 2, Drawable.screen_size[1] / 2 - 50))
        render_text(['press p to play', 'press l to see leaderboards', 'press ESC to exit'], 'middle', self.font)
        if self.keys[pygame.K_p]:
            self.mode = 'new_game'
        if self.keys[pygame.K_l]:
            self.mode = 'leaderboard'
        if self.keys[pygame.K_ESCAPE]:
            self.running = False

    def new_game(self):
        render_text(['Choose your difficulty:', 'Kiki (k)', 'Žofka (z)', 'Marťas (m)', 'Blonďák (b)'], 'middle',
                    self.font)
        if self.keys[pygame.K_q]:
            self.mode = 'main_menu'
        if self.keys[pygame.K_k]:
            self.handicap = 1.6
        if self.keys[pygame.K_y] or self.keys[pygame.K_z]:
            self.handicap = 1.4
        if self.keys[pygame.K_m]:
            self.handicap = 1.2
        if self.keys[pygame.K_b]:
            self.handicap = 1

        if self.handicap is not None:
            self.player_fish = PlayerFish(self.handicap)
            self.mode = 'game'
            self.restart()

        if self.keys[pygame.K_q]:
            self.mode = 'main_menu'

    def leaderboard(self):
        lines = ['Leaderboards:']
        data = self.load_leaderboard_data()
        for item in data:
            lines.append(f"{item['score']:.2f}s")
        lines.append('')
        lines.append('to quit press q')
        render_text(lines, 'middle', self.font)

        if self.keys[pygame.K_q]:
            self.mode = 'main_menu'

    def game(self):
        if self.player_fish is None and self.mode == 'game':
            self.player_fish = PlayerFish(self.handicap)

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
                fishes = [fish for fish in ComputerFish.computer_fishes if
                          range[0] * SCALE <= fish.size < range[1] * SCALE]
                if len(fishes) < number:
                    position = Vector2(0, RESET_DISTANCE * 1.1)
                    position = position.rotate(randint(0, 360))
                    if self.player_fish is not None:
                        position = self.player_fish.position + position
                    size = randint(*range)
                    new_fish = ComputerFish(position, size)
                    new_fish.reset_fish_position(self.player_fish)

        if self.mode != 'pause':
            self.move_fishes(self.duration, self.player_fish)
            if self.player_fish is not None:
                self.handle_movements()
            for fish in Fish.fishes:
                if fish.compute_collisions() and fish.size < 50 * SCALE:
                    if fish == self.player_fish:
                        print('you failed')
                        self.mode = 'fail'
                    fish.delete()

        Drawable.screen.fill((255, 255, 255))
        self.draw_background()

        for fish in Fish.fishes:
            fish.draw()

        self.print_stats(self.mode == 'game')

        if self.player_fish is not None and self.player_fish.size > Fish.max_size:
            self.mark_win()

    def won(self):
        render_text(f'YOU WON - time: {int(self.end_time - self.start_time)}s', 'middle', self.font)

    def fail(self):
        render_text([
            'You got eaten.',
            'Press r to restart'
        ], 'middle', self.font)
        if self.keys[pygame.K_r]:
            self.restart()

    def restart(self):
        self.start_time = None
        self.end_time = None
        current_handicap = self.player_fish.handicap
        while Fish.fishes:
            Fish.fishes[0].delete()
        self.player_fish = PlayerFish(handicap=current_handicap)
        if self.start_time is None:
            self.start_time = time()
        self.mode = 'game'

    def pause(self):
        if self.pause_time is None:
            self.pause_time = time()
        render_text(['Game is stopped', 'press p to play'], 'middle', self.font)
        if self.keys[pygame.K_p]:
            self.start_time += time() - self.pause_time
            self.pause_time = None
            self.mode = 'game'
        if self.keys[pygame.K_q]:
            self.mode = 'main_menu'

    def handle_movements(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_fish.accelerate()
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_fish.slow_down()
        else:
            self.player_fish.reset_speed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_fish.turn_left()
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_fish.turn_right()
        else:
            self.player_fish.reset_turing()

    def move_fishes(self, duration, player_fish):
        ratio = duration / (1 / 30)
        if self.mode in ['game', 'won']:
            player_fish.move(ratio)

        for fish in ComputerFish.computer_fishes:
            fish.behave()
            fish.reset_fish_position(self.player_fish)
            fish.move(ratio)

    def draw_background(self):
        if self.player_fish is None:
            Drawable.set_offset(Vector2(0, 0))
            background_position = Vector2(0, 0)
        else:
            Drawable.set_offset(self.player_fish.position)
            background_position = Vector2(round(self.player_fish.position.x / 800),
                                          round(self.player_fish.position.y / 800))

        for x in [0, 1, 2]:
            for y in [0, 1, 2]:
                pos = background_position + Vector2(x, y)

                q = int((7 * pos.x + 13 * pos.y) % 4)
                self.background.direction = [Vector2(0, 1), Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0)][q]
                self.background.position = pos * 800 - Vector2(800)
                self.background.draw()

    def print_stats(self, print_score):
        lines = []
        if DEBUG:
            lines.append(f'FPS: {int(1 / (self.duration + 0.0001))}')
        if print_score:
            lines.append(f'Score: {self.player_fish.size - PlayerFish.starting_size * SCALE}')
            lines.append(f'Time: {int(time() - self.start_time)}')
        render_text(lines, 'left', self.font, Vector2(0, 0))

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.duration = clock.tick(FPS) / 1000
            self.loop()

        print('it is done')
        pygame.quit()

    def mark_win(self):
        self.mode = 'won'
        if self.end_time is None:
            self.end_time = time()

        data = self.load_leaderboard_data()
        data.append({'score': self.end_time - self.start_time})
        data.sort(key=lambda x: x['score'])
        data = data[:5]
        self.save_leaderboard_data(data)

    def load_leaderboard_data(self):
        if exists(self.leaderboards_file_name):
            with open(self.leaderboards_file_name, 'r') as f:
                return json.load(f)

        return []

    def save_leaderboard_data(self, data):
        with open(self.leaderboards_file_name, 'w') as f:
            return json.dump(data, f)
