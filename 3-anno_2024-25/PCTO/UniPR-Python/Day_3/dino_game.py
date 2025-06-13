#!/usr/bin/env python3

import g2d
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
GRAVITY = 0.8
JUMP_STRENGTH = -16
GAME_SPEED = 6

SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (34, 139, 34)
DINO_GREEN = (50, 205, 50)
DINO_DARK = (0, 100, 0)
CACTUS_GREEN = (46, 125, 50)
CLOUD_WHITE = (255, 255, 255)
SUN_YELLOW = (255, 223, 0)
OBSTACLE_RED = (220, 20, 60)
SCORE_BLACK = (50, 50, 50)

class Dino:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
        self.width = 40
        self.height = 60
        self.velocity_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.animation_frame = 0
        self.animation_timer = 0

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

    def duck(self, ducking):
        self.is_ducking = ducking

    def update(self):
        # Animation
        self.animation_timer += 1
        if self.animation_timer > 8:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2

        # Physics
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.y += self.velocity_y

            # Check if landed
            ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
            if self.y >= ground_y:
                self.y = ground_y
                self.velocity_y = 0
                self.is_jumping = False

    def draw(self):
        # Adjust size if ducking
        height = self.height // 2 if self.is_ducking else self.height
        y_offset = self.height // 2 if self.is_ducking else 0

        # Body
        g2d.set_color(DINO_GREEN)
        g2d.draw_rect((self.x, self.y + y_offset), (self.width, height))

        # Head
        if not self.is_ducking:
            g2d.draw_circle((self.x + self.width//2, self.y - 15), 20)

            # Eye
            g2d.set_color(DINO_DARK)
            g2d.draw_circle((self.x + self.width//2 + 8, self.y - 18), 4)

        # Legs animation
        g2d.set_color(DINO_DARK)
        leg_offset = 3 if self.animation_frame == 0 else -3
        if not self.is_jumping:
            g2d.draw_rect((self.x + 5, self.y + height), (8, 15))
            g2d.draw_rect((self.x + self.width - 13 + leg_offset, self.y + height), (8, 15))

        # Tail
        g2d.set_color(DINO_GREEN)
        g2d.draw_polygon([
            (self.x - 10, self.y + height//2),
            (self.x, self.y + height//4),
            (self.x, self.y + 3*height//4)
        ])

class Obstacle:
    def __init__(self, x, obstacle_type="cactus"):
        self.x = x
        self.type = obstacle_type
        self.width = 20 if obstacle_type == "cactus" else 60
        self.height = 60 if obstacle_type == "cactus" else 30
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        if obstacle_type == "bird":
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 120
        self.animation_frame = 0
        self.animation_timer = 0

    def update(self):
        self.x -= GAME_SPEED

        # Animation for birds
        if self.type == "bird":
            self.animation_timer += 1
            if self.animation_timer > 6:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2

    def draw(self):
        if self.type == "cactus":
            # Main cactus body
            g2d.set_color(CACTUS_GREEN)
            g2d.draw_rect((self.x, self.y), (self.width, self.height))

            # Cactus arms
            g2d.draw_rect((self.x - 8, self.y + 20), (15, 8))
            g2d.draw_rect((self.x + self.width - 7, self.y + 35), (15, 8))

            # Spikes
            g2d.set_color(DINO_DARK)
            for i in range(0, self.height, 10):
                g2d.draw_circle((self.x - 2, self.y + i), 2)
                g2d.draw_circle((self.x + self.width + 2, self.y + i), 2)

        elif self.type == "bird":
            # Bird body
            g2d.set_color(OBSTACLE_RED)
            g2d.draw_circle((self.x + self.width//2, self.y + self.height//2), 15)

            # Wings
            wing_offset = 5 if self.animation_frame == 0 else -5
            g2d.draw_polygon([
                (self.x, self.y + wing_offset),
                (self.x + 25, self.y + 10 + wing_offset),
                (self.x + 10, self.y + 20 + wing_offset)
            ])
            g2d.draw_polygon([
                (self.x + self.width - 25, self.y + 10 + wing_offset),
                (self.x + self.width, self.y + wing_offset),
                (self.x + self.width - 10, self.y + 20 + wing_offset)
            ])

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

class Cloud:
    def __init__(self):
        self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200)
        self.y = random.randint(50, 150)
        self.speed = random.uniform(0.5, 1.5)
        self.size = random.randint(30, 50)

    def update(self):
        self.x -= self.speed

    def draw(self):
        g2d.set_color(CLOUD_WHITE)
        # Draw fluffy cloud
        g2d.draw_circle((self.x, self.y), self.size)
        g2d.draw_circle((self.x + self.size//2, self.y), self.size//1.2)
        g2d.draw_circle((self.x - self.size//2, self.y), self.size//1.2)
        g2d.draw_circle((self.x, self.y - self.size//3), self.size//1.5)

class Game:
    def __init__(self):
        self.dino = Dino()
        self.obstacles = []
        self.clouds = []
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.cloud_timer = 0
        self.ground_offset = 0

        # Add initial clouds
        for i in range(3):
            cloud = Cloud()
            cloud.x = random.randint(100, SCREEN_WIDTH - 100)
            self.clouds.append(cloud)

    def spawn_obstacle(self):
        obstacle_type = random.choice(["cactus", "cactus", "bird"])  # More cacti than birds
        self.obstacles.append(Obstacle(SCREEN_WIDTH, obstacle_type))

    def spawn_cloud(self):
        self.clouds.append(Cloud())

    def check_collision(self):
        dino_rect = (self.dino.x, self.dino.y, self.dino.width,
                    self.dino.height // 2 if self.dino.is_ducking else self.dino.height)

        for obstacle in self.obstacles:
            obs_rect = obstacle.get_rect()
            # Simple rectangle collision
            if (dino_rect[0] < obs_rect[0] + obs_rect[2] and
                dino_rect[0] + dino_rect[2] > obs_rect[0] and
                dino_rect[1] < obs_rect[1] + obs_rect[3] and
                dino_rect[1] + dino_rect[3] > obs_rect[1]):
                return True
        return False

    def update(self):
        if self.game_over:
            return

        # Update game objects
        self.dino.update()

        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)
                self.score += 10

        # Update clouds
        for cloud in self.clouds[:]:
            cloud.update()
            if cloud.x + cloud.size < 0:
                self.clouds.remove(cloud)

        # Spawn obstacles
        self.obstacle_timer += 1
        if self.obstacle_timer > random.randint(60, 120):
            self.spawn_obstacle()
            self.obstacle_timer = 0

        # Spawn clouds
        self.cloud_timer += 1
        if self.cloud_timer > random.randint(120, 200):
            self.spawn_cloud()
            self.cloud_timer = 0

        # Check collision
        if self.check_collision():
            self.game_over = True

        # Update ground animation
        self.ground_offset = (self.ground_offset + GAME_SPEED) % 40

    def draw_background(self):
        # Sky gradient
        for i in range(SCREEN_HEIGHT - GROUND_HEIGHT):
            gradient_factor = i / (SCREEN_HEIGHT - GROUND_HEIGHT)
            r = int(SKY_BLUE[0] + (255 - SKY_BLUE[0]) * gradient_factor * 0.3)
            g = int(SKY_BLUE[1] + (255 - SKY_BLUE[1]) * gradient_factor * 0.3)
            b = int(SKY_BLUE[2] + (255 - SKY_BLUE[2]) * gradient_factor * 0.1)
            g2d.set_color((r, g, b))
            g2d.draw_line((0, i), (SCREEN_WIDTH, i))

        # Sun
        g2d.set_color(SUN_YELLOW)
        g2d.draw_circle((SCREEN_WIDTH - 100, 80), 40)
        g2d.set_color((255, 255, 0))
        g2d.draw_circle((SCREEN_WIDTH - 100, 80), 30)

        # Ground
        g2d.set_color(GROUND_GREEN)
        g2d.draw_rect((0, SCREEN_HEIGHT - GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT))

        # Ground pattern
        g2d.set_color((20, 100, 20))
        for x in range(-40, SCREEN_WIDTH + 40, 40):
            offset_x = x - self.ground_offset
            g2d.draw_rect((offset_x, SCREEN_HEIGHT - GROUND_HEIGHT), (20, GROUND_HEIGHT))

    def draw(self):
        g2d.clear_canvas()

        self.draw_background()

        # Draw clouds
        for cloud in self.clouds:
            cloud.draw()

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw()

        # Draw dino
        self.dino.draw()

        # Draw score
        g2d.set_color(SCORE_BLACK)
        g2d.draw_text(f"Score: {self.score}", (SCREEN_WIDTH - 100, 30), 24)

        if self.game_over:
            g2d.set_color((255, 0, 0))
            g2d.draw_text("GAME OVER", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 48)
            g2d.draw_text("Press SPACE to restart", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), 24)

# Global game instance
game = Game()

def tick():
    global game

    # Handle input
    if g2d.key_pressed("Spacebar"):
        if game.game_over:
            game = Game()  # Restart game
        else:
            game.dino.jump()

    # Handle ducking
    current_keys = g2d.current_keys()
    game.dino.duck("ArrowDown" in current_keys)

    # Update game
    game.update()
    game.draw()

def main():
    g2d.init_canvas((SCREEN_WIDTH, SCREEN_HEIGHT))
    g2d.main_loop(tick, 60)

if __name__ == "__main__":
    main()
