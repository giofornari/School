class MenuItem:
    def __init__(self, n, w, m, c, p):
        self.name = n
        self.cost = p
        self.ingredients = {"water": w, "milk": m, "coffee": c}

class Menu:
    def __init__(self):
        self.menu = [
            MenuItem("latte", 200, 150, 24, 2.5),
            MenuItem("espresso", 50, 0, 18, 1.5),
            MenuItem("cappuccino", 250, 50, 24, 3),
        ]

    def get_items(self):
        o = ""
        for i in self.menu:
            o += f"{i.name}/"
        return o

    def find_drink(self, n):
        for i in self.menu:
            if i.name == n:
                return i
        print("Sorry that item is not available.")
