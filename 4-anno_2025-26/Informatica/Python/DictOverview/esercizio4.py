
parola = input("Inserisci una parola: ")
conteggio = {}
for lettera in parola:
    if lettera in conteggio:
        conteggio[lettera] += 1
    else:
        conteggio[lettera] = 1
print(conteggio)
