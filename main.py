"""
Point d'entrée principal - Boucle principale et menu du programme.
Gère la sélection des graphes et l'affichage des résultats.
"""

import sys
import os
from graph import load_graph, get_available_graphs
from floyd import floyd_warshall, detect_negative_cycle, get_negative_cycles
from display import display_both_matrices, interactive_path_display


def clear_screen():
    """Nettoie l'écran (compatible avec Windows et Unix)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    """Affiche le menu principal."""
    print("\n" + "="*60)
    print("ALGORITHME DE FLOYD-WARSHALL - Théorie des Graphes (SM601)")
    print("="*60)
    print()


def select_graph():
    """
    Permet à l'utilisateur de sélectionner un graphe.

    Returns:
        tuple: (filepath du graphe, nom du graphe) ou (None, None) si annulé
    """
    graphs = get_available_graphs("graphs")

    if not graphs:
        print("Aucun graphe disponible dans le répertoire 'graphs/'.")
        return None, None

    print("Graphes disponibles :")
    for idx, (name, path) in enumerate(graphs, 1):
        print(f"  {idx}. {name}")
    print(f"  0. Quitter")
    print()

    while True:
        try:
            choice = int(input("Choisissez un graphe (numéro) : "))

            if choice == 0:
                return None, None
            elif 1 <= choice <= len(graphs):
                name, path = graphs[choice - 1]
                return path, name
            else:
                print(f"Erreur : Veuillez entrer un numéro entre 0 et {len(graphs)}.")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre entier.")


def analyze_graph(filepath, graph_name, log_file):
    """
    Analyse un graphe avec l'algorithme de Floyd-Warshall.

    Args:
        filepath (str): Chemin du fichier graphe
        graph_name (str): Nom du fichier graphe
        log_file: Fichier de log ouvert en écriture
    """
    print(f"\n{'='*60}")
    print(f"Chargement du graphe : {graph_name}")
    print(f"{'='*60}\n")

    # Charger le graphe
    matrix, n = load_graph(filepath)

    if matrix is None:
        print("Erreur lors du chargement du graphe.")
        return

    print(f"Graphe chargé : {n} sommets")

    # Exécuter l'algorithme de Floyd-Warshall
    print(f"\nExécution de l'algorithme de Floyd-Warshall...")
    L, P = floyd_warshall(matrix, n, display_both_matrices)

    # Afficher la matrice finale
    print(f"\n{'='*60}")
    print("RÉSULTAT FINAL")
    print(f"{'='*60}")
    display_both_matrices(L, P, n)

    # Détecter les circuits absorbants
    print(f"\n{'='*60}")
    print("VÉRIFICATION DES CIRCUITS ABSORBANTS")
    print(f"{'='*60}\n")

    has_negative_cycle = detect_negative_cycle(L, n)

    if has_negative_cycle:
        negative_vertices = get_negative_cycles(L, n)
        print(f"⚠️  AVERTISSEMENT : Un circuit absorbant (cycle négatif) a été détecté !")
        print(f"Sommets impliqués : {negative_vertices}")
        print(f"\nImpossible d'afficher les chemins minimaux.")
        return
    else:
        print("✓ Aucun circuit absorbant détecté.")
        print(f"\nLes chemins minimaux sont valides.\n")

    # Proposer l'affichage interactif des chemins
    interactive_path_display(L, P, n)


def main():
    """Boucle principale du programme."""

    # Créer le répertoire 'graphs' s'il n'existe pas
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
        print("Répertoire 'graphs/' créé. Veuillez y ajouter vos fichiers graphes (.txt).\n")

    # Ouvrir le fichier de log
    with open("traces.txt", "w", encoding="utf-8") as log_file:
        # Redirection vers le fichier de log (optionnel - pour trace complète)
        # Ici on utilise simplement l'affichage console

        while True:
            clear_screen()
            display_menu()

            filepath, graph_name = select_graph()

            if filepath is None:
                print("\nAu revoir !")
                break

            try:
                analyze_graph(filepath, graph_name, log_file)
            except Exception as e:
                print(f"\nErreur lors de l'analyse : {e}")

            # Pause avant de retourner au menu
            input("\nAppuyez sur Entrée pour revenir au menu...")


if __name__ == "__main__":
    main()

