"""
Module d'affichage des matrices et reconstruction des chemins minimaux.
"""


def display_matrix(L, P, n, matrix_type="L"):
    """
    Affiche une matrice avec formatage aligné.
    
    Args:
        L (list): Matrice à afficher (distances ou prédécesseurs)
        P (list): Matrice des prédécesseurs (pour contexte)
        n (int): Nombre de sommets
        matrix_type (str): Type de matrice ("L" pour distances, "P" pour prédécesseurs)
    """
    print(f"\nMatrice {matrix_type} (Distances minimales)" if matrix_type == "L" 
          else f"\nMatrice {matrix_type} (Prédécesseurs)")
    print()
    
    # Afficher les numéros des colonnes (sommets)
    header = "   "
    for j in range(n):
        header += str(j).rjust(5)
    print(header)
    
    # Afficher chaque ligne
    for i in range(n):
        # Numéro de la ligne (sommet)
        line = f"{i} ["
        
        for j in range(n):
            cell_value = L[i][j]
            
            # Formater la cellule en fonction de sa valeur
            if matrix_type == "L":
                if cell_value == float('inf'):
                    formatted = "INF"
                else:
                    formatted = str(int(cell_value))
            else:  # matrix_type == "P"
                if cell_value == -1:
                    formatted = "-1"
                else:
                    formatted = str(cell_value)
            
            # Aligner à droite dans une largeur de 5 caractères
            line += formatted.rjust(5)
        
        line += "]"
        print(line)
    print()


def display_both_matrices(L, P, n):
    """
    Affiche les matrices L et P côte à côte pour une meilleure visualisation.
    
    Args:
        L (list): Matrice des distances minimales
        P (list): Matrice des prédécesseurs
        n (int): Nombre de sommets
    """
    display_matrix(L, P, n, "L")
    display_matrix(P, L, n, "P")


def reconstruct_path(P, start, end, n):
    """
    Reconstruit le chemin minimal entre deux sommets.
    
    Args:
        P (list): Matrice des prédécesseurs
        start (int): Sommet de départ
        end (int): Sommet d'arrivée
        n (int): Nombre de sommets
        
    Returns:
        list: Liste des sommets formant le chemin, ou None si pas de chemin
    """
    # Vérifier si un chemin existe
    if P[start][end] == -1 and start != end:
        return None
    
    # Si c'est le même sommet
    if start == end:
        return [start]
    
    # Reconstruire le chemin en remontant via les prédécesseurs
    path = []
    current = end
    
    # Limite de sécurité pour éviter les boucles infinies
    max_iterations = n + 1
    iterations = 0
    
    while current != start and iterations < max_iterations:
        path.append(current)
        current = P[start][current]
        iterations += 1
    
    if iterations >= max_iterations:
        return None  # Chemin invalide
    
    path.append(start)
    path.reverse()
    
    return path


def display_path(L, P, start, end, n):
    """
    Affiche le chemin minimal entre deux sommets.
    
    Args:
        L (list): Matrice des distances minimales
        P (list): Matrice des prédécesseurs
        start (int): Sommet de départ
        end (int): Sommet d'arrivée
        n (int): Nombre de sommets
        
    Returns:
        bool: True si le chemin a été affiché, False sinon
    """
    # Vérifier les indices
    if start < 0 or start >= n or end < 0 or end >= n:
        print(f"Erreur : Indices invalides. Les sommets doivent être entre 0 et {n-1}.")
        return False
    
    # Vérifier si une distance existe
    distance = L[start][end]
    if distance == float('inf'):
        print(f"Pas de chemin entre {start} et {end}.")
        return False
    
    # Reconstruire le chemin
    path = reconstruct_path(P, start, end, n)
    
    if path is None:
        print(f"Erreur lors de la reconstruction du chemin entre {start} et {end}.")
        return False
    
    # Afficher le chemin
    path_str = " → ".join(str(v) for v in path)
    print(f"\nChemin de {start} à {end} : {path_str}")
    print(f"Valeur du chemin : {int(distance)}")
    
    return True


def interactive_path_display(L, P, n):
    """
    Boucle interactive pour afficher les chemins minimaux.
    
    Args:
        L (list): Matrice des distances minimales
        P (list): Matrice des prédécesseurs
        n (int): Nombre de sommets
    """
    while True:
        try:
            response = input("\nVoulez-vous afficher un chemin ? (o/n) : ").strip().lower()
            
            if response == 'n':
                break
            elif response == 'o':
                try:
                    start = int(input(f"Sommet de départ (0 à {n-1}) : "))
                    end = int(input(f"Sommet d'arrivée (0 à {n-1}) : "))
                    
                    display_path(L, P, start, end, n)
                    
                except ValueError:
                    print("Erreur : Veuillez entrer des nombres entiers.")
            else:
                print("Réponse non reconnue. Veuillez entrer 'o' ou 'n'.")
        
        except KeyboardInterrupt:
            print("\n")
            break

