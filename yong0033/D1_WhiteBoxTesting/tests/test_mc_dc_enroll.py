# tests/test_enrolled_mcdc.py
"""
Condition under test (allocate):
if credit < 6 -> Rejected
elif credit > 24 -> Rejected
else -> Allowed

Mapping:
  A = (credit >= 6)
  B = (credit <= 24)
Decision = A AND B

Possible tests (truth table focal rows):
T1: A=T, B=T → Outcome=Allowed
T2: A=F, B=T → Outcome=Rejected   (flip A only)
T3: A=T, B=F → Outcome=Rejected   (flip B only)

Optimal sets of tests using MC/DC:
- {T1, T2, T3}

Chosen set:
{T1, T2, T3}


___Name___: Ong Ying Tong
___MonashID___: 34477306
"""

import unittest
from src.enrolled import enrolled


class TestEnrolledMCDC(unittest.TestCase):
    # T1 base: A=T, B=T -> Allowed (credit=12)
    def test_T1_base_allowed(self):
        self.assertEqual(
            enrolled(12), "Enrolled Allowed",
            "BASE: credit=12 satisfies 6<=credit<=24 -> Allowed."
        )

    # T2 flip A only: A=F, B=T -> Rejected (credit=5)
    def test_T2_flip_A_under(self):
        self.assertEqual(
            enrolled(5), "Enrolled Rejected",
            "Flip A: credit=5 (<6) with B still True -> Rejected."
        )

    # T3 flip B only: A=T, B=F -> Rejected (credit=25)
    def test_T3_flip_B_over(self):
        self.assertEqual(
            enrolled(25), "Enrolled Rejected",
            "Flip B: credit=25 (>24) with A still True -> Rejected."
        )