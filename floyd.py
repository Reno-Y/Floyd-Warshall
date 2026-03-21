"""
Module d'implémentation de l'algorithme Floyd-Warshall.
Calcule les chemins de valeurs minimales entre tous les couples de sommets.
"""


def floyd_warshall(matrix, n, display_func=None):
    """
    Algorithme de Floyd-Warshall pour trouver les chemins minimaux.

    Args:
        matrix (list): Matrice d'adjacence du graphe
        n (int): Nombre de sommets
        display_func (callable): Fonction pour afficher les matrices (optionnel)

    Returns:
        tuple: (matrice L des distances minimales, matrice P des prédécesseurs)
    """

    # Initialiser la matrice L (distances minimales)
    # Copie profonde de la matrice d'adjacence
    L = [row[:] for row in matrix]

    # Initialiser la matrice P (prédécesseurs)
    # P[i][j] = -1 si pas de chemin direct, sinon i (sommet source)
    P = [[-1 if matrix[i][j] == float('inf') or i == j else i for j in range(n)] for i in range(n)]

    # Afficher l'état initial
    if display_func:
        print(f"\n{'='*60}")
        print("ÉTAT INITIAL (k = -1)")
        print(f"{'='*60}")
        display_func(L, P, n)

    # Itérations de l'algorithme (k = 0 à n-1)
    for k in range(n):
        print(f"\n{'='*60}")
        print(f"ITÉRATION k = {k}")
        print(f"{'='*60}")

        # Pour chaque paire de sommets (i, j)
        for i in range(n):
            for j in range(n):
                # Calculer le chemin via le sommet intermédiaire k
                new_distance = L[i][k] + L[k][j]

                # Si ce chemin est plus court, le mettre à jour
                if new_distance < L[i][j]:
                    L[i][j] = new_distance
                    # Mettre à jour le prédécesseur
                    P[i][j] = P[k][j]

        # Afficher l'état après cette itération
        if display_func:
            display_func(L, P, n)

    return L, P


def detect_negative_cycle(L, n):
    """
    Détecte la présence d'un circuit absorbant (cycle de poids négatif).

    Args:
        L (list): Matrice des distances minimales
        n (int): Nombre de sommets

    Returns:
        bool: True si un circuit absorbant est détecté, False sinon
    """
    for i in range(n):
        if L[i][i] < 0:
            return True
    return False


def get_negative_cycles(L, n):
    """
    Récupère la liste des sommets impliqués dans des circuits absorbants.

    Args:
        L (list): Matrice des distances minimales
        n (int): Nombre de sommets

    Returns:
        list: Liste des indices des sommets avec circuits absorbants
    """
    cycles = []
    for i in range(n):
        if L[i][i] < 0:
            cycles.append(i)
    return cycles

