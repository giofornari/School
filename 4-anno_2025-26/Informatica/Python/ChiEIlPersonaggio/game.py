import random
from personaggio import Personaggio
from domanda import Domanda
from data import dati_personaggi, dati_domande

class Game:
    # inizializza il gioco
    def __init__(self):
        # lista vuota personaggi
        self.lista_personaggi = []
        # lista vuota domande
        self.lista_domande = []
        # personaggio da indovinare
        self.personaggio_segreto = None
        # contatore delle domande
        self.numero_domanda = 0
        
        # carica i personaggi
        for d in dati_personaggi:
            # crea oggetto personaggio
            p = Personaggio(d["nome"], d["professione"], d["nazionalita"], d["epoca"], d["genere"])
            # aggiungi alla lista
            self.lista_personaggi.append(p)
            
        # carica le domande
        for d in dati_domande:
            # crea oggetto domanda
            dom = Domanda(d["testo"], d["attributo"], d["valore_atteso"])
            # aggiungi alla lista
            self.lista_domande.append(dom)
            
    # scegli personaggio casuale
    def scegli_personaggio(self):
        # usa modulo random
        self.personaggio_segreto = random.choice(self.lista_personaggi)

    # mostra menu domande
    def next_question(self):
        # scegli 3 domande
        domande_scelte = random.sample(self.lista_domande, 3)
        # stampa istruzioni
        print("scegli una domanda (0 per indovinare):")
        
        # indice per ciclo
        i = 0
        # stampa le opzioni
        while i < len(domande_scelte):
            # stampa numero e testo
            print(str(i + 1) + ". " + domande_scelte[i].testo)
            # incrementa indice
            i += 1
            
        # input dell'utente
        scelta = int(input("> "))
        
        # se sceglie zero
        if scelta == 0:
            return None
        else:
            # ritorna domanda scelta
            return domande_scelte[scelta - 1]

    # controlla la domanda
    def check_answer(self, risposta, domanda):
        # usa metodo controlla
        esito = domanda.controlla(self.personaggio_segreto)
        
        # stampa la risposta
        if esito == True:
            print("risposta: sì")
        else:
            print("risposta: no")

    # utente prova indovinare
    def guess_personaggio(self):
        # stampa la domanda
        print("chi pensi che sia?")
        # prendi input utente
        nome = input("> ")
        
        # controlla se uguale
        if nome.lower() == self.personaggio_segreto.nome.lower():
            # indovinato
            print("corretto! hai indovinato il personaggio!")
        else:
            # sbagliato
            print("sbagliato! era " + self.personaggio_segreto.nome)

    # avvia il gioco
    def play(self):
        # stampa benvenuto
        print("benvenuto al gioco \"chi è il personaggio?\"")
        # stampa messaggio
        print("ho scelto un personaggio segreto. cerca di indovinare chi è!")
        
        # scegli il personaggio
        self.scegli_personaggio()
        
        # ciclo di gioco
        while True:
            # prendi la domanda
            domanda = self.next_question()
            
            # controlla se indovina
            if domanda == None:
                # chiama guess
                self.guess_personaggio()
                # termina il ciclo
                break
            else:
                # controlla e rispondi
                self.check_answer("", domanda)
                # incrementa contatore
                self.numero_domanda += 1