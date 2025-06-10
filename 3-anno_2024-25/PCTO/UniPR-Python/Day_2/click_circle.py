import g2d
import random
import math

def tick():
    if g2d.mouse_clicked():
        mouse_x, mouse_y = g2d.mouse_pos()
        
        canvas_w, canvas_h = g2d.canvas_size()
        center_x, center_y = canvas_w // 2, canvas_h // 2
        
        distance = math.sqrt((mouse_x - center_x)**2 + (mouse_y - center_y)**2)
        
        if distance < 50:
            if g2d.confirm("Vuoi chiudere l'applicazione?"):
                g2d.close_canvas()
        else:
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            
            g2d.set_color((red, green, blue))
            
            g2d.draw_circle((mouse_x, mouse_y), 20)

g2d.init_canvas((640, 480))
g2d.clear_canvas((255, 255, 255))

g2d.main_loop(tick)