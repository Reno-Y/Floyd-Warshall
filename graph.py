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
    Trie les graphes numériquement (graph1, graph2, ..., graph10, graph11)
    et non alphabétiquement (graph1, graph10, graph11, graph2, ...).

    Args:
        graphs_dir (str): Répertoire contenant les fichiers graphes

    Returns:
        list: Liste des fichiers graphes disponibles triés numériquement
    """
    import os
    import re

    graphs = []
    try:
        for filename in os.listdir(graphs_dir):
            if filename.endswith(".txt"):
                graphs.append((filename, os.path.join(graphs_dir, filename)))
    except FileNotFoundError:
        print(f"Erreur : Le répertoire '{graphs_dir}' n'existe pas.")

    # Trier numériquement : extraire le numéro du graphe
    def extract_graph_number(item):
        filename = item[0]
        # Extraire le numéro après "graph" et avant ".txt"
        match = re.search(r'graph(\d+)', filename)
        if match:
            return int(match.group(1))
        return float('inf')  # Mettre les fichiers sans numéro à la fin

    return sorted(graphs, key=extract_graph_number)


def list_graphs_direct():
    """
    Liste les graphes disponibles directement avec affichage formaté.
    Utile pour déboguer les problèmes de tri et de disponibilité.

    Returns:
        list: Liste des graphes triés numériquement
    """
    import os
    import re

    graphs_dir = "graphs"
    graphs = []

    for filename in os.listdir(graphs_dir):
        if filename.endswith(".txt"):
            graphs.append((filename, os.path.join(graphs_dir, filename)))

    def extract_graph_number(item):
        filename = item[0]
        match = re.search(r'graph(\d+)', filename)
        if match:
            return int(match.group(1))
        return float('inf')

    sorted_graphs = sorted(graphs, key=extract_graph_number)

    print(f"\nTotal : {len(sorted_graphs)} graphes\n")
    print("Graphes disponibles :")
    for i, (name, path) in enumerate(sorted_graphs):
        print(f"  {i+1}. {name}")

    return sorted_graphs


def display_available_graphs(graphs_dir="graphs"):
    """
    Affiche la liste des graphes disponibles de manière formatée.

    Args:
        graphs_dir (str): Répertoire contenant les fichiers graphes
    """
    graphs = get_available_graphs(graphs_dir)

    if not graphs:
        print("Aucun graphe disponible dans le répertoire 'graphs/'.")
        return

    print("\n" + "="*60)
    print("GRAPHES DISPONIBLES")
    print("="*60)

    for idx, (name, _) in enumerate(graphs, 1):
        print(f"  {idx}. {name}")

    print("="*60 + "\n")
