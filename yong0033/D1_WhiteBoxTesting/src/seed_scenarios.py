# src/seed_scenarios.py
from dataclasses import dataclass

@dataclass
class Course:
    code: str
    credits: int
    mode: str                 # "OnCampus" | "Online"
    prereqs_ok: bool = True
    clashes: bool = False
    capacity: int = 30
    enrolled: int = 0

    # the allocation.Seat class expects _capacity and _enrolled list
    @property
    def _capacity(self):
        return self.capacity
    @property
    def _enrolled(self):
        return [None] * self.enrolled

def build_seed(seed: str):
    """Return (student_status, current_credits, courses) for a given seed."""
    if seed == "intl_underload":
        return ("International", 3, [Course("U1", 6, "OnCampus")])  # total 9
    if seed == "intl_online_limit":
        return ("International", 0, [
            Course("U1", 6, "OnCampus"),
            Course("U2", 6, "Online"),
            Course("U3", 6, "Online"),
            Course("U4", 6, "Online"),
        ])
    if seed == "intl_ok":
        return ("International", 0, [
            Course("U1", 6, "OnCampus"),
            Course("U2", 6, "Online"),
            Course("U3", 6, "Online"),
        ])
    if seed == "domestic_ok":
        return ("Domestic", 6, [
            Course("U1", 6, "Online"),
            Course("U2", 6, "Online"),
            Course("U3", 6, "Online"),
        ])
    # default if unknown
    return ("Domestic", 6, [Course("U1", 6, "OnCampus")])
