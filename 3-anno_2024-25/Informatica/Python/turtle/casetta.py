from turtle import Screen, Turtle, done
# Setup
W, H = 800, 600
s = Screen(); s.setup(W, H)
s.bgcolor("skyblue")
t = Turtle(visible=False)
t.speed(0)
t.penup()

# Helpers
def C(x,y,r,c):
    t.goto(x,y-r); t.color(c,c)
    t.begin_fill(); t.pendown()
    t.circle(r)
    t.end_fill()
    t.penup()
def P(x,y,n,l,co,fi,hd=0):
    t.goto(x,y)
    t.setheading(hd)
    t.color(co,fi)
    t.begin_fill()
    t.pendown()
    for _ in range(n):
        t.forward(l)
        t.left(360/n)
    t.end_fill()
    t.penup()

o = -100
sz = 170

# Sole
t = C; C(-320,225,35,"yellow")
# Casa
P(o,-100,4,sz,"chocolate","orange")

P(o-27,70,3,sz*1.32,"chocolate","orange")

for x,y in [(0,0),( -80,0)]:
    P(x,y,4,50,"black","white")
    t.goto(x,y+25); t.pendown()
    t.forward(50)
    t.penup()
    t.goto(x+25,y)
    t.setheading(90)
    t.pendown()
    t.forward(50)
    t.penup()

# Porta
t.goto(-40,-97)
t.setheading(0)
t.color("black","red")
t.begin_fill()
t.pendown()
for _ in range(2):
    t.forward(50)
    t.left(90)
    t.forward(80)
    t.left(90)
t.end_fill()
t.penup()

# Pomello
t.goto(-30,-60)
t.color("black","black")
t.begin_fill()
t.pendown()
t.circle(5)
t.end_fill()

done()
