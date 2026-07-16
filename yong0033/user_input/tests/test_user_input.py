import unittest
from unittest import mock

import src.user_input as user_input

class TestUserInput(unittest.TestCase):
    def test_is_int_with_int(self):
        self.assertTrue(user_input.is_int('1'))

    def test_is_int_with_str(self):
        self.assertFalse(user_input.is_int('sdf'))

    def test_is_float_with_float(self):
        self.assertTrue(user_input.is_float('1.5'))

    def test_is_float_with_str(self):
        self.assertFalse(user_input.is_float('sdf'))

    @mock.patch('builtins.input')
    def test_read_str(self, inp):
        inp.return_value = 'hi'
        self.assertEqual('hi', user_input.read_string(''))

    @mock.patch('src.user_input.read_string')
    def test_read_int_with_int(self, readstr):
        readstr.return_value = '1'
        self.assertEqual(1, user_input.read_integer(''))
    
    @mock.patch('src.user_input.read_string')
    def test_read_int_with_str_first(self, readstr):
        readstr.side_effect = ['sdf', '1']
        self.assertEqual(1, user_input.read_integer(''))

    @mock.patch('src.user_input.read_string')
    def test_read_float_with_int(self, readstr):
        readstr.return_value = '1.5'
        self.assertEqual(1.5, user_input.read_float(''))
    
    @mock.patch('src.user_input.read_string')
    def test_read_float_with_str_first(self, readstr):
        readstr.side_effect = ['sdf', '1.5']
        self.assertEqual(1.5, user_input.read_float(''))

    @mock.patch('src.user_input.read_string')
    def test_read_int_range_in_range(self, readstr):
        readstr.return_value = '1'
        self.assertEqual(1, user_input.read_integer_range('', 0, 5))

    @mock.patch('src.user_input.read_string')
    def test_read_int_range_out_of_range_first(self, readstr):
        readstr.side_effect = ['8', '1']
        self.assertEqual(1, user_input.read_integer_range('', 0, 5))

    @mock.patch('src.user_input.read_string')
    def test_read_float_range_in_range(self, readstr):
        readstr.return_value = '1.5'
        self.assertEqual(1.5, user_input.read_float_range('', 0, 5))

    @mock.patch('src.user_input.read_string')
    def test_read_float_range_out_of_range_first(self, readstr):
        readstr.side_effect = ['8', '1.5']
        self.assertEqual(1.5, user_input.read_float_range('', 0, 5))
