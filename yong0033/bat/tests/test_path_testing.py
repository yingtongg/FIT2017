# pylint: disable=missing-module-docstring,missing-function-docstring,
# pylint: disable=missing-class-docstring,pointless-string-statement
import unittest
from src.business_logic import can_use_makerspace

'''
Feasible paths:
1: 135->148->150->151->153->154->161->164
2: 135->148->150->151->153->155->156->161->164
3: 135->148->150->151->153->155->157->158->159->161->162->164
4: 135->148->150->151->153->155->157->158->159->161->164
'''


class TestPathCoverageMakerspace(unittest.TestCase):
    # Test for 1: 135->148->150->151->153->154->161->164
    def test_1_error_patron_type(self):
        self.assertFalse(
            can_use_makerspace(
                patron_age=-1, outstanding_fees=0,
                makerspace_training=True)
        )

    # Test for 2: 135->148->150->151->153->155->156->161->164
    def test_2_minor_or_elderly(self):
        # Use either a Minor (e.g., 10) or Elderly (e.g., 90);
        # both take the same branch.
        self.assertFalse(
            can_use_makerspace(
                patron_age=10, outstanding_fees=0,
                makerspace_training=True)
        )

    # Test for 3: 135->148->150->151->153->155->157->158->159->161->162->164
    def test_3_adult_fees_positive(self):
        # Adult path; discount still leaves fees > 0 so
        # final check denies.
        self.assertFalse(
            can_use_makerspace(
                patron_age=30, outstanding_fees=10,
                makerspace_training=True)
        )

    # Test for 4: 135->148->150->151->153->155->157->158->159->161->164
    def test_4_adult_no_fees_or_untrained(self):
        # Adult path; either training=False OR
        # net fees==0 → condition at 161 is False →
        # return current result.
        # Case A (no fees, trained): should allow.
        self.assertTrue(
            can_use_makerspace(
                patron_age=30, outstanding_fees=0,
                makerspace_training=True)
        )
        # Case B (untrained, any fees outcome): still same path;
        # untrained returns False.
        self.assertFalse(
            can_use_makerspace(
                patron_age=30, outstanding_fees=0,
                makerspace_training=False)
        )

