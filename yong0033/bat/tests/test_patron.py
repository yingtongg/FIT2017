import unittest
from unittest.mock import patch
from datetime import datetime
from src.patron import Patron
from src.loan import Loan
# Ensure you have 'search' available for patching if it's imported in src.patron

# --- MOCK DEPENDENCIES ---

# 1. Mock BorrowableItem to satisfy the Loan constructor and find_loan
class MockItem:
    def __init__(self, item_id, title="Test Title", item_type="General"): # <-- ADDED item_type argument
        self._id = item_id
        self._name = title
        # *** FIX: Added _type attribute to satisfy Loan.__str__ (line 34) ***
        self._type = item_type # <-- ADDED THIS LINE

    def __str__(self):
        # We assume the item string includes the type for full coverage/realism
        return f"Item {self._id}: {self._name} ({self._type})" # <-- UPDATED __str__

# Sample JSON data for testing load_data
TEST_JSON_DATA = {
    "patron_id": 202,
    "name": "Bob",
    "age": 45,
    "outstanding_fees": 15.50,
    "gardening_tool_training": True,
    "carpentry_tool_training": False,
    "makerspace_training": True,
    "loans": [
        {"item": 1, "due": "15/10/2025"},
        {"item": 2, "due": "20/10/2025"},
        {"item": 99, "due": "25/10/2025"}
    ]
}

class TestPatron(unittest.TestCase):

    def setUp(self):
            # 1. Patron initialized with __init__
            self.default_patron = Patron()

            # 2. Patron initialized with set_new_patron_data (to cover lines 79-83)
            self.new_patron = Patron()
            self.new_patron.set_new_patron_data(101, "Alice", 30)

            # 3. Patron with loans and training (for __str__ and find_loan tests)
            self.loan_patron = Patron()

            # *** FIX: Call set_new_patron_data FIRST, as it resets all fields ***
            self.loan_patron.set_new_patron_data(202, "Bob", 45)

            # *** THEN, set the training and loans, which are meant to be active ***
            self.loan_patron._gardening_tool_training = True
            self.loan_patron._carpentry_tool_training = False
            self.loan_patron._makerspace_training = False
            self.loan1 = Loan(MockItem(50, title="Tool A", item_type="Tool"), datetime.now())
            self.loan2 = Loan(MockItem(60, title="Tool B", item_type="Tool"), datetime.now())
            self.loan_patron._loans.extend([self.loan1, self.loan2])

    # =========================================================================
    # TESTS FOR load_data & load_loans
    # =========================================================================
    @patch('src.patron.search.find_item_by_id')
    def test_load_data_id(self, mock_find_item):
        # Pass a type here too, though load_data likely only uses _id for the Loan constructor
        mock_find_item.side_effect = [MockItem(1, item_type="TypeA"), MockItem(2, item_type="TypeB"), None]
        patron = Patron()
        patron.load_data(TEST_JSON_DATA, None)
        self.assertEqual(patron._id, 202)

    @patch('src.patron.search.find_item_by_id')
    def test_load_data_name(self, mock_find_item):
        mock_find_item.side_effect = [MockItem(1), MockItem(2), None]
        patron = Patron()
        patron.load_data(TEST_JSON_DATA, None)
        self.assertEqual(patron._name, "Bob")

    @patch('src.patron.search.find_item_by_id')
    def test_load_data_age(self, mock_find_item):
        mock_find_item.side_effect = [MockItem(1), MockItem(2), None]
        patron = Patron()
        patron.load_data(TEST_JSON_DATA, None)
        self.assertEqual(patron._age, 45)

    @patch('src.patron.search.find_item_by_id')
    def test_load_data_fees(self, mock_find_item):
        mock_find_item.side_effect = [MockItem(1), MockItem(2), None]
        patron = Patron()
        patron.load_data(TEST_JSON_DATA, None)
        self.assertEqual(patron._outstanding_fees, 15.50)

    @patch('src.patron.search.find_item_by_id')
    def test_load_data_gardening_training(self, mock_find_item):
        mock_find_item.side_effect = [MockItem(1), MockItem(2), None]
        patron = Patron()
        patron.load_data(TEST_JSON_DATA, None)
        self.assertTrue(patron._gardening_tool_training)

    @patch('src.patron.search.find_item_by_id')
    def test_load_data_carpentry_training(self, mock_find_item):
        mock_find_item.side_effect = [MockItem(1), MockItem(2), None]
        patron = Patron()
        patron.load_data(TEST_JSON_DATA, None)
        self.assertFalse(patron._carpentry_tool_training)

    @patch('src.patron.search.find_item_by_id')
    def test_load_loans_skipped_loan_count(self, mock_find_item):
        mock_find_item.side_effect = [MockItem(1), MockItem(2), None]
        patron = Patron()
        patron.load_data(TEST_JSON_DATA, None)
        self.assertEqual(len(patron._loans), 2)

    # =========================================================================
    # TESTS FOR set_new_patron_data
    # =========================================================================
    def test_set_patron_id(self):
        self.assertEqual(self.new_patron._id, 101)

    def test_set_patron_name(self):
        self.assertEqual(self.new_patron._name, "Alice")

    def test_set_patron_age(self):
        self.assertEqual(self.new_patron._age, 30)

    def test_set_patron_fees_reset(self):
        self.assertEqual(self.new_patron._outstanding_fees, 0.0)

    def test_set_patron_gardening_reset(self):
        self.assertFalse(self.new_patron._gardening_tool_training)

    def test_set_patron_carpentry_reset(self):
        self.assertFalse(self.new_patron._carpentry_tool_training)

    def test_set_patron_makerspace_reset(self):
        self.assertFalse(self.new_patron._makerspace_training)

    def test_set_patron_gardening_tool_training_is_false(self):
        patron = Patron()
        patron._gardening_tool_training = True
        patron.set_new_patron_data(9001, "Test Gardener", 25)
        self.assertFalse(patron._gardening_tool_training)


    # =========================================================================
    # TESTS FOR find_loan
    # =========================================================================
    def test_find_loan_success(self):
        found_loan = self.loan_patron.find_loan(50)
        self.assertIs(found_loan, self.loan1)

    def test_find_loan_failure(self):
        not_found_loan = self.loan_patron.find_loan(999)
        self.assertIsNone(not_found_loan)

    # =========================================================================
    # TESTS FOR __str__
    # =========================================================================
    # --- Training Branches ---
    def test_str_training_none(self):
        patron = Patron()
        patron.set_new_patron_data(1, "A", 20)
        self.assertIn("Completed training: NONE", str(patron))

    def test_str_training_gardening(self):
        self.assertIn(" - gardening tools", str(self.loan_patron))

    def test_str_training_carpentry(self):
        patron = Patron()
        patron.set_new_patron_data(4, "D", 50)
        patron._carpentry_tool_training = True
        self.assertIn(" - carpentry tools", str(patron))

    def test_str_training_makerspace(self):
        patron = Patron()
        patron.set_new_patron_data(5, "E", 60)
        patron._makerspace_training = True
        self.assertIn(" - makerspace", str(patron))

    # --- Loan Branches ---
    def test_str_no_loans(self):
        self.assertIn("No current loans", str(self.new_patron))

    def test_str_single_loan(self):
        patron = Patron()
        patron.set_new_patron_data(3, "C", 40)
        patron._loans.append(Loan(MockItem(70, title="Single Tool", item_type="TypeC"), datetime.now()))
        self.assertIn("1 active loan:", str(patron))

    def test_str_multiple_loans(self):
        self.assertIn("2 active loans:", str(self.loan_patron))