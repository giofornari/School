def alphabet_war(fight):
    left_side = {'w': 4, 'p': 3, 'b': 2, 's': 1}
    right_side = {'m': 4, 'q': 3, 'd': 2, 'z': 1}
    
    n = len(fight)
    destroyed = [False] * n
    
    for i in range(n):
        if fight[i] == '*':
            destroyed[i] = True
            if i > 0:
                destroyed[i-1] = True
            if i < n-1:
                destroyed[i+1] = True
    
    # Initialize scores
    left_score = 0
    right_score = 0
    
    for i in range(n):
        if not destroyed[i] and fight[i] != '*':
            letter = fight[i]
            if letter in left_side:
                left_score += left_side[letter]
            elif letter in right_side:
                right_score += right_side[letter]
    
    if left_score > right_score:
        return "Left side wins!"
    elif right_score > left_score:
        return "Right side wins!"
    else:
        return "Let's fight again!"
