import unittest

from src.discount import calculate_discount

'''
Feasible paths:
1: 1->2->3->5->6->8->13->14->15->19->20->22
2: 1->2->3->5->6->8->13->14->16->17->19->20->22
3: 1->2->3->5->6->8->13->19->20->22
4: 1->2->3->5->6->8->9->10->19->20->22
5: 1->2->3->5->6->8->9->11->12->19->20->22
6: 1->2->3->5->8->13->14->15->19->22
7: 1->2->3->5->8->13->14->16->17->19->22
8: 1->2->3->5->8->13->19->22
9: 1->2->3->5->8->9->10->19->22
10: 1->2->3->5->8->9->11->12->19->22
'''

class TestMyCode(unittest.TestCase):
    # Test for 1: 1->2->3->5->6->8->13->14->15->19->20->22
    def test_mid_cart_senior_loyal(self):
        self.assertEqual(15, calculate_discount(110, True, 11))

    # Test for 2: 1->2->3->5->6->8->13->14->16->17->19->20->22
    def test_mid_cart_non_senior_loyal(self):
        self.assertEqual(10, calculate_discount(110, False, 11))

    # Test for 3: 1->2->3->5->6->8->13->19->20->22
    def test_low_cart_non_senior_loyal(self):
        self.assertEqual(5, calculate_discount(90, False, 11))

    # Test for 4: 1->2->3->5->6->8->9->10->19->20->22
    def test_high_cart_senior_loyal(self):
        self.assertEqual(20, calculate_discount(288, True, 11))

    # Test for 5: 1->2->3->5->6->8->9->11->12->19->20->22
    def test_high_cart_non_senior_loyal(self):
        self.assertEqual(15, calculate_discount(288, False, 11))

    # Test for 6: 1->2->3->5->8->13->14->15->19->22
    def test_mid_cart_senior_non_loyal(self):
        self.assertEqual(10, calculate_discount(110, True, 7))

    # Test for 7: 1->2->3->5->8->13->14->16->17->19->22
    def test_mid_cart_non_senior_non_loyal(self):
        self.assertEqual(5, calculate_discount(110, False, 7))

    # Test for 8: 1->2->3->5->8->13->19->22
    def test_low_cart_non_senior_non_loyal(self):
        self.assertEqual(0, calculate_discount(90, False, 7))

    # Test for 9: 1->2->3->5->8->9->10->19->22
    def test_high_cart_senior_non_loyal(self):
        self.assertEqual(15, calculate_discount(288, True, 7))

    # Test for 10: 1->2->3->5->8->9->11->12->19->22
    def test_high_cart_non_senior_non_loyal(self):
        self.assertEqual(10, calculate_discount(288, False, 7))
