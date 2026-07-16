import unittest
from unittest.mock import patch, MagicMock
from src.bat_ui import BatUI
import sys

# Mock Item: Needs _id, _name, _type, _year (used in _loan_item)
class MockItem:
    def __init__(self, i_id=1, name="Tool", item_type="T", year=2020):
        self._id = i_id
        self._name = name
        self._type = item_type
        self._year = year

# Mock Loan: Needs _item (which points to a MockItem with _id)
class MockLoan:
    def __init__(self, item_id, item_name="Tool"):
        self._item = MockItem(item_id, name=item_name)

    # Needs a __str__ method as it's printed in _return_item
    def __str__(self):
        return f"Mock Loan for {self._item._name} ID {self._item._id}"

# Mock Patron: Needs _id, _name, _age, _outstanding_fees, _makerspace_training, _loans
class MockPatron:
    def __init__(self, p_id=1, name="Test Patron", age=30, fees=0.0, makerspace_training=False, loans=None):
        self._id = p_id
        self._name = name
        self._age = age
        self._outstanding_fees = fees
        self._makerspace_training = makerspace_training
        self._loans = loans if loans is not None else []

    # Needs a __str__ method as it's printed in _search_for_patron
    def __str__(self):
        return f"Patron {self._name}, ID {self._id}"


class TestBatUI(unittest.TestCase):

    def setUp(self):
        # Mock DataManager with required internal attributes
        self.mock_data_manager = MagicMock()
        self.mock_data_manager._patron_data = []
        self.mock_data_manager._catalogue_data = []

        # Instantiate BatUI
        self.ui = BatUI(self.mock_data_manager)

    # =========================================================================
    # Helper to transition through the main menu
    # =========================================================================
    def _run_main_menu_and_check(self, input_value, expected_screen_name):
        """Runs the main menu with a specific choice and asserts the transition."""
        with patch('src.bat_ui.user_input.read_integer_range', return_value=input_value), \
             patch('builtins.print'):
            self.ui.run_current_screen()
            self.assertEqual(self.ui.get_current_screen(), expected_screen_name)


    # =========================================================================
    # TESTS FOR get_current_screen (Lines 36-50)
    # =========================================================================
    def test_get_current_screen_initial(self):
        """Covers initial screen setting."""
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    def test_get_current_screen_quit(self):
        """Covers the mapping for the QUIT screen."""
        self.ui._current_screen = self.ui._quit
        self.assertEqual(self.ui.get_current_screen(), "QUIT")

    # =========================================================================
    # TESTS FOR _main_menu (Lines 54-82)
    # =========================================================================
    def test_main_menu_to_loan_item(self):
        """Covers choice 1 transition."""
        self._run_main_menu_and_check(1, "LOAN ITEM")

    def test_main_menu_to_return_item(self):
        """Covers choice 2 transition."""
        self._run_main_menu_and_check(2, "RETURN ITEM")

    def test_main_menu_to_search_patron(self):
        """Covers choice 3 transition."""
        self._run_main_menu_and_check(3, "SEARCH FOR PATRON")

    def test_main_menu_to_register_patron(self):
        """Covers choice 4 transition."""
        self._run_main_menu_and_check(4, "REGISTER PATRON")

    def test_main_menu_to_access_makerspace(self):
        """Covers choice 5 transition."""
        self._run_main_menu_and_check(5, "ACCESS MAKERSPACE")

    def test_main_menu_to_quit(self):
        """Covers choice 6 transition."""
        self._run_main_menu_and_check(6, "QUIT")


    # =========================================================================
    # TESTS FOR _loan_item (Lines 94-141)
    # =========================================================================
    @patch('src.bat_ui.user_input.read_integer', return_value=1)
    @patch('src.bat_ui.search.find_item_by_id', return_value=None)
    @patch('builtins.print')
    def test_loan_item_no_item_found(self, mock_print, mock_search, mock_input):
        """Covers Line 105 (if item is None: print("!!! No such item..."))."""
        new_screen = self.ui._loan_item()
        self.assertEqual(new_screen, self.ui._main_menu)

    @patch('src.bat_ui.user_input.read_integer', return_value=1)
    @patch('src.bat_ui.search.find_item_by_id', return_value=MockItem(1))
    @patch('src.bat_ui.user_input.read_bool', return_value='n')
    @patch('builtins.print')
    def test_loan_item_item_not_confirmed(self, mock_print, mock_bool, mock_search, mock_input):
        """Covers Line 139 (else: print("CANCELLING LOAN"))."""
        new_screen = self.ui._loan_item()
        self.assertEqual(new_screen, self.ui._main_menu)

    @patch('src.bat_ui.user_input.read_integer', side_effect=[1, 30])
    @patch('src.bat_ui.search.find_item_by_id', return_value=MockItem(1))
    @patch('src.bat_ui.user_input.read_bool', return_value='y')
    @patch('src.bat_ui.user_input.read_string', return_value="Patron A")
    @patch('src.bat_ui.search.find_patron_by_name_and_age', return_value=None)
    @patch('builtins.print')
    def test_loan_item_no_patron_found(self, mock_print, mock_search_patron, *args):
        """Covers Line 129 (if patron is None: print("!!! NO SUCH PATRON..."))."""
        new_screen = self.ui._loan_item()
        self.assertEqual(new_screen, self.ui._main_menu)

    @patch('src.bat_ui.user_input.read_integer', side_effect=[1, 30])
    @patch('src.bat_ui.search.find_item_by_id', return_value=MockItem(1, name="Hammer"))
    @patch('src.bat_ui.user_input.read_bool', return_value='y')
    @patch('src.bat_ui.user_input.read_string', return_value="Patron A")
    @patch('src.bat_ui.search.find_patron_by_name_and_age', return_value=MockPatron(name="Patron A"))
    @patch('src.bat_ui.user_input.read_integer_range', return_value=7)
    @patch('src.bat_ui.business_logic.process_loan', return_value=True)
    @patch('builtins.print')
    def test_loan_item_success(self, mock_print, mock_loan, *args):
        """Covers Line 136 (if loan_success: print(f"Loan of {item._name}..."))."""
        self.ui._loan_item()
        mock_loan.assert_called()

    @patch('src.bat_ui.user_input.read_integer', side_effect=[1, 30])
    @patch('src.bat_ui.search.find_item_by_id', return_value=MockItem(1, name="Hammer"))
    @patch('src.bat_ui.user_input.read_bool', return_value='y')
    @patch('src.bat_ui.user_input.read_string', return_value="Patron A")
    @patch('src.bat_ui.search.find_patron_by_name_and_age', return_value=MockPatron(name="Patron A"))
    @patch('src.bat_ui.user_input.read_integer_range', return_value=7)
    @patch('src.bat_ui.business_logic.process_loan', return_value=False)
    @patch('builtins.print')
    def test_loan_item_fail(self, mock_print, mock_loan, *args):
        """Covers Line 138 (else: print(f"Sorry, {patron._name}..."))."""
        self.ui._loan_item()
        mock_loan.assert_called()


    # =========================================================================
    # TESTS FOR _return_item (Lines 153-184)
    # =========================================================================
    @patch('src.bat_ui.user_input.read_string', side_effect=["Name", "30", "ExtraName"])
    @patch('src.bat_ui.user_input.read_integer', side_effect=[30, 30])
    @patch('src.bat_ui.search.find_patron_by_name_and_age', return_value=None)
    @patch('builtins.print')
    def test_return_item_no_patron(self, mock_print, mock_search, *args):
        """Covers Line 169 (if patron is None: print("!!! NO SUCH PATRON..."))."""
        new_screen = self.ui._return_item()
        self.assertEqual(new_screen, self.ui._main_menu)


    # =========================================================================
    # TESTS FOR _search_for_patron (Lines 192-226)
    # =========================================================================
    @patch('src.bat_ui.user_input.read_integer_range', return_value=3)
    @patch('builtins.print')
    def test_search_patron_back(self, mock_print, mock_input):
        """Covers Line 213 (elif choice == 3: return self._main_menu)."""
        new_screen = self.ui._search_for_patron()
        self.assertEqual(new_screen, self.ui._main_menu)

    # --- Search by Name (Choice 1) ---
    @patch('src.bat_ui.user_input.read_integer_range', return_value=1)
    @patch('src.bat_ui.user_input.read_string', return_value="NameA")
    @patch('src.bat_ui.search.find_patron_by_name', return_value=[])
    @patch('builtins.print')
    def test_search_patron_by_name_none(self, mock_print, mock_search, *args):
        """Covers Line 217 (if not patrons_found: print("NO PATRONS FOUND..."))."""
        new_screen = self.ui._search_for_patron()
        self.assertEqual(new_screen, self.ui._search_for_patron)

    @patch('src.bat_ui.user_input.read_integer_range', return_value=1)
    @patch('src.bat_ui.user_input.read_string', return_value="NameA")
    @patch('src.bat_ui.search.find_patron_by_name', return_value=[MockPatron()])
    @patch('builtins.print')
    def test_search_patron_by_name_success(self, mock_print, mock_search, *args):
        """Covers Line 220 (else: print("PATRON(S) FOUND: ")...)."""
        new_screen = self.ui._search_for_patron()
        self.assertEqual(new_screen, self.ui._search_for_patron)

    # --- Search by Age (Choice 2) ---
    @patch('src.bat_ui.user_input.read_integer_range', return_value=2)
    @patch('src.bat_ui.user_input.read_integer', return_value=30)
    @patch('src.bat_ui.search.find_patron_by_age', return_value=[])
    @patch('builtins.print')
    def test_search_patron_by_age_none(self, mock_print, mock_search, *args):
        """Covers Line 217 (no patrons found) via age search."""
        new_screen = self.ui._search_for_patron()
        self.assertEqual(new_screen, self.ui._search_for_patron)

    @patch('src.bat_ui.user_input.read_integer_range', return_value=2)
    @patch('src.bat_ui.user_input.read_integer', return_value=30)
    @patch('src.bat_ui.search.find_patron_by_age', return_value=[MockPatron()])
    @patch('builtins.print')
    def test_search_patron_by_age_success(self, mock_print, mock_search, *args):
        """Covers Line 220 (patrons found) via age search."""
        new_screen = self.ui._search_for_patron()
        self.assertEqual(new_screen, self.ui._search_for_patron)

    # =========================================================================
    # TESTS FOR _register_patron (Lines 235-246)
    # =========================================================================
    @patch('src.bat_ui.user_input.read_string', return_value="New Patron")
    @patch('src.bat_ui.user_input.read_integer_range', return_value=50)
    @patch('builtins.print')
    def test_register_patron_calls_data_manager(self, mock_print, mock_age, mock_name):
        """Covers Line 245 (self._data_manager.register_patron)."""
        new_screen = self.ui._register_patron()
        self.mock_data_manager.register_patron.assert_called_once_with("New Patron", 50)
        self.assertEqual(new_screen, self.ui._main_menu)

    # =========================================================================
    # TESTS FOR _access_makerspace (Lines 258-279)
    # =========================================================================
    @patch('builtins.print')
    @patch('src.bat_ui.search.find_patron_by_name_and_age', return_value=None)
    @patch('src.bat_ui.user_input.read_integer', return_value=30)
    @patch('src.bat_ui.user_input.read_string', return_value="NameA")
    def test_access_makerspace_no_patron(self, mock_name, mock_age, mock_search, mock_print):
        """Covers Line 269 (if patron is None: print("!!! NO SUCH PATRON"))."""
        new_screen = self.ui._access_makerspace()
        self.assertEqual(new_screen, self.ui._main_menu)

    @patch('src.bat_ui.user_input.read_string', return_value="NameA")
    @patch('src.bat_ui.user_input.read_integer', return_value=30)
    @patch('src.bat_ui.search.find_patron_by_name_and_age')
    @patch('src.bat_ui.business_logic.can_use_makerspace', return_value=True)
    @patch('builtins.print')
    def test_access_makerspace_allowed(self, mock_print, mock_logic, mock_search, *args):
        """Covers Line 275 (if allowed: print(f"{patron._name} is allowed..."))."""
        mock_search.return_value = MockPatron(name="Patron A", age=30)
        self.ui._access_makerspace()
        mock_logic.assert_called()

    @patch('src.bat_ui.user_input.read_string', return_value="NameA")
    @patch('src.bat_ui.user_input.read_integer', return_value=30)
    @patch('src.bat_ui.search.find_patron_by_name_and_age')
    @patch('src.bat_ui.business_logic.can_use_makerspace', return_value=False)
    @patch('builtins.print')
    def test_access_makerspace_not_allowed(self, mock_print, mock_logic, mock_search, *args):
        """Covers Line 277 (else: print(f"{patron._name} is NOT allowed..."))."""
        mock_search.return_value = MockPatron(name="Patron A", age=30)
        self.ui._access_makerspace()
        self.assertFalse(mock_logic.return_value)


    # =========================================================================
    # TESTS FOR _quit (Lines 286-289)
    # =========================================================================
    @patch('builtins.print')
    def test_quit_saves_data(self, mock_print):
        """Covers Lines 287 & 288 (data_manager.save_patrons/catalogue)."""
        self.ui._quit()
        self.mock_data_manager.save_patrons.assert_called_once()

    @patch('builtins.print')
    def test_quit_returns_quit_func(self, mock_print):
        """Covers Line 289 (return self._quit)."""
        new_screen_func = self.ui._quit()
        self.assertEqual(new_screen_func, self.ui._quit)