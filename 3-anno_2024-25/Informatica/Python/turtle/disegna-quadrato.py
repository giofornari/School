from turtle import Turtle, Screen

color_step = 10
red_value = 0
square_size = 20
step_distance = 35
angle = 270+45

screen = Screen()
screen.colormode(255)

t = Turtle()
t.speed(0)
t.hideturtle()
t.penup()
t.setpos(-315, 315)

def draw_square(turtle, size, color):
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.setheading(0)  
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()

for _ in range(25):
    draw_square(t, square_size, (red_value, 0, 0))
    t.setheading(angle)
    t.forward(step_distance)
    red_value += color_step

screen.exitonclick()