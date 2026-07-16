import unittest

from src.my_code import method_to_test

'''
Possible tests:
1: A=F, B=F, C=F, D=F, Outcome=F
2: A=F, B=F, C=F, D=T, Outcome=F
3: A=F, B=F, C=T, D=F, Outcome=F
4: A=F, B=F, C=T, D=T, Outcome=F
5: A=F, B=T, C=F, D=F, Outcome=F
6: A=F, B=T, C=F, D=T, Outcome=F
7: A=F, B=T, C=T, D=F, Outcome=F
8: A=F, B=T, C=T, D=T, Outcome=F
9: A=T, B=F, C=F, D=F, Outcome=F
10: A=T, B=F, C=F, D=T, Outcome=F
11: A=T, B=F, C=T, D=F, Outcome=F
12: A=T, B=F, C=T, D=T, Outcome=T
13: A=T, B=T, C=F, D=F, Outcome=F
14: A=T, B=T, C=F, D=T, Outcome=T
15: A=T, B=T, C=T, D=F, Outcome=F
16: A=T, B=T, C=T, D=T, Outcome=T

Possible optimal sets of tests using MC/DC:
- 4, 10, 11, 12, 14
- 4, 10, 12, 13, 14
- 6, 10, 11, 12, 14
- 6, 10, 12, 13, 14

We have chosen to use the first set (4, 10, 11, 12, 14), but it's valid to pick any of the sets.
'''

class TestMyCode(unittest.TestCase):
    # Test for 4: A=F, B=F, C=T, D=T, Outcome=F
    def test_f_f_t_t(self):
        self.assertFalse(method_to_test(False, False, True, True))

    # Test for 10: A=T, B=F, C=F, D=T, Outcome=F
    def test_t_f_f_t(self):
        self.assertFalse(method_to_test(True, False, False, True))

    # Test for 11: A=T, B=F, C=T, D=F, Outcome=F
    def test_t_f_t_f(self):
        self.assertFalse(method_to_test(True, False, True, False))

    # Test for 12: A=T, B=F, C=T, D=T, Outcome=T
    def test_t_f_t_t(self):
        self.assertTrue(method_to_test(True, False, True, True))

    # Test for 14: A=T, B=T, C=F, D=T, Outcome=T
    def test_t_t_f_t(self):
        self.assertTrue(method_to_test(True, True, False, True))
