#Exercice 1.1

n = 2026
d = 7
q = n // d
r = n % d
print(f"Le quotient: {q} et le reste: {r}")
print(f"Vérification: 289 * 7 + 3 = {289 * 7 + 3}")

#Exercice 1.2

nb = 123456789
print(nb % 12345678)
print(nb // 10)

#Exercice 2.1

n = 0
for i in range(1000):
    n += 0.1
print(n)
print(n - 100)

#Exercice 2.2

def presque_egaux(a, b, tolerance=1e-9):
    return abs(a-b) <= tolerance

presque_egaux(0.1 + 0.2, 0.3)

#Exercice 3.1

print("La table de multiplication de 7:")
for i in range(1,11):
    print(f"7 x {i} = {7 * i}")

#Exercice 3.2

somme = 0
for i in range(1,101):
    somme += i
print(f"La somme des entiers de 1 à 100 donne: {somme}")
print( 100 * (100 + 1) // 2)

#Exercice 4.1

def nombre_de_chiffres(n):
    compteur = 1
    while (n >= 10):
        n = n // 10
        compteur += 1
    return compteur

print(nombre_de_chiffres(245))
print(nombre_de_chiffres(2029))
print(nombre_de_chiffres(0))

#Exercice 5.1

import math

def heron(a):
    x = 1
    tours = 0
    if a < 0:
        raise ValueError("Pas de racine carrée pour un nombre négatif")
    elif a == 0:
        return 0
        
    while True:
        tours += 1
        y = (x + a/x) / 2
        if abs(y - x) < 1e-12:
            return y
        x = y
        
print(f"Résultat de la méthode Héron: {heron(2)}")
print(f"Résultat de la méthode math.sqrt(): {math.sqrt(2)}")
print(f"Ecart entre les méthodes: {abs(heron(2) - math.sqrt(2))} < 1e-12")

#Exercice 6.1

def vers_binaire(n):
    rep = ""
    if n == 0:
        return 0
    while n != 0:
        if (n % 2) == 1:
            rep = "1" + rep
        else:
            rep = "0" + rep
        n = n // 2
    return rep
    
print(vers_binaire(37))
print(vers_binaire(0))

#Exercice 6.2

import sys

eps = 1.0
while ((1.0 + eps / 2) != 1.0):
    eps = eps / 2
print(eps)
sys.float_info.epsilon

#Exercice 7.1

import math

def racines_naif(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        raise ValueError("Pas de solution réelle")
    else:
        r = math.sqrt(delta)
        return (- b - r) / (2 * a), (- b + r) / (2 * a)

petite_racine, grande_racine = (racines_naif(1, -1e8, 1))
print(f"Petite racine: {petite_racine}, grande racine: {grande_racine}")
print(f"Produit des racines: {petite_racine * grande_racine}")

#Exercice 7.2

import math 

def racines(a, b , c):
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        raise ValueError("Pas de solution réelle")
    else:
        r = math.sqrt(delta)
        x = (- b + r) / (2 * a)
        return c / (a * x), x

petite_racine, grande_racine = (racines(1, -1e8, 1))
print(f"Petite racine: {petite_racine}, grande racine: {grande_racine}")
print(f"Produit des racines: {petite_racine * grande_racine}")

#Exercice 7.3

from fractions import Fraction

n = Fraction(0)
for i in range(1000):
   n += Fraction(1, 10)
    
print(n)
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))





