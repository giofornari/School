def find_pin(n, try_pin):
    baseline = [9] * n
    result_baseline = try_pin(baseline)
    T = 9 * n - result_baseline
    
    pin = [None] * n

    for i in range(n - 1):
        guess = [9] * n
        guess[i] = 0
        R = try_pin(guess)
        pin[i] = (R - 9 * (n - 1) + T) // 2

    pin[n - 1] = T - sum(pin[:-1])

    try_pin(pin)