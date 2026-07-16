'''Author: Charlotte Pierce
For FIT2107.
'''

import unittest

from src.calculator import Calculator


class TestCalculator(unittest.TestCase):
    '''Tests for the calculator class.'''
    def setUp(self):
        '''Set up a calculator to use in the tests.'''
        self.calc = Calculator()

    def test_initial_answer(self):
        '''Test that the initial answer starts at 0.'''
        self.assertEqual(0, self.calc.get_answer())

    def test_add_one(self):
        '''Test a basic addition calculation.'''
        self.calc.add(1)
        self.assertEqual(1, self.calc.get_answer())
