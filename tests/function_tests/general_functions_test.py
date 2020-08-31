import unittest
import functions.general_functions as gf


class GeneralFunctionsTest(unittest.TestCase):
    def test_yesno_to_bool_yes(self):
        self.assertTrue(gf.yesno_to_bool("yes"))

    def test_yesno_to_bool_no(self):
        self.assertFalse(gf.yesno_to_bool("NO"))


if __name__ == '__main__':
    unittest.main()
