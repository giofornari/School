class Domanda:
    # costruttore della classe
    def __init__(self, testo, attributo, valore_atteso):
        # assegna il testo
        self.testo = testo
        # assegna l'attributo
        self.attributo = attributo
        # assegna valore atteso
        self.valore_atteso = valore_atteso

    # controlla la risposta
    def controlla(self, personaggio):
        # variabile per valore
        valore = ""
        
        # controlla attributo professione
        if self.attributo == "professione":
            valore = personaggio.professione
        # controlla attributo nazionalita
        elif self.attributo == "nazionalita":
            valore = personaggio.nazionalita
        # controlla attributo epoca
        elif self.attributo == "epoca":
            valore = personaggio.epoca
        # controlla attributo genere
        elif self.attributo == "genere":
            valore = personaggio.genere
            
        # verifica se coincidono
        if valore == self.valore_atteso:
            return True
        else:
            return False