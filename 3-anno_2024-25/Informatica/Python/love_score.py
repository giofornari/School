def calculate_love_score(your_name, their_name):
    score1 = 0
    score2 = 0
    for letter in your_name:
        if letter in "true love":
            score1 += 1
        
    for letter in their_name:
        if letter in "true love":
            score2 += 1
    return str(score1) + str(score2)

name1 = input("What is your name? \n --> ")
name2 = input("What is their name? \n --> ")

score = calculate_love_score(name1, name2)
print(f"Your love score is {score}")
