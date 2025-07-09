import pygame
import sys
import time

from solver import trouver_solution_backpropagation, trouver_solution_lineaire
from game import dessiner_grille, dessiner_pieces, PIECES, NB_OBSTACLES, TAILLE_GRILLE, TAILLE_CASE, MARGE, Difficulte

# Initialisation de Pygame
pygame.init()
ecran = pygame.display.set_mode((TAILLE_GRILLE * TAILLE_CASE + 2 * MARGE, TAILLE_GRILLE * TAILLE_CASE + 2 * MARGE))
pygame.display.set_caption("Genius Square Solver")

def main():
    global obstacles, diff
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
                    # Vérifier si le joueur veut changer la difficulté
                    if event.pos[0] > TAILLE_GRILLE * TAILLE_CASE + MARGE:
                        x, y = event.pos
                        # Positions centrales Y des boutons (haut = y - 15) : 0:126 / 1:166 / 2:206 / 3:246 / 4:286
                        # Hauteur des boutons : 30 pixels
                        boutons_y = [111, 151, 191, 231, 271]
                        hauteur_bouton = 30

                        # Vérifier quel bouton a été cliqué
                        bouton_clique = -1
                        for i, bouton_y in enumerate(boutons_y):
                            if bouton_y <= y <= bouton_y + hauteur_bouton:
                                bouton_clique = i
                                break

                        if bouton_clique != -1:
                            diff = Difficulte.get_diff(bouton_clique)
                            print(f"Difficulté changée à {diff.name}, niveau {diff.value}")
                            obstacles = []
                            solution = None

                    if len(obstacles) == NB_OBSTACLES:
                        print("Nombre maximum d'obstacles atteint.")
                        continue
                    x, y = event.pos
                    grille_x = (x - MARGE) // TAILLE_CASE
                    grille_y = (y - MARGE) // TAILLE_CASE
                    if 0 <= grille_x < TAILLE_GRILLE and 0 <= grille_y < TAILLE_GRILLE:
                        obstacle = (grille_x, grille_y)
                        if obstacle not in obstacles:
                            obstacles.append(obstacle)

        dessiner_grille(ecran, obstacles, diff)

        if len(obstacles) == NB_OBSTACLES:
            if solution is None:
                start_time = time.time()

                # Changer la méthode de résolution ici
                solution = trouver_solution_backpropagation(obstacles, PIECES, diff.value)
                # solution = trouver_solution_lineaire(obstacles, PIECES)

                print(f"Temps de résolution : {time.time() - start_time:.3f} secondes")

            if solution:
                dessiner_pieces(ecran, solution)
            else:
                print("Aucune solution trouvée.")

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    obstacles = []
    diff = Difficulte.STARTER
    main()

