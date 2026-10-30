def flip(d, a):
    if d == 'R':
        return sorted(a)
    elif d == 'L':
        return sorted(a, reverse=True)