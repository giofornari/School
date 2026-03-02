import math

class Punto:
    def __init__(self, x=0.0, y=0.0):
        self.__x = x
        self.__y = y

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def distanza(self, p):
        return math.sqrt((self.__x - p.getX())**2 + (self.__y - p.getY())**2)

    def equals(self, p):
        return self.__x == p.getX() and self.__y == p.getY()

    def toString(self):
        return f"({self.__x}, {self.__y})"

class Triangolo:
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

    def setA(self, a):
        self.__a = a

    def setB(self, b):
        self.__b = b

    def setC(self, c):
        self.__c = c

    def getA(self):
        return self.__a

    def getB(self):
        return self.__b

    def getC(self):
        return self.__c

    def perimetro(self):
        ab = self.__a.distanza(self.__b)
        bc = self.__b.distanza(self.__c)
        ac = self.__a.distanza(self.__c)
        return ab + bc + ac

    def area(self):
        ab = self.__a.distanza(self.__b)
        bc = self.__b.distanza(self.__c)
        ac = self.__a.distanza(self.__c)
        p = self.perimetro() / 2
        return math.sqrt(p * (p - ab) * (p - bc) * (p - ac))

    def equals(self, t):
        return self.__a.equals(t.getA()) and self.__b.equals(t.getB()) and self.__c.equals(t.getC())

    def toString(self):
        return f"Triangolo({self.__a.toString()}, {self.__b.toString()}, {self.__c.toString()})"

p1 = Punto(0, 0)
p2 = Punto(3, 0)
p3 = Punto(0, 4)
t = Triangolo(p1, p2, p3)
print(f"Perimetro: {t.perimetro()}")
print(f"Area: {t.area()}")
print(t.toString())
