# def czech_sort(a):
#     abc = 'abcdefghijklmnopqrstuvwxyz'
#
#     a.sort()
#     for word in a:
#         if word[0] > 'z':
#             print(word)
#
#     return a
#
# a = [
#     'Eduard',
#     'John',
#     'Evans',
#     'Šimon',
#     'Adam',
#     'Zuzka'
# ]
#
#
#
# a = czech_sort(a)
#
# print(a)
from math import sqrt, floor, ceil



def is_prime(a):
    assert a > 0
    for i in range(2, floor(sqrt(a)) + 1):
        if a % i == 0:
            return False

    return True


def is_valid_n_polygon(polygon):
    return sum(polygon) > 2 * max(polygon)


# assert all([expected_result == is_valid_n_polygon(*triangle) for expected_result, triangle in triangle_tests])


def is_happy_number(number):
    visited_numbers = []
    while number != 1 and number not in visited_numbers:
        visited_numbers.append(number)
        number = sum([pow(int(cipher), 2) for cipher in str(number)])

    return number == 1

def is_favourable_number(number):
    for step in range(1,number):
        position = 2
        if step % position == 0:
            step.remove
        if step % position == 0 and step == number:
            return False
        position = step(position)

    return True

def is_weird_number(number):
    division_numbers = []
    for possible in range(1, (ceil(number / 2)+1)):
        if number%possible == 0:
            division_numbers.append(possible)

    differnce = abs(sum(division_numbers)-number)
    for i in reversed(division_numbers):
        if i <= differnce:
            differnce -= i
        if differnce <= 0:
            return False

    return True


tests = [
    (True, is_valid_n_polygon, (1, 2, 2.5)),
    (False, is_valid_n_polygon, (1, 2, 4)),
    (True, is_valid_n_polygon, (1, 2, 1.5)),
    (False, is_valid_n_polygon, (5, 2, 3)),
    (True, is_valid_n_polygon, (5, 2, 3, 5)),
    (False, is_valid_n_polygon, (5, 2, 3, 15)),
    (False, is_happy_number, 4),
    (False, is_happy_number, 16),
    (True, is_happy_number, 7),
    (True, is_happy_number, 1663),
    (True, is_happy_number, 13),
    (True, is_favourable_number, 31),
    (False, is_favourable_number, 82),
    (True, is_weird_number, 70),
    (False, is_weird_number, 12),
]
for expected_result, function, argument in tests:
    if expected_result != function(argument):
        print(f"funkce {function} s argumentem {argument} nevratila hodnotu {expected_result}")
        assert False

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
