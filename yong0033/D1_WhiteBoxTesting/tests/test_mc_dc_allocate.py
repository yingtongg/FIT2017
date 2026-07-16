# tests/test_can_allocate_mcdc.py
"""
Condition under test (can_allocate decision):
eligible = (6 <= credit <= 24) AND prereq_met AND (NOT clash) AND seat_available

Mapping:
  A = (6 <= credit <= 24)
  B = (prereq_met == True)
  C = (clash == False)
  D = (seat_available == True)

Possible tests (truth table focal rows):
T1: A=T, B=T, C=T, D=T → Outcome=True
T2: A=F, B=T, C=T, D=T → Outcome=False
T3: A=T, B=F, C=T, D=T → Outcome=False
T4: A=T, B=T, C=F, D=T → Outcome=False
T5: A=T, B=T, C=T, D=F → Outcome=False

Optimal sets of tests using MC/DC:
- {T1, T2, T3, T4, T5}

Chosen set:
{T1, T2, T3, T4, T5}
___Name___: Ong Ying Tong
___MonashID___: 34477306
"""

import unittest
from src.allocation import can_allocate


class TestCanAllocateMCDC(unittest.TestCase):
    # T1 base: A=T, B=T, C=T, D=T -> True
    def test_T1_base_true(self):
        self.assertEqual(
            can_allocate(credit=18, prereq_met=True, clash=False, seat_available=True)[0],
            True,
            "BASE: credit in [6,24], prereq met, no clash, seat available -> True."
        )

    # T2 flip A only (credit window) -> False
    def test_T2_flip_A_credit(self):
        self.assertEqual(
            can_allocate(credit=25, prereq_met=True, clash=False, seat_available=True)[0],
            False,
            "Flip A: credit=25 (>24) with others True -> False."
        )

    # T3 flip B only (prereq) -> False
    def test_T3_flip_B_prereq(self):
        self.assertEqual(
            can_allocate(credit=18, prereq_met=False, clash=False, seat_available=True)[0],
            False,
            "Flip B: prereq_met=False with others True -> False."
        )

    # T4 flip C only (clash) -> False
    def test_T4_flip_C_clash(self):
        self.assertEqual(
            can_allocate(credit=18, prereq_met=True, clash=True, seat_available=True)[0],
            False,
            "Flip C: clash=True (NO_CLASH=False) with others True -> False."
        )

    # T5 flip D only (seat) -> False
    def test_T5_flip_D_seat(self):
        self.assertEqual(
            can_allocate(credit=18, prereq_met=True, clash=False, seat_available=False)[0],
            False,
            "Flip D: seat_available=False with others True -> False."
        )
