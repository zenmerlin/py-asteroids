#!/usr/bin/env python3
import turtle

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

wn = turtle.Screen()
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.title("My game!")
wn.bgcolor("black")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

class Sprite():
    def __init__(self, x, y, shape, color):
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

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

class Player(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, 0, 0, shape, color)
        self.lives = 3
        self.score = 0
        self.heading = 90
        self.da = 0

    def rotate_left(self):
        self.da = 5
    
    def rotate_right(self):
        self.da = -5

    def stop_rotation(self):
        self.da = 0

player = Player(0, 0, "triangle", "white")
player.dx = 0
player.dy = 0

enemy = Sprite(0, 100, "square", "red")
enemy.dx = -1
enemy.dy = -0.3

powerup = Sprite(0, -100, "circle", "blue")
powerup.dx = 0.1
powerup.dy = 1

sprites = []
sprites.append(player)
sprites.append(enemy)
sprites.append(powerup)

wn.listen()
wn.onkeypress(player.rotate_left, "a")
wn.onkeypress(player.rotate_right, "d")
wn.onkeyrelease(player.stop_rotation, "a")
wn.onkeyrelease(player.stop_rotation, "d")

while True:
    pen.clear()

    for sprite in sprites:
        sprite.update()

    for sprite in sprites:
        sprite.render(pen)

    wn.update()
