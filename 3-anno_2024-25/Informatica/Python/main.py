from blackjack import *


while True:
    aclear()
    play_game()
    play_again = input("\nVuoi giocare ancora? Digita 's' per sì, qualsiasi altro tasto per uscire: ").lower()
    if play_again != 's':
        print("Grazie per aver giocato!")
        break