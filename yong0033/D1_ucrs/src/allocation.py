# src/allocation.py
# pylint: disable=protected-access
"""
Allocation helpers for URCS courses (minimal), instance-only.

Class:
- Seat(course)
    - seats_remaining() -> int
    - is_full() -> bool
"""

class Seat:
    def __init__(self, course):
        """
        Bind a course-like object.
        Expected attributes on course:
          - _capacity: int-like
          - _enrolled: list
        """
        self._course = course

    def seats_remaining(self):
        """
        Return number of seats remaining for the bound course.
        If capacity is missing/invalid, returns 0.
        """
        try:
            capacity = int(self._course._capacity)   # protected by assignment design
            enrolled_count = len(getattr(self._course, "_enrolled", []))
            return max(0, capacity - enrolled_count)
        except (AttributeError, TypeError, ValueError):
            return 0

    def is_full(self):
        """Return True if the bound course has no seats remaining, else False."""
        return self.seats_remaining() == 0
