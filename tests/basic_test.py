import unittest


class MyBasicTest(unittest.TestCase):
    def test_one_equals_one(self):
        value_to_check = 2
        self.assertEqual(value_to_check, 1)


if __name__ == '__main__':
    unittest.main()
