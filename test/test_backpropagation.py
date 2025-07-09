# python
import unittest
from src.solver import tourner_piece, normaliser, generer_rotations, peut_placer_piece, trouver_solution_backpropagation

class TestSolver(unittest.TestCase):
    def test_peut_placer_piece(self):
        grille = [[0] * 6 for _ in range(6)]
        piece = [(0, 0), (1, 0), (1, 1)]
        self.assertTrue(peut_placer_piece(grille, piece, 0, 0))
        self.assertFalse(peut_placer_piece(grille, piece, 5, 5))  # Hors de la grille

    def test_trouver_solution_backpropagation(self):
        obstacles = [(0, 3), (1, 4), (2, 3)]
        pieces = [{"coords": [(0, 0), (1, 0), (1, 1)]}, {"coords": [(0, 0), (0, 1), (1, 1)]}]
        solution = trouver_solution_backpropagation(obstacles, pieces)
        self.assertIsNotNone(solution)  # Vérifie qu'une solution est trouvée

    def test_trouver_solution_backpropagation_one_solution(self):
        obstacles = [(0, 3), (1, 3), (2, 4), (3, 3), (3, 5), (4, 4), (5, 3)]
        from src.game import PIECES
        solution = trouver_solution_backpropagation(obstacles, PIECES)
        self.assertIsNotNone(solution)

        obstacles = [(0, 3), (1, 4), (2, 3), (2, 5), (3, 4), (4, 3), (5, 3)]
        solution = trouver_solution_backpropagation(obstacles, PIECES)
        self.assertIsNotNone(solution)

if __name__ == "__main__":
    unittest.main()