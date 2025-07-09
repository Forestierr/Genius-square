# python
import unittest
from src.solver import generer_rotations, get_valid_placements_for_piece, trouver_solution_lineaire

class TestLinearSolver(unittest.TestCase):
    def test_get_valid_placements_for_piece(self):
        grille = [[0] * 6 for _ in range(6)]
        grille[0][3] = -1  # Ajouter un obstacle
        piece_index = 0
        placements = get_valid_placements_for_piece(grille, piece_index)
        self.assertGreater(len(placements), 0)  # Vérifie qu'il y a des placements valides
        for placement in placements:
            (x, y), shape = placement
            for dx, dy in shape:
                self.assertTrue(0 <= x + dx < 6 and 0 <= y + dy < 6)  # Vérifie les limites de la grille
                self.assertNotEqual(grille[y + dy][x + dx], -1)  # Vérifie qu'il n'y a pas d'obstacle

    def test_trouver_solution_lineaire(self):
        # Test with 1 solution grid
        obstacles = [(0, 3), (1, 3), (2, 4), (3, 3), (3, 5), (4, 4), (5, 3)]
        from src.game import PIECES
        solution = trouver_solution_lineaire(obstacles, PIECES)
        self.assertIsNotNone(solution)

        obstacles = [(0, 3), (1, 4), (2, 3), (2, 5), (3, 4), (4, 3), (5, 3)]
        solution = trouver_solution_lineaire(obstacles, PIECES)
        self.assertIsNotNone(solution)

        obstacles = [(0, 2), (0, 4), (1, 3), (2, 4), (3, 4), (4, 5), (5, 3)]
        solution = trouver_solution_lineaire(obstacles, PIECES)
        self.assertIsNotNone(solution)

if __name__ == "__main__":
    unittest.main()