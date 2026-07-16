# tests/test_loan_unit.py
import unittest
from datetime import date
from src.loan import Loan


class TestLoan(unittest.TestCase):
    def test_str_exact_format(self):
        # minimal stub item with the exact attrs Loan.__str__ uses
        item = type("Item", (), {"_id": 123, "_name": "Saw", "_type": "Tool"})()
        d = date(2025, 1, 9)
        self.assertEqual(str(Loan(item, d)), "Item 123: Saw (Tool); due 09/01/2025")

    def test_str_with_different_item(self):
        item = type("Item", (), {"_id": 7, "_name": "Sander", "_type": "Machine"})()
        d = date(2030, 12, 31)
        self.assertEqual(str(Loan(item, d)), "Item 7: Sander (Machine); due 31/12/2030")
