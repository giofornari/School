import random
import os
import time

def aclear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pesca():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    
    return sum(cards)

def compare(user_score, computer_score):
    if user_score == computer_score:
        return "Pareggio! 🙃"
    elif computer_score == 0:
        return "Hai perso! Il computer ha un Blackjack! 😱"
    elif user_score == 0:
        return "Hai vinto! Hai un Blackjack! 😎"
    elif user_score > 21:
        return "Hai perso! Hai superato 21! 😭"
    elif computer_score > 21:
        return "Hai vinto! Il computer ha superato 21! 🥳"
    elif user_score > computer_score:
        return "Hai vinto! 😁"
    else:
        return "Hai perso! 😤"





def play_game():
    print("\nBenvenuto a Blackjack'! \a \a \a \a \a \a \a \a \a \a 🎮")
    user_cards = []
    computer_cards = []
    game_over = False
    
    for _ in range(2):
        user_cards.append(pesca())
        computer_cards.append(pesca())
    
    while not game_over:
        user_score = score(user_cards)
        computer_score = score(computer_cards)
        
        print(f"\nLe tue carte: {user_cards}, punteggio attuale: {user_score}")
        print(f"Prima carta del computer: {computer_cards[0]}")
        
        if user_score == 0 or computer_score == 0 or user_score > 21:
            game_over = True
        else:
            draw_another = input("Digita 's' per pescare un'altra carta, 'n' per passare: ").lower()
            if draw_another == 's':
                user_cards.append(pesca())
            else:
                game_over = True
    
    while computer_score != 0 and computer_score < 17:
        computer_cards.append(pesca())
        computer_score = score(computer_cards)
    
    print(f"\nLa tua mano finale: {user_cards}, punteggio finale: {user_score}")
    print(f"Mano finale del computer: {computer_cards}, punteggio finale: {computer_score}")
    print(compare(user_score, computer_score))