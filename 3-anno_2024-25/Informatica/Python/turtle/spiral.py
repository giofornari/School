import turtle

linux = turtle.Screen()
linux.bgcolor("white")

bug = turtle.Turtle()
bug.speed(0)

lunghezza = 1
incremento = 0.5
angolo = 10         


for i in range(100):
    bug.forward(lunghezza)
    bug.right(angolo)
    lunghezza += incremento
linux.exitonclick()
