# src/enrolled.py
# pylint: disable=protected-access
"""
URCS: simple enrolment credit gate.

Rule (BVA/EP):
- If total credits (passed in as `credit`) < 6  -> "Enrolled Rejected"
- If total credits (passed in as `credit`) > 24 -> "Enrolled Rejected"
- Otherwise                                     -> "Enrolled Allowed"
"""

def enrolled(credit: int) -> str:
    credit = int(credit)
    if credit < 6:
        return "Enrolled Rejected"
    elif credit > 24:
        return "Enrolled Rejected"
    else:
        return "Enrolled Allowed"

