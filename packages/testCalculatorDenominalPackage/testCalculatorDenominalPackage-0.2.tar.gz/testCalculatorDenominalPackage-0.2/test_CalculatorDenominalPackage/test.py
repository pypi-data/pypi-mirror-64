import unittest
import sys
import progrem

class TestToStringMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_strings_zero(self):
        test_result_array, test_result_amount = progrem.calculate_recursive([4, 5], 2, 3, [], [], sys.maxsize)
        test_result_string = progrem.result_to_string(test_result_amount, list(test_result_array))
        self.assertEqual(test_result_string, 'no combination found.')

    def test_strings_given_nums(self):
        test_result_array, test_result_amount = progrem.calculate_recursive([1, 4, 15, 20], 4, 23, [], [], sys.maxsize)
        self.assertEqual(test_result_array, [4, 4, 15])

    def test_strings_given_nums_to_string(self):
        test_result_array, test_result_amount = progrem.calculate_recursive([1, 4, 15, 20], 4, 23, [], [], sys.maxsize)
        test_result_string = progrem.result_to_string(test_result_amount, list(test_result_array))
        self.assertEqual(test_result_string, 'coins needed are: 2 of coin 4 and 1 of coin 15')

    def test_strings_given_nums_to_string_five_denominal(self):
        test_result_array, test_result_amount = progrem.calculate_recursive([1, 2, 3, 4, 10], 5, 14, [], [], sys.maxsize)
        test_result_string = progrem.result_to_string(test_result_amount, list(test_result_array))
        self.assertEqual(test_result_string, 'coins needed are: 1 of coin 4 and 1 of coin 10')

    if __name__ == '__main__':
        unittest.main()
