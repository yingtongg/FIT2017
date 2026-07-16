from statistics import mean
import unittest
from src import statistics

class TestStatistics(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(statistics.sum([1, 2, 3, 4]), 10)
        self.assertEqual(statistics.sum([-1, -2, -3]), -6)
        self.assertEqual(statistics.sum([0, 0, 0]), 0)

    def test_mean(self):
        self.assertEqual(statistics.mean([1, 2, 3, 4]), 2.5)
        self.assertEqual(statistics.mean([10, 0]), 5.0)
        self.assertEqual(statistics.mean([5]), 5)

    def test_minimum(self):
        self.assertEqual(statistics.minimum([1, 2, 3, 4]), 1)
        self.assertEqual(statistics.minimum([10, -2, 3]), -2)
        self.assertEqual(statistics.minimum([7]), 7)
    def test_maximum(self):
        self.assertEqual(statistics.maximum([1, 2, 3, 4]), 4)
        self.assertEqual(statistics.maximum([10, -2, 3]), 10)
        self.assertEqual(statistics.maximum([7]), 7)



