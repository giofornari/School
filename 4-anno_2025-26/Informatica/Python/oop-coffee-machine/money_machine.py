class MoneyMachine:
    CURR = "$"
    COINS = {"quarters": 0.25, "dimes": 0.10, "nickles": 0.05, "pennies": 0.01}

    def __init__(self):
        self.prof = 0
        self.recv = 0

    def report(self):
        print(f"Money: {self.CURR}{self.prof}")

    def process_coins(self):
        print("Please insert coins.")
        for c in self.COINS:
            self.recv += int(input(f"How many {c}?: ")) * self.COINS[c]
        return self.recv

    def make_payment(self, cost):
        self.process_coins()
        if self.recv >= cost:
            chg = round(self.recv - cost, 2)
            print(f"Here is {self.CURR}{chg} in change.")
            self.prof += cost
            self.recv = 0
            return True
        print("Sorry that's not enough money. Money refunded.")
        self.recv = 0
        return False
