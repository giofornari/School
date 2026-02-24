import random
from nazioni import countries as nazioni

print("Benvenuto al quiz sulle nazioni! Rispondi correttamente il più a lungo possibile.")
punti = 0
try:
    while True:
        paese = random.choice(nazioni)
        campo = random.choice(["capital", "continent"])  # capitale o continente
        if campo == "capital":
            corretta = paese["capital"]
            tutte = [p["capital"] for p in nazioni]
            domanda = f"Qual è la capitale di {paese['name']}?"
        else:
            corretta = paese["continent"]
            tutte = [p["continent"] for p in nazioni]
            domanda = f"A quale continente appartiene {paese['name']}?"

        # costruisco le opzioni
        pool = list({v for v in tutte if v != corretta})
        if len(pool) >= 3:
            sbagliate = random.sample(pool, 3)
        else:
            sbagliate = []
            while len(sbagliate) < 3:
                c = random.choice(tutte)
                if c != corretta:
                    sbagliate.append(c)

        scelte = sbagliate + [corretta]
        random.shuffle(scelte)
        indice_corretta = scelte.index(corretta)

        print()
        print(domanda)
        for i, op in enumerate(scelte, start=1):
            print(f"  {i}. {op}")

        # input valido
        num = None
        while True:
            try:
                risposta = input("La tua risposta (1-4): ")
            except (EOFError, KeyboardInterrupt):
                raise
            risposta = risposta.strip()
            if not risposta:
                print("Inserisci un numero.")
                continue
            if not risposta.isdigit():
                print("Inserisci un numero.")
                continue
            num = int(risposta)
            if not 1 <= num <= len(scelte):
                print(f"Scegli un numero tra 1 e {len(scelte)}.")
                continue
            break

        if (num - 1) == indice_corretta:
            punti += 1
            print(f"Giusto! Punteggio: {punti}")
        else:
            print(f"Sbagliato! La risposta corretta era: {scelte[indice_corretta]}")
            break

except (EOFError, KeyboardInterrupt):
    print("\nGioco interrotto dall'utente.")
finally:
    print(f"Punteggio finale: {punti}")
