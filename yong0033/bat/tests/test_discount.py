# pylint: disable=missing-module-docstring,missing-function-docstring
import unittest
from src.business_logic import calculate_discount


class TestDiscountByAge(unittest.TestCase):
    """
    White-box, boundary-focused tests following the provided table.
    Test IDs 1–13 map to the spreadsheet rows; ID 0 covers the invalid-age case.
    """

    # ID 0: invalid age (< 0) -> "ERROR"
    def test_id_00_negative_age_returns_ERROR(self):
        self.assertEqual(calculate_discount(-1), "ERROR")

    # 18–49 → 0%
    def test_id_01_age_38_returns_0(self):
        self.assertEqual(calculate_discount(38), 0)

    # 50 → 0%  (boundary: exactly 50 gets no discount)
    def test_id_02_age_50_returns_0(self):
        self.assertEqual(calculate_discount(50), 0)

    # 51–64 → 10%
    def test_id_03_age_51_returns_10(self):
        self.assertEqual(calculate_discount(51), 10)

    def test_id_04_age_52_returns_10(self):
        self.assertEqual(calculate_discount(52), 10)

    def test_id_05_age_58_returns_10(self):
        self.assertEqual(calculate_discount(58), 10)

    def test_id_06_age_64_returns_10(self):
        self.assertEqual(calculate_discount(64), 10)

    # 65–89 → 15%
    def test_id_07_age_65_returns_15(self):
        self.assertEqual(calculate_discount(65), 15)

    def test_id_08_age_66_returns_15(self):
        self.assertEqual(calculate_discount(66), 15)

    def test_id_09_age_78_returns_15(self):
        self.assertEqual(calculate_discount(78), 15)

    def test_id_10_age_89_returns_15(self):
        self.assertEqual(calculate_discount(89), 15)

    # 90+ → 100%
    def test_id_11_age_90_returns_100(self):
        self.assertEqual(calculate_discount(90), 100)

    def test_id_12_age_91_returns_100(self):
        self.assertEqual(calculate_discount(91), 100)

    def test_id_13_age_98_returns_100(self):
        self.assertEqual(calculate_discount(98), 100)
