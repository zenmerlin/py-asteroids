#!/usr/bin/env python3
'''
Turtle Asteroids
'''

import math
import random
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
        self.game_over = False

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

    def del_sprite(self, sprite):
        try:
            self.sprites.remove(sprite)
            del sprite
        except ValueError as err:
            print(err)

    def listen(self): # TODO: rename/refactor 
        self.wn.listen()
        self.wn.onkeypress(self.player.accelerate, 'w')
        self.wn.onkeypress(self.player.decelerate, 's')

        self.wn.onkeypress(self.player.rotate_left, 'a')
        self.wn.onkeyrelease(self.player.stop_rotation, 'a')

        self.wn.onkeypress(self.player.rotate_right, 'd')
        self.wn.onkeyrelease(self.player.stop_rotation, 'd')

        self.wn.onkeypress(self.player.fire, 'space')

        self.wn.onkeypress(self.quit, 'BackSpace')

    def set_game_over(self):
        self.game_over = True
        self.wn.onkeypress(self.reset, 'r')

    def disp_game_over(self):
        self.pen.color('orange')
        self.pen.goto(0, 0)
        self.pen.write('Game Over', align='center', font=('Consolas', 24, 'bold'))
        # TODO: The second write call below flickers for some reason. Needs fixed.
        #self.pen.goto(0, -20)
        #self.pen.write('Press "r" to restart', align='center', font=('Consolas', 12, 'italic'))
        self.pen.color('white')
        
    def reset(self):
        # Reset player and game state
        Player.lives = 3
        Player.score = 0
        Asteroid.spawn_limit = 3
        
        # Clear all game entities TODO: this isn't clearing everything. why?
        for collider in Collider.instances:
            collider.destruct()
        for collider in Collider.instances: # keep missing one, so run again TODO: needs fixed
            collider.destruct()
        for asteroid in Asteroid.instances:
            asteroid.destruct()
        for sprite in self.sprites:
            self.del_sprite(sprite)
        print(Collider.instances)

        # Create/setup new game entities
        self.add_player(Player())
        self.listen() # reset player controls
        Asteroid.spawn(self)
        self.game_over = False

        # Clear reset key binding
        self.wn.onkeypress(None, 'r')

    def loop(self):
        self.listen()
        while self.running:
            self.pen.clear()

            for sprite in self.sprites:
                sprite.update()

            for sprite in self.sprites:
                sprite.render()

            if self.game_over:
                self.disp_game_over()
    
            self.wn.update()


class Vector2d():
    def __init__(self, dx=0, dy=0):
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


class Collider():
    instances = []

    def __init__(self, sprite, offset=0, size=1):
        self.sprite = sprite
        self.offset = offset
        self.size = size
        Collider.instances.append(self)
        self.hits = []

    def x(self):
        return self.sprite.x + self.offset * math.cos(self.sprite.rad_heading())

    def y(self):
        return self.sprite.y + self.offset * math.sin(self.sprite.rad_heading())

    def hit(self, other):
        return math.sqrt((self.x() - other.x())**2 + (self.y() - other.y())**2) <= \
            (self.size + other.size)

    def has_hits(self):
        for other in Collider.instances:
            if self != other and self.hit(other):
                self.hits.append(other)
        return len(self.hits) != 0

    def destruct(self):
        self.sprite.destruct()
        try:
            Collider.instances.remove(self)
            del self
        except ValueError as err:
            print(err)


class Sprite():
    def __init__(self, x, y, shape, color, shapesize=(None, None, None),
        heading=90):
        self.x = x
        self.y = y
        self.v2d = Vector2d(0, 0) # vector representing dx, dy
        self.heading = heading # 90 = up
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

    def rad_heading(self):
        return math.radians(self.heading)

    def update(self):
        if self.t == 0:
            self.t = time.time() # initialize time at start of game loop
            return
        t0 = self.t # record initial time
        self.t = time.time() # set current time
        self.dt = self.t - t0 # calculate elapsed time (delta t)
        self.x += self.v2d.dx * self.dt * FPS
        self.x = wrap(self.x, -(self.game.screen_width + 10)/2,
            (self.game.screen_width + 10)/2)
        self.y += self.v2d.dy * self.dt * FPS
        self.y = wrap(self.y, -(self.game.screen_height + 10)/2,
            (self.game.screen_height + 10)/2)
        self.heading += self.da * self.dt * FPS
        self.heading %= 360

    def render(self):
        self.pen.goto(self.x, self.y)
        self.pen.setheading(self.heading)
        self.pen.shape(self.shape)
        self.pen.color(self.color)
        self.pen.shapesize(*self.shapesize)
        self.pen.stamp()

    def destruct(self):
        self.game.del_sprite(self)


class Missile(Sprite):
    def __init__(self, x=0, y=0, shape='square', color='red',
        shapesize=(0.05, 3, None), heading=90, speed=12, max_range=175):
        Sprite.__init__(self, x, y, shape, color, shapesize, heading)
        self.max_range = max_range
        rad_heading = self.rad_heading()
        self.v2d.dx = speed * math.cos(rad_heading)
        self.v2d.dy = speed * math.sin(rad_heading)
        self.dist = 0 # initialize distance travelled
        self.collider = Collider(self, (shapesize[1]-1)*10, shapesize[0]*10)

    def update(self):
        Sprite.update(self)
        self.dist += self.v2d.magnitude() * self.dt * FPS
        if self.dist >= self.max_range:
            self.collider.destruct()
            return
        if self.collider.has_hits():
            for collider in self.collider.hits:
                collider.destruct()
            self.collider.destruct()
        

class Player(Sprite):
    lives = 0
    score = 0

    def __init__(self, x=0, y=0, shape='triangle', color='white',
        shapesize=(0.5, 1, None)):
        Sprite.__init__(self, x, y, shape, color, shapesize)
        self.heading = 90
        self.av = 5 # angular velocity (degrees per second)
        self.shot_cooldown = 0
        self.collider = Collider(sprite=self, size=shapesize[1]*1.25)

    def rotate_left(self):
        self.da = 1 * self.av
    
    def rotate_right(self):
        self.da = -1 * self.av

    def stop_rotation(self):
        self.da = 0

    def accelerate(self):
        heading = self.rad_heading()
        self.v2d.dx += self.accel * math.cos(heading) * self.dt * FPS
        self.v2d.dy += self.accel * math.sin(heading) * self.dt * FPS
        self.v2d.clamp(MAX_SPEED)

    def decelerate(self):
        heading = math.radians(self.heading + 180)
        self.v2d.dx += self.accel * math.cos(heading) * self.dt * FPS
        self.v2d.dy += self.accel * math.sin(heading) * self.dt * FPS
        self.v2d.clamp(MAX_SPEED)

    def update(self):
        Sprite.update(self)
        if self.shot_cooldown != 0:
            self.shot_cooldown = clamp(self.shot_cooldown-self.dt, 0, 10)
        if self.collider.has_hits():
            for collider in self.collider.hits:
                collider.destruct()
            self.collider.destruct()

    def fire(self):
        if self.shot_cooldown == 0:
            self.shot_cooldown = 0.1
            heading = self.rad_heading()
            x = self.x + 40 * math.cos(heading)
            y = self.y + 40 * math.sin(heading)
            missile = Missile(x=x, y=y, heading=self.heading)
            self.game.add_sprite(missile)
    
    def destruct(self):
        if Player.lives:
            Player.lives -= 1
            self.game.add_player(Player())
            self.game.listen()
        else:
            self.game.set_game_over()
        super().destruct()


class Asteroid(Sprite):
    instances = []
    spawn_limit = 3

    def __init__(self, x=0, y=0, shape='circle', color='grey',
        size=3, v2d=Vector2d()):
        Sprite.__init__(self, x, y, shape, color, (size, size))
        self.v2d = v2d
        self.collider = Collider(self, 0, size*10)

    @staticmethod
    def spawn(game):
        for i in range(Asteroid.spawn_limit):
            x = random.randint(-game.screen_width/2,
                game.screen_width/2)
            y = random.randint(-game.screen_height/2,
                game.screen_height/2)
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)

            ast = Asteroid(x=x, y=y, size=3, v2d=Vector2d(dx, dy))
            game.add_sprite(ast)
            Asteroid.instances.append(ast)
        Asteroid.spawn_limit += 1

    def update(self):
        Sprite.update(self)

    def destruct(self):
        Asteroid.instances.remove(self)
        # TODO: code smell. Needs refactor
        if len(Asteroid.instances) == 0 and not self.game.game_over:
            Asteroid.spawn(self.game)
        super().destruct()


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
    'title': 'Turtle Asteroids!',
}

game = Game(config)
game.add_player(Player())
Asteroid.spawn(game)
game.loop()
