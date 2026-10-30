import turtle as t
import math

tim = t.Turtle()
tim.speed("fastest")
tim.hideturtle()

screen = t.Screen()
screen.bgcolor("black")

colori = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]

R = 150   # raggio fisso
r = 80    # raggio mobile
d = 100   # distanza dal centro

step = 0.05
giri = int(2 * math.pi * r / math.gcd(int(R), int(r)))

for i, col in enumerate(colori):
    tim.pencolor(col)
    tim.penup()
    # posizione iniziale
    x0 = (R - r) + d
    tim.goto(x0, 0)
    tim.pendown()
    theta = 0
    while theta <= giri * 2 * math.pi + step:
        x = (R - r) * math.cos(theta) + d * math.cos((R - r) / r * theta)
        y = (R - r) * math.sin(theta) - d * math.sin((R - r) / r * theta)
        tim.goto(x, y)
        theta += step
    r -= 8
    d -= 5

screen.exitonclick()
