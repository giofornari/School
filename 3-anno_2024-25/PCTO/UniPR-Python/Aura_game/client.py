import g2d
import socket
import pickle
import threading
import sys
import random
import math

# =============================================================================
# --- CONFIGURAZIONE DEL CLIENT ---
# =============================================================================
SERVER_ADDRESS = "game.franciuto.com"  # CAMBIA QUESTO con il tuo dominio
SERVER_PORT = 12345
VIEW_W, VIEW_H = 900, 700
FPS = 60

# =============================================================================
# --- CLASSI DI GIOCO (LOGICA CLIENT-SIDE) ---
# =============================================================================

# Costanti
ARENA_W, ARENA_H = 3000, 2000
COLORS = {
    'player': (100, 150, 255), 'crystal': (255, 200, 50),
    'enemy': (255, 80, 80), 'powerup': (150, 255, 150),
    'boss': (200, 50, 200), 'projectile': (255, 255, 255)
}

# ***** INIZIO MODIFICA IMPORTANTE *****
# Aggiungiamo una definizione vuota di GameWorld.
# Serve solo a pickle per sapere come ricostruire l'oggetto ricevuto dal server.
class GameWorld:
    pass
# ***** FINE MODIFICA IMPORTANTE *****

class Player:
    def draw(self, camera, is_me):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y

        if self.invincible_time > 0 and int(self.invincible_time / 6) % 2:
            alpha = 128 # In futuro, g2d potrebbe supportare l'alpha
        else:
            alpha = 255

        color = list(COLORS['player'])
        if self.powers['speed'] > 0: color[1] = 255
        if self.powers['shield'] > 0: color[0] = 255
        if self.powers['rapid_fire'] > 0: color[2] = 255

        g2d.set_color(tuple(color))
        g2d.draw_rect((screen_x, screen_y), (self.w, self.h))

        if is_me:
            g2d.set_color((255, 255, 255))
            g2d.draw_polygon([(screen_x + self.w/2, screen_y - 10),
                              (screen_x + self.w/2 - 5, screen_y - 15),
                              (screen_x + self.w/2 + 5, screen_y - 15)])

        if self.powers['shield'] > 0:
            g2d.set_color((100, 200, 255))
            g2d.draw_circle((screen_x + self.w/2, screen_y + self.h/2), self.w + 5)

class Projectile:
    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        g2d.set_color(COLORS['projectile'])
        g2d.draw_circle((screen_x + self.w/2, screen_y + self.h/2), 4)

class Crystal:
    def __init__(self): self.pulse = random.random() * 10
    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        self.pulse += 5 / FPS
        pulse_size = 2 + math.sin(self.pulse) * 1
        g2d.set_color(COLORS['crystal'])
        g2d.draw_circle((screen_x + self.w/2, screen_y + self.h/2), self.w/2 + pulse_size)

class Enemy:
    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        color = COLORS['enemy'] if self.type == "basic" else COLORS['boss']

        if self.dead:
            alpha = int(255 * (1 - self.death_time / 60))
            g2d.set_color(color) # Modificare se g2d supporterà alpha
        else:
            g2d.set_color(color)
        
        g2d.draw_rect((screen_x, screen_y), (self.w, self.h))

        if not self.dead:
            bar_w, bar_h = self.w, 4
            health_ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
            g2d.set_color((100, 100, 100))
            g2d.draw_rect((screen_x, screen_y - 8), (bar_w, bar_h))
            g2d.set_color((255, 0, 0) if health_ratio < 0.3 else (255, 255, 0) if health_ratio < 0.7 else (0, 255, 0))
            g2d.draw_rect((screen_x, screen_y - 8), (bar_w * health_ratio, bar_h))

class PowerUp:
    def __init__(self): self.pulse = random.random() * 10
    def draw(self, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        self.pulse += 3 / FPS
        pulse_offset = math.sin(self.pulse) * 2
        g2d.set_color(COLORS['powerup'])
        g2d.draw_rect((screen_x, screen_y + pulse_offset), (self.w, self.h))

class SmoothCamera:
    def __init__(self):
        self.x = self.y = 0.0
        self.target_x = self.target_y = 0.0
        self.lerp_factor = 0.12

    def follow(self, target_obj):
        if not target_obj: return
        self.target_x = target_obj.x - VIEW_W // 2
        self.target_y = target_obj.y - VIEW_H // 2
        self.target_x = max(0, min(self.target_x, ARENA_W - VIEW_W))
        self.target_y = max(0, min(self.target_y, ARENA_H - VIEW_H))

    def update(self):
        self.x += (self.target_x - self.x) * self.lerp_factor
        self.y += (self.target_y - self.y) * self.lerp_factor

# =============================================================================
# --- LOGICA DI RETE CLIENT ---
# =============================================================================

world = None
world_lock = threading.Lock()
client_socket = None
my_player_id = -1
camera = SmoothCamera()

def receive_thread():
    global world
    buffer = b""
    payload_size = 4

    while True:
        try:
            while len(buffer) < payload_size:
                packet = client_socket.recv(4096)
                if not packet: raise ConnectionAbortedError
                buffer += packet
            
            msg_size = int.from_bytes(buffer[:payload_size], 'big')
            buffer = buffer[payload_size:]

            while len(buffer) < msg_size:
                buffer += client_socket.recv(4096)
            
            packed_state = buffer[:msg_size]
            buffer = buffer[msg_size:]
            
            with world_lock:
                # Il client ora sa cos'è GameWorld e può deserializzarlo
                world = pickle.loads(packed_state)

        except (ConnectionAbortedError, ConnectionResetError, EOFError, pickle.UnpicklingError) as e:
            print(f"❌ Errore di connessione o deserializzazione: {e}")
            with world_lock:
                world = "disconnected"
            break

def tick():
    global world

    if client_socket.fileno() != -1: # Controlla se il socket è ancora valido
        mouse_world_x = g2d.mouse_pos()[0] + camera.x
        mouse_world_y = g2d.mouse_pos()[1] + camera.y
        inputs = {
            'keys': g2d.current_keys(),
            'shoot': g2d.mouse_clicked(),
            'mouse_pos': (mouse_world_x, mouse_world_y)
        }
        try:
            client_socket.send(pickle.dumps(inputs))
        except OSError:
            pass
            
    g2d.clear_canvas((20, 30, 60))

    with world_lock:
        current_world = world
    
    if current_world == "disconnected":
        g2d.draw_text("Disconnesso dal server.", (VIEW_W / 2, VIEW_H / 2), 24, (255, 100, 100))
        g2d.update_canvas()
        return

    if not current_world:
        g2d.draw_text("In attesa dei dati dal server...", (VIEW_W / 2, VIEW_H / 2), 24)
        g2d.update_canvas()
        return
        
    my_player = current_world.players.get(my_player_id)
    camera.follow(my_player)
    camera.update()

    # Le classi inviate dal server hanno già i metodi 'draw' definiti qui sul client.
    # Possiamo semplicemente chiamarli.
    for crystal_obj in current_world.crystals:
        # Per oggetti con animazioni client-side, potremmo usare un approccio più avanzato,
        # ma per ora questo va bene anche se l'animazione non sarà perfetta.
        if not hasattr(crystal_obj, 'pulse'): crystal_obj.pulse = 0
        crystal_obj.pulse += 5 / FPS
        Crystal.draw(crystal_obj, camera) # Chiamiamo il metodo della classe

    for powerup_obj in current_world.powerups:
        if not hasattr(powerup_obj, 'pulse'): powerup_obj.pulse = 0
        powerup_obj.pulse += 3 / FPS
        PowerUp.draw(powerup_obj, camera)

    for enemy_obj in current_world.enemies:
        enemy_obj.draw(camera)

    for proj_obj in current_world.projectiles:
        proj_obj.draw(camera)

    for player_id, player_obj in current_world.players.items():
        player_obj.draw(camera, player_id == my_player_id)
        
    draw_ui(my_player, current_world)
    
    g2d.update_canvas()

def draw_ui(player, current_world):
    if not player:
        g2d.draw_text("Sei stato eliminato!", (VIEW_W / 2, VIEW_H / 2), 24, (255, 100, 100))
        return
        
    g2d.set_color((50,50,50)); g2d.draw_rect((10,10), (200,20))
    health_ratio = player.hp / player.max_hp if player.max_hp > 0 else 0
    color = (255,0,0) if health_ratio < 0.3 else (255,255,0) if health_ratio < 0.7 else (0,255,0)
    g2d.set_color(color); g2d.draw_rect((10,10), (200 * health_ratio, 20))
    g2d.set_color((255,255,255)); g2d.draw_text(f"HP: {int(player.hp)}/{player.max_hp}", (110,20), 14)

    g2d.draw_text(f"Score: {player.score}", (VIEW_W-80, 20), 16)
    g2d.draw_text(f"Wave: {current_world.wave}", (VIEW_W-80, 45), 16)

def main():
    global client_socket, my_player_id
    
    print("===================================")
    print("       AURA - CLIENT MULTIPLAYER   ")
    print("===================================")
    
    try:
        addr = g2d.prompt(f"Indirizzo del server (default: {SERVER_ADDRESS}):")
        if not addr: addr = SERVER_ADDRESS
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"🔌 In connessione a {addr}:{SERVER_PORT}...")
        client_socket.connect((addr, SERVER_PORT))
        
        my_player_id = pickle.loads(client_socket.recv(1024))
        print(f"✅ Connesso! Il tuo ID è: {my_player_id}")
        
    except Exception as e:
        g2d.alert(f"Impossibile connettersi al server: {e}")
        return

    threading.Thread(target=receive_thread, daemon=True).start()

    g2d.init_canvas((VIEW_W, VIEW_H))
    g2d.main_loop(tick, fps=FPS)
    client_socket.close()

if __name__ == "__main__":
    main()
