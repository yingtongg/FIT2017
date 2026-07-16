import unittest
from unittest.mock import patch
# Import all functions from the target module
from src.user_input import (
    is_int,
    is_float,
    read_string,
    read_integer,
    read_float,
    read_integer_range,
    read_float_range,
    read_bool
)

# --- TEST SUITE (Adhering to the "one class" constraint) ---

class TestUserInputCoverage(unittest.TestCase):

    # =========================================================================
    # TESTS FOR is_int (Covers lines 16-17)
    # =========================================================================
    def test_is_int_valid(self):
        # Successful path (Line ~14)
        self.assertTrue(is_int("123"))

    def test_is_int_invalid_type(self):
        # Covers the except ValueError branch (Line ~16-17)
        self.assertFalse(is_int("hello"))

    # =========================================================================
    # TESTS FOR is_float (Covers lines 24-28)
    # =========================================================================
    def test_is_float_valid(self):
        # Successful path (Line ~24)
        self.assertTrue(is_float("12.34"))

    def test_is_float_invalid_type(self):
        # Covers the except ValueError branch (Line ~26-28)
        self.assertFalse(is_float("hello"))

    # =========================================================================
    # TESTS FOR read_string (Covers line 34)
    # =========================================================================
    @patch('builtins.input', return_value="test_input")
    def test_read_string(self, mock_input):
        # Line 34 is covered by simply calling and returning input()
        result = read_string("Prompt: ")
        self.assertEqual(result, "test_input")

    # =========================================================================
    # TESTS FOR read_integer (Covers lines 44-45)
    # Patched to simulate one invalid input followed by a valid one.
    # =========================================================================
    @patch('src.user_input.read_string', side_effect=["invalid", "5"])
    def test_read_integer_invalid_then_valid(self, mock_read_string):
        # Invalid input ("invalid") triggers the loop body (Lines 44-45) once.
        # The second input ("5") exits the loop and returns.
        result = read_integer("Prompt: ")
        self.assertEqual(result, 5)

    @patch('src.user_input.read_string', return_value="10")
    def test_read_integer_valid(self, mock_read_string):
        # Tests the successful path (no loop)
        result = read_integer("Prompt: ")
        self.assertEqual(result, 10)

    # =========================================================================
    # TESTS FOR read_float (Covers lines 53-57)
    # Patched to simulate one invalid input followed by a valid one.
    # =========================================================================
    @patch('src.user_input.read_string', side_effect=["invalid", "1.5"])
    def test_read_float_invalid_then_valid(self, mock_read_string):
        # Invalid input ("invalid") triggers the loop body (Lines 53-57) once.
        # The second input ("1.5") exits the loop and returns.
        result = read_float("Prompt: ")
        self.assertEqual(result, 1.5)

    # =========================================================================
    # TESTS FOR read_integer_range (Covers lines 75-79)
    # Patched to simulate out-of-range input followed by a valid one.
    # =========================================================================
    @patch('src.user_input.read_integer', side_effect=[0, 10, 5])
    def test_read_integer_range_low_then_high_then_valid(self, mock_read_integer):
        # 1. 0: num < min_val (Triggers loop: Line 75-77)
        # 2. 10: num > max_val (Triggers loop: Line 75-77)
        # 3. 5: Valid (Exits loop)
        result = read_integer_range("Prompt: ", 1, 8)
        self.assertEqual(result, 5)

    @patch('src.user_input.read_integer', return_value=4)
    def test_read_integer_range_valid_first_time(self, mock_read_integer):
        # Tests the successful path (no loop)
        result = read_integer_range("Prompt: ", 1, 8)
        self.assertEqual(result, 4)

    # =========================================================================
    # TESTS FOR read_float_range (Covers lines 86-90)
    # Patched to simulate out-of-range input followed by a valid one.
    # =========================================================================
    @patch('src.user_input.read_float', side_effect=[-1.0, 10.0, 5.5])
    def test_read_float_range_low_then_high_then_valid(self, mock_read_float):
        # 1. -1.0: num < min_val (Triggers loop: Lines 86-88)
        # 2. 10.0: num > max_val (Triggers loop: Lines 86-88)
        # 3. 5.5: Valid (Exits loop)
        result = read_float_range("Prompt: ", 1.0, 8.0)
        self.assertEqual(result, 5.5)

    # =========================================================================
    # TESTS FOR read_bool (Covers lines 97-99)
    # Patched to simulate invalid input followed by a valid one.
    # =========================================================================
    @patch('src.user_input.read_string', side_effect=["bad", "Y"])
    def test_read_bool_invalid_then_y(self, mock_read_string):
        # 1. "bad": Triggers the loop body (Line 97-99)
        # 2. "Y": Returns "y" after .lower()
        result = read_bool("Prompt: ")
        self.assertEqual(result, 'y')

    @patch('src.user_input.read_string', side_effect=["N"])
    def test_read_bool_n(self, mock_read_string):
        # Tests the 'n' path
        result = read_bool("Prompt: ")
        self.assertEqual(result, 'n')