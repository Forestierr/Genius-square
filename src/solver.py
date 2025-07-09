import pygame
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary, PULP_CBC_CMD

from src.game import PIECES, TAILLE_CASE, MARGE, dessiner_grille, dessiner_pieces

# Constantes
TAILLE_GRILLE = 6

def tourner_piece(piece):
    """Tourne une pièce de 90° dans le sens horaire, centrée autour de (0,0)."""
    return [(y, -x) for x, y in piece]

def normaliser(piece):
    """Recalcule les coordonnées pour que le coin supérieur gauche soit à (0,0)."""
    min_x = min(x for x, y in piece)
    min_y = min(y for x, y in piece)
    return [(x - min_x, y - min_y) for x, y in piece]

def symetrie_piece(piece):
    """Retourne la symétrie horizontale de la pièce par rapport à l'axe vertical passant par (0,0)."""
    return [(-x, y) for x, y in piece]

def generer_rotations(piece):
    """
    Génère toutes les rotations distinctes d'une pièce.
    """
    rotations = set()
    current = piece
    for _ in range(4):
        normalisee = tuple(sorted(normaliser(current)))
        rotations.add(normalisee)
        current = tourner_piece(current)

    return [list(rotation) for rotation in rotations]

def generer_rotations_et_symetries(piece):
    """
    Génère toutes les rotations et symétries distinctes d'une pièce.
    """
    formes = set()
    for base in (piece, symetrie_piece(piece)):
        current = base
        for _ in range(4):
            normalisee = tuple(sorted(normaliser(current)))
            formes.add(normalisee)
            current = tourner_piece(current)
    return [list(forme) for forme in formes]

# Algorithme de backtracking
def placer_piece(grille, piece, x, y, valeur):
    for dx, dy in piece:
        nx, ny = x + dx, y + dy
        grille[ny][nx] = valeur

def peut_placer_piece(grille, piece, x, y):
    for dx, dy in piece:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < TAILLE_GRILLE and 0 <= ny < TAILLE_GRILLE):
            return False
        if grille[ny][nx] != 0:
            return False
    return True

def resoudre(grille, pieces, index):
    if index == len(pieces):
        return True

    piece = pieces[index]["coords"]
    rotations = generer_rotations_et_symetries(piece)
    for rotation in rotations:
        for y in range(TAILLE_GRILLE):
            for x in range(TAILLE_GRILLE):
                if peut_placer_piece(grille, rotation, x, y):
                    placer_piece(grille, rotation, x, y, index + 1)
                    if resoudre(grille, pieces, index + 1):
                        return True
                    placer_piece(grille, rotation, x, y, 0)
    return False

def trouver_solution_backpropagation(obstacles, pieces):
    global iter
    grille = [[0] * TAILLE_GRILLE for _ in range(TAILLE_GRILLE)]
    for x, y in obstacles:
        grille[y][x] = -1
    if resoudre(grille, pieces, 0):
        return grille
    else:
        return None

# Algorithme linéaire
def get_valid_placements(grille, piece_index, piece_rotations):
    placements = []
    for shape in piece_rotations:
        max_dx = max(x for x, y in shape)
        max_dy = max(y for x, y in shape)
        for y in range(TAILLE_GRILLE - max_dy):
            for x in range(TAILLE_GRILLE - max_dx):
                if all(0 <= x+dx < TAILLE_GRILLE and 0 <= y+dy < TAILLE_GRILLE and grille[y+dy][x+dx] == 0
                       for dx, dy in shape):
                    placements.append(((x, y), shape))
    return placements

def get_valid_placements_for_piece(grille, piece_index):
    """
    Génère toutes les positions valides pour une pièce donnée sur la grille.

    Args:
        grille: La grille de jeu (2D list) avec 0 = case libre, -1 = obstacle
        piece_index: L'index de la pièce dans PIECES

    Returns:
        List de tuples ((x, y), shape) représentant position et forme de la pièce
    """
    piece = PIECES[piece_index]["coords"]
    rotations = generer_rotations_et_symetries(piece)

    placements = []

    for shape in rotations:
        # Pour chaque position possible sur la grille
        for start_y in range(TAILLE_GRILLE):
            for start_x in range(TAILLE_GRILLE):
                # Vérifier si la pièce peut être placée à cette position
                can_place = True

                for dx, dy in shape:
                    new_x = start_x + dx
                    new_y = start_y + dy

                    # Vérifier les limites de la grille
                    if not (0 <= new_x < TAILLE_GRILLE and 0 <= new_y < TAILLE_GRILLE):
                        can_place = False
                        break

                    # Vérifier que la case n'est pas occupée ou un obstacle
                    if grille[new_y][new_x] != 0:
                        can_place = False
                        break

                if can_place:
                    placements.append(((start_x, start_y), shape))

    return placements

def solveur_lineaire(grille, pieces):
    model = LpProblem("GeniusSquareSolver", LpMinimize)

    variables = {}
    placement_data = {}

    # Génération des variables et contraintes pour chaque pièce
    for i, piece in enumerate(pieces):
        vars_for_piece = []
        rotations = generer_rotations_et_symetries(piece["coords"])
        valid_placements = get_valid_placements(grille, i, rotations)
        placement_data[i] = valid_placements

        # Vérifier qu'il y a au moins un placement valide pour cette pièce
        if not valid_placements:
            print(f"Aucun placement valide trouvé pour la pièce {i}")
            return None

        for idx, ((x, y), shape) in enumerate(valid_placements):
            var = LpVariable(f"x_{i}_{idx}", 0, 1, LpBinary)
            variables[(i, idx)] = var
            vars_for_piece.append(var)

        # Contrainte : exactement une position par pièce
        model += lpSum(vars_for_piece) == 1

    # Contrainte : chaque case libre doit être couverte exactement une fois
    for y in range(TAILLE_GRILLE):
        for x in range(TAILLE_GRILLE):
            if grille[y][x] == 0:  # Case libre
                recouvrements = []
                for i, data in placement_data.items():
                    for idx, ((ox, oy), shape) in enumerate(data):
                        # Vérifier si cette variable couvre la case (x, y)
                        if (x, y) in [(ox + dx, oy + dy) for dx, dy in shape]:
                            recouvrements.append(variables[(i, idx)])

                # Chaque case libre doit être couverte exactement une fois
                if recouvrements:  # S'assurer qu'il y a au moins une variable
                    model += lpSum(recouvrements) == 1
                else:
                    print(f"Aucune pièce ne peut couvrir la case ({x}, {y})")
                    return None

    # Fonction objectif (minimiser - peut être n'importe quoi)
    model += 0

    # Résolution
    result = model.solve(PULP_CBC_CMD(msg=False))

    if result != 1:  # 1 = LpStatusOptimal
        print(f"Résolution échouée. Statut: {result}")
        return None

    # Construction de la solution
    solution = [[-1 if grille[y][x] == -1 else 0 for x in range(TAILLE_GRILLE)] for y in range(TAILLE_GRILLE)]

    for (i, idx), var in variables.items():
        if var.varValue == 1:
            (ox, oy), shape = placement_data[i][idx]
            for dx, dy in shape:
                x, y = ox + dx, oy + dy
                solution[y][x] = i + 1

    return solution

def trouver_solution_lineaire(obstacles, pieces):
    grille = [[0] * TAILLE_GRILLE for _ in range(TAILLE_GRILLE)]
    for x, y in obstacles:
        grille[y][x] = -1
    return solveur_lineaire(grille, pieces)


