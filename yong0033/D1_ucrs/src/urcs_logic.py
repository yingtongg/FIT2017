# src/urcs_logic.py
# pylint: disable=protected-access
"""
URCS business logic (minimal, pure functions, no typing imports).

Rule (BVA): Eligible only if total credits AFTER enrolment are between
6 and 24 inclusive. (<6 or >24 = reject)

"""

# -----------------------------
# Credit helpers (fixed 6–24 inclusive)
# -----------------------------

def credits_after(current_credits, course_credits):
    """Return credits after enrolment."""
    return int(current_credits) + int(course_credits)

def credits_rule_ok(total_after):
    """
    EXACT POLICY:
      return (True, "OK")          if 6 <= total_after <= 24
      return (False, "UNDER_LOAD") if total_after < 6
      return (False, "OVER_LOAD")  if total_after > 24
    """
    if total_after < 6:
        return False, "UNDER_LOAD"
    elif total_after > 24:
        return False, "OVER_LOAD"
    else:
        return True, "OK"

# convenience wrapper (if other code calls this name)
def credits_ok(total_after, credit_min=6, credit_max=24):
    return credits_rule_ok(total_after)

# -----------------------------
# Eligibility helpers
# -----------------------------

def _to_string_list(items):
    """Return a list of strings from an iterable; handle None safely."""
    result = []
    if items is None:
        return result
    for x in items:
        result.append(str(x))
    return result

def prereq_ok(completed, required, override=False):
    """
    Check prerequisites. If override=True, always OK.
    completed/required: iterables of course codes (strings)
    Returns (ok, reason_code).
    """
    if override is True:
        return True, "OK"

    completed_list = _to_string_list(completed)
    required_list = _to_string_list(required)

    all_present = True
    for req in required_list:
        if req not in completed_list:
            all_present = False
            break

    if all_present:
        return True, "OK"
    else:
        return False, "PREREQ"

def no_clash(student_slots, course_slots):
    """
    True if there is NO timetable clash; False if any overlap.
    student_slots/course_slots: iterables of slot labels (strings)
    Returns (ok, reason_code).
    """
    student_list = _to_string_list(student_slots)
    course_list = _to_string_list(course_slots)

    clash_found = False
    for slot in course_list:
        if slot in student_list:
            clash_found = True
            break

    if clash_found:
        return False, "CLASH"
    else:
        return True, "OK"

# -----------------------------
# Top-level decisions (uses fixed 6–24 rule)
# -----------------------------

def decide_eligibility(
    *,
    current_credits,
    course_credits,
    completed_courses,
    required_prereqs,
    student_slots,
    course_slots,
    prereq_override=False
):
    """
    Decide eligibility to enrol (ignores seats/waitlist).
    Returns ("Approved" or "Rejected", reason_code).

    Order:
      1) PREREQ
      2) CLASH
      3) CREDIT WINDOW (6–24 inclusive)
    """
    ok, reason = prereq_ok(completed_courses, required_prereqs, override=prereq_override)
    if ok is False:
        return "Rejected", reason

    ok, reason = no_clash(student_slots, course_slots)
    if ok is False:
        return "Rejected", reason

    total = credits_after(current_credits, course_credits)
    ok, reason = credits_rule_ok(total)
    if ok is False:
        return "Rejected", reason

    return "Approved", "OK"

def decide_allocation(
    *,
    eligibility,
    seat_available,
    waitlist_pref_opt_in=None
):
    """
    Decide allocation outcome given eligibility and seat state.

    Returns one of:
      - "Allocated Approved", "OK"
      - "Allocated Rejected", "ELIGIBILITY" or "NO_SEATS"
      - "Waitlisted",        "NO_SEATS"
    """
    if eligibility != "Approved":
        return "Allocated Rejected", "ELIGIBILITY"

    if seat_available is True:
        return "Allocated Approved", "OK"

    if waitlist_pref_opt_in is True:
        return "Waitlisted", "NO_SEATS"
    else:
        return "Allocated Rejected", "NO_SEATS"

def decide_enrolment_and_allocation(
    *,
    current_credits,
    course_credits,
    completed_courses,
    required_prereqs,
    student_slots,
    course_slots,
    seat_available,
    waitlist_pref_opt_in=None,
    prereq_override=False
):
    """
    One-shot decision used by your pairwise/EP-BVA tables.
    Returns ("Allocated Approved" | "Allocated Rejected" | "Waitlisted", reason_code).
    """
    eligibility, reason = decide_eligibility(
        current_credits=current_credits,
        course_credits=course_credits,
        completed_courses=completed_courses,
        required_prereqs=required_prereqs,
        student_slots=student_slots,
        course_slots=course_slots,
        prereq_override=prereq_override,
    )

    if eligibility != "Approved":
        return "Allocated Rejected", reason

    return decide_allocation(
        eligibility=eligibility,
        seat_available=seat_available,
        waitlist_pref_opt_in=waitlist_pref_opt_in
    )

# -----------------------------
# Optional: helpers for bucketed EP/BVA tests
# -----------------------------

def bucket_rep(bucket):
    """
    Map your bucket labels to a concrete credit used for evaluation.
      "Under6"  -> 5   (reject)
      "6to12"   -> 12  (edge accept)
      "13to24"  -> 18  (interior accept)
      "Above24" -> 25  (reject)
    """
    b = str(bucket).strip()
    b_lower = b.lower()
    if b_lower == "under6" or b_lower == "under_6" or b == "<6":
        return 5
    elif b == "6to12" or b == "6-12" or b == "6_to_12" or b == "6–12":
        return 12
    elif b == "13to24" or b == "13-24" or b == "13_to_24" or b == "13–24":
        return 18
    elif b_lower == "above24" or b_lower == "over24" or b == ">24":
        return 25
    try:
        return int(b)
    except Exception:
        return 0
