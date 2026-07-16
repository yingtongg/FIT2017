# test/test_can_enrolled.py
"""
Black-box tests for src/enrolled.py::allocate
___Name___: Ong Ying Tong
___MonashID___: 34477306
"""

import unittest
from src.enrolled import enrolled


class TestAllocateFromExcel(unittest.TestCase):
    # TO 1: credits=5, prereq Met, clash Yes, seat Yes -> Rejected (clash)
    def test_id_1_credit_5_reject(self):
        self.assertEqual(enrolled(5), "Enrolled Rejected", "Expected REJECTED: total credits = 5 (below minimum 6).")

    # TO 2: credits=6, prereq Not Met, clash No, seat Yes -> Rejected (prereq)
    def test_id_2_credit_6_accept(self):
        self.assertEqual(enrolled(6), "Enrolled Allowed", "Expected ALLOWED: total credits = 6 (lower boundary).")
    # TO 3: credits=7, prereq Met, clash No, seat No, waitlist None -> Rejected (full, no waitlist)
    def test_id_3_credit_7_accept(self):
        self.assertEqual(enrolled(7), "Enrolled Allowed", "Expected ALLOWED: total credits = 7 (within 6-12 range).")
     # TO 4: credits=8, prereq Met, clash No, seat No, waitlist True -> Rejected (waitlisted, not allocated)
    def test_id_4_credit_8_accept(self):
        self.assertEqual(enrolled(8), "Enrolled Allowed", "Expected ALLOWED: total credits = 8 (within 6-12 range).")
    # TO 5: credits=9 (<12), prereq Met, clash No, seat Yes -> Rejected (underload)
    def test_id_5_credit_11_accept(self):
        self.assertEqual(enrolled(11), "Enrolled Allowed", "Expected ALLOWED: total credits = 11 (within 6-12 range).")
    # TO 6: credits=12 (boundary), prereq Met, clash No, seat Yes -> Allocated
    def test_id_6_credit_12_accept(self):
        self.assertEqual(enrolled(12), "Enrolled Allowed", "Expected ALLOWED: total credits = 12 (upper boundary of 6-12).")

    # TO 7: credits=13, prereq Met, clash No, seat Yes -> Allocated
    def test_id_7_credit_13_accept(self):
        self.assertEqual(enrolled(13), "Enrolled Allowed", "Expected ALLOWED: total credits = 13 (lower boundary of 13-24).")
    # TO 8: credits=14, prereq Met, clash No, seat Yes -> Rejected (overload)
    def test_id_8_credit_14_accept(self):
        self.assertEqual(enrolled(14), "Enrolled Allowed", "Expected ALLOWED: total credits = 14 (within 13-24 range).")
    # TO 9: credits=23 (valid EP), prereq Met, clash No, seat Yes -> Allocated
    def test_id_9_credit_23_accept(self):
        self.assertEqual(enrolled(23), "Enrolled Allowed", "Expected ALLOWED: total credits = 23 (within 13-24 range).")
    # TO 10: credits=24, prereq Not Met, clash Yes, seat Yes -> Rejected
    def test_id_10_credit_24_accept(self):
        self.assertEqual(enrolled(24), "Enrolled Allowed", "Expected ALLOWED: total credits = 24 (upper boundary).")

    # TO 11: credits=25, prereq Met, clash No, seat Yes -> Rejected
    def test_id_11_credit_25_reject(self):
        self.assertEqual(enrolled(25), "Enrolled Rejected", "Expected REJECTED: total credits = 25 (exceeds maximum 24).")
    # TO 12: credits=26, prereq Met, clash No, seat Yes, waitlist True -> Allocated (waitlist irrelevant when seats exist)
    def test_id_12_credit_26_reject(self):
        self.assertEqual(enrolled(26), "Enrolled Rejected", "Expected REJECTED: total credits = 26 (exceeds maximum 24).")
    # TO 12: credits=30, prereq Met, clash No, seat Yes, waitlist True -> Allocated (waitlist irrelevant when seats exist)
    def test_id_13_credit_30_reject(self):
        self.assertEqual(enrolled(30), "Enrolled Rejected", "Expected REJECTED: total credits = 30 (well above maximum 24).")

