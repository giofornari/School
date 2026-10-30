from g2d import *
import random
CANVAS_SIZE = (1000,800)
init_canvas(CANVAS_SIZE)  # width, height
square_n = int(prompt("How many squares do you want to draw?"))

for square in range(square_n):
    size = random.randint(10, 100)
    draw_rect((random.randint(0, CANVAS_SIZE[0]), random.randint(0, CANVAS_SIZE[1])), (size, size))
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    set_color(color)
main_loop()  # manage the window/canvas
