def persistence(n):
    a = 0
    while n >= 10:
        a +=1
        b=1
        for c in str(n):
            b *= int(c)
        n = b
    return a