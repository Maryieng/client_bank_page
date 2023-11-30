import unittest

from src.services import simple_search


class SimpleSearchTestCase(unittest.TestCase):
    def test_simple_search_no_results(self):
        request = "nonexistent"
        expected_result = []
        actual_result = simple_search(request)
        self.assertEqual(expected_result, actual_result)

    def test_simple_search_error(self):
        request = "error"
        expected_result = []
        actual_result = simple_search(request)
        self.assertEqual(expected_result, actual_result)

    def test_simple_search_exception(self):
        request = "exception"
        expected_result = []
        actual_result = simple_search(request)
        self.assertEqual(expected_result, actual_result)

    def test_simple_search_error_as_e(self):
        request = 1
        expected_result = []
        actual_result = simple_search(request)
        self.assertEqual(expected_result, actual_result)
