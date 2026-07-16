# src/course.py
# pylint: disable=protected-access
"""
URCS Course model (minimal, no typing hints/imports).
"""

class Course:
    """
    Represents a course offering in URCS (minimal).
    """

    def __init__(self):
        # Core identifying/course fields
        self._id = "NO DATA LOADED"
        self._code = "NO DATA LOADED"
        self._title = "NO DATA LOADED"
        self._credits = "NO DATA LOADED"

        # Delivery/constraints
        self._mode = "NO DATA LOADED"          # e.g. "Online" | "On_campus" | "Hybrid"
        self._prerequisites = []               # list of course codes (strings)
        self._timeslots = set()                # e.g. {"Mon09-11", "Thu14-16"}

        # Allocation state (data only; no logic here)
        self._capacity = "NO DATA LOADED"
        self._enrolled = []                    # student ids (ints)
        self._waitlist = []                    # student ids (ints)

    def load_data(self, json_record):
        """
        Load course info from a JSON-like dict.

        Expected keys (required): id, code, title, credits, capacity
        Optional keys: mode, prerequisites(list[str]), timeslots(list[str]),
                       enrolled(list[int]), waitlist(list[int])
        """
        self._id = int(json_record["id"])
        self._code = str(json_record["code"])
        self._title = str(json_record["title"])
        self._credits = int(json_record["credits"])

        self._capacity = int(json_record["capacity"])
        self._mode = str(json_record.get("mode", self._mode))

        prereqs = json_record.get("prerequisites", [])
        self._prerequisites = [str(p) for p in prereqs]

        slots = json_record.get("timeslots", [])
        self._timeslots = set(str(s) for s in slots)

        self._enrolled = [int(sid) for sid in json_record.get("enrolled", [])]
        self._waitlist = [int(sid) for sid in json_record.get("waitlist", [])]

    def __str__(self):
        cap = f"{len(self._enrolled)}/{self._capacity}" if isinstance(self._capacity, int) else str(self._capacity)
        prereq_txt = ", ".join(self._prerequisites) if self._prerequisites else "none"
        slot_txt = ", ".join(sorted(self._timeslots)) if self._timeslots else "n/a"
        wl_txt = f"{len(self._waitlist)} on waitlist" if self._waitlist else "no waitlist"
        return (
            f"Course {self._code} ({self._title})\n"
            f"Credits: {self._credits}, Mode: {self._mode}\n"
            f"Capacity: {cap} ({wl_txt})\n"
            f"Prerequisites: {prereq_txt}\n"
            f"Timeslots: {slot_txt}"
        )
