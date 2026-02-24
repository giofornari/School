from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

m = Menu()
cm = CoffeeMaker()
mm = MoneyMachine()

on = True

while on:
    opts = m.get_items()
    c = input(f"What would you like? ({opts}): ")
    if c == "off":
        on = False
    elif c == "report":
        cm.report()
        mm.report()
    else:
        d = m.find_drink(c)
        if d:
            if cm.is_resource_sufficient(d):
                if mm.make_payment(d.cost):
                    cm.make_coffee(d)
