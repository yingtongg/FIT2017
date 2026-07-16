# src/data_manager.py
# pylint: disable=protected-access
"""
URCS Data Manager (minimal, no typing imports)

Loads/saves:
- Courses -> src.course.Course objects
- Students -> plain dicts

Uses paths from src.config: STUDENT_DATA, COURSE_DATA
"""

import json
import sys

from src.course import Course
from src import config


class DataManager:
    def __init__(self):
        # Load courses first (students may reference course codes)
        self._course_data = []
        self.load_courses()

        self._student_data = []
        self.load_students()

    # ---------------------------
    # Student operations
    # ---------------------------

    def register_student(self, name, current_credits=0, completed_courses=None, timeslots=None, holds=False):
        """
        Register a new student with a unique ID and simple defaults.
        Returns the created student dict.
        """
        if completed_courses is None:
            completed_courses = []
        if timeslots is None:
            timeslots = []

        if self._student_data:
            next_id = max(s.get("student_id", 0) for s in self._student_data) + 1
        else:
            next_id = 1

        student = {
            "student_id": int(next_id),
            "name": str(name),
            "current_credits": int(current_credits),
            "completed_courses": [str(c) for c in completed_courses],
            "timeslots": [str(t) for t in timeslots],
            "holds": bool(holds),
        }
        self._student_data.append(student)
        return student

    def load_students(self):
        """
        Load students from config.STUDENT_DATA.
        On error: print message and exit (matches teacher style).
        """
        try:
            with open(config.STUDENT_DATA, "r", encoding="utf-8") as f:
                raw = json.load(f)

            students = []
            for rec in raw:
                s = {
                    "student_id": int(rec["student_id"]),
                    "name": str(rec["name"]),
                    "current_credits": int(rec.get("current_credits", 0)),
                    "completed_courses": [str(c) for c in rec.get("completed_courses", [])],
                    "timeslots": [str(t) for t in rec.get("timeslots", [])],
                    "holds": bool(rec.get("holds", False)),
                }
                students.append(s)

            self._student_data = students
        except (OSError, json.JSONDecodeError, KeyError):
            print("ERROR LOADING STUDENT DATA: EXITING.")
            sys.exit()

    def save_students(self):
        """Overwrite student data file."""
        with open(config.STUDENT_DATA, "w", encoding="utf-8") as f:
            json.dump(self._student_data, f, indent=2, ensure_ascii=False)

    # ---------------------------
    # Course operations
    # ---------------------------

    def load_courses(self):
        """
        Load courses from config.COURSE_DATA into Course objects.
        On error: print message and exit.
        """
        try:
            with open(config.COURSE_DATA, "r", encoding="utf-8") as f:
                raw = json.load(f)

            courses = []
            for rec in raw:
                c = Course()
                c.load_data(rec)
                courses.append(c)

            self._course_data = courses
        except (OSError, json.JSONDecodeError, KeyError):
            print("ERROR LOADING COURSE DATA: EXITING.")
            sys.exit()

    def save_courses(self):
        """Overwrite course data file."""
        def encode_course(c):
            return {
                "id": c._id,
                "code": c._code,
                "title": c._title,
                "credits": c._credits,
                "capacity": c._capacity,
                "mode": c._mode,
                "prerequisites": list(c._prerequisites),
                "timeslots": sorted(c._timeslots),
                "enrolled": list(c._enrolled),
                "waitlist": list(c._waitlist),
            }

        payload = [encode_course(c) for c in self._course_data]
        with open(config.COURSE_DATA, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    # ---------------------------
    # Accessors (handy for tests)
    # ---------------------------

    @property
    def courses(self):
        return self._course_data

    @property
    def students(self):
        return self._student_data
