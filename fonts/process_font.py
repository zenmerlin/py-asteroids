#!/usr/bin/env python3
'''
Split font.gif sprite sheet into separate gif files to be imported into game
'''

from PIL import Image

#import pdb
import os
import sys

TILE_SIZE = 7  # width and height (square) of tile in pixels
TILE_OFFSET = 1 # offset between rows and columns in pixels (to right and down)
COMPILED_DIR = 'compiled'

# Clean up compiled directory
try:
    for f in os.listdir(COMPILED_DIR):
        try:
            print('removing {}'.format(f))
            os.remove('{}/{}'.format(COMPILED_DIR, f))
        except IsADirectoryError as err:
            print('{} is a directory, cannot remove, skipping.'.format(f))
except FileNotFoundError as err:
    print('{} directory does not exist'.format(COMPILED_DIR))
except err:
    print('Unexpected error occurred: {}'.format(err))
    sys.exit(1)


CHARS = [
    ' ', '!', '"', '#', '$', '%', '&', "'",
    '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?',
    '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
    '`', '{', '|', '}', '~'
]

CHAR_NAMES = [
    'space', 'bang', 'dquote', 'hash', 'dollar', 'percent', 'amp', 'squote',
    'lparen', 'rparen', 'ast', 'plus', 'comma', 'dash', 'period', 'fslash',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', 'colon', 'semicolon', 'lt', 'eq', 'gt', 'question',
    'at', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z', 'lbracket', 'bslash', 'rbracket', 'carrot', 'underscore',
    'backtick', 'lbrace', 'bar', 'rbrace', 'tilde'
]

SIZES = {
    '8px': 1,
    '16px': 2,
    '24px': 3
}

TRANSPARENT = (0, 0, 0, 0)

COLORS = {
    'white': (255, 255, 255, 255),
    'red': (255, 0, 0, 0),
    'green': (0, 255, 0, 255),
    'blue': (0, 0, 255, 255)
}

i_src = Image.open('null_terminator.png')

#pdb.set_trace()
for i, char in enumerate(CHARS):
    r1 = i % 8 * (TILE_SIZE + TILE_OFFSET)
    c1 = i // 8 * (TILE_SIZE + TILE_OFFSET)
    r2 = r1 + TILE_SIZE
    c2 = c1 + TILE_SIZE
    coords = (r1, c1, r2, c2)
    print('coords: ({}, {}, {}, {}), name: {}, val: {}'.format(
        r1, c1, r2, c2, CHAR_NAMES[i], char))
    i_cropped = i_src.crop(coords)
    for size in SIZES.keys():
        i_resized = i_cropped.resize(size=(i_cropped.width*SIZES[size],
            i_cropped.height*SIZES[size]), resample=Image.BOX)
        for color in COLORS.keys():
            i_final = i_resized.copy()
            pixeldata = i_final.load()
            for x in range(i_final.width):
                for y in range(i_final.height):
                    if pixeldata[x, y] == COLORS['white']:
                        pixeldata[x, y] = COLORS[color]
                    else:
                        pixeldata[x, y] = TRANSPARENT
            i_final.save('{}/{}_{}_{}.gif'.format(COMPILED_DIR, CHAR_NAMES[i],
                color, size), transparency=1)
        i_resized.close()
    i_cropped.close()
    
i_src.close()
