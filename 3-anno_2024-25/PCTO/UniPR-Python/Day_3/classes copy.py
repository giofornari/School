import g2d
import random
import math

# Costanti di gioco
ARENA_W, ARENA_H = 2000, 1500
VIEW_W, VIEW_H = 800, 600
FPS = 60

# Colori
COLORS = {
    'player': (100, 150, 255),
    'crystal': (255, 200, 50),
    'enemy': (255, 80, 80),
    'powerup': (150, 255, 150),
    'projectile': (255, 255, 255),
}

class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.w, self.h = 20, 20
        self.speed = 200
        self.hp = 100
        self.max_hp = 100
        self.score = 0
        self.last_shot = 0
        self.shot_cooldown = 15  # frame di attesa tra spari
        
        # Potenziamenti semplificati
        self.speed_boost = 0
        self.rapid_fire = 0
        
        self.invincible_time = 0
        self.crystals_collected = 0
        self.enemies_killed = 0

    def update(self):
        keys = g2d.current_keys()
        dx = dy = 0
        
        # Movimento con WASD
        if "w" in keys and self.y > 0:
            dy -= 1
        if "s" in keys and self.y < ARENA_H - self.h:
            dy += 1
        if "a" in keys and self.x > 0:
            dx -= 1
        if "d" in keys and self.x < ARENA_W - self.w:
            dx += 1

        # Applica velocità
        current_speed = self.speed
        if self.speed_boost > 0:
            current_speed *= 1.5
            self.speed_boost -= 1

        self.x += dx * current_speed / 60
        self.y += dy * current_speed / 60

        # Aggiorna poteri
        if self.rapid_fire > 0:
            self.rapid_fire -= 1
        if self.invincible_time > 0:
            self.invincible_time -= 1

        self.last_shot += 1

    def shoot(self, target_x, target_y):
        """Spara verso il target"""
        cooldown = 8 if self.rapid_fire > 0 else self.shot_cooldown
        if self.last_shot >= cooldown:
            self.last_shot = 0
            return True
        return False

    def take_damage(self, damage):
        """Ricevi danno se non invincibile"""
        if self.invincible_time <= 0:
            self.hp -= damage
            self.invincible_time = 60  # 1 secondo
            return True
        return False

    def collect_crystal(self, crystal):
        """Raccogli cristallo"""
        self.score += crystal.value
        self.crystals_collected += 1
        crystal.collected = True
        
        # Possibilità di rigenerare salute
        if random.random() < 0.2:
            self.hp = min(self.max_hp, self.hp + 10)

    def collect_powerup(self, powerup):
        """Raccogli potenziamento"""
        powerup.collected = True
        if powerup.type == "speed":
            self.speed_boost = 300  # 5 secondi
        elif powerup.type == "rapid_fire":
            self.rapid_fire = 300  # 5 secondi

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        # Effetto lampeggiante se invincibile
        if self.invincible_time > 0 and self.invincible_time % 10 < 5:
            return  # Non disegnare per creare lampeggio

        # Cambia colore in base ai poteri attivi
        color = list(COLORS['player'])
        if self.speed_boost > 0:
            color[1] = 255  # Più verde per velocità
        if self.rapid_fire > 0:
            color[2] = 255  # Più blu per fuoco rapido

        g2d.set_color(tuple(color))
        g2d.draw_rect((screen_x, screen_y), (self.w, self.h))

class Projectile:
    def __init__(self, x, y, target_x, target_y, speed=400):
        self.x, self.y = x, y
        self.w, self.h = 6, 6
        
        # Calcola direzione
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            self.vx = (dx / distance) * speed / 60
            self.vy = (dy / distance) * speed / 60
        else:
            self.vx = self.vy = 0
        
        self.life = 120  # 2 secondi

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        return self.life > 0 and 0 <= self.x <= ARENA_W and 0 <= self.y <= ARENA_H

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        g2d.set_color(COLORS['projectile'])
        g2d.draw_rect((screen_x, screen_y), (self.w, self.h))

class Crystal:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.w, self.h = 15, 15
        self.value = random.randint(10, 25)
        self.collected = False

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        if self.collected:
            return
        
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        
        if -self.w <= screen_x <= VIEW_W and -self.h <= screen_y <= VIEW_H:
            g2d.set_color(COLORS['crystal'])
            g2d.draw_rect((screen_x, screen_y), (self.w, self.h))

class Enemy:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.w, self.h = 20, 20
        self.hp = 25
        self.max_hp = 25
        self.speed = 60
        self.damage = 15
        self.last_attack = 0
        self.attack_cooldown = 90  # 1.5 secondi
        self.dead = False

    def update(self, player):
        if self.dead:
            return True
        
        # Insegui il giocatore
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0 and distance > 25:
            self.x += (dx / distance) * self.speed / 60
            self.y += (dy / distance) * self.speed / 60
        
        # Mantieni nei limiti
        self.x = max(0, min(self.x, ARENA_W - self.w))
        self.y = max(0, min(self.y, ARENA_H - self.h))
        
        # Attacca se vicino
        self.last_attack += 1
        if distance < 35 and self.last_attack > self.attack_cooldown:
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
        if self.dead:
            return
        
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        
        if -self.w <= screen_x <= VIEW_W and -self.h <= screen_y <= VIEW_H:
            g2d.set_color(COLORS['enemy'])
            g2d.draw_rect((screen_x, screen_y), (self.w, self.h))
            
            # Barra della vita semplificata
            if self.hp < self.max_hp:
                health_ratio = self.hp / self.max_hp
                g2d.set_color((100, 100, 100))
                g2d.draw_rect((screen_x, screen_y - 6), (self.w, 3))
                g2d.set_color((255, 0, 0))
                g2d.draw_rect((screen_x, screen_y - 6), (self.w * health_ratio, 3))

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x, self.y = x, y
        self.w, self.h = 12, 12
        self.type = power_type  # "speed" o "rapid_fire"
        self.collected = False

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def draw(self, camera):
        if self.collected:
            return
        
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        
        if -self.w <= screen_x <= VIEW_W and -self.h <= screen_y <= VIEW_H:
            g2d.set_color(COLORS['powerup'])
            g2d.draw_rect((screen_x, screen_y), (self.w, self.h))

class Camera:
    def __init__(self):
        self.x = self.y = 0.0
        self.target_x = self.target_y = 0.0

    def follow_player(self, player):
        # Centra la camera sul giocatore
        self.target_x = player.x - VIEW_W // 2
        self.target_y = player.y - VIEW_H // 2
        
        # Mantieni nei limiti dell'arena
        self.target_x = max(0, min(self.target_x, ARENA_W - VIEW_W))
        self.target_y = max(0, min(self.target_y, ARENA_H - VIEW_H))

    def update(self):
        # Movimento fluido verso il target
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1

def collision_rect(rect1, rect2):
    """Controlla collisione tra due rettangoli"""
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)

class GameWorld:
    def __init__(self):
        self.camera = Camera()
        self.player = Player(ARENA_W // 2, ARENA_H // 2)
        
        # Liste degli oggetti di gioco
        self.crystals = []
        self.enemies = []
        self.projectiles = []
        self.powerups = []
        
        # Stato del gioco
        self.game_state = "playing"  # "playing", "paused", "game_over"
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 120  # 2 secondi tra spawn
        
        # Genera contenuto iniziale
        self.generate_crystals()
        self.spawn_initial_enemies()

    def generate_crystals(self):
        """Genera cristalli nell'arena"""
        for _ in range(50):
            x = random.randint(50, ARENA_W - 50)
            y = random.randint(50, ARENA_H - 50)
            
            # Evita di spawnar troppo vicino al giocatore
            if abs(x - self.player.x) > 100 or abs(y - self.player.y) > 100:
                self.crystals.append(Crystal(x, y))

    def spawn_initial_enemies(self):
        """Spawna alcuni nemici iniziali"""
        for _ in range(5):
            self.spawn_single_enemy()

    def spawn_single_enemy(self):
        """Spawna un singolo nemico lontano dal giocatore"""
        attempts = 0
        while attempts < 20:  # Massimo 20 tentativi
            x = random.randint(0, ARENA_W - 25)
            y = random.randint(0, ARENA_H - 25)
            distance = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
            if distance > 150:
                self.enemies.append(Enemy(x, y))
                break
            attempts += 1

    def spawn_powerup(self, x, y):
        """Spawna un potenziamento"""
        power_types = ["speed", "rapid_fire"]
        power_type = random.choice(power_types)
        self.powerups.append(PowerUp(x, y, power_type))

    def update(self):
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
                self.player.take_damage(enemy.damage)
            if result and not enemy.dead:
                active_enemies.append(enemy)
        self.enemies = active_enemies
        
        # Controlla collisioni
        self.check_collisions()
        
        # Spawna nemici continuamente
        self.continuous_enemy_spawn()
        
        # Controlla game over
        if self.player.hp <= 0:
            self.game_state = "game_over"

    def handle_input(self):
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
        player_rect = self.player.get_rect()
        
        # Giocatore vs Cristalli
        for crystal in self.crystals:
            if not crystal.collected and collision_rect(player_rect, crystal.get_rect()):
                self.player.collect_crystal(crystal)
        
        # Giocatore vs PowerUps
        for powerup in self.powerups:
            if not powerup.collected and collision_rect(player_rect, powerup.get_rect()):
                self.player.collect_powerup(powerup)
        
        # Proiettili vs Nemici
        for projectile in self.projectiles[:]:
            proj_rect = projectile.get_rect()
            for enemy in self.enemies:
                if not enemy.dead and collision_rect(proj_rect, enemy.get_rect()):
                    if enemy.take_damage(20):
                        self.player.enemies_killed += 1
                        self.player.score += 50
                        
                        # Possibilità di spawn powerup
                        if random.random() < 0.2:
                            self.spawn_powerup(enemy.x, enemy.y)
                    
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break

    def continuous_enemy_spawn(self):
        """Spawna nemici continuamente nel tempo"""
        self.enemy_spawn_timer += 1
        
        # Se ci sono meno di 8 nemici e è passato abbastanza tempo, spawna un nuovo nemico
        if len(self.enemies) < 8 and self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.spawn_single_enemy()
            self.enemy_spawn_timer = 0
            
            # Riduci gradualmente il tempo tra spawn (max velocità: 1 secondo)
            if self.enemy_spawn_delay > 60:
                self.enemy_spawn_delay -= 2

    def draw(self):
        # Sfondo semplice
        g2d.clear_canvas((20, 30, 60))
        
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
        
        # UI
        self.draw_ui()

    def draw_ui(self):
        # Barra della vita
        g2d.set_color((50, 50, 50))
        g2d.draw_rect((10, 10), (200, 20))
        
        health_ratio = self.player.hp / self.player.max_hp
        if health_ratio > 0.7:
            color = (0, 255, 0)
        elif health_ratio > 0.3:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        
        g2d.set_color(color)
        g2d.draw_rect((10, 10), (200 * health_ratio, 20))
        
        # Testo UI
        g2d.set_color((255, 255, 255))
        g2d.draw_text(f"HP: {self.player.hp}", (15, 25), 14)
        g2d.draw_text(f"Score: {self.player.score}", (VIEW_W - 100, 20), 16)
        g2d.draw_text(f"Enemies: {len(self.enemies)}", (VIEW_W - 100, 40), 16)
        
        # Indicatori poteri attivi
        if self.player.speed_boost > 0:
            g2d.set_color(COLORS['powerup'])
            g2d.draw_text(f"SPEED: {self.player.speed_boost//60 + 1}s", (VIEW_W - 120, 60), 12)
        
        if self.player.rapid_fire > 0:
            g2d.set_color(COLORS['powerup'])
            g2d.draw_text(f"RAPID: {self.player.rapid_fire//60 + 1}s", (VIEW_W - 120, 80), 12)
        
        # Statistiche
        g2d.set_color((200, 200, 200))
        g2d.draw_text(f"Crystals: {self.player.crystals_collected}", (10, VIEW_H - 40), 12)
        g2d.draw_text(f"Kills: {self.player.enemies_killed}", (10, VIEW_H - 25), 12)
        
        # Istruzioni
        g2d.draw_text("WASD: Move | Mouse: Shoot | P: Pause", (10, VIEW_H - 10), 10)
        
        # Schermate speciali
        if self.game_state == "game_over":
            g2d.set_color((0, 0, 0, 150))
            g2d.draw_rect((0, 0), (VIEW_W, VIEW_H))
            
            g2d.set_color((255, 255, 255))
            g2d.draw_text("GAME OVER", (VIEW_W // 2 - 60, VIEW_H // 2 - 30), 24)
            g2d.draw_text(f"Final Score: {self.player.score}", (VIEW_W // 2 - 70, VIEW_H // 2), 16)
            g2d.draw_text(f"Enemies Killed: {self.player.enemies_killed}", (VIEW_W // 2 - 80, VIEW_H // 2 + 20), 14)
        
        elif self.game_state == "paused":
            g2d.set_color((0, 0, 0, 150))
            g2d.draw_rect((0, 0), (VIEW_W, VIEW_H))
            
            g2d.set_color((255, 255, 255))
            g2d.draw_text("PAUSED", (VIEW_W // 2 - 40, VIEW_H // 2), 20)
            g2d.draw_text("Press P to continue", (VIEW_W // 2 - 70, VIEW_H // 2 + 25), 14)

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