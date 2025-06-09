from g2d import *

init_canvas((600, 400))  # width, height

set_color((255, 255, 0))  # red + green = yellow
draw_rect((150, 100), (250, 200))  # left-top position, size

set_color((0, 255, 0))
draw_line((150, 100), (400, 300))  # point1, point2

set_color((0, 0, 255))
draw_circle((400, 300), 20)  # center, radius

set_color((255, 0, 0))
draw_text("4ur4", (150, 100), 40)  # text, center, font-size
alert("dio")
main_loop()  # manage the window/canvas
