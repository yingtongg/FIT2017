# tests/test_can_allocate.py
"""
___Name___: Ong Ying Tong
___MonashID___: 34477306
"""

import unittest
from src.can_allocate import can_allocate


class TestCanAllocateFromExcel(unittest.TestCase):

    # TO 1: credits=12, prereq Met, clash Yes, seat Yes -> Allocated Rejected (clash)
    def test_id_1(self):
        self.assertEqual(
            can_allocate(credit=12, prereq_met=True, clash=True, seat_available=True)[0],
            False,
            "Expected ALLOCATE REJECTED: clash present despite valid credits and seat."
        )

    # TO 2: credits=25, prereq Not_Met, clash No, seat No -> Allocated Rejected (overload / no seat / prereq)
    def test_id_2(self):
        self.assertEqual(
            can_allocate(credit=25, prereq_met=False, clash=False, seat_available=False)[0],
            False,
            "Expected ALLOCATE REJECTED: over credit limit, prerequisite not met, and no seat."
        )

    # TO 3: credits=18, prereq Met, clash No, seat Yes -> Allocated Approved
    def test_id_3(self):
        self.assertEqual(
            can_allocate(credit=18, prereq_met=True, clash=False, seat_available=True)[0],
            True,
            "Expected ALLOCATE APPROVED: credits OK, prereq met, no clash, seat available."
        )
    # TO 4: credits=12, prereq Met, clash Yes, seat No -> Allocated Rejected (clash + no seat)
    def test_id_4(self):
        self.assertEqual(
            can_allocate(credit=12, prereq_met=True, clash=True, seat_available=False)[0],
            False,
            "ALLOCATEREJECTED: clash and no seat."
        )

    # TO 5: credits=18, prereq Not_Met, clash Yes, seat No -> Allocated Rejected (prereq + clash + no seat)
    def test_id_5(self):
        self.assertEqual(
            can_allocate(credit=18, prereq_met=False, clash=True, seat_available=False)[0],
            False,
            "ALLOCATE REJECTED: prerequisite not met (plus clash and no seat)."
        )

    # TO 6: credits=25, prereq Not_Met, clash No, seat Yes -> Allocated Rejected (overload + prereq)
    def test_id_6(self):
        self.assertEqual(
            can_allocate(credit=25, prereq_met=False, clash=False, seat_available=True)[0],
            False,
            "ALLOCATE REJECTED: over credit limit and prerequisite not met."
        )

    # TO 7: credits=5, prereq Met, clash No, seat Yes -> Allocated Rejected (underload)
    def test_id_7(self):
        self.assertEqual(
            can_allocate(credit=5, prereq_met=True, clash=False, seat_available=True)[0],
            False,
            "ALLOCATE REJECTED: under credit minimum (<6)."
        )

    # TO 8: credits=18, prereq Met, clash Yes, seat No -> Allocated Rejected (clash + no seat)
    def test_id_8(self):
        self.assertEqual(
            can_allocate(credit=18, prereq_met=True, clash=True, seat_available=False)[0],
            False,
            "ALLOCATE REJECTED: clash and no seat despite valid credits and prereq."
        )

    # TO 9: credits=5, prereq Not_Met, clash Yes, seat No -> Allocated Rejected (underload + prereq + clash + no seat)
    def test_id_9(self):
        self.assertEqual(
            can_allocate(credit=5, prereq_met=False, clash=True, seat_available=False)[0],
            False,
            "ALLOCATE REJECTED: underload, prerequisite not met, and clash/no seat."
        )

    # TO 10: credits=5, prereq Met, clash No, seat No -> Allocated Rejected (underload + no seat)
    def test_id_10(self):
        self.assertEqual(
            can_allocate(credit=5, prereq_met=True, clash=False, seat_available=False)[0],
            False,
            "ALLOCATE REJECTED: underload and no seat."
        )

    # TO 11: credits=12, prereq Not_Met, clash No, seat Yes -> Allocated Rejected (prerequisite)
    def test_id_11(self):
        self.assertEqual(
            can_allocate(credit=12, prereq_met=False, clash=False, seat_available=True)[0],
            False,
            "ALLOCATE REJECTED: prerequisite not met."
        )
    # TO 12: credits=25, prereq Met, clash Yes, seat No -> Allocated Rejected (overload + clash + no seat)
    def test_id_12(self):
        self.assertEqual(
            can_allocate(credit=25, prereq_met=True, clash=True, seat_available=False)[0],
            False,
            "ALLOCATE REJECTED: over credit limit and clash/no seat."
        )