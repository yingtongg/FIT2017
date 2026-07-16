# pylint: disable=missing-module-docstring,
# pylint: disable=missing-function-docstring,missing-class-docstring
import unittest
from src.business_logic import can_borrow_carpentry_tool


class TestCanBorrowCarpentryTool(unittest.TestCase):
    def test_fees_owed_denied(self):
        self.assertFalse(can_borrow_carpentry_tool(
            30, 7, 10, True))

    def test_underage_denied(self):
        self.assertFalse(can_borrow_carpentry_tool(
            17, 7, 0, True))

    def test_elderly_denied(self):
        self.assertFalse(can_borrow_carpentry_tool(
            90, 7, 0, True))

    def test_length_over_limit_denied(self):
        self.assertFalse(can_borrow_carpentry_tool(
            30, 15, 0, True))

    def test_training_not_completed_denied(self):
        self.assertFalse(can_borrow_carpentry_tool(
            30, 7, 0, False))

    def test_valid_borrow_allowed(self):
        self.assertTrue(can_borrow_carpentry_tool(
            30, 7, 0, True))
