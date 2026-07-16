# src/search.py
# pylint: disable=protected-access
"""
Tiny helpers for searching lists of Course objects.
"""

def find_course_by_id(course_id, course_data):
    """Return the course whose _id equals course_id, or None if not found."""
    if course_data is None:
        return None
    for course in course_data:
        if getattr(course, "_id", None) == course_id:
            return course
    return None

def find_course_by_code(code, course_data):
    """Return the course whose _code matches (case-insensitive), or None."""
    if course_data is None:
        return None
    target = str(code).lower()
    for course in course_data:
        if str(getattr(course, "_code", "")).lower() == target:
            return course
    return None
