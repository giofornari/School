import socket
import threading
import pickle
import time
import random
import math

# =============================================================================
# --- CONFIGURAZIONE DEL SERVER ---
# =============================================================================
HOST = '0.0.0.0'  # Ascolta su tutte le interfacce disponibili
PORT = 12345      # Porta TCP da esporre con Cloudflare Tunnel
SERVER_TICK_RATE = 30  # Aggiornamenti del mondo di gioco al secondo
TICK_INTERVAL = 1.0 / SERVER_TICK_RATE

# =============================================================================
# --- CLASSI DI GIOCO (LOGICA SERVER-SIDE) ---
# Queste classi sono state adattate dal tuo file originale.
# Tutta la logica di disegno (metodi `draw`) è stata rimossa.
# =============================================================================

# Costanti di gioco
ARENA_W, ARENA_H = 3000, 2000

class Player:
    def __init__(self, x, y, player_id):
        self.id = player_id
        self.x, self.y = x, y
        self.w, self.h = 20, 20
        self.speed = 200
        self.base_speed = 200
        self.hp = 100
        self.max_hp = 100
        self.score = 0
        self.last_shot = 0
        self.shot_cooldown = 12
        self.powers = {'speed': 0, 'shield': 0, 'rapid_fire': 0}
        self.invincible_time = 0
        self.crystals_collected = 0
        self.enemies_killed = 0
        # Dati di input ricevuti dal client
        self.inputs = {'keys': set(), 'shoot': None, 'mouse_pos': (0, 0)}

    def update(self, tick_interval):
        keys = self.inputs['keys']
        dx = dy = 0
        if "w" in keys and self.y > 0: dy -= 1
        if "s" in keys and self.y < ARENA_H - self.h: dy += 1
        if "a" in keys and self.x > 0: dx -= 1
        if "d" in keys and self.x < ARENA_W - self.w: dx += 1

        current_speed = self.base_speed * (1.5 if self.powers['speed'] > 0 else 1)
        
        # Normalizzazione del movimento diagonale
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
            
        self.x += dx * current_speed * tick_interval
        self.y += dy * current_speed * tick_interval
        
        self.x = max(0, min(self.x, ARENA_W - self.w))
        self.y = max(0, min(self.y, ARENA_H - self.h))

        for power in self.powers:
            if self.powers[power] > 0: self.powers[power] -= 1
        if self.invincible_time > 0: self.invincible_time -= 1
        self.last_shot += 1

    def shoot(self):
        cooldown = 6 if self.powers['rapid_fire'] > 0 else self.shot_cooldown
        if self.last_shot >= cooldown:
            self.last_shot = 0
            return True
        return False

    def take_damage(self, damage):
        if self.invincible_time <= 0 and self.powers['shield'] <= 0:
            self.hp -= damage
            if self.hp < 0: self.hp = 0
            self.invincible_time = 60
            return True
        return False

    def collect_crystal(self, crystal):
        self.score += crystal.value
        self.crystals_collected += 1
        crystal.collected = True
        if random.random() < 0.3:
            self.hp = min(self.max_hp, self.hp + 10)

    def collect_powerup(self, powerup):
        powerup.collected = True
        self.powers[powerup.type] = 480

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

class Projectile:
    def __init__(self, x, y, target_x, target_y, speed=400):
        self.x, self.y = x, y
        self.w, self.h = 8, 8
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            self.vx = (dx / distance) * speed
            self.vy = (dy / distance) * speed
        else:
            self.vx = self.vy = 0
        self.life = 180

    def update(self, tick_interval):
        self.x += self.vx * tick_interval
        self.y += self.vy * tick_interval
        self.life -= 1
        return self.life > 0 and 0 <= self.x <= ARENA_W and 0 <= self.y <= ARENA_H

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

class Crystal:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.w, self.h = 20, 20
        self.value = random.randint(10, 30)
        self.collected = False
    def get_rect(self): return (self.x, self.y, self.w, self.h)

class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x, self.y = x, y
        self.w, self.h = 25, 25
        self.type = enemy_type
        self.hp = 30 if enemy_type == "basic" else 60
        self.max_hp = self.hp
        self.speed = 80 if enemy_type == "basic" else 50
        self.damage = 10 if enemy_type == "basic" else 20
        self.last_attack = 0
        self.attack_cooldown = 90
        self.dead = False
        self.death_time = 0

    def update(self, players, tick_interval):
        if self.dead:
            self.death_time += 1
            return self.death_time < 60

        # Trova il giocatore più vicino
        target_player = None
        min_dist = float('inf')
        for p in players.values():
            dist = math.sqrt((p.x - self.x)**2 + (p.y - self.y)**2)
            if dist < min_dist:
                min_dist = dist
                target_player = p
        
        if not target_player:
            return True

        # Insegui il giocatore più vicino
        dx = target_player.x - self.x
        dy = target_player.y - self.y
        
        if min_dist > 0 and min_dist > 30:
            self.x += (dx / min_dist) * self.speed * tick_interval
            self.y += (dy / min_dist) * self.speed * tick_interval

        self.x = max(0, min(self.x, ARENA_W - self.w))
        self.y = max(0, min(self.y, ARENA_H - self.h))

        # Attacca se vicino
        self.last_attack += 1
        if min_dist < 40 and self.last_attack > self.attack_cooldown:
            self.last_attack = 0
            if target_player.take_damage(self.damage):
                return "attack" # Segnala un attacco andato a segno

        return True

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.dead = True
            return True
        return False

    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x, self.y = x, y
        self.w, self.h = 15, 15
        self.type = power_type
        self.collected = False
    def get_rect(self): return (self.x, self.y, self.w, self.h)

def collision_rect(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

class GameWorld:
    def __init__(self):
        self.players = {}
        self.crystals = []
        self.enemies = []
        self.projectiles = []
        self.powerups = []
        self.wave = 1
        self.enemies_to_spawn = 5
        self.wave_timer = 0
        self.generate_crystals(80)
        self.spawn_enemies()

    def add_player(self, player_id):
        x = random.randint(100, ARENA_W - 100)
        y = random.randint(100, ARENA_H - 100)
        self.players[player_id] = Player(x, y, player_id)
        print(f"Player {player_id} aggiunto al gioco.")

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
            print(f"Player {player_id} rimosso.")

    def handle_player_input(self, player_id, inputs):
        if player_id in self.players:
            player = self.players[player_id]
            player.inputs = inputs
            if inputs.get('shoot'):
                if player.shoot():
                    world_x, world_y = inputs['mouse_pos']
                    proj = Projectile(
                        player.x + player.w / 2, player.y + player.h / 2,
                        world_x, world_y
                    )
                    self.projectiles.append(proj)

    def update(self, tick_interval):
        # Aggiorna giocatori
        for player in self.players.values():
            player.update(tick_interval)

        # Aggiorna nemici
        active_enemies = []
        for enemy in self.enemies:
            if enemy.update(self.players, tick_interval):
                active_enemies.append(enemy)
        self.enemies = active_enemies
        
        # Aggiorna proiettili
        self.projectiles = [p for p in self.projectiles if p.update(tick_interval)]

        # Collisioni
        self.check_collisions()
        
        # Gestione ondate
        self.manage_waves()
        
        # Gestione morte giocatori
        dead_players = [pid for pid, p in self.players.items() if p.hp <= 0]
        for pid in dead_players:
            self.remove_player(pid)


    def check_collisions(self):
        # Proiettili vs Nemici
        for projectile in self.projectiles[:]:
            proj_rect = projectile.get_rect()
            for enemy in self.enemies:
                if not enemy.dead and collision_rect(proj_rect, enemy.get_rect()):
                    if enemy.take_damage(25): # Danno proiettile
                        # Trova il giocatore che ha sparato (per ora, il più vicino)
                        # Nota: un sistema migliore assocerebbe il proiettile a un giocatore
                        for p in self.players.values():
                            p.score += 50
                            p.enemies_killed += 1
                        if random.random() < 0.3:
                            self.spawn_powerup(enemy.x, enemy.y)
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break

        # Giocatori vs Oggetti
        for player in self.players.values():
            player_rect = player.get_rect()
            # vs Cristalli
            for crystal in self.crystals[:]:
                if not crystal.collected and collision_rect(player_rect, crystal.get_rect()):
                    player.collect_crystal(crystal)
                    self.crystals.remove(crystal)
            # vs Powerups
            for powerup in self.powerups[:]:
                if not powerup.collected and collision_rect(player_rect, powerup.get_rect()):
                    player.collect_powerup(powerup)
                    self.powerups.remove(powerup)

    def manage_waves(self):
        self.wave_timer += 1
        active_enemies = [e for e in self.enemies if not e.dead]
        if not active_enemies and self.wave_timer > 180:
            self.wave += 1
            self.enemies_to_spawn = min(20, 5 + self.wave * 2)
            self.spawn_enemies()
            self.wave_timer = 0
            if self.wave % 3 == 0:
                self.generate_crystals(40)

    def generate_crystals(self, count):
        for _ in range(count):
            self.crystals.append(Crystal(random.randint(50, ARENA_W - 50), random.randint(50, ARENA_H - 50)))

    def spawn_enemies(self):
        for _ in range(self.enemies_to_spawn):
            while True:
                x = random.randint(0, ARENA_W - 30)
                y = random.randint(0, ARENA_H - 30)
                # Spawna lontano da tutti i giocatori
                if all(math.sqrt((x - p.x)**2 + (y - p.y)**2) > 300 for p in self.players.values()) or not self.players:
                    break
            enemy_type = "boss" if random.random() < 0.1 else "basic"
            self.enemies.append(Enemy(x, y, enemy_type))

    def spawn_powerup(self, x, y):
        power_types = ["speed", "shield", "rapid_fire"]
        self.powerups.append(PowerUp(x, y, random.choice(power_types)))

# =============================================================================
# --- LOGICA DI RETE ---
# =============================================================================

clients = {} # {conn: player_id}
world = GameWorld()
world_lock = threading.Lock()
player_counter = 0

def handle_client(conn, player_id):
    """Gestisce la connessione di un singolo client."""
    with world_lock:
        world.add_player(player_id)

    try:
        while True:
            data = conn.recv(2048)
            if not data:
                break
            inputs = pickle.loads(data)
            with world_lock:
                world.handle_player_input(player_id, inputs)
    except (ConnectionResetError, pickle.UnpicklingError, EOFError):
        print(f"Client {player_id} disconnesso.")
    finally:
        with world_lock:
            world.remove_player(player_id)
        del clients[conn]
        conn.close()

def game_loop():
    """Loop principale del server che aggiorna il mondo e invia lo stato."""
    while True:
        start_time = time.time()
        
        with world_lock:
            world.update(TICK_INTERVAL)
            # Usiamo pickle per serializzare l'intero oggetto mondo. Semplice ma efficace.
            state_data = pickle.dumps(world)
        
        message = len(state_data).to_bytes(4, 'big') + state_data
        
        for conn in list(clients.keys()):
            try:
                conn.sendall(message)
            except (ConnectionBrokenPipeError, OSError):
                # La disconnessione verrà gestita dal thread del client
                pass
        
        # Mantieni un tick rate costante
        elapsed_time = time.time() - start_time
        sleep_time = TICK_INTERVAL - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

def main():
    """Funzione principale che avvia il server."""
    global player_counter
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR permette di riavviare subito il server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"✅ Server avviato e in ascolto su {HOST}:{PORT}")
    print("In attesa di connessioni...")

    # Avvia il loop di gioco in un thread separato
    threading.Thread(target=game_loop, daemon=True).start()

    while True:
        conn, addr = server_socket.accept()
        player_id = player_counter
        player_counter += 1
        
        print(f"➡️  Nuova connessione da {addr}, assegnato Player ID: {player_id}")
        clients[conn] = player_id
        
        # Invia l'ID al nuovo client
        conn.send(pickle.dumps(player_id))
        
        # Avvia un thread per gestire gli input del client
        thread = threading.Thread(target=handle_client, args=(conn, player_id), daemon=True)
        thread.start()

if __name__ == "__main__":
    print("===================================")
    print("      AURA - SERVER MULTIPLAYER    ")
    print("===================================")
    print("ATTENZIONE: questo server usa 'pickle' per la comunicazione.")
    print("Non esporlo a client non fidati per evitare rischi di sicurezza.")
    print("-----------------------------------")
    main()
