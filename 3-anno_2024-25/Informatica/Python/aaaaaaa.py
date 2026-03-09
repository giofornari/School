from turtle import Turtle, Screen
import random, time
from tkinter import messagebox

f = Screen()

ts = []
cs = ['red', 'blue', 'green', 'yellow', 'orange', 'black', 'purple']
dy = 40
y0 = -120
cs_txt = ', '.join([c.capitalize() for c in cs])

ok = False
while not ok:
    sc = f.textinput("Benvenuto alla Gara delle Tartarughe!", "Su quale vuoi scommettere? " + cs_txt)
    if sc.lower() not in cs:
        f.textinput("Errore", "Colore non valido. Riprova: " + cs_txt)
    else:
        ok = True

for i in range(len(cs)):
    t = Turtle(shape='turtle')
    t.color(cs[i])
    t.penup()
    yp = y0 + dy * i
    t.setpos(-350, yp)
    ts.append(t)

if ok:
    go = True
else:
    go = False

while go:
    for t in ts:
        p = random.randint(0, 10)
        t.forward(p)
        if t.xcor() > (800 / 2) - 10:
            go = False
            win = t.color()[0]
            msg = f"La vincente è la tartaruga {win}!"

txt = f"\nHai scelto: {sc.capitalize()}.\n"
txt += f"La vincente: {win.capitalize()}."

if win == sc.lower():
    title = "Vittoria!"
    txt += "\nHai vinto la scommessa!"
else:
    title = "Sconfitta!"
    txt += "\nHai perso..."

messagebox.showinfo(title, msg + "\n" + txt)