rubrica = {}
while True:
    print("1 - add person, 2 - search number, 3 - show all, 4 - exit")
    sceltaa = input("scegli: ")

    match sceltaa:
        case '1':
            nome = input("nome: ")
            numero = input("num = ")
            rubrica[nome] = numero
        case '2':
            cerca = input("persona to search: ")
            print(f"numero cercato: {rubrica.get(cerca) if rubrica.get(cerca) else 'Non trovato'}")
        case '3':
            for nome, numero in rubrica.items():
                print(f"{nome}: {numero}")
        case '4':
            break