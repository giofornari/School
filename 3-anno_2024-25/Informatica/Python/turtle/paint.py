import turtle
import random

def r_col():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)

def quad(arch, len):
    for _ in range(4):
        arch.forward(len)
        arch.right(90)

linux = turtle.Screen()
linux.bgcolor("white")
linux.colormode(1.0)

t = turtle.Turtle()
t.speed(0)

num_q = int(input("Quanti quadrati vuoi disegnare? "))
len = 50

for _ in range(num_q):
    t.penup()
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)
    t.goto(x, y)
    
    colore = r_col()
    t.fillcolor(colore)
    t.pencolor(colore)
    
    t.begin_fill()
    t.pendown()
    quad(t, len)
    t.end_fill()

linux.exitonclick()
