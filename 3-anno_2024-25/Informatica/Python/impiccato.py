import random
import os

winner_message = """
      ___________
     \'._==_==_=_.\'
     .-\:      /-.
    | (|:.     |) |
     \'-|:.     |-\'
       \::.    /
        \'::. .\'
          ) (
        _.\' \'._
       `\"\"\"\"\"\"\"`
"""

greeting = """
Benvenuto in Impiccato!
Il gioco consiste nel cercare di indovinare una parola
indovinando lettere una alla volta.
Se credi di sapere la parola, puoi anche scriverla interamente.
Buon divertimento!
"""
print("""
__________________________________________
||                                        ||
||  Seleziona il livello di difficoltà:   ||
||       1. Facile                        ||
||       2. Medio                         ||
||       3. Difficile                     ||
||________________________________________||
      """)
match input("Seleziona il livello : "):
    case "1":
        print("Livello Facile")
        disctionary = "parole.txt"
    case "2":
        print("Livello Medio")
        disctionary = "parole2.txt"
    case "3":
        print("Livello Difficile")
        disctionary = "parole3.txt"
    case default:
        print("Livello non valido")

with open(disctionary, "r") as f:
    parole = f.readlines()
    parola = random.choice(parole).strip()
errori = 0
user_word = ""
letters = ""

displayed_word = ""
def get_hangman_stage(errors):
    hangman_stages = [
        """
         ___________.._______  
        | .__________))______|  
        | | / /      ||  
        | |/ /       ||  
        | | /        ||  
        | |/         ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |         / | | \\  
        \"\"\"\"\"\"\"\"\"\"|_`-' `-' |\"\"\"|  
        |\"|\"\"\"\"\"\"\\ \\       '\"|\"|
        | |        \\ \\        | |  
        : :         \\ \\       : :  
        . .          `'       . .  
        """,
        """
         ___________.._______  
        | .__________))______|  
        | | / /      ||  
        | |/ /       ||  
        | | /        ||.-''.
        | |/         |/  _  \\  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |         / | | \\  
        \"\"\"\"\"\"\"\"\"\"|_`-' `-' |\"\"\"|  
        |\"|\"\"\"\"\"\"\\ \\       '\"|\"|
        | |        \\ \\        | |  
        : :         \\ \\       : :  
        . .          `'       . .  
        """,
        """
         ___________.._______  
        | .__________))______|  
        | | / /      ||  
        | |/ /       ||  
        | | /        ||.-''.
        | |/         |/  _  \\  
        | |          ||  `/,|  
        | |          (\\`_.')  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |          ||  
        | |         / | | \\  
        \"\"\"\"\"\"\"\"\"\"|_`-' `-' |\"\"\"|  
        |\"|\"\"\"\"\"\"\\ \\       '\"|\"|
        | |        \\ \\        | |  
        : :         \\ \\       : :  
        . .          `'       . .  
        """,
        """
         ___________.._______  
        | .__________))______|  
        | | / /      ||  
        | |/ /       ||  
        | | /        ||.-''.
        | |/         |/  _  \\  
        | |          ||  `/,|  
        | |          (\\`_.')  
        | |         .-`--'.  
        | |        /Y .    
        | |       // |    
        | |      //  |    
        | |     ')   |    
        | |          ||  
        | |         / | | \\  
        \"\"\"\"\"\"\"\"\"\"|_`-' `-' |\"\"\"|  
        |\"|\"\"\"\"\"\"\\ \\       '\"|\"|
        | |        \\ \\        | |  
        : :         \\ \\       : :  
        . .          `'       . .  
        """,
        """
         ___________.._______  
        | .__________))______|  
        | | / /      ||  
        | |/ /       ||  
        | | /        ||.-''.
        | |/         |/  _  \\  
        | |          ||  `/,|  
        | |          (\\`_.')  
        | |         .-`--'.  
        | |        /Y . . Y\\  
        | |       // |   | \\\\  
        | |      //  | . |  \\\\  
        | |     ')   |   |   (`  
        | |          ||  
        | |         / | | \\  
        \"\"\"\"\"\"\"\"\"\"|_`-' `-' |\"\"\"|  
        |\"|\"\"\"\"\"\"\\ \\       '\"|\"|
        | |        \\ \\        | |  
        : :         \\ \\       : :  
        . .          `'       . .  
        """,
        """
         ___________.._______  
        | .__________))______|  
        | | / /      ||  
        | |/ /       ||  
        | | /        ||.-''.
        | |/         |/  _  \\  
        | |          ||  `/,|  
        | |          (\\`_.')  
        | |         .-`--'.  
        | |        /Y . . Y\\  
        | |       // |   | \\\\  
        | |      //  | . |  \\\\  
        | |     ')   |   |   (`  
        | |          ||'||  
        | |          || ||  
        | |          || ||  
        \"\"\"\"\"\"\"\"\"\"|_`-' `-' |\"\"\"|  
        |\"|\"\"\"\"\"\"\\ \\       '\"|\"|
        | |        \\ \\        | |  
        : :         \\ \\       : :  
        . .          `'       . .  
        """
    ]
    return hangman_stages[min(errors, len(hangman_stages) - 1)]


while displayed_word != parola:
    try:
        os.system("clear")
    except:
        pass
    print(greeting)
    print(parola)  
    print(get_hangman_stage(errori))
    displayed_word = ' '.join([letter if letter in letters else '_' for letter in parola])
    print(f"Parola: {displayed_word}")
    user_word = str(input("Inserisci la tua scelta: ")).lower()    
    if len(user_word) > 1:
        if user_word == parola:
            print("Hai indovinato!")
            break
        else:
            print(get_hangman_stage(errori))
            print("Parola errata!")
            errori += 1
    else:
        if user_word in parola:
            letters += user_word
            print("Lettera corretta!")
        else:
            print("Lettera errata!")
            errori += 1
    if errori >= 6:
        print(get_hangman_stage(6))
        print("\t\t\tHai perso!")
        print(f"La parola era: {parola}\n")
#        print("Sei un fallito!")
        exit(0)
    displayed_word = ''.join([letter if letter in letters else '' for letter in parola])
try:
    os.system("clear")
except:
    pass
print(winner_message)
print("Complimenti!!\n\nHai Vinto!!")
