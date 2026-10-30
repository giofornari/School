import random
from turtle import Turtle, Screen
from tkinter import messagebox

# Constants
fin = 800
x_i = -fin // 2 + 20
x_e = fin // 2 - 20
colors = ['blue', 'red']

def init_race():
    screen = Screen()
    screen.setup(width=fin, height=400)
    turtles = []
    spacing = 80
    y_start = -spacing / 2
    for i, color in enumerate(colors):
        t = Turtle(shape='turtle')
        t.color(color)
        t.penup()
        t.goto(x_i, y_start + i * spacing)
        turtles.append(t)
    return screen, turtles


def ask_question(player):
    ops = ['+', '-', '*', '/']
    op = random.choice(ops)
    b = random.randint(1, 100) 
    a = random.randint(1, 100) if op != '/' else random.randint(1, 12)*b
    question = f"Giocatore {player + 1}, quanto fa {a} {op} {b}?"
    try:
        answer = int(screen.numinput("Domanda di matematica", question))
    except:
        return False
    correct = None
    if op == '+': correct = a + b
    elif op == '-': correct = a - b
    elif op == '*': correct = a * b
    else: correct = a // b
#    answer = correct
    return answer == correct


screen, turtles = init_race()
winner = None
while not winner:
    for idx, t in enumerate(turtles):
        if ask_question(idx):
            t.forward(10)
            if t.xcor() >= x_e:
                winner = idx
                break

msg = f"Il vincitore è il Giocatore {winner + 1} ({colors[winner].capitalize()})!"
messagebox.showinfo("Fine della gara", msg)
screen.bye()
