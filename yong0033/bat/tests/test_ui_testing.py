# tests/test_ui_testing.py
# pylint: disable=protected-access,missing-class-docstring,missing-module-docstring

import unittest
from unittest import mock
from src import user_input
from src.bat_ui import BatUI


class TestMainMenu(unittest.TestCase):
    def setUp(self):
        """Start fresh on MAIN MENU for each test."""
        self.bat_ui = BatUI(data_manager=None)

    # --------------------------
    # Choices 1 to 6 (valid routes)
    # --------------------------
    @mock.patch("src.user_input.read_integer_range", return_value=1)
    def test_choice_1_routes_to_loan_item(self, _read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "LOAN ITEM")

    @mock.patch("src.user_input.read_integer_range", return_value=2)
    def test_choice_2_routes_to_return_item(self, _read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "RETURN ITEM")

    @mock.patch("src.user_input.read_integer_range", return_value=3)
    def test_choice_3_routes_to_search_for_patron(self, _read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "SEARCH FOR PATRON")

    @mock.patch("src.user_input.read_integer_range", return_value=4)
    def test_choice_4_routes_to_register_patron(self, _read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "REGISTER PATRON")

    @mock.patch("src.user_input.read_integer_range", return_value=5)
    def test_choice_5_routes_to_access_makerspace(self, _read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "ACCESS MAKERSPACE")

    @mock.patch("src.user_input.read_integer_range", return_value=6)
    def test_choice_6_routes_to_quit(self, _read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "QUIT")

    # -------------------------------------------------
    # Invalid choices at the SAME (UI) level:
    # Patch read_integer_range with out-of-range numbers and
    # verify we remain on MAIN MENU (no navigation).
    # -------------------------------------------------
    @mock.patch("src.user_input.read_integer_range", return_value=0)  # too low
    def test_invalid_choice_low_stays_on_main_menu(self, _read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "MAIN MENU")

    @mock.patch("src.user_input.read_integer_range", return_value=9)  # too high
    def test_invalid_choice_high_stays_on_main_menu(self, _read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "MAIN MENU")

    @mock.patch("src.user_input.read_integer_range", return_value=2)
    def test_reprompts_is_handled_by_helper_and_routes(self, mock_read):
        self.bat_ui.run_current_screen()
        self.assertEqual(self.bat_ui.get_current_screen(), "RETURN ITEM")


    @mock.patch("builtins.input", side_effect=["0", "9", "2"])
    def test_read_integer_range_reprompts_until_valid(self, mock_in):
        val = user_input.read_integer_range("Choice: ", 1, 6)
        self.assertEqual(val, 2)          # returns the first valid entry


    @mock.patch("builtins.input", side_effect=["0", "9", "2"])
    def test_read_integer_range_reprompts_until_valid2(self, mock_in):
        val2 = user_input.read_integer_range("Choice: ", 1, 6)
        self.assertEqual(mock_in.call_count, 3)  # 2 invalid + 1 valid
