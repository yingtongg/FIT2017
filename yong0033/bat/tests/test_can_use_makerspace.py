# pylint: disable=missing-module-docstring,
# pylint: disable=missing-function-docstring,missing-class-docstring
import unittest
from src.business_logic import can_use_makerspace


class TestCanUseMakerspace(unittest.TestCase):
    def test_negative_age_error(self):
        self.assertFalse(can_use_makerspace(
            -1, 0, True))

    def test_minor_denied(self):
        self.assertFalse(can_use_makerspace(
            10, 0, True))

    def test_elderly_denied(self):
        self.assertFalse(can_use_makerspace(
            95, 0, True))

    def test_adult_with_training_and_no_fees_allowed(self):
        self.assertTrue(can_use_makerspace(
            30, 0, True))

    def test_adult_with_training_but_fees_denied(self):
        self.assertFalse(can_use_makerspace(
            30, 10, True))

    def test_adult_without_training_denied(self):
        self.assertFalse(can_use_makerspace(
            30, 0, False))
