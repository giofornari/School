import turtle as t
import random

tim = t.Turtle()
tim.speed("fastest")
t.colormode(255)
for _ in range(360):
    tim.pencolor(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    tim.circle(150)
    tim.right(1)
t.Screen().exitonclick()
