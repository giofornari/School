from turtle import *
import random

t = Turtle()
t.speed(0)
t.penup()
colormode(255)

punto = 20
gappp = 30

ax = -150
by = -150

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

for row in range(10):
    for col in range(10):
        x = ax + col * gappp
        y = by + row * gappp
        t.goto(x, y)
        t.dot(punto, random_color())

t.hideturtle()
done()
