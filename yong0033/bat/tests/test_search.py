# tests/test_search.py
import unittest
from types import SimpleNamespace

import src.search as S


# --- tiny helpers to make test data easy to read ---
def patron(name, age):
    return SimpleNamespace(_name=name, _age=age)

def item(_id):
    return SimpleNamespace(_id=_id)


class TestSearch(unittest.TestCase):
    # ---------- find_patron_by_name ----------

    def test_find_patron_by_name_exact_match(self):
        """Exact case match only ('Ann' vs 'ann')."""
        patrons = [patron("Ann", 30), patron("ann", 25)]
        result = S.find_patron_by_name("Ann", patrons)
        self.assertEqual(len(result), 1)

    def test_find_patron_by_name_no_match(self):
        """No one named 'Zed' -> empty list."""
        patrons = [patron("Ann", 30), patron("Ben", 22)]
        result = S.find_patron_by_name("Zed", patrons)
        self.assertEqual(len(result), 0)

    # ---------- find_patron_by_age ----------

    def test_find_patron_by_age_two_hits(self):
        """Two patrons aged 20 -> length 2."""
        patrons = [patron("A", 20), patron("B", 20), patron("C", 21)]
        result = S.find_patron_by_age(20, patrons)
        self.assertEqual(len(result), 2)

    def test_find_patron_by_age_zero_hits(self):
        """No patron aged 20 -> empty list."""
        patrons = [patron("A", 19), patron("B", 21)]
        result = S.find_patron_by_age(20, patrons)
        self.assertEqual(len(result), 0)

    # ---------- find_patron_by_name_and_age (name is case-insensitive) ----------

    def test_find_patron_by_name_and_age_found(self):
        """'ann' matches stored 'Ann' when age also matches."""
        patrons = [patron("Ann", 30), patron("Ben", 22)]
        found = S.find_patron_by_name_and_age("ann", 30, patrons)
        self.assertEqual(getattr(found, "_age", None), 30)

    def test_find_patron_by_name_and_age_wrong_age(self):
        """Right name, wrong age -> None."""
        patrons = [patron("Ann", 30)]
        found = S.find_patron_by_name_and_age("Ann", 31, patrons)
        self.assertEqual(getattr(found, "_age", None), None)

    def test_find_patron_by_name_and_age_wrong_name(self):
        """Right age, wrong name -> None."""
        patrons = [patron("Ben", 30)]
        found = S.find_patron_by_name_and_age("Ann", 30, patrons)
        self.assertEqual(getattr(found, "_age", None), None)

    # ---------- find_item_by_id ----------

    def test_find_item_by_id_found(self):
        """Existing id -> returns that item."""
        items = [item(101), item(202)]
        found = S.find_item_by_id(202, items)
        self.assertEqual(getattr(found, "_id", None), 202)

    def test_find_item_by_id_not_found(self):
        """Missing id -> None."""
        items = [item(1), item(2)]
        found = S.find_item_by_id(9, items)
        self.assertEqual(getattr(found, "_id", None), None)
