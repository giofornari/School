import random, os, sys, time
from colorama import *
init(autoreset=True)

# Data provided
data = [
    {'name': 'Instagram', 'follower_count': 686, 'description': 'Piattaforma di social media', 'country': 'Stati Uniti'},
    {'name': 'Cristiano Ronaldo', 'follower_count': 651, 'description': 'Calciatore', 'country': 'Portogallo'},
    {'name': 'Lionel Messi', 'follower_count': 505, 'description': 'Calciatore', 'country': 'Argentina'},
    {'name': 'Selena Gomez', 'follower_count': 421, 'description': 'Cantante e attrice', 'country': 'Stati Uniti'},
    {'name': 'Dwayne Johnson', 'follower_count': 394, 'description': 'Attore e ex wrestler', 'country': 'Stati Uniti'},
    {'name': 'Kylie Jenner', 'follower_count': 394, 'description': 'Personaggio televisivo e imprenditrice', 'country': 'Stati Uniti'},
    {'name': 'Ariana Grande', 'follower_count': 376, 'description': 'Cantante e attrice', 'country': 'Stati Uniti'},
    {'name': 'Kim Kardashian', 'follower_count': 357, 'description': 'Personaggio televisivo e imprenditrice', 'country': 'Stati Uniti'},
    {'name': 'Beyoncé', 'follower_count': 312, 'description': 'Cantante e attrice', 'country': 'Stati Uniti'},
    {'name': 'Khloé Kardashian', 'follower_count': 303, 'description': 'Personaggio televisivo e imprenditrice', 'country': 'Stati Uniti'},
    {'name': 'Nike', 'follower_count': 301, 'description': 'Azienda di abbigliamento sportivo', 'country': 'Stati Uniti'},
    {'name': 'Justin Bieber', 'follower_count': 294, 'description': 'Cantante', 'country': 'Canada'},
    {'name': 'Kendall Jenner', 'follower_count': 288, 'description': 'Modella e personaggio televisivo', 'country': 'Stati Uniti'},
    {'name': 'Taylor Swift', 'follower_count': 282, 'description': 'Cantante e cantautrice', 'country': 'Stati Uniti'},
    {'name': 'National Geographic', 'follower_count': 279, 'description': 'Rivista e organizzazione scientifica', 'country': 'Stati Uniti'},
    {'name': 'Virat Kohli', 'follower_count': 270, 'description': 'Crickettista', 'country': 'India'},
    {'name': 'Jennifer Lopez', 'follower_count': 249, 'description': 'Cantante e attrice', 'country': 'Stati Uniti'},
    {'name': 'Neymar', 'follower_count': 229, 'description': 'Calciatore', 'country': 'Brasile'},
    {'name': 'Nicki Minaj', 'follower_count': 226, 'description': 'Rapper e cantautrice', 'country': 'Trinidad e Tobago'},
    {'name': 'Kourtney Kardashian', 'follower_count': 219, 'description': 'Personaggio televisivo e imprenditrice', 'country': 'Stati Uniti'},
    {'name': 'Miley Cyrus', 'follower_count': 213, 'description': 'Cantante e attrice', 'country': 'Stati Uniti'},
    {'name': 'Katy Perry', 'follower_count': 204, 'description': 'Cantante', 'country': 'Stati Uniti'},
    {'name': 'Zendaya', 'follower_count': 179, 'description': 'Attrice e cantante', 'country': 'Stati Uniti'},
    {'name': 'Kevin Hart', 'follower_count': 177, 'description': 'Comico e attore', 'country': 'Stati Uniti'},
    {'name': 'Real Madrid CF', 'follower_count': 173, 'description': 'Club di calcio', 'country': 'Spagna'}
]
logo = f"""
    __  ___       __             
   / / / (_)___ _/ /_  ___  _____
  / /_/ / / __ `/ __ \\/ _ \\/ ___/           {Fore.GREEN}=== BENVENUTO A HIGHER LOWER! ==={Fore.CYAN}
 / __  / / /_/ / / / /  __/ /           
/_/ ///_/\\__, /_/ /_/\\___/_/           {Fore.BLUE}Indovina se la prossima voce ha più follower (h) o meno (l). {Fore.CYAN}
   / /  /____/_      _____  _____
  / /   / __ \ | /| / / _ \\/ ___/
 / /___/ /_/ / |/ |/ /  __/ /    
/_____/\\____/|__/|__/\\___/_/     
"""

vs = r"""
 _    __    
| |  / /____
| | / / ___/
| |/ (__  ) 
|___/____(_)
"""

GAME_ART = f"""{Fore.CYAN}
{logo}
{Style.RESET_ALL}
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def formattante(entry):
    return f"{Fore.YELLOW}{entry['name']}{Style.RESET_ALL}, {entry['description']} from {entry['country']}"

def get_random_entry(exclude=None):
    choices = data.copy()
    if exclude:
        choices = [entry for entry in choices if entry != exclude]
    return random.choice(choices)
## function found to delete n lines ##
def delete_last_lines(n=1):
    """Delete the last `n` lines from stdout."""
    for _ in range(n):
        sys.stdout.write("\x1b[1A")  # Move cursor up one line
        sys.stdout.write("\x1b[2K")   # Clear the line


def play():
    init(autoreset=True)
    score = 0
    scelta_corrente = get_random_entry()
    streak = 0

    clear_screen()
    print(GAME_ART)

    while True:
        next = get_random_entry(exclude=scelta_corrente)
        print(f"{Fore.YELLOW}A: {formattante(scelta_corrente)}")
        print(f"\n{Fore.MAGENTA}\t\t\tVS{Style.RESET_ALL}")
        print(f"\n{Fore.BLUE}Rivelazione...{Style.RESET_ALL}", end="")
        time.sleep(1)
        print(f"\rB: {formattante(next)} {Fore.BLUE}({next['follower_count']} follower){Style.RESET_ALL}")
        guess = ""
        while guess not in ("h", "l"):
            guess = input(
                f"B ha più follower? [{Fore.RED}h = {Style.RESET_ALL}maggiore  ~ {Fore.RED}l = {Style.RESET_ALL}minore]: "
            ).lower().strip()
            if guess not in ("h", "l"):
                print(f"{Fore.RED}Input non valido. Usa 'h' o 'l'.{Style.RESET_ALL}")


        is_correct = (
            (guess == "h" and next["follower_count"] >= scelta_corrente["follower_count"]) or
            (guess == "l" and next["follower_count"] <= scelta_corrente["follower_count"])
        )

        if is_correct:
            score += 1
            streak += 1
            print(f"{Fore.GREEN}✔ Corretto! {Style.RESET_ALL} Punteggio: {Fore.YELLOW}{score}{Style.RESET_ALL} (Serie: {streak})")
            delete_last_lines(9)
            scelta_corrente = next
        else:
            print(f"{Fore.RED}✖ Sbagliato! {Style.RESET_ALL} La risposta era: {'maggiore' if next['follower_count'] > scelta_corrente['follower_count'] else 'minore'}e.")
            print(f"\n{Fore.CYAN}=== FINE PARTITA ===")
            print(f"Punteggio finale: {Fore.YELLOW}{score}{Style.RESET_ALL}")
            if input("Vuoi rigiocare? (s/n): ").lower() == "s":
                play()
            else:
                print(f"{Fore.CYAN}\nGrazie per aver giocato! A presto!{Style.RESET_ALL}")


        time.sleep(0.5)
        print(f"\n{'-' * 50}\n")

        
if __name__ == "__main__":
    play()