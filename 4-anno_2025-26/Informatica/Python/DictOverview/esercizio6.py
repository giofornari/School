rubrica = {}
while True:
    print("\n1. Aggiungi contatto\n2. Cerca numero\n3. Visualizza tutti\n4. Esci")
    scelta = input("Scegli un'opzione: ")
    if scelta == "1":
        nome = input("Nome: ")
        numero = input("Numero: ")
        rubrica[nome] = numero
    elif scelta == "2":
        nome = input("Nome da cercare: ")
        if nome in rubrica:
            print(f"Numero di {nome}: {rubrica[nome]}")
        else:
            print("Contatto non trovato.")
    elif scelta == "3":
        for nome, numero in rubrica.items():
            print(f"{nome}: {numero}")
    elif scelta == "4":
        break
    else:
        print("Scelta non valida.")
