import g2d
import random
import math

# Costanti di gioco
ARENA_W, ARENA_H = 3000, 2000
VIEW_W, VIEW_H = 900, 700
FPS = 60

# Colori
COLORS = {
    'player': (100, 150, 255),
    'crystal': (255, 200, 50),
    'enemy': (255, 80, 80),
    'powerup': (150, 255, 150),
    'boss': (200, 50, 200),
    'projectile': (255, 255, 255),
    'barrier': (100, 100, 100)
}
class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y # cordinate di spawn
        self.w, self.h = 20, 20 # dimensione
        self.speed = 200  # velocità variabile
        self.base_speed = 200  # velocità del personaggio
        self.hp = 100  # vita in aggiornamento
        self.max_hp = 100  # massima vita
        self.score = 0  # punteggio
        self.last_shot = 0  # frame da ultimo sparo
        self.shot_cooldown = 12 # frame di attesa tra spari

        # Potenziamenti
        self.powers = {
            'speed': 0,      # Tempo rimanente in frame
            'shield': 0,
            'rapid_fire': 0
        }

        self.invincible_time = 0 # attesa tra un danno e un altro

        self.crystals_collected = 0 # cristalli raccolti
        self.enemies_killed = 0 # kills

    def update(self):
        keys = g2d.current_keys()
        dx = dy = 0
    ## MOVIMENTI CON WASD
        if "w" in keys and self.y > 0:
            dy -= 1
        if "s" in keys and self.y < ARENA_H - self.h:
            dy += 1
        if "a" in keys and self.x > 0:
            dx -= 1
        if "d" in keys and self.x < ARENA_W - self.w:
            dx += 1

        # # Normalizza movimento diagonale - quando il giocatore si muove in diagonale
        # # (premendo due tasti contemporaneamente come W+D), il movimento risulterebbe
        # # più veloce della velocità normale. La normalizzazione mantiene la stessa
        # # velocità in tutte le direzioni.
        # #
        # # Spiegazione matematica: se dx=1 e dy=1, la velocità totale sarebbe √(1²+1²) = √2 ≈ 1.414
        # # Per normalizzare a velocità 1, dividiamo per √2: 1/√2 = √2/2 ≈ 0.707
        # # Così dx=0.707 e dy=0.707 danno velocità totale √(0.707²+0.707²) = √(0.5+0.5) = 1
        # if dx != 0 and dy != 0:
        #     dx *= 0.707
        #     dy *= 0.707


        current_speed = self.base_speed
        if self.powers['speed'] > 0:
            current_speed *= 1.5

        self.x += dx * current_speed / 60
        self.y += dy * current_speed / 60

        # Aggiorna poteri
        for power in self.powers:
            if self.powers[power] > 0:
                self.powers[power] -= 1

        # Aggiorna invincibilità
        if self.invincible_time > 0:
            self.invincible_time -= 1

        # Cooldown sparo
        self.last_shot += 1

    def shoot(self, target_x, target_y):
        """Spara verso il target"""
        cooldown = 6 if self.powers['rapid_fire'] > 0 else self.shot_cooldown  # 0.1 secondi * 60 fps
        if self.last_shot >= cooldown:
            self.last_shot = 0
            return True
        return False

    def take_damage(self, damage):
        """Ricevi danno se non invincibile"""
        if self.invincible_time <= 0 and self.powers['shield'] <= 0:
            self.hp -= damage
            self.invincible_time = 60  # 1 secondo * 60 fps
            return True
        return False

    def collect_crystal(self, crystal):
        """Raccogli cristallo"""
        self.score += crystal.value
        self.crystals_collected += 1
        crystal.collected = True

        # Chance di rigenerare salute
        if random.random() < 0.3:
            self.hp = min(self.max_hp, self.hp + 10)

    def collect_powerup(self, powerup):
        """Raccogli potenziamento"""
        powerup.collected = True
        self.powers[powerup.type] = 480  # 8 secondi * 60 fps

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        # Effetto lampeggiante se invincibile
        if self.invincible_time > 0 and int(self.invincible_time / 6) % 2:
            alpha = 128
        else:
            alpha = 255

        # Colore base o con poteri attivi
        color = list(COLORS['player'])
        if self.powers['speed'] > 0:
            color[1] = 255  # Più verde per velocità
        if self.powers['shield'] > 0:
            color[0] = 255  # Più rosso per scudo
        if self.powers['rapid_fire'] > 0:
            color[2] = 255  # Più blu per fuoco rapido

        g2d.set_color(tuple(color))
        g2d.draw_rect((screen_x, screen_y), (self.w, self.h))

        # Indicatore scudo
        if self.powers['shield'] > 0:
            g2d.set_color((100, 200, 255))
            g2d.draw_circle((screen_x + self.w//2, screen_y + self.h//2), self.w + 5)

class Projectile:
    def __init__(self, x, y, target_x, target_y, speed=400):
        self.x, self.y = x, y
        self.w, self.h = 8, 8

        dx = target_x - x # delta per la distanza
        dy = target_y - y
        distance = math.sqrt(dx*dx + dy*dy) # formula della distanza tra due punti

        if distance > 0:
            self.vx = (dx / distance) * speed / 60 # calcolo velocita orizzontale per 60fps
            self.vy = (dy / distance) * speed / 60 # calcolo velocita verticale per 60fps
        else:
            self.vx = self.vy = 0

        self.life = 180  # Durata in frame (3 secondi * 60 fps)

    def update(self):
        self.x += self.vx # movimento per frame
        self.y += self.vy
        self.life -= 1
        return self.life > 0 and 0 <= self.x <= ARENA_W and 0 <= self.y <= ARENA_H

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        g2d.set_color(COLORS['projectile'])
        g2d.draw_circle((screen_x + self.w//2, screen_y + self.h//2), 4)

class Crystal:
    """Cristalli da raccogliere"""
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.w, self.h = 20, 20
        self.value = random.randint(10, 30)
        self.pulse = 0
        self.collected = False

    def update(self):
        self.pulse += 5 / 60 # equivalente a dt * 5 a 60fps

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        if self.collected:
            return

        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        if -self.w <= screen_x <= VIEW_W and -self.h <= screen_y <= VIEW_H:
            # Effetto pulsante
            pulse_size = 2 + math.sin(self.pulse) * 1
            g2d.set_color(COLORS['crystal'])
            g2d.draw_circle((screen_x + self.w//2, screen_y + self.h//2),
                           self.w//2 + pulse_size)


class Enemy:
    """Nemici che inseguono il giocatore"""
    def __init__(self, x, y, enemy_type="basic"):
        self.x, self.y = x, y
        self.w, self.h = 25, 25
        self.type = enemy_type
        self.hp = 30 if enemy_type == "basic" else 60
        self.max_hp = self.hp
        self.speed = 80 if enemy_type == "basic" else 50
        self.damage = 10 if enemy_type == "basic" else 20
        self.last_attack = 0
        self.attack_cooldown = 90  # 1.5 secondi * 60 fps
        self.color = COLORS['enemy'] if enemy_type == "basic" else COLORS['boss']
        self.dead = False
        self.death_time = 0

    def update(self, player):
        if self.dead:
            self.death_time += 1
            return self.death_time < 60  # 1 secondo * 60 fps

        # Insegui il giocatore
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance > 0 and distance > 30:
            self.x += (dx / distance) * self.speed / 60
            self.y += (dy / distance) * self.speed / 60

        # Mantieni nei limiti dell'arena
        self.x = max(0, min(self.x, ARENA_W - self.w))
        self.y = max(0, min(self.y, ARENA_H - self.h))

        # Attacca se vicino
        self.last_attack += 1
        if distance < 40 and self.last_attack > self.attack_cooldown:
            self.last_attack = 0
            return "attack"

        return True

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.dead = True
            return True
        return False

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        if -self.w <= screen_x <= VIEW_W and -self.h <= screen_y <= VIEW_H:
            if self.dead:
                # Effetto morte
                alpha = int(255 * (1 - self.death_time / 60))
                color = (self.color[0], self.color[1], self.color[2])
                g2d.set_color(color)
            else:
                g2d.set_color(self.color)

            g2d.draw_rect((screen_x, screen_y), (self.w, self.h))

            # Barra della vita
            if not self.dead:
                bar_w = self.w
                bar_h = 4
                health_ratio = self.hp / self.max_hp

                g2d.set_color((100, 100, 100))
                g2d.draw_rect((screen_x, screen_y - 8), (bar_w, bar_h))

                g2d.set_color((255, 0, 0) if health_ratio < 0.3 else (255, 255, 0) if health_ratio < 0.7 else (0, 255, 0))
                g2d.draw_rect((screen_x, screen_y - 8), (bar_w * health_ratio, bar_h))


class PowerUp:
    """Potenziamenti temporanei"""
    def __init__(self, x, y, power_type):
        self.x, self.y = x, y
        self.w, self.h = 15, 15
        self.type = power_type  # "speed", "shield", "rapid_fire"
        self.collected = False
        self.pulse = 0

    def update(self):
        self.pulse += 3 / 60  # equivalente dt * 3 a 60fps

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        if self.collected:
            return

        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        if -self.w <= screen_x <= VIEW_W and -self.h <= screen_y <= VIEW_H:
            pulse_offset = math.sin(self.pulse) * 2
            g2d.set_color(COLORS['powerup'])
            g2d.draw_rect((screen_x, screen_y + pulse_offset), (self.w, self.h))


class SmoothCamera:
    """Camera fluida ottimizzata"""
    def __init__(self):
        self.x = self.y = 0.0
        self.target_x = self.target_y = 0.0
        self.lerp_factor = 0.12

    def follow_player(self, player):
        # Centra la camera sul giocatore
        self.target_x = player.x - VIEW_W // 2
        self.target_y = player.y - VIEW_H // 2

        # Mantieni nei limiti
        self.target_x = max(0, min(self.target_x, ARENA_W - VIEW_W))
        self.target_y = max(0, min(self.target_y, ARENA_H - VIEW_H))

    def update(self):
        # Movimento fluido verso il target
        self.x += (self.target_x - self.x) * self.lerp_factor
        self.y += (self.target_y - self.y) * self.lerp_factor



def collision_rect(rect1, rect2):
    """Controlla collisione tra due rettangoli"""
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)


class Particle:
    def __init__(self, x, y, vx, vy, color, life):
        self.x, self.y = x, y
        self.vx, self.vy = vx / 60, vy / 60  # velocità per frame
        self.color = color
        self.life = life * 60  # converti in frame
        self.max_life = self.life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        return self.life > 0

    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        if -10 <= screen_x <= VIEW_W + 10 and -10 <= screen_y <= VIEW_H + 10:
            g2d.set_color(self.color)
            g2d.draw_circle((screen_x, screen_y), 2)


class GameWorld:
    """Mondo di gioco completo"""

    def __init__(self):
        self.camera = SmoothCamera()
        self.player = Player(ARENA_W // 2, ARENA_H // 2)

        # Game objects
        self.crystals = []
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.powerups = []

        # Game state
        self.game_state = "playing"  # "playing", "paused", "game_over"
        self.wave = 1
        self.enemies_to_spawn = 5
        self.spawn_timer = 0
        self.wave_timer = 0

        # Genera contenuto iniziale
        self.generate_crystals()
        self.spawn_enemies()

        # Audio feedback (simulato con particelle)
        self.screen_shake = 0

    def generate_crystals(self):
        """Genera cristalli nell'arena"""
        for _ in range(80):
            x = random.randint(50, ARENA_W - 50)
            y = random.randint(50, ARENA_H - 50)

            # Evita di spawnar troppo vicino al giocatore
            if abs(x - self.player.x) > 100 or abs(y - self.player.y) > 100:
                self.crystals.append(Crystal(x, y))

    def spawn_enemies(self):
        """Spawna nemici per l'ondata corrente"""
        for _ in range(self.enemies_to_spawn):
            # Spawna lontano dal giocatore
            while True:
                x = random.randint(0, ARENA_W - 30)
                y = random.randint(0, ARENA_H - 30)
                distance = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
                if distance > 200:
                    break

            enemy_type = "boss" if random.random() < 0.1 else "basic"
            self.enemies.append(Enemy(x, y, enemy_type))

    def spawn_powerup(self, x, y):
        """Spawna un potenziamento"""
        power_types = ["speed", "shield", "rapid_fire"]
        power_type = random.choice(power_types)
        self.powerups.append(PowerUp(x, y, power_type))

    def create_particles(self, x, y, color, count=10):
        """Crea particelle per effetti"""
        for _ in range(count):
            vx = random.uniform(-100, 100)
            vy = random.uniform(-150, -50)
            life = random.uniform(0.5, 1.5)
            self.particles.append(Particle(x, y, vx, vy, color, life))

    def update(self):
        """Aggiorna tutto il mondo di gioco"""
        if self.game_state != "playing":
            return

        # Input di gioco
        self.handle_input()

        # Aggiorna oggetti
        self.player.update()
        self.camera.follow_player(self.player)
        self.camera.update()

        # Aggiorna proiettili
        self.projectiles = [p for p in self.projectiles if p.update()]

        # Aggiorna nemici
        active_enemies = []
        for enemy in self.enemies:
            result = enemy.update(self.player)
            if result == "attack":
                if self.player.take_damage(enemy.damage):
                    self.screen_shake = 18  # 0.3 secondi * 60 fps
                    self.create_particles(self.player.x, self.player.y, (255, 0, 0), 5)
            if result:
                active_enemies.append(enemy)
        self.enemies = active_enemies

        # Aggiorna cristalli e potenziamenti
        for crystal in self.crystals:
            crystal.update()
        for powerup in self.powerups:
            powerup.update()

        # Aggiorna particelle
        self.particles = [p for p in self.particles if p.update()]

        # Controlla collisioni
        self.check_collisions()

        # Gestione ondate
        self.manage_waves()

        # Controlla game over
        if self.player.hp <= 0:
            self.game_state = "game_over"

        # Aggiorna screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1

    def handle_input(self):
        """Gestisce input di gioco"""
        # Sparo con mouse
        if g2d.mouse_clicked():
            mouse_x, mouse_y = g2d.mouse_pos()
            world_x = mouse_x + self.camera.x
            world_y = mouse_y + self.camera.y

            if self.player.shoot(world_x, world_y):
                projectile = Projectile(
                    self.player.x + self.player.w//2,
                    self.player.y + self.player.h//2,
                    world_x, world_y
                )
                self.projectiles.append(projectile)

        # Pausa
        if g2d.key_pressed("p"):
            self.game_state = "paused" if self.game_state == "playing" else "playing"

    def check_collisions(self):
        """Controlla tutte le collisioni"""
        player_rect = self.player.get_rect()

        # Giocatore vs Cristalli
        for crystal in self.crystals:
            if not crystal.collected and collision_rect(player_rect, crystal.get_rect()):
                self.player.collect_crystal(crystal)
                self.create_particles(crystal.x, crystal.y, COLORS['crystal'], 8)

        # Giocatore vs PowerUps
        for powerup in self.powerups:
            if not powerup.collected and collision_rect(player_rect, powerup.get_rect()):
                self.player.collect_powerup(powerup)
                self.create_particles(powerup.x, powerup.y, COLORS['powerup'], 6)

        # Proiettili vs Nemici
        for projectile in self.projectiles[:]:
            proj_rect = projectile.get_rect()
            for enemy in self.enemies:
                if not enemy.dead and collision_rect(proj_rect, enemy.get_rect()):
                    if enemy.take_damage(25):
                        self.player.enemies_killed += 1
                        self.player.score += 50

                        # Chance di spawn powerup
                        if random.random() < 0.3:
                            self.spawn_powerup(enemy.x, enemy.y)

                        self.create_particles(enemy.x, enemy.y, enemy.color, 12)

                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break

    def manage_waves(self):
        """Gestisce le ondate di nemici"""
        self.wave_timer += 1

        # Controlla se l'ondata è completata
        active_enemies = [e for e in self.enemies if not e.dead]
        if len(active_enemies) == 0 and self.wave_timer > 180:  # 3 secondi * 60 fps
            self.wave += 1
            self.enemies_to_spawn = min(20, 5 + self.wave * 2)
            self.spawn_enemies()
            self.wave_timer = 0

            # Spawna più cristalli ogni 3 ondate
            if self.wave % 3 == 0:
                self.generate_crystals()

    def draw_background(self):
        """Disegna lo sfondo dell'arena"""
        # Gradiente di sfondo
        g2d.clear_canvas((20, 30, 60))

        # Stelle/punti di sfondo
        random.seed(42)  # Seed fisso per consistenza
        for _ in range(200):
            x = random.randint(0, ARENA_W)
            y = random.randint(0, ARENA_H)
            screen_x = x - self.camera.x
            screen_y = y - self.camera.y

            if -10 <= screen_x <= VIEW_W + 10 and -10 <= screen_y <= VIEW_H + 10:
                g2d.set_color((100, 100, 150))
                g2d.draw_circle((screen_x, screen_y), 1)

    def draw_ui(self):
        """Disegna l'interfaccia utente"""
        # Barra della vita
        g2d.set_color((50, 50, 50))
        g2d.draw_rect((10, 10), (200, 20))

        health_ratio = self.player.hp / self.player.max_hp
        color = (255, 0, 0) if health_ratio < 0.3 else (255, 255, 0) if health_ratio < 0.7 else (0, 255, 0)
        g2d.set_color(color)
        g2d.draw_rect((10, 10), (200 * health_ratio, 20))

        # Testo UI
        g2d.set_color((255, 255, 255))
        g2d.draw_text(f"HP: {self.player.hp}/{self.player.max_hp}", (110, 20), 14)
        g2d.draw_text(f"Score: {self.player.score}", (VIEW_W - 80, 20), 16)
        g2d.draw_text(f"Wave: {self.wave}", (VIEW_W - 80, 45), 16)

        # Indicatori poteri attivi
        y_offset = 70
        for power, time_left in self.player.powers.items():
            if time_left > 0:
                power_names = {"speed": "SPEED", "shield": "SHIELD", "rapid_fire": "RAPID"}
                g2d.set_color(COLORS['powerup'])
                g2d.draw_text(f"{power_names[power]}: {time_left/60:.1f}s",
                             (VIEW_W - 100, y_offset), 12)
                y_offset += 20

        # Statistiche
        g2d.set_color((200, 200, 200))
        g2d.draw_text(f"Crystals: {self.player.crystals_collected}", (10, VIEW_H - 60), 12)
        g2d.draw_text(f"Kills: {self.player.enemies_killed}", (10, VIEW_H - 40), 12)

        # Istruzioni
        g2d.draw_text("WASD: Move | Mouse: Shoot | P: Pause", (VIEW_W // 2, VIEW_H - 20), 12)

        # Game Over
        if self.game_state == "game_over":
            g2d.set_color((0, 0, 0))
            g2d.draw_rect((0, 0), (VIEW_W, VIEW_H))

            g2d.set_color((255, 255, 255))
            g2d.draw_text("GAME OVER", (VIEW_W // 2, VIEW_H // 2 - 50), 32)
            g2d.draw_text(f"Final Score: {self.player.score}", (VIEW_W // 2, VIEW_H // 2), 20)
            g2d.draw_text(f"Wave Reached: {self.wave}", (VIEW_W // 2, VIEW_H // 2 + 30), 16)

        # Pause
        elif self.game_state == "paused":
            g2d.set_color((0, 0, 0))
            g2d.draw_rect((0, 0), (VIEW_W, VIEW_H))

            g2d.set_color((255, 255, 255))
            g2d.draw_text("PAUSED", (VIEW_W // 2, VIEW_H // 2), 24)
            g2d.draw_text("Press P to continue", (VIEW_W // 2, VIEW_H // 2 + 30), 16)

    def draw(self):
        """Disegna tutto il mondo"""
        # Applica screen shake
        shake_x = shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.uniform(-3, 3)
            shake_y = random.uniform(-3, 3)

        # Disegna sfondo
        self.draw_background()

        # Disegna oggetti di gioco (con shake)
        original_camera_x = self.camera.x
        original_camera_y = self.camera.y
        self.camera.x += shake_x
        self.camera.y += shake_y

        # Disegna tutti gli oggetti
        for crystal in self.crystals:
            crystal.draw(self.camera)

        for powerup in self.powerups:
            powerup.draw(self.camera)

        for enemy in self.enemies:
            enemy.draw(self.camera)

        for projectile in self.projectiles:
            projectile.draw(self.camera)

        self.player.draw(self.camera)

        for particle in self.particles:
            particle.draw(self.camera)

        # Ripristina posizione camera
        self.camera.x = original_camera_x
        self.camera.y = original_camera_y

        # UI sempre in primo piano
        self.draw_ui()

# Variabili globali
world = None

def tick():
    world.update()
    world.draw()

def main():
    global world

    g2d.init_canvas((VIEW_W, VIEW_H))
    world = GameWorld()

    g2d.main_loop(tick, fps=FPS)

if __name__ == "__main__":
    main()
