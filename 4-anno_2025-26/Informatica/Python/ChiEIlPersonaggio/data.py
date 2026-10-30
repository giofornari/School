# data.py
# dati per il gioco

# lista di personaggi famosi
dati_personaggi = [
    {"nome": "Albert Einstein", "professione": "scienziato", "nazionalita": "tedesca", "epoca": "XX secolo", "genere": "maschio"},
    {"nome": "Leonardo da Vinci", "professione": "artista", "nazionalita": "italiana", "epoca": "XV secolo", "genere": "maschio"},
    {"nome": "Marie Curie", "professione": "scienziato", "nazionalita": "polacca", "epoca": "XX secolo", "genere": "femmina"},
    {"nome": "Napoleone Bonaparte", "professione": "politico", "nazionalita": "francese", "epoca": "XIX secolo", "genere": "maschio"},
    {"nome": "Frida Kahlo", "professione": "artista", "nazionalita": "messicana", "epoca": "XX secolo", "genere": "femmina"},
    {"nome": "Isaac Newton", "professione": "scienziato", "nazionalita": "britannica", "epoca": "XVII secolo", "genere": "maschio"},
    {"nome": "Cleopatra", "professione": "politico", "nazionalita": "egiziana", "epoca": "I secolo", "genere": "femmina"},
    {"nome": "Nikola Tesla", "professione": "scienziato", "nazionalita": "serba", "epoca": "XIX secolo", "genere": "maschio"},
    {"nome": "Coco Chanel", "professione": "artista", "nazionalita": "francese", "epoca": "XX secolo", "genere": "femmina"},
    {"nome": "Galileo Galilei", "professione": "scienziato", "nazionalita": "italiana", "epoca": "XVI secolo", "genere": "maschio"},
    # nuovi personaggi (estensione)
    {"nome": "Giulio Cesare", "professione": "politico", "nazionalita": "romana", "epoca": "I secolo a.C.", "genere": "maschio"},
    {"nome": "Vincent van Gogh", "professione": "artista", "nazionalita": "olandese", "epoca": "XIX secolo", "genere": "maschio"},
    {"nome": "Ada Lovelace", "professione": "scienziato", "nazionalita": "britannica", "epoca": "XIX secolo", "genere": "femmina"},
    {"nome": "Pablo Picasso", "professione": "artista", "nazionalita": "spagnola", "epoca": "XX secolo", "genere": "maschio"},
    {"nome": "Winston Churchill", "professione": "politico", "nazionalita": "britannica", "epoca": "XX secolo", "genere": "maschio"},
    {"nome": "William Shakespeare", "professione": "artista", "nazionalita": "britannica", "epoca": "XVI secolo", "genere": "maschio"},
]

# lista di domande disponibili
dati_domande = [
    {"testo": "È uno scienziato?", "attributo": "professione", "valore_atteso": "scienziato"},
    {"testo": "È un artista?", "attributo": "professione", "valore_atteso": "artista"},
    {"testo": "È un politico?", "attributo": "professione", "valore_atteso": "politico"},
    {"testo": "È italiano?", "attributo": "nazionalita", "valore_atteso": "italiana"},
    {"testo": "È francese?", "attributo": "nazionalita", "valore_atteso": "francese"},
    {"testo": "È tedesco?", "attributo": "nazionalita", "valore_atteso": "tedesca"},
    {"testo": "È britannico?", "attributo": "nazionalita", "valore_atteso": "britannica"},
    {"testo": "È spagnolo?", "attributo": "nazionalita", "valore_atteso": "spagnola"},
    {"testo": "È olandese?", "attributo": "nazionalita", "valore_atteso": "olandese"},
    {"testo": "È romano?", "attributo": "nazionalita", "valore_atteso": "romana"},
    {"testo": "È vissuto nel XX secolo?", "attributo": "epoca", "valore_atteso": "XX secolo"},
    {"testo": "È vissuto nel XIX secolo?", "attributo": "epoca", "valore_atteso": "XIX secolo"},
    {"testo": "È vissuto nel XVII secolo?", "attributo": "epoca", "valore_atteso": "XVII secolo"},
    {"testo": "È vissuto nel XVI secolo?", "attributo": "epoca", "valore_atteso": "XVI secolo"},
    {"testo": "È vissuto nel I secolo a.C.?", "attributo": "epoca", "valore_atteso": "I secolo a.C."},
    {"testo": "È di genere femminile?", "attributo": "genere", "valore_atteso": "femmina"},
]