# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
import unittest
from src.business_logic import type_of_patron


class TestTypeOfPatron(unittest.TestCase):
    # ERROR path
    def test_negative_age_returns_error(self):
        self.assertEqual(type_of_patron(-1), "ERROR")

    # Minor (lower & upper bounds)
    def test_age_0_is_minor(self):
        self.assertEqual(type_of_patron(0), "Minor")

    def test_age_17_is_minor(self):
        self.assertEqual(type_of_patron(17), "Minor")

    # Adult (boundary & typical)
    def test_age_18_is_adult(self):
        self.assertEqual(type_of_patron(18), "Adult")

    def test_age_89_is_adult(self):
        self.assertEqual(type_of_patron(89), "Adult")

    # Elderly (boundary & upper)
    def test_age_90_is_elderly(self):
        self.assertEqual(type_of_patron(90), "Elderly")

    def test_age_120_is_elderly(self):
        self.assertEqual(type_of_patron(120), "Elderly")
