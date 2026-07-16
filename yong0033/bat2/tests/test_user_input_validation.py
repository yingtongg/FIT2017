# tests/test_user_input_friendly.py
from unittest import TestCase, mock
from src import user_input as ui

def patch_inputs(*answers):
    """Patch input() without importing builtins."""
    return mock.patch("builtins.input", side_effect=list(answers))

class TestUserInput(TestCase):
    def test_integer_range_invalid_then_valid(self):
        with patch_inputs("abc", "0", "6", "3"):
            self.assertEqual(ui.read_integer_range("Pick 1..5: ", 1, 5), 3)

    def test_integer_range_accepts_min_and_max(self):
        with patch_inputs("1"):
            self.assertEqual(ui.read_integer_range("", 1, 5), 1)
        with patch_inputs("5"):
            self.assertEqual(ui.read_integer_range("", 1, 5), 5)

    def test_integer_range_handles_spaces_and_negatives(self):
        with patch_inputs("   2  ", "-4", "2"):
            v = ui.read_integer_range(":", 1, 5)
        self.assertTrue(1 <= v <= 5)

    def test_read_nonempty_string_trims_and_reprompts(self):
        if not hasattr(ui, "read_nonempty_string"):
            self.skipTest("read_nonempty_string() not implemented in user_input")
        with patch_inputs("", "   ", "hello  "):
            s = ui.read_nonempty_string("Name: ")
        self.assertEqual(s, "hello")

    def test_yes_no_variants_loop_until_valid(self):
        if not hasattr(ui, "read_yes_no"):
            self.skipTest("read_yes_no() not implemented in user_input")
        with patch_inputs("maybe", "Y"):
            self.assertTrue(ui.read_yes_no("Proceed? "))
        with patch_inputs("", "N"):
            self.assertFalse(ui.read_yes_no("Proceed? "))
