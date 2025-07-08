import pygame
import sys
import random

# Constantes
TAILLE_GRILLE = 6
TAILLE_CASE = 60
MARGE = 50
LARGEUR = TAILLE_GRILLE * TAILLE_CASE + 2 * MARGE
HAUTEUR = TAILLE_GRILLE * TAILLE_CASE + 2 * MARGE
NB_OBSTACLES = 7

# Représentation des pièces (coordonnées relatives)
PIECES = [
    {"coords": [(0, 0), (1, 0), (2, 0), (3, 0)], "angle": 0, "couleur": (148, 149, 153)},  # 4 carrés en ligne
    {"coords": [(0, 0), (1, 0), (2, 0), (1, 1)], "angle": 0, "couleur": (254, 242, 0)},    # 4 carrés en T
    {"coords": [(0, 0), (1, 0), (1, 1), (2, 1)], "angle": 0, "couleur": (223, 29, 63)},    # 4 carrés en Z
    {"coords": [(0, 0), (1, 0), (2, 0), (2, 1)], "angle": 0, "couleur": (1, 174, 240)},    # 4 carrés en L
    {"coords": [(0, 0), (1, 0), (0, 1), (1, 1)], "angle": 0, "couleur": (64, 175, 73)},    # 4 carrés en carré
    {"coords": [(0, 0), (1, 0), (1, 1)], "angle": 0, "couleur": (154, 37, 142)},           # 3 carrés en L
    {"coords": [(0, 0), (1, 0), (2, 0)], "angle": 0, "couleur": (247, 148, 29)},           # 3 carrés en ligne
    {"coords": [(0, 0), (1, 0)], "angle": 0, "couleur": (151, 89, 40)},                    # 2 carrés en ligne
    {"coords": [(0, 0)], "angle": 0, "couleur": (35, 64, 142)}                             # 1 carré
]

obstacles = []

# Initialisation de Pygame
pygame.init()
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Genius Square Solver")

# Couleurs
BLANC = (255, 255, 255)
GRIS = (198, 197, 195)
BLEU = (26, 45, 88)
BEIGE = (245, 208, 140)

def tourner_piece(piece):
    """Génère une rotation de 90° dans le sens horaire."""
    return [(-y, x) for x, y in piece]

def generer_rotations(piece):
    """Génère toutes les rotations possibles d'une pièce."""
    rotations = []
    coords = piece["coords"]
    for _ in range(4):  # 0°, 90°, 180°, 270°
        coords = tourner_piece(coords)
        rotations.append(coords)
    return rotations

def placer_piece(grille, piece, x, y, valeur):
    """Place ou retire une pièce sur la grille."""
    for dx, dy in piece:
        nx, ny = x + dx, y + dy
        grille[ny][nx] = valeur

    global obstacles
    dessiner_grille(obstacles)
    dessiner_pieces(grille)
    pygame.display.flip()
    pygame.time.delay(100)  # Pause pour visualiser le placement

def peut_placer_piece(grille, piece, x, y):
    """Vérifie si une pièce peut être placée à une position donnée."""
    for dx, dy in piece:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < TAILLE_GRILLE and 0 <= ny < TAILLE_GRILLE):
            return False  # Hors de la grille
        if grille[ny][nx] != 0:
            return False  # Case déjà occupée
    return True

def resoudre(grille, pieces, index):
    """Algorithme de backtracking pour placer toutes les pièces."""
    if index == len(pieces):
        return True  # Toutes les pièces ont été placées

    piece = pieces[index]
    rotations = generer_rotations(piece)
    for rotation in rotations:
        for y in range(TAILLE_GRILLE):
            for x in range(TAILLE_GRILLE):
                if peut_placer_piece(grille, rotation, x, y):
                    placer_piece(grille, rotation, x, y, index + 1)
                    if resoudre(grille, pieces, index + 1):
                        return True
                    placer_piece(grille, rotation, x, y, 0)  # Retirer la pièce
    return False

def trouver_solution(obstacles):
    """Trouve une solution pour placer les pièces."""
    grille = [[0] * TAILLE_GRILLE for _ in range(TAILLE_GRILLE)]
    for x, y in obstacles:
        grille[y][x] = -1  # Marquer les obstacles
    if resoudre(grille, PIECES, 0):
        print("Solution trouvée ! Appuyez sur 'R' pour réinitialiser.")
        return grille
    else:
        print("Aucune solution trouvée.")
        return None

def generer_obstacles():
    positions = set()
    while len(positions) < NB_OBSTACLES:
        x = random.randint(0, TAILLE_GRILLE - 1)
        y = random.randint(0, TAILLE_GRILLE - 1)
        positions.add((x, y))
    return list(positions)

def dessiner_grille(obstacles):
    ecran.fill(BLEU)
    font = pygame.font.Font(None, 36)  # Police par défaut, taille 36

    # Dessiner les lettres en haut
    for i in range(TAILLE_GRILLE):
        lettre = chr(65 + i)  # Convertit 0, 1, 2... en A, B, C...
        texte = font.render(lettre, True, BLANC)
        ecran.blit(texte, (MARGE + i * TAILLE_CASE + TAILLE_CASE // 2 - texte.get_width() // 2, MARGE // 2 - texte.get_height() // 2))

    # Dessiner les chiffres sur le côté gauche
    for i in range(TAILLE_GRILLE):
        chiffre = str(i + 1)
        texte = font.render(chiffre, True, BLANC)
        ecran.blit(texte, (MARGE // 2 - texte.get_width() // 2, MARGE + i * TAILLE_CASE + TAILLE_CASE // 2 - texte.get_height() // 2))

    # Grille
    for i in range(TAILLE_GRILLE + 1):
        pygame.draw.line(ecran, GRIS, (MARGE, MARGE + i * TAILLE_CASE), (MARGE + TAILLE_GRILLE * TAILLE_CASE, MARGE + i * TAILLE_CASE), 2)
        pygame.draw.line(ecran, GRIS, (MARGE + i * TAILLE_CASE, MARGE), (MARGE + i * TAILLE_CASE, MARGE + TAILLE_GRILLE * TAILLE_CASE), 2)

    # Obstacles
    for (x, y) in obstacles:
        rect = pygame.Rect(MARGE + x * TAILLE_CASE + 5, MARGE + y * TAILLE_CASE + 5, TAILLE_CASE - 10, TAILLE_CASE - 10)
        pygame.draw.ellipse(ecran, BEIGE, rect)

def dessiner_pieces(pieces):
    for y in range(TAILLE_GRILLE):
        for x in range(TAILLE_GRILLE):
            if pieces[y][x] > 0:  # Si une pièce est placée
                couleur = PIECES[pieces[y][x] - 1]["couleur"]
                rect = pygame.Rect(MARGE + x * TAILLE_CASE + 2, MARGE + y * TAILLE_CASE + 2, TAILLE_CASE - 4, TAILLE_CASE - 4)
                pygame.draw.rect(ecran, couleur, rect)

def main():
    global obstacles
    solution = None

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    obstacles = []
                    solution = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if len(obstacles) == NB_OBSTACLES:
                        print("Nombre maximum d'obstacles atteint.")
                        continue
                    x, y = event.pos
                    # Convertir les coordonnées de la souris en coordonnées de grille
                    grille_x = (x - MARGE) // TAILLE_CASE
                    grille_y = (y - MARGE) // TAILLE_CASE
                    if 0 <= grille_x < TAILLE_GRILLE and 0 <= grille_y < TAILLE_GRILLE:
                        obstacle = (grille_x, grille_y)
                        if obstacle not in obstacles:
                            obstacles.append(obstacle)  # Ajouter l'obstacle

        dessiner_grille(obstacles)

        if len(obstacles) == NB_OBSTACLES:
            if solution is None:
                solution = trouver_solution(obstacles)

            if solution:
                dessiner_pieces(solution)
            else:
                print("Aucune solution trouvée.")

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

