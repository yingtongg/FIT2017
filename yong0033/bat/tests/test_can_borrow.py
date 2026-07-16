# pylint: disable=missing-module-docstring,missing-function-docstring
# pylint: disable=missing-class-docstring,
# pylint: disable=invalid-name,pointless-string-statement
import unittest
from src.business_logic import can_borrow


class TestCanBorrow(unittest.TestCase):
    """
    White-box tests for can_borrow.
    Each test is linked to the Excel TestIDs (1-13) and targets the
    internal decisions in the business logic file.
    """
    # TestID 1: Book, age 18, fees > 0 -> Denied
    def test_T1_book_age_18_fees_denied(self):
        allowed = can_borrow("Book", 18, 2, 2,
                             False, True)
        self.assertFalse(allowed)

    # TestID 2: Carpentry tool, age 99 (elderly), no fees,
    # training completed -> Denied
    def test_T2_carpentry_age_99_denied(self):
        allowed = can_borrow("Carpentry tool", 99, 7, 0,
                             False, True)
        self.assertFalse(allowed)

    # TestID 3: Carpentry tool, under 18, fees > 0,
    # training completed -> Denied
    def test_T3_carpentry_under_18_fees_denied(self):
        allowed = can_borrow("Carpentry tool", 17, 14, 2,
                             True, True)
        self.assertFalse(allowed)

    # TestID 4: Gardening tool, under 18, no fees,
    # training not completed -> Denied
    def test_T4_gardening_under_18_no_training_denied(self):
        allowed = can_borrow("Gardening tool", 13, 7, 0,
                             False, False)
        self.assertFalse(allowed)

    # TestID 5: Book, age 90, fees > 0 -> Denied
    def test_T5_book_age_90_fees_denied(self):
        allowed = can_borrow("Book", 90, 14, 2,
                             False, False)
        self.assertTrue(allowed)

    # TestID 6: Gardening tool, age 91, no fees,
    # training completed -> Allowed
    def test_T6_gardening_age_91_training_allowed(self):
        allowed = can_borrow("Gardening tool", 91, 2, 0,
                             True, False)
        self.assertTrue(allowed)

    # TestID 7: Book, age 93, fees > 0 -> Denied
    def test_T7_book_age_93_fees_denied(self):
        allowed = can_borrow("Book", 93, 7, 2,
                             False, False)
        self.assertTrue(allowed)

    # TestID 8: Carpentry tool, age 18, no fees,
    # training not completed -> Denied
    def test_T8_carpentry_age_18_no_training_denied(self):
        allowed = can_borrow("Carpentry tool", 18, 2, 0,
                             False, False)
        self.assertFalse(allowed)

    # TestID 9: Gardening tool, age 70, no fees,
    # training not completed -> Denied
    def test_T9_gardening_age_70_no_training_denied(self):
        allowed = can_borrow("Gardening tool", 70, 2, 0,
                             False, False)
        self.assertFalse(allowed)

    # TestID 10: Book, age 15, no fees -> Allowed
    def test_T10_book_under_18_allowed(self):
        allowed = can_borrow("Book", 15, 2, 0,
                             True, True)
        self.assertTrue(allowed)

    # TestID 11: Gardening tool, age 65, fees > 0,
    # training completed -> Denied
    def test_T11_gardening_age_65_fees_denied(self):
        allowed = can_borrow("Gardening tool", 65, 7, 2,
                             True, True)
        self.assertFalse(allowed)

    # TestID 12: Carpentry tool, age 50, no fees,
    # training completed -> Allowed
    def test_T12_carpentry_age_50_training_allowed(self):
        allowed = can_borrow("Carpentry tool", 50, 10, 0,
                             False, True)
        self.assertTrue(allowed)

    # TestID 13: Gardening tool, age 4, no fees,
    # training not completed -> Denied
    def test_T13_gardening_age_4_no_training_denied(self):
        allowed = can_borrow("Gardening tool", 4, 14, 0,
                             False, False)
        self.assertFalse(allowed)
