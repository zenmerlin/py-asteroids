#!/usr/bin/env python3
'''
2D Top Down Game
'''

import turtle

# Screen setup
# Tile Size: 16x16
# Screen Size: 480x256 (30x16 tiles)
SCREEN_WIDTH = 480 
SCREEN_HEIGHT = 256
wn = turtle.Screen()
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.title('Game')
wn.bgcolor('black')
wn.tracer(0)

# Pen setup
pen = turtle.Turtle()
pen.speed(0)
pen.shape('square')
pen.color('white')
pen.penup()
pen.hideturtle()

# Classes
class Game():
    def __init__(self, config):
        self.screen_width = config['width']
        self.screen_height = config['height']
        self.title = 'Game Title Here' if 'title' not in config.keys() else \
            config['title']
        self.bgcolor = 'black' if 'bgcolor' not in config.keys() else \
            config['bgcolor']
        self.wn = turtle.Screen()
        setup_screen()

    def setup_screen():
        self.wn.setup(self.screen_width, self.screen_height)
        self.wn.title(self.title)
        self.wn.bgcolor(self.bgcolor)
        self.wn.tracer(0)

    def loop(self):
        while True:
            pen.clear()

            for sprite in sprites:
                sprite.update()

            for sprite in sprites:
                sprite.render()
    
            wn.update()


class Sprite():
    def __init__(self, pen, x, y, shape, color):
        self.pen = pen
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = 0
        self.dy = 0
        self.heading = 0
        self.da = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.heading += self.da

    def render(self):
        self.pen.goto(self.x, self.y)
        self.pen.setheading(self.heading)
        self.pen.shape(self.shape)
        self.pen.color(self.color)
        self.pen.stamp()


class Player(Sprite):
    def __init__(self, pen, x=0, y=0, shape='triangle', color='white'):
        Sprite.__init__(self, pen, x, y, shape, color)
        self.lives = 3
        self.score = 0
        self.heading = 90
        self.da

    def rotate_left(self):
        self.da = 5
    
    def rotate_right(self):
        self.da = -5

    def stop_rotation(self):
        self.da = 0


player = Player(pen)

sprites = []
sprites.append(player)

#wn.listen()
#wn.onkeypress(player.rotate_left, 'a')
#wn.onkeypress(player.rotate_right, 'd')
#wn.onkeyrelease(player.stop_rotation, 'a')
#wn.onkeyrelease(player.stop_rotation, 'd')

