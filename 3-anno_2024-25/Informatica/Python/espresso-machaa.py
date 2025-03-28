import json
import os
from colorama import Fore, Back, Style
banner = """
 █████  █████ █████       ███████████ █████ ██████   ██████   █████████   ███████████ ██████████               █████████     ███████    ███████████ ███████████ ██████████ ██████████ ██████████
░░███  ░░███ ░░███       ░█░░░███░░░█░░███ ░░██████ ██████   ███░░░░░███ ░█░░░███░░░█░░███░░░░░█              ███░░░░░███  ███░░░░░███ ░░███░░░░░░█░░███░░░░░░█░░███░░░░░█░░███░░░░░█░░███░░░░░█
 ░███   ░███  ░███       ░   ░███  ░  ░███  ░███░█████░███  ░███    ░███ ░   ░███  ░  ░███  █ ░              ███     ░░░  ███     ░░███ ░███   █ ░  ░███   █ ░  ░███  █ ░  ░███  █ ░  ░███  █ ░ 
 ░███   ░███  ░███           ░███     ░███  ░███░░███ ░███  ░███████████     ░███     ░██████               ░███         ░███      ░███ ░███████    ░███████    ░██████    ░██████    ░██████   
 ░███   ░███  ░███           ░███     ░███  ░███ ░░░  ░███  ░███░░░░░███     ░███     ░███░░█               ░███         ░███      ░███ ░███░░░█    ░███░░░█    ░███░░█    ░███░░█    ░███░░█   
 ░███   ░███  ░███      █    ░███     ░███  ░███      ░███  ░███    ░███     ░███     ░███ ░   █            ░░███     ███░░███     ███  ░███  ░     ░███  ░     ░███ ░   █ ░███ ░   █ ░███ ░   █
 ░░████████   ███████████    █████    █████ █████     █████ █████   █████    █████    ██████████             ░░█████████  ░░░███████░   █████       █████       ██████████ ██████████ ██████████
  ░░░░░░░░   ░░░░░░░░░░░    ░░░░░    ░░░░░ ░░░░░     ░░░░░ ░░░░░   ░░░░░    ░░░░░    ░░░░░░░░░░               ░░░░░░░░░     ░░░░░░░    ░░░░░       ░░░░░       ░░░░░░░░░░ ░░░░░░░░░░ ░░░░░░░░░░ 
"""
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def login_register():
    users = load_users()
    while True:
        scelta = input("Scegli: [login/register]: ").strip().lower()
        if scelta == "login":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if username in users and users[username]["password"] == password:
                print("Login effettuato.\n")
                return username, users
            else:
                print("Credenziali errate.\n")
        elif scelta == "register":
            username = input("Scegli un username: ").strip()
            if username in users:
                print("Username già esistente.\n")
                continue
            password = input("Scegli una password: ").strip()
            # Set default balance to 0.0
            users[username] = {"password": password, "balance": 0.0}
            save_users(users)
            print("Registrazione completata. Ora effettua il login.\n")
        else:
            print("Opzione non valida.\n")

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
        print("\n--- REPORT RISORSE MACCHINA ---")
        for risorsa, quantita in self.resources.items():
            if risorsa in ['water', 'milk']:
                unita = 'ml'
            elif risorsa == 'coffee':
                unita = 'g'
            else:
                unita = ''
            print(f"{risorsa.capitalize()}: {quantita}{unita}")

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

        self.users[self.current_user]["balance"] = round(user_balance - costo_bevanda, 2)
        self.users["admin"]["balance"] += costo_bevanda
        save_users(self.users)

        for ingrediente, quantita_richiesta in self.menu[bevanda]['ingredients'].items():
            self.resources[ingrediente] -= quantita_richiesta

        print(f"Ecco il tuo {bevanda}. Buona degustazione!")
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

    def avvia(self):
        print(f"{Fore.LIGHTRED_EX}{banner}{Fore.RESET}")
        print("\n--- Benvenuto alla Macchina del Caffè ---")
        while True:
            if current_user == "admin":
                print("\n--- Accesso amministratore ---")
                self.report()
                print("\n")
                scelta = int(input("Cosa desideri? (1. logout \n 2. add resources \n 3. withdraw all \n 4. destroy machine ): "))
                
            else:
                scelta = input(
                    "\nCosa desideri? (espresso / latte / cappuccino / add (money) / balance / logout): "
                ).lower()
                
                if scelta == 'off':
                    print("Chiusura della macchina.")
                    break

                if scelta == 'logout':
                    print("Logout effettuato.")
                    break

                if scelta == 'report':
                    self.report()
                    continue

                if scelta == 'balance':
                    self.show_balance()
                    continue

                if scelta == 'add':
                    self.add_money()
                    continue

                if scelta not in self.menu:
                    print("Opzione non valida. Riprova.")
                    continue
                
                if self.risorse_sufficienti(scelta):
                    self.prepara_bevanda(scelta)


current_user, users = login_register()
macchina = MacchinaDelCaffe(current_user, users)
macchina.avvia()