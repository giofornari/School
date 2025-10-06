def create_phone_number(n):
    bas = ['[', ']', ' ', ',']
    for b in bas:
        n = str(n).replace(b,"")
    return str("(" + n[0:3] + ") " + n[3:6] + "-" + n[6:])