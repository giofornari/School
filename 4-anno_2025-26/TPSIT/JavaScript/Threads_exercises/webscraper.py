from bs4 import BeautifulSoup

import threading
from requests import get   # libreria per richieste http e gestione di sessione con cookies

search_word = input("Che cosa vuoi cercare nei websites: ")
num = 0
urls = []
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()] # leggo tutti gli url da file (+500)

def scrape(url): # funzione distribuita sui thread
    global num
    try:
        resp = get(url, timeout=5) # gettiamo il sito (si, sono lenti...)
        #print(f"{url} - {resp.status_code}") # status code per aura
        
        if resp.status_code == 200: # necessario altrimenti bestemmie
            soup = BeautifulSoup(resp.content, 'html.parser')  # parser fondamentali per understanding dei tag
            page_text = soup.get_text() #ottenngo un estratto
            
            if search_word.lower() in page_text.lower(): # cerco la tua parola nel testo 
                print(f"\n'{search_word}' trovato in {url}") # te lo mostro
                num += 1                
                            
    except Exception: # gestisco l'errore ignorandolo
        pass

listadellaspesa = []

for url in urls:
    t = threading.Thread(target=scrape, args=[url])
    listadellaspesa.append(t)
    t.start()

for t in listadellaspesa:
    t.join()

print(f"\ntrovato {num} volte, per dio") if num != 0 else print("404 - not found")



















"""
ATTENZIONE! ⚠️
Nessuna divinità è stata chiamata in causa: “per Dio!” è solo un’antica interiezione nobile, 
usata per dare forza e solennità alle emozioni — un elegante “accidenti!” d’altri tempi, 
con un tocco teatrale e zero peccati linguistici.
"""