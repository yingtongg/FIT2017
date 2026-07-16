'''
Author: Charlotte Pierce

Code for FIT2107 Software Quality and Testing.
'''


import unittest
from unittest import mock

from src.user_input import (is_int, is_float, read_string,
                            read_integer, read_float, read_integer_range,
                            read_float_range)


class TestUserInput(unittest.TestCase):
    '''Tests for the user input functions.'''

    def test_is_int_with_int(self):
        '''Test that a string number is recognised as a valid int.'''
        self.assertTrue(is_int('1'))

    def test_is_int_with_str(self):
        '''Test that text is not recognised as a valid int.'''
        self.assertFalse(is_int('sdf'))

    def test_is_float_with_float(self):
        '''Test that a string float is recognised as a valid float.'''
        self.assertTrue(is_float('1.5'))

    def test_is_float_with_str(self):
        '''Test that text is not recognised as a valid float.'''
        self.assertFalse(is_float('sdf'))

    @mock.patch('builtins.input')
    def test_read_str(self, inp):
        '''Check that read string returns an expected string, using mocking.'''
        inp.return_value = 'hi'
        self.assertEqual('hi', read_string(''))

    @mock.patch('src.user_input.read_string')
    def test_read_int_with_int(self, readstr):
        '''Check that read integer returns the right integer, using mocking.'''
        readstr.return_value = '1'
        self.assertEqual(1, read_integer(''))

    @mock.patch('src.user_input.read_string')
    def test_read_int_with_str_first(self, readstr):
        '''Check that read integer rejects non-int inputs, using mocking.'''
        readstr.side_effect = ['sdf', '1']
        self.assertEqual(1, read_integer(''))

    @mock.patch('src.user_input.read_string')
    def test_read_float_with_int(self, readstr):
        '''Check that read float returns the right float, using mocking.'''
        readstr.return_value = '1.5'
        self.assertEqual(1.5, read_float(''))

    @mock.patch('src.user_input.read_string')
    def test_read_float_with_str_first(self, readstr):
        '''Check that read float rejects non-float inputs, using mocking.'''
        readstr.side_effect = ['sdf', '1.5']
        self.assertEqual(1.5, read_float(''))

    @mock.patch('src.user_input.read_string')
    def test_read_int_range_in_range(self, readstr):
        '''Check that read integer range works with expected input.'''
        readstr.return_value = '1'
        self.assertEqual(1, read_integer_range('', 0, 5))

    @mock.patch('src.user_input.read_string')
    def test_read_int_range_out_of_range_first(self, readstr):
        '''Check that read integer range rejects input outside
        the specified range.'''
        readstr.side_effect = ['8', '1']
        self.assertEqual(1, read_integer_range('', 0, 5))

    @mock.patch('src.user_input.read_string')
    def test_read_float_range_in_range(self, readstr):
        '''Check that read float range works with expected input.'''
        readstr.return_value = '1.5'
        self.assertEqual(1.5, read_float_range('', 0, 5))

    @mock.patch('src.user_input.read_string')
    def test_read_float_range_out_of_range_first(self, readstr):
        '''Check that read float range rejects input outside
        the specified range.'''
        readstr.side_effect = ['8', '1.5']
        self.assertEqual(1.5, read_float_range('', 0, 5))
