alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def encrypt(messaggio, shift_n):
    msg_cifrato = ""
    for char in messaggio:
        if char in alfabeto:
            index1 = alfabeto.index(char)
            index2 = (index1 + shift_n) % len(alfabeto)
            msg_cifrato += alfabeto[index2]
        
        else:
            msg_cifrato += char
    print(f"Il messaggio cifrato è: {msg_cifrato}")

def decode(messaggio, shift_n):
    msg_decifrato = ""
    for char in messaggio:
        if char in alfabeto:
            index1 = alfabeto.index(char)
            index2 = (index1 - shift_n) % len(alfabeto)
            msg_decifrato += alfabeto[index2]
        else:
            msg_decifrato += char
    print(f"The decoded text is: {msg_decifrato}")

direction = input("Inserisci 1 per cifrare o 2 per decifrare:\n").lower()
text = input("Inserisci il messaggio:\n").lower()
shift = int(input("Inserisci il numero di shift:\n"))

if direction == "1":
    encrypt(messaggio=text, shift_n=shift)
elif direction == "2":
    decode(messaggio=text, shift_n=shift)
else:
    print("Input non valido. Inserisci 1 o 2.")
