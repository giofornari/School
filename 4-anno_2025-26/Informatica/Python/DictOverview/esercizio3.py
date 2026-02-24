grades = {
    "math": 8,
    "italian": 7,
    "history": 6,
    "english": 9
}
print(list(grades.keys()))
print(list(grades.values()))
for subject, grade in grades.items():
    print(f"{subject}: {grade}")
print(sum(grades.values()) / len(grades))
