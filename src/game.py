import pygame
import random

# Constantes
TAILLE_GRILLE = 6
TAILLE_CASE = 60
MARGE = 100
LARGEUR = TAILLE_GRILLE * TAILLE_CASE + 2 * MARGE
HAUTEUR = TAILLE_GRILLE * TAILLE_CASE + 2 * MARGE
NB_OBSTACLES = 7

# Couleurs
BLANC = (255, 255, 255)
GRIS = (198, 197, 195)
BLEU = (26, 45, 88)
BEIGE = (245, 208, 140)

# Représentation des pièces
PIECES = [
    {"coords": [(0, 0), (1, 0), (2, 0), (3, 0)], "angle": 0, "couleur": (148, 149, 153)},
    {"coords": [(0, 0), (1, 0), (2, 0), (1, 1)], "angle": 0, "couleur": (254, 242, 0)},
    {"coords": [(0, 0), (1, 0), (1, 1), (2, 1)], "angle": 0, "couleur": (223, 29, 63)},
    {"coords": [(0, 0), (1, 0), (2, 0), (2, 1)], "angle": 0, "couleur": (1, 174, 240)},
    {"coords": [(0, 0), (1, 0), (0, 1), (1, 1)], "angle": 0, "couleur": (64, 175, 73)},
    {"coords": [(0, 0), (1, 0), (1, 1)], "angle": 0, "couleur": (154, 37, 142)},
    {"coords": [(0, 0), (1, 0), (2, 0)], "angle": 0, "couleur": (247, 148, 29)},
    {"coords": [(0, 0), (1, 0)], "angle": 0, "couleur": (151, 89, 40)},
    {"coords": [(0, 0)], "angle": 0, "couleur": (35, 64, 142)}
]

def generer_obstacles():
    positions = set()
    while len(positions) < NB_OBSTACLES:
        x = random.randint(0, TAILLE_GRILLE - 1)
        y = random.randint(0, TAILLE_GRILLE - 1)
        positions.add((x, y))
    return list(positions)

def dessiner_grille(ecran, obstacles):
    ecran.fill(BLEU)
    font = pygame.font.Font(None, 36)
    font_titre = pygame.font.Font(None, 48)
    font_sous_titre = pygame.font.Font(None, 24)

    # Titre principal
    titre = font_titre.render("Genius Square Solver", True, BLANC)
    ecran.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, 10))

    # Sous-titre
    sous_titre = font_sous_titre.render("Appuyez sur 'R' pour réinitialiser", True, BLANC)
    ecran.blit(sous_titre, (LARGEUR // 2 - sous_titre.get_width() // 2, 500))


    for i in range(TAILLE_GRILLE):
        lettre = chr(65 + i)
        texte = font.render(lettre, True, BLANC)
        ecran.blit(texte, (MARGE + i * TAILLE_CASE + TAILLE_CASE // 2 - texte.get_width() // 2, MARGE - texte.get_height() - 10))

    for i in range(TAILLE_GRILLE):
        chiffre = str(i + 1)
        texte = font.render(chiffre, True, BLANC)
        ecran.blit(texte, (MARGE - texte.get_width() - 10, MARGE + i * TAILLE_CASE + TAILLE_CASE // 2 - texte.get_height() // 2))

    for i in range(TAILLE_GRILLE + 1):
        pygame.draw.line(ecran, GRIS, (MARGE, MARGE + i * TAILLE_CASE), (MARGE + TAILLE_GRILLE * TAILLE_CASE, MARGE + i * TAILLE_CASE), 2)
        pygame.draw.line(ecran, GRIS, (MARGE + i * TAILLE_CASE, MARGE), (MARGE + i * TAILLE_CASE, MARGE + TAILLE_GRILLE * TAILLE_CASE), 2)

    for (x, y) in obstacles:
        rect = pygame.Rect(MARGE + x * TAILLE_CASE + 5, MARGE + y * TAILLE_CASE + 5, TAILLE_CASE - 10, TAILLE_CASE - 10)
        pygame.draw.ellipse(ecran, BEIGE, rect)

def dessiner_pieces(ecran, pieces):
    for y in range(TAILLE_GRILLE):
        for x in range(TAILLE_GRILLE):
            if pieces[y][x] > 0:
                couleur = PIECES[pieces[y][x] - 1]["couleur"]
                rect = pygame.Rect(MARGE + x * TAILLE_CASE + 2, MARGE + y * TAILLE_CASE + 2, TAILLE_CASE - 4, TAILLE_CASE - 4)
                pygame.draw.rect(ecran, couleur, rect)

