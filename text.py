"""
Split font.gif sprite sheet into separate gif files to be imported into game
"""

from PIL import Image

from enum import Enum
import os
import sys


# Default character set
CHARS = [
    " ", "!", '"', "#", "$", "%", "&", "'",
    "(", ")", "*", "+", ",", "-", ".", "/",
    "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", ":", ";", "<", "=", ">", "?",
    "@", "A", "B", "C", "D", "E", "F", "G",
    "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W",
    "X", "Y", "Z", "[", "\\", "]", "^", "_",
    "`", "{", "|", "}", "~"
]

# File system friendly names for each character in character set
CHAR_NAMES = [
    "space", "bang", "dquote", "hash", "dollar", "percent", "amp", "squote",
    "lparen", "rparen", "ast", "plus", "comma", "dash", "period", "fslash",
    "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "colon", "semicolon", "lt", "eq", "gt", "question",
    "at", "A", "B", "C", "D", "E", "F", "G",
    "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W",
    "X", "Y", "Z", "lbracket", "bslash", "rbracket", "carrot", "underscore",
    "backtick", "lbrace", "bar", "rbrace", "tilde"
]

# Default tile size and offset
TILE_SIZE = 7  # width and height (square) of tile in pixels
TILE_OFFSET = 1 # offset between rows and columns in pixels (to right and down)


# Text color definitions in RGBA format
# Color preprocessing is done in RGBA mode, but image mode will be P (palette).
# The ALPHA color definition is used to define which color will be used to
# identify transparent pixels
class Color(Enum):
    WHITE = (255, 255, 255, 255)
    RED = (255, 0, 0, 0)
    GREEN = (0, 255, 0, 255)
    BLUE = (0, 0, 255, 255)
    ALPHA = (0, 0, 0, 0)


# Multipliers for text sizes in pixel height
# Multipler is relative to base TILE_SIZE
class Size(Enum):
    8px = 1
    16px = 2
    24px = 3


# Text justification with respect to anchor
class Align(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2 


class TextWriter():
    def __init__(self, src, tile_size=TILE_SIZE, tile_offset=TILE_OFFSET,
            colors=Color, color=Color.WHITE, sizes=Size, size=Size.8px,
            align=Align.LEFT, font_dir):
        self._src = src
        self._tile_size = tile_size
        self._tile_offset = tile_offset
        self._colors = colors
        self._color = color
        self._sizes = sizes
        self._size = size
        self._align = align
        self._font_dir = font_dir

