# src/can_allocate.py

def can_allocate(
    credit: int,
    prereq_met: bool,
    clash: bool,
    seat_available: bool,
    waitlist_opt_in: bool | None = None,
) -> tuple[bool, int]:
    # RED step: approve everything so only TO3 (which expects True) passes,
    # and the other 11 (which expect False) fail.
    return (True, 0)
