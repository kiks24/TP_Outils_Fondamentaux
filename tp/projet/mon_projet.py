import time
import numpy as np
import matplotlib.pyplot as plt


# ========== OUTIL MATRICIEL : PIVOT DE GAUSS ===========


def resoudre(A, b, tolerance=1e-14):
    """Résout un système linéaire A * x = b par le pivot de Gauss avec pivot partiel."""
    n = len(A)
    M = []
    for i in range(n):
        ligne = []
        for j in range(len(A[i])):
            ligne.append(A[i][j])
        ligne.append(b[i])
        M.append(ligne)
        
    for k in range(n):
        meilleure = k
        valeur_max = abs(M[k][k])
        for i in range(k + 1, n):
            if abs(M[i][k]) > valeur_max:
                valeur_max = abs(M[i][k])
                meilleure = i
                
        if abs(M[meilleure][k]) <= tolerance:
            raise ValueError("systeme singulier ou mal pose")
            
        # Échange des lignes
        temp = M[k]
        M[k] = M[meilleure]
        M[meilleure] = temp
        
        # Élimination sous la diagonale
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] = M[i][j] - facteur * M[k][j]
                
    # Remontée
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        somme = M[i][n]
        for j in range(i + 1, n):
            somme = somme - M[i][j] * x[j]
        x[i] = somme / M[i][i]
        
    return x



# ========== RECHERCHE DE RACINES (POLYNOME DU PRET) ==========


def fonction_pret(t, capital, mensualite, nb_mois):
    """Polynôme financier reliant le capital, les mensualités et le taux."""
    if t <= 0:
        return capital / nb_mois - mensualite
    return capital * t * (1 + t)**nb_mois / ((1 + t)**nb_mois - 1) - mensualite

def derivee(f, x, h=1e-5):
    """Dérivée numérique centrée pour la méthode de Newton."""
    return (f(x + h) - f(x - h)) / (2 * h)

def taux_dichotomie(capital, mensualite, nb_mois, a=0.0, b=0.2, tolerance=1e-8, max_iter=100):
    """Méthode de la dichotomie (robuste)."""
    f = lambda t: fonction_pret(t, capital, mensualite, nb_mois)
    iterations = 0
    for _ in range(max_iter):
        iterations += 1
        milieu = (a + b) / 2
        if abs(f(milieu)) < tolerance:
            return milieu, iterations
        if f(a) * f(milieu) < 0:
            b = milieu
        else:
            a = milieu
    return (a + b) / 2, iterations

def taux_newton(capital, mensualite, nb_mois, x0=0.01, tolerance=1e-8, max_iter=50):
    """Méthode de Newton (rapide)."""
    f = lambda t: fonction_pret(t, capital, mensualite, nb_mois)
    x = x0
    iterations = 0
    for _ in range(max_iter):
        iterations += 1
        fx = f(x)
        if abs(fx) < tolerance:
            return x, iterations
        dfx = derivee(f, x)
        if abs(dfx) < 1e-12:
            break
        x_suivant = x - fx / dfx
        if abs(x_suivant - x) < tolerance:
            return x_suivant, iterations
        x = x_suivant
    return x, iterations



# ========== INTEGRATION NUMERIQUE (COUT DES INTERETS) ==========


def fonction_interet_continu(x, capital, taux_mensuel):
    """Modélise l'encours du capital au fil du temps (en mois)."""
    capital_restant = capital * (1 - x / 240)
    if capital_restant < 0:
         capital_restant = 0
    return capital_restant * taux_mensuel

def integration_trapezes(f, a, b, N, capital, taux_mensuel):
    """Calcule l'intégrale approchée par la méthode des trapèzes."""
    h = (b - a) / N
    somme = 0.5 * (f(a, capital, taux_mensuel) + f(b, capital, taux_mensuel))
    for i in range(1, N):
        x_i = a + i * h
        somme = somme + f(x_i, capital, taux_mensuel)
    return somme * h



# ========== SIMULATIONS ET TESTS ==========


print("=== PARTIE MATRICIELLE (SYSTEME LINEAIRE) ===")
# Un système simple pour répartir des fonds entre projets (ex: A * x = b)
A_mat = [[2, 1, 1], [1, 3, 2], [1, 0, 4]]
b_vec = [50000, 80000, 60000]
repartition = resoudre(A_mat, b_vec)
print("Répartition des investissements (Gauss maison) :", [round(v, 2) for v in repartition])

print("\n=== PARTIE FINANCIERE (TAUX DE PRET) ===")
capital_emprunte = 180000
mensualite_souhaitee = 1000
duree_mois = 240

taux_d, it_d = taux_dichotomie(capital_emprunte, mensualite_souhaitee, duree_mois)
taux_n, it_n = taux_newton(capital_emprunte, mensualite_souhaitee, duree_mois)

print(f"Dichotomie : Taux annuel = {taux_d * 12 * 100:.3f}% ({it_d} itérations)")
print(f"Newton     : Taux annuel = {taux_n * 12 * 100:.3f}% ({it_n} itérations)")

# Intégration des intérêts
cout_interets = integration_trapezes(fonction_interet_continu, 0, duree_mois, 100, capital_emprunte, taux_d)
print(f"Coût total estimé des intérêts (Trapèzes) : {cout_interets:.2f} €")



# =========== VISUALISATION GRAPHIQUE ==========


mensualites_test = range(900, 1500, 50)
iters_dich = []
iters_newt = []
for m in mensualites_test:
    _, id_ = taux_dichotomie(capital_emprunte, m, duree_mois)
    _, in_ = taux_newton(capital_emprunte, m, duree_mois)
    iters_dich.append(id_)
    iters_newt.append(in_)

plt.figure(figsize=(7, 4))
plt.plot(list(mensualites_test), iters_dich, label="Dichotomie", marker="o")
plt.plot(list(mensualites_test), iters_newt, label="Newton", marker="s")
plt.xlabel("Mensualité (€)")
plt.ylabel("Nombre d'itérations")
plt.title("Comparaison des performances des méthodes de recherche de racines")
plt.legend()
plt.grid(True)
plt.show()
