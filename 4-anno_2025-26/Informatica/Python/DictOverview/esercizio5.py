books = [
    {"title": "1984", "author": "Orwell", "year": 1949},
    {"title": "Dune", "author": "Herbert", "year": 1965},
    {"title": "Foundation", "author": "Asimov", "year": 1951}
]
for book in books:
    print(book["title"])
for book in books:
    if book["year"] < 1960:
        print(book)
titolo = input("Inserisci il titolo del libro da cercare: ")
trovato = None
for book in books:
    if book["title"].lower() == titolo.lower():
        trovato = book
        break
if trovato:
    print(f"Autore: {trovato['author']}")
else:
    print("Libro non trovato.")

