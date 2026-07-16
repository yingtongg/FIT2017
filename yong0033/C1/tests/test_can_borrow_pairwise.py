"""
test_can_borrow_pairwise.py

Black-box *pairwise* tests for `src/can_borrow.py::can_borrow`.

Test design summary
-------------------
Goal: Validate borrowing *eligibility* (allowed/denied) and *age-based
discount* returned by the SUT without peeking at its implementation.

Primary factors (pairwise inputs)
  1) ItemType            : {"Book", "Carpentry", "Gardening"}
  2) Age (years)         : representative boundaries {4, 13, 15, 17, 18, 50, 65, 70, 90, 91, 93, 99}
  3) Loan length (days)  : {2, 7, 14}  (not validated by rules, but included for pairing)
  4) Outstanding fees    : {True, False}
  5) Gardening training  : {"Completed", "NotCompleted", "N/A"}
  6) Carpentry training  : {"Completed", "NotCompleted", "N/A"}

Rules under test (expected externally from the spec)
  • Fees: If a patron has outstanding fees → borrowing is denied
          (discount is still computed from age).
  • Books: Allowed iff no outstanding fees.
  • Carpentry: Allowed only for ages 18-89 inclusive *and* carpentry training == "Completed".
  • Gardening: Allowed only when gardening training == "Completed" (age doesn't grant an override).
  • Discount by age:
        0-50  → 0%
        51-64 → 10%
        65-89 → 15%
        90+   → 100%

Parameter order required by the SUT call (VERY IMPORTANT)
    can_borrow(item_type, age, loan_length_days, has_fees, gardening_training, carpentry_training)
This file consistently calls `can_borrow` with that exact ordering.

Pairwise set
------------
The 13 tests below are a reduced pairwise suite. Each case lists
its intended scenario (ID N) and asserts both:
  (a) eligibility (allowed / denied)
  (b) discount % consistent with the age rule
___Name___: Ong Ying Tong
___MonashID___: 34477306
"""
import unittest
from src.can_borrow import can_borrow


class TestCanBorrowPairwise(unittest.TestCase):
    """Each test follows: Input → (expected_allowed, expected_discount)."""
    # ID 1: Book, age 18, Fees Yes -> Denied (fees), 0%
    def test_book_18_fees_yes_denied(self):
        allowed, discount = can_borrow("Book", 18, 2, True, "NotCompleted", "Completed")
        self.assertFalse(allowed, "Borrow should be denied due to outstanding fees.")
        self.assertEqual(discount, 0, "Age 18 should get 0% discount.")

    # ID 2: Carpentry, age 99, Completed -> Denied (90+), 100%
    def test_carpentry_99_completed_denied(self):
        allowed, discount = can_borrow("Carpentry", 99, 7, False, "N/A", "Completed")
        self.assertFalse(allowed, "Borrow should be denied for age 90+.")
        self.assertEqual(discount, 100, "Age 99 should get 100% discount.")

    # ID 3: Carpentry, age 17, Completed -> Denied (under 18), 0%
    def test_carpentry_17_completed_denied(self):
        allowed, discount = can_borrow("Carpentry", 17, 14, False, "Completed", "N/A")
        self.assertFalse(allowed, "Carpentry requires age 18 or above.")
        self.assertEqual(discount, 0, "Age 17 should get 0% discount.")

    # ID 4: Gardening, age 13, NotCompleted -> Denied, 0%
    def test_gardening_13_notcompleted_denied(self):
        allowed, discount = can_borrow("Gardening", 13, 7, False, "NotCompleted", "NotCompleted")
        self.assertFalse(allowed, "Gardening requires completed training.")
        self.assertEqual(discount, 0, "Age 13 should get 0% discount.")

    # ID 5: Book, age 90, Fees Yes -> Denied (fees), 100%
    def test_book_90_fees_yes_denied(self):
        allowed, discount = can_borrow("Book", 90, 14, True, "N/A", "NotCompleted")
        self.assertFalse(allowed, "Borrow should be denied due to outstanding fees.")
        self.assertEqual(discount, 100, "Age 90 should get 100% discount.")

    # ID 6: Gardening, age 91, Completed -> Allowed, 100%
    def test_gardening_91_completed_allowed(self):
        allowed, discount = can_borrow("Gardening", 91, 2, False, "Completed", "N/A")
        self.assertTrue(allowed, "Gardening with completed training should be allowed.")
        self.assertEqual(discount, 100, "Age 91 should get 100% discount.")

    # ID 7: Book, age 93, Fees Yes -> Denied (fees), 100%
    def test_book_93_fees_yes_denied(self):
        allowed, discount = can_borrow("Book", 93, 7, True, "NotCompleted", "N/A")
        self.assertFalse(allowed, "Borrow should be denied due to outstanding fees.")
        self.assertEqual(discount, 100, "Age 93 should get 100% discount.")

    # ID 8: Carpentry, age 18, Carpentry NotCompleted -> Denied (training), 0%
    def test_carpentry_18_notcompleted_denied(self):
        allowed, discount = can_borrow("Carpentry", 18, 2, False, "Completed", "NotCompleted")
        self.assertFalse(allowed, "Carpentry requires completed carpentry training.")
        self.assertEqual(discount, 0, "Age 18 should get 0% discount.")

    # ID 9: Gardening, age 70, training N/A -> Denied (needs Completed), 15%
    def test_gardening_70_na_denied(self):
        allowed, discount = can_borrow("Gardening", 70, 2, False, "N/A", "N/A")
        self.assertFalse(allowed, "Gardening requires completed training; 'N/A' is not sufficient.")
        self.assertEqual(discount, 15, "Age 70 should get 15% discount.")

    # ID 10: Book, age 15, Fees No -> Allowed, 0%
    def test_book_15_allowed(self):
        allowed, discount = can_borrow("Book", 15, 2, False, "Completed", "Completed")
        self.assertTrue(allowed, "Books should be allowed when there are no outstanding fees.")
        self.assertEqual(discount, 0, "Age 15 should get 0% discount.")

    # ID 11: Carpentry, age 50, Carpentry Completed -> Allowed, 10%
    def test_carpentry_50_completed_allowed(self):
        allowed, discount = can_borrow("Carpentry", 50, 14, False, "NotCompleted", "Completed")
        self.assertTrue(allowed, "Carpentry should be allowed for 18-89 with completed carpentry training.")
        self.assertEqual(discount, 10, "Age 50 should get 10% discount.")

    # ID 12: Gardening, age 4, N/A/NotCompleted -> Denied, 0%
    def test_gardening_4_na_notcompleted_denied(self):
        allowed, discount = can_borrow("Gardening", 4, 14, False, "N/A", "NotCompleted")
        self.assertFalse(allowed, "Gardening requires completed training; age 4 without training should be denied.")
        self.assertEqual(discount, 0, "Age 4 should get 0% discount.")

    # ID 13: Book, age 65, Fees No -> Allowed, 15%
    def test_age_65_disc_15(self):
        allowed, discount = can_borrow("Book", 65, 2, False, "N/A", "N/A")
        self.assertTrue(allowed, "Books should be allowed when there are no outstanding fees.")
        self.assertEqual(discount, 15, "Age 65 should get 15% discount.")


if __name__ == "__main__":
    unittest.main()

