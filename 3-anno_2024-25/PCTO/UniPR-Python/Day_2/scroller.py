from sys import _xoptions
from g2d import *
import random


SCREEN = (500,500)

init_canvas(SCREEN)

ARENA_W, ARENA_H = 1600, 1200  # Dimensioni dell'arena totale
VIEW_W, VIEW_H = 800, 600      # Dimensioni della vista (canvas)
SCROLL_SPEED = 10              # Velocità di scroll in pixel

class Sprites:
    def __init__(self, x, y, w, h, color):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.color = color

    def draw(self, view_x, view_y):
        screen_x = self.x - view_x
        screen_y = self.y - view_y

        if (screen_x + self.w >= 0 and screen_x < SCREEN[0] and screen_y + self.h >= 0 and screen_y < SCREEN[1]):
            set_color(self.color)
            draw_rect((screen_x, screen_y), (self.w, self.h))

class Player(Sprites):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, (0, 128, 255))
        self.speed = 5

    def update(self):
        keys = current_keys()

        if "w" in keys and self.y > 0:
            self.y -= self.speed
        if "s" in keys and self.y < ARENA_H - self.h:
            self.y += self.speed
        if "a" in keys and self.x > 0:
            self.x -= self.speed
        if "d" in keys and self.x < ARENA_W - self.w:
            self.x += self.speed

    def draw(self, view_x, view_y):
        screen_x = self.x - view_x
        screen_y = self.y - view_y

        if (screen_x + self.w >= 0 and screen_x < VIEW_W and
            screen_y + self.h >= 0 and screen_y < VIEW_H):

            # Corpo del giocatore
            set_color(self.color)
            draw_rect((screen_x, screen_y), (self.w, self.h))

            # Bordo
            set_color((255, 255, 255))
            set_stroke(2)
            draw_rect((screen_x, screen_y), (self.w, self.h))
            set_stroke(0)

class GameWorld:
    """Gestisce il mondo di gioco con il sistema di scroll"""
    def __init__(self):
        self.view_x = 0  # Posizione X della vista nell'arena
        self.view_y = 0  # Posizione Y della vista nell'arena

        # Crea il giocatore al centro dell'arena
        self.player = Player(ARENA_W // 2, ARENA_H // 2)

        # Crea oggetti casuali nell'arena
        self.objects = []
        for _ in range(50):
            x = random.randint(0, ARENA_W - 50)
            y = random.randint(0, ARENA_H - 50)
            w = random.randint(20, 80)
            h = random.randint(20, 80)
            color = (random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255))
            self.objects.append(Sprites(x, y, w, h, color))

    def update_view(self):
        """Aggiorna la posizione della vista basandosi sui tasti cursore"""
        keys = current_keys()

        # Scroll con i tasti cursore
        if "ArrowUp" in keys and self.view_y > 0:
            self.view_y -= SCROLL_SPEED
        if "ArrowDown" in keys and self.view_y < ARENA_H - VIEW_H:
            self.view_y += SCROLL_SPEED
        if "ArrowLeft" in keys and self.view_x > 0:
            self.view_x -= SCROLL_SPEED
        if "ArrowRight" in keys and self.view_x < ARENA_W - VIEW_W:
            self.view_x += SCROLL_SPEED

        # Mantieni la vista entro i limiti dell'arena
        self.view_x = max(0, min(self.view_x, ARENA_W - VIEW_W))
        self.view_y = max(0, min(self.view_y, ARENA_H - VIEW_H))

    def center_view_on_player(self):
        """Centra la vista sul giocatore (opzionale)"""
        # Calcola la posizione della vista per centrare il giocatore
        target_x = self.player.x - VIEW_W // 2
        target_y = self.player.y - VIEW_H // 2

        # Mantieni la vista entro i limiti dell'arena
        self.view_x = max(0, min(target_x, ARENA_W - VIEW_W))
        self.view_y = max(0, min(target_y, ARENA_H - VIEW_H))

    def draw_grid(self):
        """Disegna una griglia per mostrare il movimento"""
        set_color((200, 200, 200))

        # Linee verticali
        for x in range(0, ARENA_W, 100):
            screen_x = x - self.view_x
            if 0 <= screen_x <= VIEW_W:
                draw_line((screen_x, 0), (screen_x, VIEW_H))

        # Linee orizzontali
        for y in range(0, ARENA_H, 100):
            screen_y = y - self.view_y
            if 0 <= screen_y <= VIEW_H:
                draw_line((0, screen_y), (VIEW_W, screen_y))

    def draw_ui(self):
        """Disegna l'interfaccia utente"""
        # Informazioni sulla vista
        set_color((0, 0, 0))
        info = f"Vista: ({self.view_x}, {self.view_y}) - Giocatore: ({self.player.x}, {self.player.y})"
        draw_text(info, (VIEW_W // 2, 20), 16)

        # Istruzioni
        instructions = [
            "WASD: Muovi giocatore",
            "Frecce: Scorri vista",
            "C: Centra su giocatore"
        ]

        for i, instruction in enumerate(instructions):
            set_color((50, 50, 50))
            draw_text(instruction, (100, VIEW_H - 60 + i * 20), 14)

        # Mini-mappa (opzionale)
        self.draw_minimap()

    def draw_minimap(self):
        """Disegna una mini-mappa nell'angolo"""
        map_w, map_h = 160, 120
        map_x, map_y = VIEW_W - map_w - 10, 10
        scale_x, scale_y = map_w / ARENA_W, map_h / ARENA_H

        # Sfondo della mini-mappa
        set_color((0, 0, 0, 128))
        draw_rect((map_x, map_y), (map_w, map_h))

        # Bordo
        set_color((255, 255, 255))
        set_stroke(1)
        draw_rect((map_x, map_y), (map_w, map_h))
        set_stroke(0)

        # Vista corrente sulla mini-mappa
        view_map_x = map_x + self.view_x * scale_x
        view_map_y = map_y + self.view_y * scale_y
        view_map_w = VIEW_W * scale_x
        view_map_h = VIEW_H * scale_y

        set_color((255, 255, 0, 100))
        draw_rect((view_map_x, view_map_y), (view_map_w, view_map_h))

        # Giocatore sulla mini-mappa
        player_map_x = map_x + self.player.x * scale_x
        player_map_y = map_y + self.player.y * scale_y
        set_color((255, 0, 0))
        draw_circle((player_map_x, player_map_y), 3)

    def update(self):
        """Aggiorna il mondo di gioco"""
        # Aggiorna il giocatore
        self.player.update()

        # Aggiorna la vista
        self.update_view()

        # Centra la vista sul giocatore se richiesto
        if "c" in current_keys():
            self.center_view_on_player()

    def draw(self):
        """Disegna tutto il mondo visibile"""
        # Pulisci il canvas
        clear_canvas((100, 150, 200))

        # Disegna la griglia
        self.draw_grid()

        # Disegna tutti gli oggetti
        for obj in self.objects:
            obj.draw(self.view_x, self.view_y)

        # Disegna il giocatore
        self.player.draw(self.view_x, self.view_y)

        # Disegna l'UI
        self.draw_ui()

world = None

def tick():
    """Funzione chiamata ad ogni frame"""
    global world
    world.update()
    world.draw()

init_canvas((VIEW_W, VIEW_H))
world = GameWorld()
world.center_view_on_player()
main_loop(tick)
