school = {
    "Luca": {"math": 8, "english": 7},
    "Anna": {"math": 9, "english": 8},
    "Marco": {"math": 6, "english": 7}
}
print(school["Anna"])
print(school["Marco"]["math"])
for studente, voti in school.items():
    media = sum(voti.values()) / len(voti)
    print(f"{studente}: media {media}")
best = max(school.items(), key=lambda item: sum(item[1].values()) / len(item[1]))
best_media = sum(best[1].values()) / len(best[1])
print(f"Studente con media più alta: {best[0]} ({best_media})")
