import random
import os

greeting = """
Benvenuto in Impiccato!
Il gioco consiste nel cercare di indovinare una parola
indovinando lettere una alla volta.
Se credi di sapere la parola, puoi anche scriverla interamente.
Buon divertimento!
"""
with open("parole.txt", "r") as f:
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
        print("Hai perso!")
        print(f"La parola era: {parola}\n")
#        print("Sei un fallito!")
        break
    displayed_word.replace((' ', '') for " " in letters)

