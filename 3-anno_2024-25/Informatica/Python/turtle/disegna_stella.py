import turtle as t
import math

t.speed(0)
t.penup()
t.pencolor("red")
t.fillcolor("yellow")
t.screensize(800, 600)

def disegna_fiocco6(lato: float) -> None:
    start_pos = t.position()
    start_heading = t.heading()

    for x in range(2):
        # imposta lo spessore della penna
        t.pensize(5 if x else 0)

        # triangolo superiore
        t.penup()
        t.setposition(start_pos)          # riparto sempre dal centro
        t.setheading(start_heading)       # e con la stessa direzione
        t.forward(lato/2)
        t.left(90)
        t.forward(lato/2)
        t.right(90)
        t.pendown()
        if x == 0: t.begin_fill()
        for _ in range(3):
            t.forward(lato)
            t.right(120)
        if x == 0: t.end_fill()

        # triangolo inferiore
        t.penup()
        t.setposition(start_pos)
        t.setheading(start_heading)
        t.forward(lato/2)
        t.right(90)
        t.forward(lato/ int(math.sqrt(lato)))
        t.left(90)
        t.pendown()
        if x == 0: t.begin_fill()
        for _ in range(3):
            t.forward(lato)
            t.left(120)
        if x == 0: t.end_fill()
        t.penup()
    t.setposition(start_pos)
    t.setheading(start_heading)

def disegna_stella(lato: float) -> None:
    start_pos = t.position()
    start_heading = t.heading()
    t.pensize()
    t.pendown()
    t.begin_fill()
    for _ in range(5):
        t.forward(lato)
        t.right(144)
    t.end_fill()
    t.penup()

    t.setposition(start_pos)
    t.setheading(start_heading)
    t.stamp()



disegna_stella(100)
t.goto(100, -300)
disegna_fiocco6(100)

t.done()
