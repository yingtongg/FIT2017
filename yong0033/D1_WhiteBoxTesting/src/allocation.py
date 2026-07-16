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
# --- MC/DC target: simple allocation predicate used by tests ---

def can_allocate(
    credit: int,
    prereq_met: bool,
    clash: bool,
    seat_available: bool,
    waitlist_opt_in: bool | None = None,
) -> tuple[bool, int]:
    """
    Return (ok, reason_code) where:
      ok = True if eligible and seat available, else False
      reason_code:
        0 = OK
        1 = CREDIT (under/over 6..24)
        2 = PREREQ (prerequisite not met)
        3 = CLASH  (timetable clash)
        4 = SEAT   (no seat available)

    Note: waitlist_opt_in is ignored for MC/DC tests.
    """
    # A: CREDIT_OK
    credit_val = int(credit)
    if credit_val < 6 or credit_val > 24:
        return (False, 1)

    # B: PREREQS_OK
    if not prereq_met:
        return (False, 2)

    # C: NO_CLASH
    if clash:
        return (False, 3)

    # D: SEAT
    if not seat_available:
        return (False, 4)

    return (True, 0)
# ---------- H1 extension: International vs Domestic readiness ----------

def _coerce_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default

def _bool(x, default=False):
    return bool(x) if x is not None else default

def _course_to_tuple(course):
    """
    Extract the fields we need from any 'course-like' object.
    Expected (with fallbacks):
      - code: str (default "UNK")
      - credits|credit: int (default 0)
      - mode: "OnCampus" | "Online" (default "OnCampus")
      - prereqs_ok: bool (default True)
      - clashes: bool (default False)
      - _capacity, _enrolled: used to compute seat availability
    """
    code = getattr(course, "code", "UNK")
    credits = _coerce_int(getattr(course, "credits", getattr(course, "credit", 0)), 0)
    mode = getattr(course, "mode", "OnCampus")
    prereqs_ok = _bool(getattr(course, "prereqs_ok", True), True)
    clashes = _bool(getattr(course, "clashes", False), False)

    # re-use Seat to compute seats
    seat_available = not Seat(course).is_full()
    return (code, credits, mode, prereqs_ok, clashes, seat_available)

def check_eligibility(student_status: str,
                      current_credits: int,
                      courses: list) -> tuple[bool, str | None]:
    """
    Returns (ready, reason). When blocked, 'reason' is a user-facing string.
    - Applies your D1 base rules (credit limit, prereqs, clash, seat)
    - Adds H1 rules for International students:
        * total credits >= 12
        * at least one OnCampus unit
        * at most 2 Online units
    """
    # normalize inputs
    status = (student_status or "Domestic").strip().capitalize()
    base_current = _coerce_int(current_credits, 0)

    # shape the plan
    shaped = [_course_to_tuple(c) for c in (courses or [])]
    total = base_current + sum(c[1] for c in shaped)  # credits

    online_count = sum(1 for c in shaped if c[2] == "Online")
    has_on_campus = any(c[2] == "OnCampus" for c in shaped)

    # ---- D1 base rules (same semantics as can_allocate) ----
    if total > 24:
        return (False, "Credit limit exceeded (>24)")
    if any(not c[3] for c in shaped):           # prereqs_ok
        return (False, "Missing prerequisites")
    if any(c[4] for c in shaped):               # clashes
        return (False, "Timetable clash")
    if any(not c[5] for c in shaped):           # seat_available
        return (False, "No available seats")

    # ---- H1 extras for International ----
    if status == "International":
        if total < 12:
            return (False, f"International: current load {total} < 12")
        if not has_on_campus:
            return (False, "International: at least one on-campus unit required")
        if online_count > 2:
            return (False, "International: online unit limit exceeded")

    return (True, None)

def can_enrol_with_plan(student_status: str,
                        current_credits: int,
                        courses: list) -> tuple[bool, str | None]:
    """
    Convenience entrypoint for tests/UI. Delegates to check_eligibility().
    Keeps D1's can_allocate() untouched.
    """
    return check_eligibility(student_status, current_credits, courses)

