# Student name: Ong Ying Tong
# Student ID:34477306

import unittest
from src.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()   # fresh calculator for each test

    def test_initial_answer(self):
        self.assertEqual(0, self.calc.get_answer())

    def test_add(self):
        calc = Calculator()
        calc.add(5)
        self.assertEqual(5, calc.get_answer())
        calc.add(3)
        self.assertEqual(8, calc.get_answer())

    def test_add_negative(self):
        calc = Calculator()
        calc.add(-4)
        self.assertEqual(-4, calc.get_answer())
        calc.add(-6)
        self.assertEqual(-10, calc.get_answer())

    def test_subtract_positive(self):
        calc = Calculator()
        calc.add(10)
        calc.subtract(3)   # 10 - 3
        self.assertEqual(7, calc.get_answer())

    def test_subtract_negative(self):
        calc = Calculator()
        calc.add(5)
        calc.subtract(-4)  # 5 - (-4) = 9
        self.assertEqual(9, calc.get_answer())

    def test_multiply_positive(self):
        calc = Calculator()
        calc.add(3)
        calc.multiply(4)   # 3 * 4
        self.assertEqual(12, calc.get_answer())

    def test_multiply_negative(self):
        calc = Calculator()
        calc.add(3)
        calc.multiply(-2)  # 3 * -2
        self.assertEqual(-6, calc.get_answer())

    def test_divide_positive(self):
        calc = Calculator()
        calc.add(12)
        calc.divide(3)     # 12 / 3
        self.assertEqual(4, calc.get_answer())

    def test_divide_negative(self):
        calc = Calculator()
        calc.add(12)
        calc.divide(-3)    # 12 / -3
        self.assertEqual(-4, calc.get_answer())

    def test_divide_by_zero(self):
        calc = Calculator()
        calc.add(5)
        with self.assertRaises(ZeroDivisionError):
            calc.divide(0)

    # -------------------------
    # Method chaining tests
    # -------------------------
    def test_method_chaining_add_and_subtract(self):
        calc = Calculator()
        result = calc.add(10).subtract(5).add(-3).get_answer()
        # (((0 + 10) - 5) + (-3)) = 2
        self.assertEqual(2, result)

    def test_method_chaining_multiply(self):
        calc = Calculator()
        result = calc.add(2).multiply(3).multiply(-2).get_answer()
        # (((0 + 2) * 3) * -2) = -12
        self.assertEqual(-12, result)

    def test_method_chaining_divide(self):
        calc = Calculator()
        result = calc.add(20).divide(2).divide(-5).get_answer()
        # (((0 + 20) / 2) / -5) = -2
        self.assertEqual(-2, result)

    def test_method_chaining_all_operations(self):
        calc = Calculator()
        result = calc.add(10).subtract(3).add(-2).multiply(-2).divide(5).get_answer()
        # ((((0+10) - 3) + (-2)) * -2) / 5 = -2
        self.assertEqual(-2, result)
