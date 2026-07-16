# tests/test_business_logic_gapfill_oneclass.py
import unittest
import src.business_logic as BL

class TestBLGapFillOneClass(unittest.TestCase):
    class Dummy:
        """
        Single reusable shape for both 'patron' and 'item'.
        Only the attributes you care about are set via kwargs.
        """
        def __init__(self, **kw):
            # patron-ish
            self._name = kw.get("_name", "Pat")
            self._age = kw.get("_age", 30)
            self._outstanding_fees = kw.get("_outstanding_fees", 0.0)
            self._gardening_tool_training = kw.get("_gardening_tool_training", False)
            self._carpentry_tool_training = kw.get("_carpentry_tool_training", False)
            self._makerspace_training = kw.get("_makerspace_training", False)
            self._loans = kw.get("_loans", [])

            # item-ish
            self._type = kw.get("_type", "Book")
            self._id = kw.get("_id", 101)
            self._year = kw.get("_year", 2000)
            self._on_loan = kw.get("_on_loan", 0)

        # present for completeness; not needed in these tests
        def find_loan(self, item_id: int):
            for ln in self._loans:
                it = getattr(ln, "_item", None)
                if getattr(it, "_id", None) == item_id:
                    return ln
            return None

    # --- line ~69: can_borrow_book early deny when length >= 56
    def test_book_too_long_is_denied(self):
        self.assertFalse(BL.can_borrow_book(patron_age=40, length_of_loan=56, outstanding_fees=0.0))

    # --- line ~89: gardening tool denied when fees remain after discount
    def test_gardening_tool_denied_when_fees_remain(self):
        # Age 40 => 0% discount; any positive fees remain
        self.assertFalse(BL.can_borrow_gardening_tool(patron_age=40, length_of_loan=7,
                                                      outstanding_fees=5.0, gardening_tool_training=True))

    # --- line ~124: carpentry tool denied when length > 14
    def test_carpentry_tool_denied_when_too_long(self):
        self.assertFalse(BL.can_borrow_carpentry_tool(patron_age=40, length_of_loan=15,
                                                      outstanding_fees=0.0, carpentry_tool_training=True))

    # --- line ~214: makerspace denied when patron type is ERROR (age < 0)
    def test_makerspace_denied_when_age_error(self):
        self.assertFalse(BL.can_use_makerspace(patron_age=-1, outstanding_fees=0.0, makerspace_training=True))

    # --- lines ~225-227: makerspace denied for Minor
    def test_makerspace_denied_for_minor(self):
        self.assertFalse(BL.can_use_makerspace(patron_age=12, outstanding_fees=0.0, makerspace_training=True))

    # --- lines ~225-227: makerspace denied for Elderly (>= 90)
    def test_makerspace_denied_for_elderly(self):
        self.assertFalse(BL.can_use_makerspace(patron_age=90, outstanding_fees=0.0, makerspace_training=True))

    # --- lines ~242-252: process_loan false path (cannot borrow)
    def test_process_loan_false_path(self):
        patron = self.Dummy(_age=40, _outstanding_fees=10.0)   # fees block borrowing
        item = self.Dummy(_type="Book", _id=202, _on_loan=0)
        self.assertFalse(BL.process_loan(patron, item, length_of_loan=7))
