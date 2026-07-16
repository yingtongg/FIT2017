import unittest
from unittest import mock

import src.number_guess as number_guess

class TestNumberGuess(unittest.TestCase):
    @mock.patch('builtins.input')
    def test_get_guess_in_range(self, inp):
        inp.return_value = '5'
        self.assertEqual(5, number_guess.get_guess())

    @mock.patch('builtins.input')
    def test_get_guess_first_out_of_range(self, inp):
        inp.side_effect = ['188', '5']
        self.assertEqual(5, number_guess.get_guess())

    def test_guess_too_high_is_too_high(self):
        self.assertTrue(number_guess.guess_too_high(87, 50))

    def test_guess_too_high_is_not_too_high(self):
        self.assertFalse(number_guess.guess_too_high(43, 50))

    def test_guess_too_low_is_too_low(self):
        self.assertTrue(number_guess.guess_too_low(43, 50))

    def test_guess_too_low_is_not_too_low(self):
        self.assertFalse(number_guess.guess_too_low(66, 50))

    def test_guess_correct_is_correct(self):
        self.assertTrue(number_guess.guess_correct(50, 50))

    def test_guess_correct_is_not_correct(self):
        self.assertFalse(number_guess.guess_correct(51, 50))

    @mock.patch('random.randint')
    def test_select_answer(self, rint):
        rint.return_value = 50
        self.assertEqual(50, number_guess.select_answer())

    @mock.patch('builtins.input')
    @mock.patch('random.randint')
    def test_two_normal_games(self, rint, inp):
        inp.side_effect = ['51', '49', '50', 'y', '51', '49', '50', 'n']
        rint.return_value = 50
        number_guess.play_game()
        self.assertTrue(True)

    @mock.patch('builtins.input')
    @mock.patch('random.randint')
    def test_too_many_guesses(self, rint, inp):
        inp.side_effect = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'n']
        rint.return_value = 50
        number_guess.play_game()
        self.assertTrue(True)