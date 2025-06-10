import g2d
x, y = 100, 200
dx = 3
size = 30

def tick():
    global x, dx
    if g2d.mouse_clicked():
        dx = -dx
    x += dx
    canvas_w, canvas_h = g2d.canvas_size()
    if x > canvas_w + 100:
        x = -100
    elif x < -100:
        x = canvas_w + 100

    g2d.clear_canvas()
    draw(x, y)

def draw(x, y):
    g2d.set_color((34, 139, 34))
    g2d.set_stroke(0)
    g2d.draw_circle((x, y), size // 2)

g2d.init_canvas((800, 400))
g2d.clear_canvas()

g2d.set_color((0, 0, 0))
g2d.draw_text("Clicca per invertire la direzione della tartaruga!", (400, 50), 20)

g2d.main_loop(tick, fps=60)
