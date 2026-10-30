class Domanda:
    # inizializza istanza
    def __init__(self, txt, attr, val):
        self.testo = txt
        self.attributo = attr
        self.valore_atteso = val

    # verifica attributo
    def controlla(self, p):
        v = ""
        
        if self.attributo == "professione":
            v = p.professione
        elif self.attributo == "nazionalita":
            v = p.nazionalita
        elif self.attributo == "epoca":
            v = p.epoca
        elif self.attributo == "genere":
            v = p.genere
            
        if v == self.valore_atteso:
            return True
        else:
            return False