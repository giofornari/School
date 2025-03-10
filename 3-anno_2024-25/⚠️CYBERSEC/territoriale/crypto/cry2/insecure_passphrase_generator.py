import os
import string
import random


words = [
    "casa", "albero", "notte", "sole", "montagna", "fiume", "mare", "vento", "nuvola", 
    "pioggia", "strada", "amico", "sorriso", "viaggio", "tempo", "cuore", "stella", 
    "sogno", "giorno", "libro", "porta", "luce", "ombra", "silenzio", "fiore", "luna"
]

passphrase = []

##

def reverse_passphrase(passphrase_str):
    words_dict = {
        "casa": 0, "albero": 1, "notte": 2, "sole": 3, "montagna": 4, "fiume": 5, "mare": 6, "vento": 7, "nuvola": 8,
        "pioggia": 9, "strada": 10, "amico": 11, "sorriso": 12, "viaggio": 13, "tempo": 14, "cuore": 15, "stella": 16,
        "sogno": 17, "giorno": 18, "libro": 19, "porta": 20, "luce": 21, "ombra": 22, "silenzio": 23, "fiore": 24, "luna": 25
    }
    
    passphrase_list = passphrase_str.split('-')
    reversed_flag = ""
    for word in passphrase_list:
        if word in words_dict:
            reversed_flag += chr(words_dict[word] + ord('a'))
        elif word.isdigit():
            reversed_flag += str(words.index(word))
        else:
            reversed_flag += word
    return reversed_flag

with open("passphrase.txt", 'r') as rf:
    passphrase_str = rf.read()
    print(reverse_passphrase(passphrase_str))
