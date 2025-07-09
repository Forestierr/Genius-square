import unittest
from src.solver import *
from src.game import PIECES

class TestSolver(unittest.TestCase):
	def test_tourner_piece(self):
		piece = PIECES[0]["coords"]
		exepected = [(0, 0), (0, -1), (0, -2), (0, -3)]
		self.assertEqual(tourner_piece(piece), exepected)

		piece = PIECES[1]["coords"]
		expected = [(0, 0), (0, -1), (0, -2), (1, -1)]
		self.assertEqual(tourner_piece(piece), expected)

		piece = PIECES[1]["coords"]
		expected = [(0, 0), (-1, 0), (-2, 0), (-1, -1)]
		piece = tourner_piece(tourner_piece(piece))
		self.assertEqual(piece, expected)

		piece = PIECES[8]["coords"]
		expected = [(0, 0)]
		self.assertEqual(tourner_piece(piece), expected)


	def test_normaliser(self):
		piece = PIECES[0]["coords"]
		expected = [(0, 3), (0, 2), (0, 1), (0, 0)]
		self.assertEqual(normaliser(tourner_piece(piece)), expected)

		piece = PIECES[1]["coords"]
		expected = [(0, 2), (0, 1), (0, 0), (1, 1)]
		self.assertEqual(normaliser(tourner_piece(piece)), expected)

		# Piece 1 est une forme en T, on teste la rotation deux fois
		piece = PIECES[1]["coords"]
		expected = [(2, 1), (1, 1), (0, 1), (1, 0)]
		piece = tourner_piece(tourner_piece(piece))
		self.assertEqual(normaliser(piece), expected)

		# Piece 1 test la rotation 4 fois
		piece = PIECES[1]["coords"]
		expected = [(0, 0), (1, 0), (2, 0), (1, 1)]
		piece = tourner_piece(tourner_piece(tourner_piece(tourner_piece(piece))))
		self.assertEqual(normaliser(piece), expected)

		piece = PIECES[2]["coords"]
		expected = [(0, 2), (0, 1), (1, 1), (1, 0)]
		piece = tourner_piece(piece)
		self.assertEqual(normaliser(piece), expected)

		piece = PIECES[8]["coords"]
		expected = [(0, 0)]
		self.assertEqual(normaliser(tourner_piece(piece)), expected)


	def test_generer_rotations(self):
		piece = PIECES[0]["coords"]
		rotations = generer_rotations(piece)
		expected = [
			[(0, 0), (0, 1), (0, 2), (0, 3)],
			[(0, 0), (1, 0), (2, 0), (3, 0)]
		]
		for rotation in rotations:
			self.assertIn(rotation, expected)

		piece = PIECES[1]["coords"]
		rotations = generer_rotations(piece)
		expected = [
			[(0, 0), (0, 1), (0, 2), (1, 1)],
			[(0, 1), (1, 0), (1, 1), (1, 2)],
			[(0, 0), (1, 0), (1, 1), (2, 0)],
			[(0, 1), (1, 0), (1, 1), (2, 1)]
		]
		self.assertEqual(len(rotations), len(expected))
		for rotation in rotations:
			self.assertIn(rotation, expected)

		piece = PIECES[2]["coords"]
		rotations = generer_rotations(piece)
		expected = [
			[(0, 0), (1, 0), (1, 1), (2, 1)],
			[(0, 1), (0, 2), (1, 0), (1, 1)]
		]
		self.assertEqual(len(rotations), len(expected))
		for rotation in rotations:
			self.assertIn(rotation, expected)

		piece = PIECES[8]["coords"]
		rotations = generer_rotations(piece)
		expected = [
			[(0, 0)]
		]
		self.assertEqual(len(rotations), len(expected))
		for rotation in rotations:
			self.assertIn(rotation, expected)

	def test_generer_rotations_et_symetries(self):
		piece = PIECES[0]["coords"]
		expected = [
			[(0, 0), (0, 1), (0, 2), (0, 3)],
			[(0, 0), (1, 0), (2, 0), (3, 0)]
		]
		rotations = generer_rotations_et_symetries(piece)
		self.assertEqual(len(rotations), len(expected))
		for rotation in rotations:
			self.assertIn(rotation, expected)

		piece = PIECES[1]["coords"]
		expected = [
			[(0, 0), (0, 1), (0, 2), (1, 1)],
			[(0, 1), (1, 0), (1, 1), (1, 2)],
			[(0, 0), (1, 0), (1, 1), (2, 0)],
			[(0, 1), (1, 0), (1, 1), (2, 1)]
		]
		rotations = generer_rotations_et_symetries(piece)
		self.assertEqual(len(rotations), len(expected))
		for rotation in rotations:
			self.assertIn(rotation, expected)

		piece = PIECES[2]["coords"]
		expected = [
			[(0, 0), (1, 0), (1, 1), (2, 1)],
			[(0, 1), (0, 2), (1, 0), (1, 1)],
			[(0, 0), (0, 1), (1, 1), (1, 2)],
			[(0, 1), (1, 0), (1, 1), (2, 0)]
		]
		rotations = generer_rotations_et_symetries(piece)
		self.assertEqual(len(rotations), len(expected))
		for rotation in rotations:
			self.assertIn(rotation, expected)

		piece = PIECES[8]["coords"]
		expected = [
			[(0, 0)]
		]
		rotations = generer_rotations_et_symetries(piece)
		self.assertEqual(len(rotations), len(expected))
		for rotation in rotations:
			self.assertIn(rotation, expected)

	def test_difficulte(self):
		from src.game import Difficulte
		self.assertEqual(Difficulte.get_diff(0), Difficulte.WIZARD)
		self.assertEqual(Difficulte.get_diff(1), Difficulte.MASTER)
		self.assertEqual(Difficulte.get_diff(2), Difficulte.EXPERT)
		self.assertEqual(Difficulte.get_diff(3), Difficulte.JUNIOR)
		self.assertEqual(Difficulte.get_diff(4), Difficulte.STARTER)
		self.assertEqual(Difficulte.get_diff(5), Difficulte.STARTER)

	def test_verifier_placement_diff(self):
		grille = [[0] * 7 for _ in range(7)]
		piece = PIECES[7]["coords"]
		# Placer la pièce dans la grille
		for x, y in piece:
			grille[x][y] = 8

		piece = PIECES[8]["coords"]

		self.assertTrue(verifier_placement_diff(grille, piece, 8, 1, 1, 4))

		self.assertFalse(verifier_placement_diff(grille, piece, 8, 1, 1, 3))
		self.assertTrue(verifier_placement_diff(grille, piece, 8, 2, 1, 3))
		self.assertTrue(verifier_placement_diff(grille, piece, 8, 1, 2, 3))
