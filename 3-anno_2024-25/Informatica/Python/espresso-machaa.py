"""
@Autore: Giordano Fornari
@Versione: 1.0
"""
### CONFIGURAZIONE ###
USERS_FILE = "./users.json"
adminp = {"admin": {"password": "password", "balance": 0.0}}
### -------------  ###

### LIBRERIE NECESSARIE ###
import json, os #per destroy e per salvare i dati
from colorama import Fore, Back, Style #per colori
from getpass import getpass as inputg #per password
from time import sleep #per sleep
### ------------------- ###

### ASCII SECTION ###
user_menu = f"""
┌───────────────────────────────────┐
│      {Fore.CYAN}COFFEE MACHINE MENU{Style.RESET_ALL}        │
├───────────────────────────────────┤
│ {Fore.YELLOW}1. Espresso{Style.RESET_ALL}                     │
│ {Fore.LIGHTMAGENTA_EX}2. Latte{Style.RESET_ALL}                        │
│ {Fore.LIGHTBLUE_EX}3. Cappuccino{Style.RESET_ALL}                   │
│ {Fore.GREEN}4. Add Money{Style.RESET_ALL}                    │
│ {Fore.CYAN}5. Check Balance{Style.RESET_ALL}                │
│ {Fore.RED}6. Logout{Style.RESET_ALL}                       │
└───────────────────────────────────┘
>>> """
banner = r"""
██████╗  █████╗ ██████╗ ██╗███████╗████████╗ █████╗ 
██╔══██╗██╔══██╗██╔══██╗██║██╔════╝╚══██╔══╝██╔══██╗
██████╔╝███████║██████╔╝██║███████╗   ██║   ███████║
██╔══██╗██╔══██║██╔══██╗██║╚════██║   ██║   ██╔══██║
██████╔╝██║  ██║██║  ██║██║███████║   ██║   ██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝
                                                    
██████╗ ██████╗  ██████╗                            
██╔══██╗██╔══██╗██╔═══██╗                           
██████╔╝██████╔╝██║   ██║                           
██╔═══╝ ██╔══██╗██║   ██║                           
██║     ██║  ██║╚██████╔╝                           
╚═╝     ╚═╝  ╚═╝ ╚═════╝       """
machina = r"""
        /~~~~~~~~~~~~~~~~~~~/|
       /              /######/ / |
      /              /______/ /  |
     ========================= /||
     |_______________________|/ ||
      |  \****/     \__,,__/    ||
      |===\**/       __,,__     ||    Giordano Fornari
      |______________\====/%____||
      |   ___        /~~~~\ %  / |
     _|  |===|===   /      \%_/  |
    | |  |###|     |########| | /
    |____\###/______\######/__|/
    ~~~~~~~~~~~~~~~~~~~~~~~~~~"""
cappuccino = r'''
                      (
                        )     (
                 ___...(-------)-....___
             .-""       )    (          ""-.
       .-'``'|-._             )         _.-|
      /  .--.|   `""---...........---""`   |
     /  /    |                             |
     |  |    |                             |
      \  \   |                             |
       `\ `\ |                             |
         `\ `|                             |
         _/ /\                             /
        (__/  \                           /
     _..---""` \                         /`""---.._
  .-'           \                       /          '-.
 :               `-.__             __.-'              :
 :                  ) ""---...---"" (                 :
  '._               `"--...___...--"`              _.'
    \\""--..__                              __..--""/
     '._     """----.....______.....----"""     _.'
        `""--..,,_____            _____,,..--""`
                      `"""----"""`

'''
latte = r'''
   _________
  | _______ |
 / \         \
/___\_________\
|   | \       |
|   |  \      |
|   |   \     |
|   | M  \    |
|   |     \   |
|   |\  I  \  |
|   | \     \ |
|   |  \  L  \|
|   |   \     |
|   |    \  K |
|   |     \   |
|   |      \  |
|___|_______\_|
'''
espresso = r'''


     )))
    (((
  +-----+
  |     |]
  `-----'  
___________
`---------'
'''
admin_menu = f"""
┌───────────────────────┐
│ ADMIN MENU (choose) │
├───────────────────────┤
│ {Fore.LIGHTRED_EX}1. Logout{Style.RESET_ALL}           │
│ {Fore.YELLOW}2. Add Resources{Style.RESET_ALL}    │
│ {Fore.GREEN}3. Withdraw All{Style.RESET_ALL}     │
│ {Fore.BLUE}4. Destroy Machine{Style.RESET_ALL}  │
└───────────────────────┘
>>> """
"""
banner_old =
 █████  █████ █████       ███████████ █████ ██████   ██████   █████████   ███████████ ██████████               █████████     ███████    ███████████ ███████████ ██████████ ██████████ ██████████
░░███  ░░███ ░░███       ░█░░░███░░░█░░███ ░░██████ ██████   ███░░░░░███ ░█░░░███░░░█░░███░░░░░█              ███░░░░░███  ███░░░░░███ ░░███░░░░░░█░░███░░░░░░█░░███░░░░░█░░███░░░░░█░░███░░░░░█
 ░███   ░███  ░███       ░   ░███  ░  ░███  ░███░█████░███  ░███    ░███ ░   ░███  ░  ░███  █ ░              ███     ░░░  ███     ░░███ ░███   █ ░  ░███   █ ░  ░███  █ ░  ░███  █ ░  ░███  █ ░ 
 ░███   ░███  ░███           ░███     ░███  ░███░░███ ░███  ░███████████     ░███     ░██████               ░███         ░███      ░███ ░███████    ░███████    ░██████    ░██████    ░██████   
 ░███   ░███  ░███           ░███     ░███  ░███ ░░░  ░███  ░███░░░░░███     ░███     ░███░░█               ░███         ░███      ░███ ░███░░░█    ░███░░░█    ░███░░█    ░███░░█    ░███░░█   
 ░███   ░███  ░███      █    ░███     ░███  ░███      ░███  ░███    ░███     ░███     ░███ ░   █            ░░███     ███░░███     ███  ░███  ░     ░███  ░     ░███ ░   █ ░███ ░   █ ░███ ░   █
 ░░████████   ███████████    █████    █████ █████     █████ █████   █████    █████    ██████████             ░░█████████  ░░░███████░   █████       █████       ██████████ ██████████ ██████████
  ░░░░░░░░   ░░░░░░░░░░░    ░░░░░    ░░░░░ ░░░░░     ░░░░░ ░░░░░   ░░░░░    ░░░░░    ░░░░░░░░░░               ░░░░░░░░░     ░░░░░░░    ░░░░░       ░░░░░       ░░░░░░░░░░ ░░░░░░░░░░ ░░░░░░░░░░ 

"""
### ------------ ###

### FUNZIONI DI LOGIN / REGISTER ###
def load_users():
    """ carcica user da JSON. """
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}
        
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_users(users):
    """ salva gli user"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def login_register():
    """ gestisce login e register """
    users = load_users()
    while True:
        scelta = input("Scegli: \n1 --> [login]\n2 --> [register]\n>> ").strip().lower()
        if scelta == "1":
            username = input("Username: ").strip()
            password = inputg("Password: ").strip()
            if username in users and users[username]["password"] == password:
                print("Login effettuato.\n")
                return username, users
            elif username == "admin" and password == adminp["admin"]["password"]:
                users["admin"] = {"password": password, "balance": 0.0}
                save_users(users)
                return username, users
            else:
                print("Credenziali errate.\n")
        elif scelta == "2":
            username = input("Scegli un username: ").strip()
            if username in users:
                print("Username già esistente.\n")
                continue
            password = inputg("Scegli una password: ").strip()
            # Set default balance to 0.0
            users[username] = {"password": password, "balance": 0.0}
            save_users(users)
            print("Registrazione completata. Ora effettua il login.\n")
        else:
            print("Opzione non valida.\n")
### ---------------------------- ###

### CLASSE CAFFÈ ###
class MacchinaDelCaffe:
    def __init__(self, current_user, users):
        self.current_user = current_user
        self.users = users

        self.menu = {
            "espresso": {
                "ingredients": {
                    "water": 50,
                    "coffee": 18,
                },
                "cost": 1.5,
            },
            "latte": {
                "ingredients": {
                    "water": 200,
                    "milk": 150,
                    "coffee": 24,
                },
                "cost": 2.5,
            },
            "cappuccino": {
                "ingredients": {
                    "water": 250,
                    "milk": 100,
                    "coffee": 24,
                },
                "cost": 3.0,
            }
        }

        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }
        
        self.valori_monete = {
            'quarter': 0.25,
            'dime': 0.10,
            'nickel': 0.05,
            'penny': 0.01
        }

    def report(self):
        clear_screen()
        message = f""
        for risorsa, quantita in self.resources.items():
            if risorsa in ['water', 'milk']:
                unita = 'ml'
            elif risorsa == 'coffee':
                unita = 'g'
            else:
                unita = ''
            message += f"\r│ |> {risorsa.capitalize()}: {quantita}{unita}\n"
        report_menu = f"""
        \r┌───────────────────────┐
        \r│ REPORT                │
        \r├───────────────────────┤
        \r│                       │
        \r{message}│
        \r└───────────────────────┘"""
        print(report_menu)
        sleep(2)

    def risorse_sufficienti(self, bevanda):
        for ingrediente, quantita_richiesta in self.menu[bevanda]['ingredients'].items():
            if self.resources.get(ingrediente, 0) < quantita_richiesta:
                print(f"Spiacente, non c'è abbastanza {ingrediente}.")
                return False
        return True

    def prepara_bevanda(self, bevanda):
        costo_bevanda = self.menu[bevanda]['cost']
        user_balance = self.users[self.current_user]["balance"]

        if user_balance < costo_bevanda:
            print("Saldo insufficiente per acquistare la bevanda.")
            return False

        self.users[self.current_user]["balance"] = user_balance - costo_bevanda
        self.users["admin"]["balance"] += costo_bevanda
        save_users(self.users)

        for ingrediente, quantita_richiesta in self.menu[bevanda]['ingredients'].items():
            self.resources[ingrediente] -= quantita_richiesta

        print(f"Ecco il tuo {cappuccino if bevanda == 'cappuccino' else latte if bevanda == 'latte' else espresso}. Buona degustazione!")
        return True

    def show_balance(self):
        balance = self.users[self.current_user]["balance"]
        print(f"Il tuo saldo: ${balance}")

    def withdraw_all(self):
        balance = self.users[self.current_user]["balance"]
        self.users[self.current_user]["balance"] = 0.0
        save_users(self.users)
        print(f"Saldo ritirato: ${balance}")
        
    def add_money(self):
        while True:
            try:
                amount = float(input("Inserisci l'importo da aggiungere: "))
                break
            except ValueError:
                print("Inserisci un numero valido.")
        self.users[self.current_user]["balance"] = round(self.users[self.current_user]["balance"] + amount, 2)
        save_users(self.users)
        print(f"Nuovo saldo: ${self.users[self.current_user]['balance']}")

    def add_resources(self):
        for risorsa, quantita in self.resources.items():
            print(f"Inserisci la quantità di {risorsa}: ", end="")
            input_value = input()
            if input_value.isdigit():
                self.resources[risorsa] += int(input_value)
            else:
                print("Valore non valido. Riprova.")
                continue
        self.report()
        print("Risorse aggiornate.")

    def destroy_machine(self):
        os.remove(USERS_FILE)
        os.remove(__file__)
        print("Macchina distrutta.")
        exit()
    
    def withdraw_all(self):
        self.users["admin"]["balance"] = 0.0
        save_users(self.users)
        print("Tutti i fondi sono stati ritirati.")

    def avvia(self):
        while True:
            if current_user == "admin":
                clear_screen()
                print("\n--- Console di amministrazione ---")
                sleep(1)
                print(f"{Fore.LIGHTBLACK_EX}{Style.DIM}Benvenuto, admin.{Style.RESET_ALL}") 
                scelta = input(admin_menu)
                match scelta:
                    case "1":
                        print("Logout effettuato.")
                        break
                    case "2":
                        self.add_resources()
                    case "3":
                        self.withdraw_all()
                    case "4":
                        self.destroy_machine()
                        break
                    case "":
                        self.report()
                    
            else:
                scelta = input(user_menu).lower()
                match scelta:
                    case "6":
                        print(f"{Fore.YELLOW}Logout effettuato.{Style.RESET_ALL}")
                        break

                    case "4":
                        print(f"{Fore.GREEN}Aggiunta di denaro...{Style.RESET_ALL}")
                        self.add_money()
                        continue

                    case "5":
                        print(f"{Fore.BLUE}Saldo disponibile: ...{Style.RESET_ALL}")
                        self.show_balance()
                        continue

                    case "1":
                        print(f"{Fore.MAGENTA}Preparazione di un espresso...{Style.RESET_ALL}")
                        scelta = "espresso"
                    case "2":
                        print(f"{Fore.CYAN}Preparazione di un latte...{Style.RESET_ALL}")
                        scelta = "latte"
                        
                    case "3":
                        print(f"{Fore.LIGHTMAGENTA_EX}Preparazione di un cappuccino...{Style.RESET_ALL}")
                        scelta = "cappuccino"
                    
                    case "earn":
                        if users["admin"]["password"] == input("Password? >>> "):
                            print(f"Il saldo di admin è {users["admin"]["balance"]} £ ")
                        continue
                    case "rep":
                        self.report()
                        continue
                    
                    case "off":
                        print(f"{Fore.RED}Spegnimento della macchina...{Style.RESET_ALL}")
                        exit(0)
                    
                if scelta in ["espresso", "latte", "cappuccino"] and self.risorse_sufficienti(scelta):
                    self.prepara_bevanda(scelta)
                    sleep(3)
                    clear_screen()
                
### ------------ ###
print(f"{Fore.LIGHTRED_EX}{banner}{Fore.GREEN}{machina}{Style.RESET_ALL}")
macchina = None
while True:
    current_user, users = login_register()
    if macchina == None:
        macchina = MacchinaDelCaffe(current_user, users)
    macchina.avvia()
    clear_screen()
