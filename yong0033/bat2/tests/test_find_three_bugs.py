import unittest
from datetime import date, timedelta
from src.business_logic import can_borrow_book, can_borrow_carpentry_tool, process_return
from src.loan import Loan

class TestBorrowingRules(unittest.TestCase):
    class Item:
        def __init__(self, _id):
            self._id = _id
            self._on_loan = 0

    class Patron:
        def __init__(self):
            self._loans = []
        def find_loan(self, item_id):
            for L in self._loans:
                if L._item._id == item_id:
                    return L

    # --- Bug A: Book loan length boundary (56 allowed, 57 blocked) ---
    def test_book_56_allowed(self):
        ok = can_borrow_book(patron_age=30, length_of_loan=56, outstanding_fees=0.0)
        self.assertTrue(ok, "Expected: books up to 56 days are allowed; Got: denied (False).")

    def test_book_57_blocked(self):
        ok = can_borrow_book(patron_age=30, length_of_loan=57, outstanding_fees=0.0)
        self.assertFalse(ok, "Expected: 57 days should be blocked; Got: allowed (True).")

    # --- Bug B: Carpentry age threshold (18 should be allowed) ---
    def test_carpentry_17_denied(self):
        ok = can_borrow_carpentry_tool(17, 14, 0.0, True)
        self.assertFalse(ok, "Expected: age 17 denied for carpentry tools; Got: allowed (True).")

    def test_carpentry_18_allowed(self):
        ok = can_borrow_carpentry_tool(18, 14, 0.0, True)
        self.assertTrue(ok, "Expected: age 18 allowed for carpentry tools; Got: denied (False).")

    # --- Bug C: Returning an item decrements on_loan and removes the loan ---
    def test_process_return_decrements_on_loan(self):
        item = self.Item(1)
        item._on_loan = 1
        patron = self.Patron()
        patron._loans.append(Loan(item, date.today() + timedelta(days=7)))

        process_return(patron, 1)

        self.assertEqual(
            item._on_loan, 0,
            f"Expected item._on_loan to decrement to 0 after return; Got: {item._on_loan}."
        )

    def test_process_return_removes_loan_record(self):
        item = self.Item(2)
        item._on_loan = 1
        patron = self.Patron()
        patron._loans.append(Loan(item, date.today() + timedelta(days=7)))

        process_return(patron, 2)

        self.assertEqual(
            len(patron._loans), 0,
            f"Expected patron._loans to be empty after return; Got: {len(patron._loans)} remaining."
        )
