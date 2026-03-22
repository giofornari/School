import random
from personaggio import Personaggio
from domanda import Domanda
from data import dati_personaggi, dati_domande

class Game:
    # costruttore classe
    def __init__(self):
        self.lista_personaggi = []
        self.lista_domande = []
        self.secrett = None
        self.numero_domanda = 0
        self.tentativi = 3 # max tentativi
        self.punteggio = 100 # punti base
        
        for d in dati_personaggi:
            p = Personaggio(d["nome"], d["professione"], d["nazionalita"], d["epoca"], d["genere"])
            self.lista_personaggi.append(p)
            
        for d in dati_domande:
            dom = Domanda(d["testo"], d["attributo"], d["valore_atteso"])
            self.lista_domande.append(dom)
            
    # sceglie casualmente
    def scegli_personaggio(self):
        self.secrett = random.choice(self.lista_personaggi)

    # mostra e seleziona
    def next_question(self):
        # penalizza ogni domanda
        if self.numero_domanda > 0:
            self.punteggio -= 5
            
        # indizio progressivo
        if self.numero_domanda == 5:
            print("indizio: è " + self.secrett.genere)
            
        scelte = random.sample(self.lista_domande, 3)
        print("scegli domanda (0 indovina):")
        
        i = 0
        while i < len(scelte):
            print(str(i + 1) + ". " + scelte[i].testo)
            i += 1
            
        s = int(input("> "))
        
        if s == 0:
            return None
        else:
            return scelte[s - 1]

    # controlla e stampa
    def check_answer(self, r, dom):
        esito = dom.controlla(self.secrett)
        
        if esito:
            print("risposta: sì")
        else:
            print("risposta: no")

    # tentativo finale
    def guess_personaggio(self):
        print("chi pensi sia? (tentativi: " + str(self.tentativi) + ")")
        n = input("> ")
        
        if n.lower() == self.secrett.nome.lower():
            print("esatto! hai indovinato!")
            print("punteggio finale: " + str(self.punteggio))
            return True
        else:
            self.tentativi -= 1
            self.punteggio -= 20
            print("errore!")
            if self.tentativi == 0:
                print("perso! era " + self.secrett.nome)
            return False

    # ciclo principale
    def play(self):
        print("benvenuto al gioco")
        self.scegli_personaggio()
        
        while self.tentativi > 0:
            dom = self.next_question()
            
            if dom == None:
                vinto = self.guess_personaggio()
                if vinto or self.tentativi == 0:
                    break
            else:
                self.check_answer("", dom)
                self.numero_domanda += 1