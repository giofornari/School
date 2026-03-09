with open("input.txt", "r") as file:
    lines = file.readlines()

voti = []
dicto = {}

for line in lines:
    nome, voto = line.strip().split()
    voto = int(voto)
    voti.append(voto)
    
    if voto not in dicto:
        dicto[voto] = []
    dicto[voto].append(nome)

media = sum(voti) / len(voti)

max_v = max(voti)

max_vs = dicto[max_v]

print(f"Media dei voti: {media:.2f}")
print(f"Voto più alto: {max_v}")
print("Studenti con il voto più alto:", ", ".join(max_vs))
print("Dizionario studenti per voto:", dicto)
