from typing import List

from pygame import Vector2

from src.drawable import Drawable


def render_text(text, orientation, font, position=None):
    if not isinstance(text, list):
        text = [text]

    if position is None:
        position = Drawable.screen_size / 2

    screen = Drawable.screen
    line_height = font.get_height() + 2
    start_height = position.y
    text_width_coefficient = 0

    if orientation == 'right':
        text_width_coefficient = 1

    if orientation == 'middle':
        start_height = position.y - (line_height * len(text)) / 2
        text_width_coefficient = 1/2

    for i, line in enumerate(text):
        text_surface = font.render(line, False, (0, 0, 0))
        vector = (position.x - text_surface.get_width() * text_width_coefficient, start_height + line_height * i)
        screen.blit(text_surface, vector)
    
    
    
# render_lines(['stats: 1', 'sta: 2', 'neco: 5'], 'left', position, font)

# position is top left
# stats: 1
# sta: 2
# neco: 5


# position is in middle
# stats: 1
#   sta: 2
#  neco: 5

# position is top right
# stats: 1
#  sta: 2
#  neco55
