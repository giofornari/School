#!/usr/bin/env python3
"""
Frogger Game
A classic arcade game where you guide a frog across roads and rivers.
Use arrow keys to move, avoid cars, and hop on logs to cross water.
"""

from g2d import *
import random
import math

# Game constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CELL_SIZE = 40
ROWS = CANVAS_HEIGHT // CELL_SIZE
COLS = CANVAS_WIDTH // CELL_SIZE

# Colors
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)

class Frog:
    def __init__(self):
        self.x = CANVAS_WIDTH // 2 - CELL_SIZE // 2
        self.y = CANVAS_HEIGHT - CELL_SIZE
        self.size = CELL_SIZE - 4
        self.on_log = None
        self.lives = 3
        self.score = 0
        self.level = 1

    def move(self, dx, dy):
        new_x = self.x + dx * CELL_SIZE
        new_y = self.y + dy * CELL_SIZE

        # Boundary checking
        if 0 <= new_x <= CANVAS_WIDTH - CELL_SIZE and 0 <= new_y <= CANVAS_HEIGHT - CELL_SIZE:
            self.x = new_x
            self.y = new_y

            # Score for moving forward
            if dy < 0:
                self.score += 10

    def get_row(self):
        return self.y // CELL_SIZE

    def get_col(self):
        return self.x // CELL_SIZE

    def reset_position(self):
        self.x = CANVAS_WIDTH // 2 - CELL_SIZE // 2
        self.y = CANVAS_HEIGHT - CELL_SIZE
        self.on_log = None

    def draw(self):
        # Draw frog body
        set_color(GREEN)
        draw_circle((self.x + CELL_SIZE//2, self.y + CELL_SIZE//2), self.size//2)

        # Draw eyes
        set_color(BLACK)
        draw_circle((self.x + CELL_SIZE//2 - 8, self.y + CELL_SIZE//2 - 8), 3)
        draw_circle((self.x + CELL_SIZE//2 + 8, self.y + CELL_SIZE//2 - 8), 3)

class Car:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = CELL_SIZE - 4
        self.height = CELL_SIZE - 8

    def update(self):
        self.x += self.speed

        # Wrap around screen
        if self.speed > 0 and self.x > CANVAS_WIDTH:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = CANVAS_WIDTH

    def draw(self):
        set_color(self.color)
        set_stroke(0)
        draw_rect((self.x, self.y + 4), (self.width, self.height))

        # Draw windows
        set_color(BLACK)
        draw_rect((self.x + 4, self.y + 8), (self.width - 8, self.height - 8))

    def collides_with(self, frog):
        return (self.x < frog.x + frog.size and
                self.x + self.width > frog.x and
                self.y < frog.y + frog.size and
                self.y + self.height > frog.y)

class Log:
    def __init__(self, x, y, speed, length):
        self.x = x
        self.y = y
        self.speed = speed
        self.length = length
        self.width = length * CELL_SIZE
        self.height = CELL_SIZE - 8

    def update(self):
        self.x += self.speed

        # Wrap around screen
        if self.speed > 0 and self.x > CANVAS_WIDTH:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = CANVAS_WIDTH

    def draw(self):
        set_color(BROWN)
        set_stroke(0)
        draw_rect((self.x, self.y + 4), (self.width, self.height))

        # Draw log texture
        set_color((101, 50, 5))
        for i in range(0, self.width, 20):
            draw_line((self.x + i, self.y + 4), (self.x + i, self.y + self.height + 4))

    def on_log(self, frog):
        return (self.x <= frog.x + frog.size and
                self.x + self.width >= frog.x and
                self.y <= frog.y + frog.size and
                self.y + self.height >= frog.y)

class Game:
    def __init__(self):
        self.frog = Frog()
        self.cars = []
        self.logs = []
        self.game_over = False
        self.won = False
        self.setup_level()

    def setup_level(self):
        self.cars.clear()
        self.logs.clear()

        # Create cars on road rows (bottom half)
        road_rows = [10, 8, 6, 4]  # Road positions
        colors = [RED, YELLOW, BLUE, WHITE]

        for i, row in enumerate(road_rows):
            speed = (2 + self.frog.level) * (1 if i % 2 == 0 else -1)
            color = colors[i % len(colors)]

            # Create multiple cars per row
            for j in range(3):
                x = j * (CANVAS_WIDTH // 3) + random.randint(0, 100)
                if speed < 0:
                    x = CANVAS_WIDTH - x
                self.cars.append(Car(x, row * CELL_SIZE, speed, color))

        # Create logs on water rows (top half)
        water_rows = [2, 3, 1]  # Water positions

        for i, row in enumerate(water_rows):
            speed = (1 + self.frog.level * 0.5) * (1 if i % 2 == 0 else -1)
            length = random.randint(2, 4)

            # Create multiple logs per row
            for j in range(2):
                x = j * (CANVAS_WIDTH // 2) + random.randint(0, 150)
                if speed < 0:
                    x = CANVAS_WIDTH - x
                self.logs.append(Log(x, row * CELL_SIZE, speed, length))

    def update(self):
        if self.game_over or self.won:
            return

        # Handle input
        if key_pressed("ArrowUp"):
            self.frog.move(0, -1)
        elif key_pressed("ArrowDown"):
            self.frog.move(0, 1)
        elif key_pressed("ArrowLeft"):
            self.frog.move(-1, 0)
        elif key_pressed("ArrowRight"):
            self.frog.move(1, 0)

        # Update cars
        for car in self.cars:
            car.update()

        # Update logs
        for log in self.logs:
            log.update()

        # Check frog position
        frog_row = self.frog.get_row()

        # Check if frog reached the top (won)
        if frog_row <= 0:
            self.won = True
            self.frog.score += 1000
            return

        # Check if frog is in water
        if frog_row in [1, 2, 3]:  # Water rows
            self.frog.on_log = None
            # Check if frog is on a log
            for log in self.logs:
                if log.on_log(self.frog):
                    self.frog.on_log = log
                    self.frog.x += log.speed  # Move with log
                    break

            # If not on log, frog drowns
            if self.frog.on_log is None:
                self.frog_dies()

        # Check car collisions
        elif frog_row in [4, 6, 8, 10]:  # Road rows
            for car in self.cars:
                if car.collides_with(self.frog):
                    self.frog_dies()
                    break

        # Keep frog on screen when on log
        if self.frog.on_log:
            if self.frog.x < 0:
                self.frog.x = 0
            elif self.frog.x > CANVAS_WIDTH - CELL_SIZE:
                self.frog.x = CANVAS_WIDTH - CELL_SIZE

    def frog_dies(self):
        self.frog.lives -= 1
        if self.frog.lives <= 0:
            self.game_over = True
        else:
            self.frog.reset_position()

    def draw_background(self):
        # Draw grass (safe zones)
        set_color(DARK_GREEN)
        set_stroke(0)
        draw_rect((0, 0), (CANVAS_WIDTH, CELL_SIZE))  # Top safe zone
        draw_rect((0, CANVAS_HEIGHT - CELL_SIZE), (CANVAS_WIDTH, CELL_SIZE))  # Bottom safe zone
        draw_rect((0, 5 * CELL_SIZE), (CANVAS_WIDTH, CELL_SIZE))  # Middle safe zone

        # Draw water
        set_color(BLUE)
        for row in [1, 2, 3]:
            draw_rect((0, row * CELL_SIZE), (CANVAS_WIDTH, CELL_SIZE))

        # Draw roads
        set_color(GRAY)
        for row in [4, 6, 8, 10]:
            draw_rect((0, row * CELL_SIZE), (CANVAS_WIDTH, CELL_SIZE))

        # Draw road lines
        set_color(WHITE)
        for row in [4, 6, 8, 10]:
            y = row * CELL_SIZE + CELL_SIZE // 2
            for x in range(0, CANVAS_WIDTH, 40):
                draw_rect((x, y - 1), (20, 2))

    def draw(self):
        clear_canvas(BLACK)
        self.draw_background()

        # Draw logs
        for log in self.logs:
            log.draw()

        # Draw cars
        for car in self.cars:
            car.draw()

        # Draw frog
        self.frog.draw()

        # Draw UI
        set_color(WHITE)
        draw_text(f"Lives: {self.frog.lives}", (70, 20), 16)
        draw_text(f"Score: {self.frog.score}", (200, 20), 16)
        draw_text(f"Level: {self.frog.level}", (330, 20), 16)

        if self.game_over:
            set_color(RED)
            draw_text("GAME OVER", (CANVAS_WIDTH//2, CANVAS_HEIGHT//2), 32)
            draw_text("Press R to restart", (CANVAS_WIDTH//2, CANVAS_HEIGHT//2 + 40), 16)
        elif self.won:
            set_color(YELLOW)
            draw_text("LEVEL COMPLETE!", (CANVAS_WIDTH//2, CANVAS_HEIGHT//2), 32)
            draw_text("Press SPACE to continue", (CANVAS_WIDTH//2, CANVAS_HEIGHT//2 + 40), 16)

    def restart(self):
        self.frog = Frog()
        self.game_over = False
        self.won = False
        self.setup_level()

    def next_level(self):
        self.frog.level += 1
        self.frog.reset_position()
        self.won = False
        self.setup_level()

def tick():
    global game

    if key_pressed("r") and game.game_over:
        game.restart()
    elif key_pressed("Spacebar") and game.won:
        game.next_level()

    game.update()
    game.draw()

def main():
    global game
    init_canvas((CANVAS_WIDTH, CANVAS_HEIGHT))
    game = Game()

    # Show instructions
    alert("Welcome to Frogger!\n\nUse arrow keys to move.\nAvoid cars, hop on logs to cross water.\nReach the top to win!\n\nPress OK to start!")

    main_loop(tick, 30)

if __name__ == "__main__":
    main()
