# tests/test_discount.py
"""
Black-box tests for src/discount.py::calculate_discount
Aligned with the spec:
- 0-50  -> 0%
- 51-64 -> 10%   
- 65-89 -> 15%
- 90+   -> 100%
___Name___: Ong Ying Tong
___MonashID___: 34477306
"""

import unittest
from src.discount import calculate_discount


class TestDiscountFromExcel(unittest.TestCase):
    # Representatives + boundaries (13 total)

    def test_id_1_age_38_expect_0(self):
        self.assertEqual(calculate_discount(38), 0, "38 years old should get 0% discount")

    def test_id_2_age_50_expect_10(self):
        # If your spec says "over 50" (strictly >50) is 10%, change expected to 0.
        self.assertEqual(calculate_discount(50), 0, "50 years old should get 0% discount")

    def test_id_3_age_51_expect_10(self):
        self.assertEqual(calculate_discount(51), 10, "51 years old should get 10% discount")

    def test_id_4_age_52_expect_10(self):
        self.assertEqual(calculate_discount(52), 10, "52 years old should get 10% discount")

    def test_id_5_age_58_expect_10(self):
        self.assertEqual(calculate_discount(58), 10, "58 years old should get 10% discount")

    def test_id_6_age_64_expect_10(self):
        # FIXED: 64 is still in the 50–64 bracket → 10%
        self.assertEqual(calculate_discount(64), 10, "64 years old should get 10% discount")

    def test_id_7_age_65_expect_15(self):
        self.assertEqual(calculate_discount(65), 15, "65 years old should get 15% discount")

    def test_id_8_age_66_expect_15(self):
        self.assertEqual(calculate_discount(66), 15, "66 years old should get 15% discount")

    def test_id_9_age_78_expect_15(self):
        self.assertEqual(calculate_discount(78), 15, "78 years old should get 15% discount")

    def test_id_10_age_89_expect_15(self):
        self.assertEqual(calculate_discount(89), 15, "89 years old should get 15% discount")

    def test_id_11_age_90_expect_100(self):
        self.assertEqual(calculate_discount(90), 100, "90 years old should get 100% discount")

    def test_id_12_age_91_expect_100(self):
        self.assertEqual(calculate_discount(91), 100, "91 years old should get 100% discount")

    def test_id_13_age_98_expect_100(self):
        self.assertEqual(calculate_discount(98), 100, "98 years old should get 100% discount")


if __name__ == "__main__":
    unittest.main()

