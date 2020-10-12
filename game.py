#!/usr/bin/env python3
'''
Turtle Asteroids
'''

import math
import time
import turtle


# Constants
FPS = 60
MAX_SPEED = 5



# Classes
class Game():
    def __init__(self, config):
        self.screen_width = 800 if 'screen_width' not in config.keys() else \
            config['screen_width']
        self.screen_height = 600 if 'screen_height' not in config.keys() else \
            config['screen_height']
        self.title = 'Game Title Here' if 'title' not in config.keys() else \
            config['title']
        self.bgcolor = 'black' if 'bgcolor' not in config.keys() else \
            config['bgcolor']
        self.wn = turtle.Screen()
        self.setup_screen()
        self.pen = turtle.Turtle()
        self.setup_pen()
        self.sprites = []
        self.running = True

    def setup_screen(self):
        self.wn.setup(self.screen_width, self.screen_height)
        self.wn.title(self.title)
        self.wn.bgcolor(self.bgcolor)
        self.wn.tracer(0)

    def setup_pen(self):
        self.pen.speed(0)
        self.pen.shape('square')
        self.pen.color('white')
        self.pen.penup()
        self.pen.hideturtle()

    def quit(self):
        self.running = False

    def add_player(self, player):
        self.player = player
        self.add_sprite(player)

    def add_sprite(self, sprite):
        sprite.set_pen(self.pen)
        sprite.set_game(self)
        self.sprites.append(sprite)

    def listen(self):
        self.wn.listen()
        self.wn.onkeypress(self.player.accelerate, 'w')

        self.wn.onkeypress(self.player.rotate_left, 'a')
        self.wn.onkeyrelease(self.player.stop_rotation, 'a')

        self.wn.onkeypress(self.player.rotate_right, 'd')
        self.wn.onkeyrelease(self.player.stop_rotation, 'd')

        self.wn.onkeypress(self.quit, 'BackSpace')

    def loop(self):
        self.listen()
        while self.running:
            self.pen.clear()

            for sprite in self.sprites:
                sprite.update()

            for sprite in self.sprites:
                sprite.render()
    
            self.wn.update()


class Vector2d():
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def magnitude(self):
        return math.sqrt(self.dx**2 + self.dy**2)

    def clamp(self, limit):
        mag = self.magnitude()
        if mag > limit:
            ratio = limit / mag
            self.dx *= ratio
            self.dy *= ratio


class Sprite():
    def __init__(self, x, y, shape, color, shapesize=(None, None, None)):
        self.x = x
        self.y = y
        self.dx = 0 # detla y (change in x on each update)
        self.dy = 0 # delta x (change in y on each update)
        self.heading = 90 # default to up
        self.da = 0 # delta angle
        self.shape = shape
        self.color = color
        self.shapesize = shapesize
        self.t = 0 # time at update
        self.dt = 0 # delta t (time change between updates)
        self.accel = 2 # acceleration

    def set_pen(self, pen):
        self.pen = pen

    def set_game(self, game):
        self.game = game

    def update(self):
        if self.t == 0:
            self.t = time.time() # initialize time at start of game loop
            return
        t0 = self.t # record initial time
        self.t = time.time() # set current time
        self.dt = self.t - t0 # calculate elapsed time (delta t)
        self.x += self.dx * self.dt * FPS
        self.x = wrap(self.x, -(self.game.screen_width + 10)/2,
            (self.game.screen_width + 10)/2)
        self.y += self.dy * self.dt * FPS
        self.y = wrap(self.y, -(self.game.screen_height + 10)/2,
            (self.game.screen_height + 10)/2)
        self.heading += self.da * self.dt * FPS
        self.heading %= 360
        #print('t0: {}, self.t: {}, dt: {}, self.da: {}, heading: {}'.format(t0, self.t, dt, self.da, self.heading))

    def render(self):
        self.pen.goto(self.x, self.y)
        self.pen.setheading(self.heading)
        self.pen.shape(self.shape)
        self.pen.color(self.color)
        self.pen.shapesize(*self.shapesize)
        self.pen.stamp()


class Player(Sprite):
    def __init__(self, x=0, y=0, shape='triangle', color='white',
        shapesize=(None, None, None)):
        Sprite.__init__(self, x, y, shape, color, shapesize)
        self.lives = 3
        self.score = 0
        self.heading = 90
        self.av = 5 # angular velocity (degrees per second)

    def rotate_left(self):
        self.da = 1 * self.av
    
    def rotate_right(self):
        self.da = -1 * self.av

    def stop_rotation(self):
        self.da = 0

    def accelerate(self):
        v2d = Vector2d(self.dx, self.dy)
        v2d.dx += self.accel * math.cos(math.radians(self.heading)) * self.dt * FPS
        v2d.dy += self.accel * math.sin(math.radians(self.heading)) * self.dt * FPS
        v2d.clamp(MAX_SPEED)
        self.dx = v2d.dx
        self.dy = v2d.dy


# Functions
def wrap(val, minimum, maximum):
    if val < minimum:
        return maximum
    elif val > maximum:
        return minimum
    else:
        return val


def clamp(val, minimum, maximum):
    if val < minimum:
        return minimum
    elif val > maximum:
        return maximum
    else:
        return val


# Main
config = {
    'screen_width': 800,
    'screen_height': 600,
    'title': 'my title',
}
game = Game(config)
game.add_player(Player(shapesize=(0.5, 1)))
game.loop()
