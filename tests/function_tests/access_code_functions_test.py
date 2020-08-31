import unittest
import datetime
import functions.access_code_functions as acf


class AccessCodeFunctionsTest(unittest.TestCase):
    def test_generate_unique_access_code(self):
        generated_value = acf.generate_unique_access_code()
        self.assertTrue(len(generated_value) == 6)
        self.assertTrue(generated_value.isnumeric())

    def test_check_expiry_date_is_valid_with_valid_result_no_date(self):
        self.assertIsNone(acf.check_expiry_date_is_valid(None, 15, "hours"))

    def test_check_expiry_date_is_valid_with_invalid_result_no_date(self):
        self.assertEqual(acf.check_expiry_date_is_valid(None, 99, "days"),
                         "The date cannot be more than 31 days after today's date.")

    def test_check_expiry_date_is_valid_with_valid_result_with_date(self):
        self.assertIsNone(acf.check_expiry_date_is_valid(datetime.datetime.now() + datetime.timedelta(days=1),
                                                         15, "hours"))

    def test_check_expiry_date_is_valid_with_invalid_result_with_date(self):
        self.assertEqual(acf.check_expiry_date_is_valid(datetime.datetime.now() + datetime.timedelta(days=1),
                                                         99, "days"),
                         "The date cannot be more than 31 days after today's date.")


if __name__ == '__main__':
    unittest.main()
