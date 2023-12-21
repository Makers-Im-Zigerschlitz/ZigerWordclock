# pyright: reportMissingImports=false

import random
import settings
from rainbowio import colorwheel

OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 40, 0)
GREEN = (0, 255, 0)
TEAL = (0, 255, 120)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
WHITE = (255, 255, 255)

COLS = [RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA]
RAND_COLS = []


def rand_setup():
    for i in range(126):  # TODO
        RAND_COLS.append(random.choice(COLS))


def rnd(i):
    return RAND_COLS[i]


def fancy(i):
    return settings.PALLETE[i % 3]


def all_the_colours(i):
    return COLS[i % len(COLS)]


def rand_pallete():
    c1 = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))
    c2 = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))
    c3 = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))
    return [c1, c2, c3]


def rainbow(i):
    rc_index = (i * 256 // settings.LED_NUMBER)
    return colorwheel(rc_index & 255)


'''
Colours from pallete: 
    Hour:   settings.PALLETE[2]
    Minute: settings.PALLETE[1]
    Words:  settings.PALLETE[0]

Setting pallete:
    settings.PALLETE = colours.<PALETTE_NAME>
'''

PALLETE_WHITE = [WHITE, WHITE, WHITE]
PALLETE_AUTUMN = [(255, 60, 0), 0xFF1200, YELLOW]
PALLETE_XMAS = [RED, WHITE, GREEN]
PALLETE_AURORA = [PURPLE, TEAL, (0, 255, 60)]
PALLETE_RANDOM = rand_pallete()
PALS = [PALLETE_XMAS, PALLETE_AURORA, PALLETE_AUTUMN]

rand_setup()
