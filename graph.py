"""
Module de chargement et représentation du graphe.
Gère la lecture des fichiers .txt et le stockage en mémoire.
"""


def load_graph(filepath):
    """
    Charge un graphe depuis un fichier .txt.

    Format attendu :
    Ligne 1 : nombre de sommets (n)
    Ligne 2 : nombre d'arcs (m)
    Lignes suivantes : <sommet_source> <sommet_dest> <valeur>

    Args:
        filepath (str): Chemin du fichier graphe

    Returns:
        tuple: (matrice d'adjacence, nombre de sommets)
               La matrice est de taille n×n avec float('inf') pour absence d'arc
               et 0 sur la diagonale
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Récupérer le nombre de sommets et d'arcs
        n = int(lines[0].strip())
        m = int(lines[1].strip())

        # Initialiser la matrice d'adjacence
        # INF pour absence d'arc, 0 sur la diagonale
        matrix = [[float('inf') if i != j else 0 for j in range(n)] for i in range(n)]

        # Remplir la matrice avec les arcs du fichier
        for i in range(2, 2 + m):
            if i < len(lines):
                parts = lines[i].strip().split()
                if len(parts) == 3:
                    source = int(parts[0])
                    dest = int(parts[1])
                    weight = int(parts[2])

                    # Vérifier la validité des indices
                    if 0 <= source < n and 0 <= dest < n:
                        matrix[source][dest] = weight

        return matrix, n

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filepath}' n'existe pas.")
        return None, 0
    except ValueError as e:
        print(f"Erreur de lecture du fichier : {e}")
        return None, 0


def get_available_graphs(graphs_dir="graphs"):
    """
    Liste les graphes disponibles dans le répertoire.

    Args:
        graphs_dir (str): Répertoire contenant les fichiers graphes

    Returns:
        list: Liste des fichiers graphes disponibles
    """
    import os
    graphs = []
    try:
        for filename in os.listdir(graphs_dir):
            if filename.endswith(".txt"):
                graphs.append((filename, os.path.join(graphs_dir, filename)))
    except FileNotFoundError:
        print(f"Erreur : Le répertoire '{graphs_dir}' n'existe pas.")

    return sorted(graphs)

