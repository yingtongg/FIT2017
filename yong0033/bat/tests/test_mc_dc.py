# pylint: disable=missing-module-docstring,missing-function-docstring,
# pylint: disable=missing-class-docstring,invalid-name,
# pylint: disable=pointless-string-statement
import unittest
from src.business_logic import can_borrow_carpentry_tool

'''
Condition under test (line 126):
if (fees_owed > 0) or
(patron_age <= 18) or (patron_age >= 90):
    return False

Mapping:
  A = (fees_owed > 0)
  B = (patron_age <= 18)
  C = (patron_age >= 90)


Possible tests (truth table):
T1: A=F, B=F, C=F → Outcome=Allow
T2: A=T, B=F, C=F → Outcome=Deny
T3: A=F, B=T, C=F → Outcome=Deny
T4: A=F, B=F, C=T → Outcome=Deny

Optimal sets of tests using MC/DC:
- {T1, T2, T3, T4}

Chosen set:
{T1, T2, T3, T4}
'''


class TestMCDCCarpentryTool(unittest.TestCase):
    # T1: A=F, B=F, C=F → Allow
    def test_T1_all_false(self):
        self.assertTrue(
            can_borrow_carpentry_tool(
                patron_age=30, length_of_loan=7,
                outstanding_fees=0, carpentry_tool_training=True
            )
        )

    # T2: A=T, B=F, C=F → Deny (flip A)
    def test_T2_fees_true(self):
        self.assertFalse(
            can_borrow_carpentry_tool(
                patron_age=30, length_of_loan=7,
                outstanding_fees=5, carpentry_tool_training=True
            )
        )

    # T3: A=F, B=T, C=F → Deny (flip B)
    def test_T3_underage(self):
        self.assertFalse(
            can_borrow_carpentry_tool(
                patron_age=17, length_of_loan=7,
                outstanding_fees=0, carpentry_tool_training=True
            )
        )

    # T4: A=F, B=F, C=T → Deny (flip C)
    def test_T4_elderly(self):
        self.assertFalse(
            can_borrow_carpentry_tool(
                patron_age=90, length_of_loan=7,
                outstanding_fees=0, carpentry_tool_training=True
            )
        )
